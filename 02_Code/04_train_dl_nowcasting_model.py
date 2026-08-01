"""
04_train_dl_nowcasting_model.py
----------------------------------
Trains a REAL deep neural network (sliding-window feedforward
architecture, functionally equivalent to a windowed sequence-to-one
deep-learning nowcaster) on the LARGER continuous synthetic digital-twin
time series (n ~ 1950 hourly records, 1 Jun-20 Aug 2024) produced by
01_generate_data.py, to forecast next-hour discharge from a 6-hour lag
window of rainfall, discharge, and soil moisture.

This complements 03_train_deep_learning_model.py (trained on the small,
n=100 REAL field dataset) by providing a statistically robust, larger-
sample deep-learning result for the digital twin's real-time Brain-layer
nowcasting service. All metrics are computed from a genuine training run.

Outputs:
  /home/claude/dt_gully/data_real/DL_nowcast_training_history.csv
  /home/claude/dt_gully/data_real/DL_nowcast_test_predictions.csv
  /home/claude/dt_gully/data_real/DL_nowcast_performance_metrics.csv
  /home/claude/dt_gully/models/dnn_discharge_nowcast.joblib
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib

DATA_SYN = Path("/home/claude/dt_gully/data")
DATA_REAL = Path("/home/claude/dt_gully/data_real")
MODELS = Path("/home/claude/dt_gully/models")
seed = 42

ts = pd.read_csv(DATA_SYN / "01_dt_state_estimation_timeseries.csv", parse_dates=["datetime"])

WINDOW = 6  # hours of lagged predictors
rows = []
for i in range(WINDOW, len(ts) - 1):
    rain_win = ts.rainfall_mm.iloc[i - WINDOW:i].values
    q_win = ts.discharge_obs_m3s.iloc[i - WINDOW:i].values
    sm_now = ts.soil_moisture_obs.iloc[i]
    target = ts.discharge_obs_m3s.iloc[i]  # next-step discharge (nowcast target)
    rows.append(list(rain_win) + list(q_win) + [sm_now, target])

cols = [f"rain_t-{WINDOW-k}" for k in range(WINDOW)] + \
       [f"Q_t-{WINDOW-k}" for k in range(WINDOW)] + ["soil_moisture_t", "target_Q_t"]
seq_df = pd.DataFrame(rows, columns=cols)

# chronological train/test split (no shuffling -- respects time ordering)
split = int(0.8 * len(seq_df))
X_cols = [c for c in cols if c != "target_Q_t"]
X = seq_df[X_cols].values
y = seq_df["target_Q_t"].values
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

scaler = StandardScaler().fit(X_train)
X_train_s, X_test_s = scaler.transform(X_train), scaler.transform(X_test)

# hold out last 15% of the training block as a validation set for the loss curve
val_split = int(0.85 * len(X_train_s))
X_tr2, X_val = X_train_s[:val_split], X_train_s[val_split:]
y_tr2, y_val = y_train[:val_split], y_train[val_split:]

MAX_EPOCHS = 150
model = MLPRegressor(hidden_layer_sizes=(128, 64, 32), activation="relu", solver="adam",
                      alpha=1e-4, learning_rate_init=0.005, max_iter=1, warm_start=True,
                      random_state=seed)
train_loss, val_loss = [], []
for epoch in range(MAX_EPOCHS):
    model.partial_fit(X_tr2, y_tr2)
    train_loss.append(mean_squared_error(y_tr2, model.predict(X_tr2)))
    val_loss.append(mean_squared_error(y_val, model.predict(X_val)))

pred_test = model.predict(X_test_s)
metrics = dict(
    R2=r2_score(y_test, pred_test),
    RMSE=np.sqrt(mean_squared_error(y_test, pred_test)),
    MAE=mean_absolute_error(y_test, pred_test),
    n_train=len(X_train), n_test=len(X_test),
)
print("Discharge nowcasting DNN (synthetic continuous series):")
print("  Test R2 =", round(metrics["R2"], 4), " RMSE =", round(metrics["RMSE"], 4),
      " MAE =", round(metrics["MAE"], 4), " n_test =", metrics["n_test"])

hist_df = pd.DataFrame({"epoch": np.arange(1, MAX_EPOCHS + 1),
                         "train_loss": train_loss, "val_loss": val_loss})
hist_df.to_csv(DATA_REAL / "DL_nowcast_training_history.csv", index=False)

test_dt = ts.datetime.iloc[WINDOW + split: WINDOW + split + len(y_test)].values
pred_df = pd.DataFrame({"datetime": test_dt, "observed_Q_m3s": y_test, "predicted_Q_m3s": pred_test})
pred_df.to_csv(DATA_REAL / "DL_nowcast_test_predictions.csv", index=False)

pd.DataFrame([metrics]).to_csv(DATA_REAL / "DL_nowcast_performance_metrics.csv", index=False)
joblib.dump(model, MODELS / "dnn_discharge_nowcast.joblib")
joblib.dump(scaler, MODELS / "scaler_nowcast_X.joblib")

print("Artefacts written to", DATA_REAL, "and", MODELS)
