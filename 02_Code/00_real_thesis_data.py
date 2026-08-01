"""
00_real_thesis_data.py
-----------------------
Transcribes the ACTUAL field-measured data tables from the author's
undergraduate thesis:

  Halilu, N. (2024). "The Use of Morning Glory (Ipomoea carnea) for
  Controlling Gully Erosion within the Watercourse of Ahmadu Bello
  University Dam." B.Eng. Project (U18AE2018), Department of
  Agricultural and Bio-Resources Engineering, Ahmadu Bello University,
  Zaria, Nigeria.

Source tables reproduced (Chapter 4 results): Table 4.1 (channel
geometry at 20 stations along a 2.5 km watercourse, surveyed every
125 m), Table 4.2-4.6 (sediment transport rate, flow velocity, soil
shear and water depth at 20 stations under five experimental
conditions: pre-control baseline; pre-control after 1.0 m external
ponding; post-control [Morning Glory] after 1.0 m ponding; pre-control
after 1.5 m ponding; post-control after 1.5 m ponding), and Table 4.7-4.8
(observed vs. linear-model-predicted stream velocity, pre- and
post-control).

These are REAL measured values transcribed directly from the thesis
manuscript (not synthetic). Output: /home/claude/dt_gully/data_real/*.csv
"""
import pandas as pd
from pathlib import Path

OUT = Path("/home/claude/dt_gully/data_real")
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Table 4.1 - Channel geometry at 20 stations (125 m spacing, 2.5 km reach)
# ---------------------------------------------------------------------
t41 = pd.DataFrame({
    "station": list(range(1, 21)),
    "breadth_m": [1.78,1.95,1.92,2.01,2.20,2.30,1.94,2.70,2.30,2.20,
                  1.90,3.00,2.20,1.98,2.01,2.23,2.52,3.35,2.96,2.81],
    "depth1_m": [2.10,2.20,1.83,1.95,2.80,2.50,3.00,2.20,2.50,2.30,
                 1.95,1.67,1.53,1.65,1.83,1.76,1.10,1.23,1.76,2.01],
    "depth2_m": [2.20,2.01,1.85,1.90,2.86,2.54,2.54,2.23,2.23,2.31,
                 1.95,1.65,1.53,1.96,1.84,1.67,1.10,1.20,1.70,2.01],
    "avg_depth_m": [2.15,2.10,1.84,1.92,2.83,2.52,2.77,2.22,2.37,2.31,
                    1.95,1.66,1.53,1.96,1.84,1.72,1.10,1.22,1.73,2.01],
    "slope_pct": [0.90,0.67,1.20,0.95,0.90,0.70,1.10,0.76,0.56,2.10,
                  1.30,1.40,0.96,0.96,1.05,1.12,1.10,1.51,1.32,1.08],
})
t41["design_breadth_m"] = 1.5
t41["design_depth_m"] = 0.5
t41.to_csv(OUT / "Table4_1_channel_geometry.csv", index=False)

# ---------------------------------------------------------------------
# Helper: five experimental-condition tables (Tables 4.2-4.6)
# columns: station, depth_ft, slope_dec, soil_shear_lb_ft2,
#          sed_transport_lb_s_410ft, sed_transport_kg_s_m, velocity_ms
# ---------------------------------------------------------------------
def cond_table(name, depth_ft, slope_dec, shear, sed_lb, sed_kg, vel):
    df = pd.DataFrame({
        "station": list(range(1, 21)),
        "water_depth_ft": depth_ft,
        "slope_decimal": slope_dec,
        "soil_shear_lb_ft2": shear,
        "sediment_transport_lb_s_410ft": sed_lb,
        "sediment_transport_kg_s_m": sed_kg,
        "velocity_ms": vel,
    })
    df.to_csv(OUT / f"{name}.csv", index=False)
    return df

# Table 4.2 - Pre-control baseline (before any external ponding)
t42 = cond_table(
    "Table4_2_precontrol_baseline",
    depth_ft=[0.94,1.24,1.44,1.15,1.05,0.66,1.32,0.98,0.82,0.52,
              0.98,0.82,0.98,0.81,0.72,0.75,1.21,1.08,1.08,1.09],
    slope_dec=[0.0090,0.0067,0.0120,0.0095,0.0090,0.0070,0.0110,0.0076,0.0056,0.0210,
               0.0130,0.0140,0.0096,0.0096,0.0105,0.0112,0.0110,0.0151,0.0132,0.0108],
    shear=[0.530,0.499,1.061,0.690,0.561,0.312,0.936,0.437,0.312,0.680,
           0.811,0.686,0.580,0.480,0.499,0.499,0.811,0.998,0.874,0.749],
    sed_lb=[20.64,15.90,84.19,35.27,23.17,6.989,65.46,13.95,6.89,34.61,
            48.92,34.86,24.79,16.86,18.28,18.28,48.91,33.55,29.38,41.64],
    sed_kg=[0.24,0.19,1.00,0.42,0.28,0.08,0.78,0.16,0.08,0.41,
            0.58,0.41,0.29,0.20,0.22,0.22,0.58,0.39,0.35,0.495],
    vel=[0.75,0.63,1.07,0.89,0.81,0.63,1.01,0.63,0.23,1.51,
         1.05,0.85,0.83,0.97,0.94,1.07,0.90,0.90,0.97,1.09],
)

# Table 4.3 - Pre-control after 1.0 m external ponding
t43 = cond_table(
    "Table4_3_precontrol_ponding_1_0m",
    depth_ft=[2.11,3.20,2.00,3.11,2.10,1.09,3.21,1.12,1.01,1.21,
              1.21,2.21,2.02,3.21,2.01,0.98,2.21,1.09,1.31,2.10],
    slope_dec=[0.0090,0.0067,0.0120,0.0095,0.0090,0.0070,0.0110,0.0076,0.0056,0.0210,
               0.0130,0.0140,0.0096,0.0096,0.0105,0.0112,0.0110,0.0151,0.0132,0.0108],
    shear=[1.18,1.34,2.40,1.84,1.18,0.48,2.20,0.53,0.35,1.58,
           0.98,1.93,1.21,1.92,1.32,0.68,1.51,1.03,1.08,1.42],
    sed_lb=[105.23,135.69,302.62,256.01,96.21,16.40,366.35,20.93,9.03,189.29,
            72.25,281.75,110.37,278.83,131.45,34.61,172.19,79.85,87.84,152.21],
    sed_kg=[1.25,1.61,3.60,3.05,1.15,0.20,4.35,0.24,0.11,2.25,
            0.86,3.35,1.31,3.32,1.56,0.41,2.05,0.95,1.05,1.81],
    vel=[1.20,1.00,1.50,0.90,1.25,1.40,1.30,0.90,0.70,2.00,
         1.30,1.20,1.00,1.10,1.30,1.20,1.00,1.10,1.30,1.30],
)

# Table 4.4 - Post-control (Morning Glory) after 1.0 m ponding
t44 = cond_table(
    "Table4_4_postcontrol_ponding_1_0m",
    depth_ft=[1.92,2.81,2.12,2.73,1.56,1.09,2.36,1.12,0.56,1.00,
              1.00,2.02,1.51,3.00,1.56,0.95,3.20,1.20,1.52,1.78],
    slope_dec=[0.0090,0.0067,0.0120,0.0095,0.0090,0.0070,0.0110,0.0076,0.0056,0.0210,
               0.0130,0.0140,0.0096,0.0096,0.0105,0.0112,0.0110,0.0151,0.0132,0.0108],
    shear=[1.08,1.17,1.59,1.62,0.88,0.47,1.61,0.53,0.19,1.31,
           0.81,1.76,0.90,1.80,1.02,0.65,2.19,1.13,1.25,1.19],
    sed_lb=[20.19,94.19,174.39,181.05,47.18,14.99,179.91,19.11,2.49,108.48,
            44.96,213.81,55.58,223.67,71.49,28.55,331.45,87.83,107.57,97.45],
    sed_kg=[0.95,1.12,2.07,2.10,0.56,0.18,2.14,0.23,0.03,1.29,
            0.53,2.54,0.66,2.66,0.85,0.34,3.94,1.05,1.28,1.16],
    vel=[1.00,0.75,1.20,0.90,1.25,1.40,1.20,0.91,0.60,1.08,
         1.20,1.10,0.70,0.60,1.00,0.90,0.88,0.22,0.95,1.10],
)

# Table 4.5 - Pre-control after 1.5 m external ponding
t45 = cond_table(
    "Table4_5_precontrol_ponding_1_5m",
    depth_ft=[2.51,3.60,3.50,3.20,2.40,1.50,3.23,1.30,1.20,2.01,
              1.51,1.61,2.31,3.60,2.20,1.20,2.63,1.30,1.50,2.20],
    slope_dec=[0.0090,0.0067,0.0120,0.0095,0.0090,0.0070,0.0110,0.0076,0.0056,0.0210,
               0.0130,0.0140,0.0096,0.0096,0.0105,0.0112,0.0110,0.0151,0.0132,0.0108],
    shear=[1.41,1.51,2.62,1.89,1.34,0.66,2.20,0.62,0.42,2.62,
           1.22,1.41,1.38,2.15,1.44,0.84,1.79,1.22,1.24,1.48],
    sed_lb=[150.06,172.19,89.52,270.16,135.48,27.71,369.19,28.73,13.072,529.27,
            112.21,150.06,143.73,350.91,156.55,52.98,242.25,112.29,115.94,165.39],
    sed_kg=[1.79,2.05,1.07,3.21,1.61,0.33,4.39,0.34,0.16,6.30,
            1.33,1.78,1.71,4.17,1.86,0.63,2.88,1.33,1.38,1.97],
    vel=[1.70,1.20,1.80,1.20,1.50,1.70,1.80,1.20,1.40,2.20,
         1.50,1.60,1.20,1.40,1.70,1.40,1.20,1.60,1.30,1.40],
)

# Table 4.6 - Post-control (Morning Glory) after 1.5 m ponding
t46 = cond_table(
    "Table4_6_postcontrol_ponding_1_5m",
    depth_ft=[2.31,3.46,3.51,3.22,2.20,1.25,3.00,1.01,2.95,1.42,
              2.50,2.40,2.20,3.20,2.10,1.00,2.30,1.20,1.30,2.10],
    slope_dec=[0.0090,0.0067,0.0120,0.0095,0.0090,0.0070,0.0110,0.0076,0.0056,0.0210,
               0.0130,0.0140,0.0096,0.0096,0.0105,0.0112,0.0110,0.0151,0.0132,0.0108],
    shear=[1.30,1.45,2.62,1.91,1.24,0.55,2.06,0.47,1.03,1.86,
           2.03,2.10,1.32,1.92,1.38,0.69,1.58,1.13,1.07,1.40],
    sed_lb=[116.39,144.93,474.77,251.51,105.85,20.59,320.97,15.28,72.91,238.88,
            284.12,303.83,120.02,254.58,131.23,32.97,172.19,87.83,78.71,95.28],
    sed_kg=[1.39,1.72,5.64,2.99,1.26,0.24,3.87,0.18,0.87,2.84,
            3.38,3.61,1.43,3.03,1.56,0.39,2.04,1.04,0.93,1.33],
    vel=[1.50,1.01,1.63,0.98,1.20,1.40,1.20,1.00,0.98,2.10,
         1.40,1.30,0.98,1.20,1.10,1.20,0.70,1.00,1.20,1.01],
)

# ---------------------------------------------------------------------
# Table 4.7 / 4.8 - Linear model (Vs = 0.0859*Qs + 0.9136) validation
# ---------------------------------------------------------------------
t47 = pd.DataFrame({
    "condition": ["pre-control"] * 5,
    "sediment_transport_kg_s_m": [0.8, 1.1, 1.4, 1.8, 2.1],
    "observed_velocity_ms": [0.95, 1.15, 1.39, 1.58, 1.77],
    "predicted_velocity_ms": [0.98, 1.15, 1.39, 1.57, 1.73],
})
t48 = pd.DataFrame({
    "condition": ["post-control"] * 5,
    "sediment_transport_kg_s_m": [0.6, 0.9, 1.1, 1.3, 1.6],
    "observed_velocity_ms": [0.64, 0.79, 0.99, 1.17, 1.33],
    "predicted_velocity_ms": [0.62, 0.79, 0.95, 1.11, 1.29],
})
t47_48 = pd.concat([t47, t48], ignore_index=True)
t47_48.to_csv(OUT / "Table4_7_8_velocity_model_validation.csv", index=False)

# ---------------------------------------------------------------------
# Consolidated long-format real dataset (100 records: 20 stations x 5
# experimental conditions) -- this is the primary REAL training dataset
# used for the deep-learning model in 02_train_deep_learning_model.py
# ---------------------------------------------------------------------
frames = []
for label, df in [
    ("precontrol_baseline", t42), ("precontrol_ponding_1.0m", t43),
    ("postcontrol_ponding_1.0m", t44), ("precontrol_ponding_1.5m", t45),
    ("postcontrol_ponding_1.5m", t46),
]:
    d = df.copy()
    d["condition"] = label
    d["biocontrol"] = 1 if "postcontrol" in label else 0
    d["ponding_depth_m"] = 0.0 if "baseline" in label else (1.0 if "1.0m" in label else 1.5)
    frames.append(d)
real_long = pd.concat(frames, ignore_index=True)
real_long["water_depth_m"] = real_long.water_depth_ft * 0.3048
real_long.to_csv(OUT / "Real_field_dataset_consolidated.csv", index=False)

print("Real thesis data written to", OUT)
for f in sorted(OUT.glob("*.csv")):
    print(" -", f.name, "(", sum(1 for _ in open(f)) - 1, "records)")
print("\nConsolidated real dataset shape:", real_long.shape)
