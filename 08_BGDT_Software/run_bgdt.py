#!/usr/bin/env python3
"""
run_bgdt.py
------------
Command-line entry point for the Bomo Gully Digital Twin (BG-DT) v1.0.

Usage
-----
    python run_bgdt.py                     # full demo run with synthetic sensors
    python run_bgdt.py --real-data FILE     # also fit the real-data DNN on a CSV
    python run_bgdt.py --output-dir DIR     # write CSV/PNG outputs to DIR
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bgdt import BomoGullyDigitalTwin
from bgdt.config import BGDTConfig
from bgdt import metrics as bgdt_metrics


def main():
    parser = argparse.ArgumentParser(description="Run the Bomo Gully Digital Twin (BG-DT) v1.0")
    parser.add_argument("--real-data", type=str, default=None,
                         help="Path to a real field CSV (e.g. Real_field_dataset_consolidated.csv) "
                              "to additionally train the real-data deep-learning model on.")
    parser.add_argument("--output-dir", type=str, default="outputs",
                         help="Directory to write result CSVs/PNGs into.")
    parser.add_argument("--no-nowcast", action="store_true",
                         help="Skip training the (slower) discharge-nowcasting DNN.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print(">>> Initialising BG-DT v1.0 ...")
    dt = BomoGullyDigitalTwin.from_default_config()

    print(">>> Running Physical + Digital + Brain + Service layers ...")
    dt.run()
    dt.report()

    # --- Save the assimilated state trajectory ---
    traj = pd.DataFrame({
        "datetime": dt.sensors.timestamps,
        "rainfall_mm": dt.digital_layer_output["rainfall_mm"],
        "discharge_m3s": dt.assimilated["discharge"]["posterior_mean"],
        "discharge_ci_lower": dt.assimilated["discharge"]["ci_lower"],
        "discharge_ci_upper": dt.assimilated["discharge"]["ci_upper"],
        "water_level_m": dt.assimilated["water_level"]["posterior_mean"],
        "soil_moisture": dt.assimilated["soil_moisture"]["posterior_mean"],
        "sediment_conc_mgL": dt.assimilated["sediment_conc"]["posterior_mean"],
    })
    traj_path = os.path.join(args.output_dir, "bgdt_assimilated_state.csv")
    traj.to_csv(traj_path, index=False)
    print(f">>> Assimilated state trajectory written to {traj_path}")

    # --- Scenario + Sobol tables ---
    scen_path = os.path.join(args.output_dir, "bgdt_scenario_simulation.csv")
    dt.scenario_table.to_csv(scen_path, index=False)
    sobol_path = os.path.join(args.output_dir, "bgdt_sobol_sensitivity.csv")
    dt.sobol_table.to_csv(sobol_path, index=False)
    print(f">>> Scenario simulation written to {scen_path}")
    print(f">>> Sobol sensitivity indices written to {sobol_path}")
    print(dt.sobol_table.to_string(index=False))

    # --- Optional: train the real-data DNN on a supplied real dataset ---
    if args.real_data:
        print(f">>> Fitting real-data DNN on {args.real_data} ...")
        real_df = pd.read_csv(args.real_data)
        vel_metrics = dt.fit_deep_learning(real_df, target="velocity_ms")
        sed_metrics = dt.fit_deep_learning(real_df, target="sediment_transport_kg_s_m")
        print("    Velocity model:", vel_metrics)
        print("    Sediment model:", sed_metrics)

    if not args.no_nowcast:
        print(">>> Training discharge-nowcasting DNN (this may take a moment) ...")
        now_metrics = dt.fit_nowcasting_dnn()
        print("    Nowcast model:", now_metrics)

    print(">>> Done. BG-DT v1.0 run complete.")


if __name__ == "__main__":
    main()
