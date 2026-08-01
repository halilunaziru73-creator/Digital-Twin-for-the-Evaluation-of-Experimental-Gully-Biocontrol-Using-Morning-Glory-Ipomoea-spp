"""
bgdt.deep_learning
-------------------
Brain Layer: deep feedforward neural networks (multi-layer perceptrons).

Implements, verbatim, the manuscript's:
  Eq. (13)  L(w) = (1/N) sum_i (y_i - yhat_i(w))^2   (MSE loss, minimised via Adam)

Two models are provided, matching Section 4.5 / Table 5 of the manuscript:
  - `RealDataDNN`     : trained on the small (n=100) real field dataset
                        (Section 3.5) to predict sediment transport rate
                        and flow velocity.
  - `NowcastDNN`       : trained on a larger continuous time series using a
                        sliding lag window to forecast next-hour discharge.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from .config import DeepLearningConfig


def _train_with_loss_history(X_train, y_train, X_test, y_test, hidden, lr, alpha,
                              epochs, seed, val_frac=0.2):
    """Shared training loop: fits an MLPRegressor one epoch at a time via
    `partial_fit`, recording the Eq. (13) MSE loss on a held-out
    validation split at every epoch (used for the training curves in
    Fig. 12)."""
    model = MLPRegressor(hidden_layer_sizes=hidden, activation="relu", solver="adam",
                          alpha=alpha, learning_rate_init=lr, max_iter=1,
                          warm_start=True, random_state=seed)
    X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=val_frac, random_state=seed)
    train_loss, val_loss = [], []
    for _ in range(epochs):
        model.partial_fit(X_tr, y_tr)
        train_loss.append(mean_squared_error(y_tr, model.predict(X_tr)))
        val_loss.append(mean_squared_error(y_val, model.predict(X_val)))
    pred_test = model.predict(X_test)
    metrics = dict(
        R2=r2_score(y_test, pred_test),
        RMSE=np.sqrt(mean_squared_error(y_test, pred_test)),
        MAE=mean_absolute_error(y_test, pred_test),
    )
    return model, np.array(train_loss), np.array(val_loss), pred_test, metrics


class RealDataDNN:
    """Deep network trained on the real, small field dataset (Section 3.5)
    to predict sediment transport rate or flow velocity from static
    predictors."""

    FEATURES = ["water_depth_m", "slope_decimal", "soil_shear_lb_ft2", "biocontrol", "ponding_depth_m"]

    def __init__(self, cfg: DeepLearningConfig, target: str = "velocity_ms"):
        self.cfg = cfg
        self.target = target
        self.scaler = StandardScaler()
        self.model = None
        self.history = {}
        self.metrics_ = {}

    def fit(self, df: pd.DataFrame) -> dict:
        X = df[self.FEATURES].values
        y = df[self.target].values
        Xs = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            Xs, y, test_size=0.25, random_state=self.cfg.random_state)
        model, tr_loss, val_loss, pred_test, metrics = _train_with_loss_history(
            X_train, y_train, X_test, y_test,
            hidden=self.cfg.real_data_hidden_layers, lr=self.cfg.real_data_lr,
            alpha=self.cfg.real_data_alpha, epochs=self.cfg.real_data_epochs,
            seed=self.cfg.random_state,
        )
        self.model = model
        self.history = {"train_loss": tr_loss, "val_loss": val_loss}
        self.metrics_ = metrics
        self._y_test, self._pred_test = y_test, pred_test
        return metrics

    def predict(self, X_raw: np.ndarray) -> np.ndarray:
        return self.model.predict(self.scaler.transform(X_raw))


class NowcastDNN:
    """Deep network trained on a sliding lag-window of a continuous time
    series to forecast next-hour discharge (Section 4.5)."""

    def __init__(self, cfg: DeepLearningConfig):
        self.cfg = cfg
        self.scaler = StandardScaler()
        self.model = None
        self.history = {}
        self.metrics_ = {}

    @staticmethod
    def _build_windows(rainfall: np.ndarray, discharge: np.ndarray,
                        soil_moisture: np.ndarray, window: int):
        rows, targets = [], []
        for i in range(window, len(discharge) - 1):
            rain_win = rainfall[i - window:i]
            q_win = discharge[i - window:i]
            sm_now = soil_moisture[i]
            rows.append(np.concatenate([rain_win, q_win, [sm_now]]))
            targets.append(discharge[i])
        return np.array(rows), np.array(targets)

    def fit(self, rainfall: np.ndarray, discharge: np.ndarray, soil_moisture: np.ndarray) -> dict:
        window = self.cfg.nowcast_lag_window_h
        X, y = self._build_windows(rainfall, discharge, soil_moisture, window)
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        Xs_train = self.scaler.fit_transform(X_train)
        Xs_test = self.scaler.transform(X_test)

        model, tr_loss, val_loss, pred_test, metrics = _train_with_loss_history(
            Xs_train, y_train, Xs_test, y_test,
            hidden=self.cfg.nowcast_hidden_layers, lr=self.cfg.nowcast_lr,
            alpha=self.cfg.nowcast_alpha, epochs=self.cfg.nowcast_epochs,
            seed=self.cfg.random_state,
        )
        self.model = model
        self.history = {"train_loss": tr_loss, "val_loss": val_loss}
        self.metrics_ = metrics
        self._y_test, self._pred_test = y_test, pred_test
        return metrics
