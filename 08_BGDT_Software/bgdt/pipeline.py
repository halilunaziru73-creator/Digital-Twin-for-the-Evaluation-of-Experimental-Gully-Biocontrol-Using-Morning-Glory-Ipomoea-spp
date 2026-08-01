"""
bgdt.pipeline
--------------
Orchestrates the four layers (Physical, Digital, Brain, Service) into a
single, runnable Digital Twin, matching the architecture of Fig. 5 in the
manuscript.

>>> from bgdt import BomoGullyDigitalTwin
>>> dt = BomoGullyDigitalTwin.from_default_config()
>>> dt.run()
>>> dt.report()
>>> dt.state["discharge_m3s"]
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import BGDTConfig
from .physical import SensorNetwork
from . import hydrology, hydraulics, vegetation, sediment, metrics
from .bayesian import assimilate_all_states
from .ml_model import SedimentYieldModel
from .deep_learning import RealDataDNN, NowcastDNN
from .scenario import scenario_simulation, sobol_indices, monte_carlo_uncertainty


class BomoGullyDigitalTwin:
    """Bomo Gully Digital Twin (BG-DT) v1.0 -- top-level orchestrator."""

    def __init__(self, config: BGDTConfig = None):
        self.config = config or BGDTConfig()
        self.sensors: SensorNetwork | None = None
        self.digital_layer_output: dict = {}
        self.assimilated: dict = {}
        self.ml_model: SedimentYieldModel | None = None
        self.dl_real: dict = {}
        self.dl_nowcast: NowcastDNN | None = None
        self.scenario_table: pd.DataFrame | None = None
        self.sobol_table: pd.DataFrame | None = None
        self.state: dict = {}
        self._has_run = False

    # ------------------------------------------------------------------
    @classmethod
    def from_default_config(cls) -> "BomoGullyDigitalTwin":
        return cls(BGDTConfig())

    # ------------------------------------------------------------------
    def ingest(self, sensors: SensorNetwork = None):
        """Physical Layer: attach a real or simulated sensor network."""
        self.sensors = sensors or SensorNetwork.simulate(random_state=self.config.random_seed)
        return self

    # ------------------------------------------------------------------
    def run_digital_layer(self):
        """Digital Layer: rainfall -> soil moisture -> discharge (Eq. 2-4),
        plus vegetation-adjusted hydraulics (Eq. 5-7) and sediment supply
        (Eq. 10) for baseline vs. biocontrol conditions."""
        if self.sensors is None:
            self.ingest()
        rain = self.sensors.rainfall_mm
        hydro_out = hydrology.discharge_from_rainfall(rain, self.config.hydrology)

        depth_m = 0.35 + 0.028 * np.clip(hydro_out["discharge"], 0.01, None) ** 0.75
        ndvi_baseline = np.full_like(rain, 0.25)
        ndvi_biocontrol = np.full_like(rain, 0.78)
        n_bio = hydraulics.vegetation_adjusted_manning_n(ndvi_biocontrol, np.full_like(rain, 30.0), self.config.hydraulics)
        v_bio = hydraulics.manning_velocity(depth_m, self.config.hydraulics.bed_slope, n_bio)
        tau_b = hydraulics.bed_shear_stress(depth_m, self.config.hydraulics)
        omega = hydraulics.unit_stream_power(v_bio, depth_m, self.config.hydraulics)

        A_baseline = sediment.rusle_soil_loss(self.config.sediment, biocontrol=False)
        A_biocontrol = sediment.rusle_soil_loss(self.config.sediment, biocontrol=True)

        rld_baseline = vegetation.ndvi_to_root_length_density(ndvi_baseline)
        rld_biocontrol = vegetation.ndvi_to_root_length_density(ndvi_biocontrol)
        fs_baseline = vegetation.factor_of_safety(depth_m, rld_baseline, self.config.vegetation)
        fs_biocontrol = vegetation.factor_of_safety(depth_m, rld_biocontrol, self.config.vegetation)

        self.digital_layer_output = {
            "datetime": self.sensors.timestamps, "rainfall_mm": rain,
            "soil_moisture": hydro_out["soil_moisture"], "discharge_m3s": hydro_out["discharge"],
            "water_depth_m": depth_m, "velocity_ms": v_bio, "shear_stress_Pa": tau_b,
            "stream_power_Nms": omega,
            "annual_soil_loss_baseline_t_ha_yr": A_baseline,
            "annual_soil_loss_biocontrol_t_ha_yr": A_biocontrol,
            "factor_of_safety_baseline": np.nanmean(fs_baseline),
            "factor_of_safety_biocontrol": np.nanmean(fs_biocontrol),
        }
        return self

    # ------------------------------------------------------------------
    def run_brain_layer(self, observations: dict = None):
        """Brain Layer: Bayesian assimilation (Eq. 11) of the Digital-Layer
        trajectory against streaming observations (synthetic if none
        supplied), plus fitting of the SHAP-explainable GBM (Eq. 12)."""
        if not self.digital_layer_output:
            self.run_digital_layer()

        rng = np.random.default_rng(self.config.random_seed)
        model_traj = {
            "discharge": self.digital_layer_output["discharge_m3s"],
            "water_level": 0.35 + 0.028 * self.digital_layer_output["discharge_m3s"] ** 0.75,
            "soil_moisture": self.digital_layer_output["soil_moisture"],
            "sediment_conc": 4.2 * np.clip(self.digital_layer_output["discharge_m3s"], 0.01, None) ** 1.35,
        }
        if observations is None:
            observations = {k: v + rng.normal(0, 0.05 * (np.std(v) + 1e-6), len(v))
                             for k, v in model_traj.items()}

        self.assimilated = assimilate_all_states(model_traj, observations, self.config.bayesian)
        return self

    # ------------------------------------------------------------------
    def fit_ml_model(self, X: pd.DataFrame, y: np.ndarray) -> dict:
        """Brain Layer: fit the gradient-boosted sediment-yield model and
        report held-out performance (Eq. 12; Table 6-analog)."""
        self.ml_model = SedimentYieldModel(self.config.ml)
        return self.ml_model.fit(X, y)

    def fit_deep_learning(self, real_df: pd.DataFrame = None, target: str = "velocity_ms") -> dict:
        """Brain Layer: train the real-data DNN (Eq. 13) if real field
        data is supplied."""
        if real_df is None:
            return {}
        dnn = RealDataDNN(self.config.deep_learning, target=target)
        metrics_out = dnn.fit(real_df)
        self.dl_real[target] = dnn
        return metrics_out

    def fit_nowcasting_dnn(self) -> dict:
        """Brain Layer: train the discharge-nowcasting DNN (Eq. 13) on the
        continuous Digital-Layer trajectory."""
        if not self.digital_layer_output:
            self.run_digital_layer()
        self.dl_nowcast = NowcastDNN(self.config.deep_learning)
        return self.dl_nowcast.fit(
            self.digital_layer_output["rainfall_mm"],
            self.digital_layer_output["discharge_m3s"],
            self.digital_layer_output["soil_moisture"],
        )

    # ------------------------------------------------------------------
    def run_service_layer(self):
        """Service Layer: return-period scenario simulation and Sobol
        global sensitivity analysis (Eq. 14)."""
        self.scenario_table = scenario_simulation(self.config.scenario)
        self.sobol_table = sobol_indices(self.config.scenario)
        return self

    # ------------------------------------------------------------------
    def run(self, observations: dict = None):
        """Run the full four-layer pipeline end-to-end."""
        self.ingest()
        self.run_digital_layer()
        self.run_brain_layer(observations=observations)
        self.run_service_layer()

        i = -1  # most recent timestep -> current live state
        self.state = {
            "rainfall_mm": self.digital_layer_output["rainfall_mm"][i],
            "water_level_m": self.assimilated["water_level"]["posterior_mean"][i],
            "discharge_m3s": self.assimilated["discharge"]["posterior_mean"][i],
            "soil_moisture": self.assimilated["soil_moisture"]["posterior_mean"][i],
            "sediment_conc_mgL": self.assimilated["sediment_conc"]["posterior_mean"][i],
        }
        self._has_run = True
        return self

    # ------------------------------------------------------------------
    def report(self) -> str:
        """Print a concise, human-readable run summary."""
        if not self._has_run:
            self.run()
        lines = [
            f"Bomo Gully Digital Twin (BG-DT) v1.0 -- run summary",
            f"  Site: {self.config.site_name}",
            f"  Simulation length: {len(self.sensors)} hourly steps",
            f"  Total rainfall: {self.sensors.rainfall_mm.sum():.1f} mm",
            f"  Annual soil loss (baseline):    {self.digital_layer_output['annual_soil_loss_baseline_t_ha_yr']:.1f} t/ha/yr",
            f"  Annual soil loss (biocontrol):   {self.digital_layer_output['annual_soil_loss_biocontrol_t_ha_yr']:.1f} t/ha/yr",
            f"  Factor of safety (baseline):     {self.digital_layer_output['factor_of_safety_baseline']:.2f}",
            f"  Factor of safety (biocontrol):   {self.digital_layer_output['factor_of_safety_biocontrol']:.2f}",
            f"  Current assimilated discharge:  {self.state['discharge_m3s']:.2f} m3/s",
        ]
        if self.sobol_table is not None:
            top = self.sobol_table.iloc[0]
            lines.append(f"  Most sensitive parameter: {top['parameter']} (total-order Sobol = {top['total_order']:.2f})")
        text = "\n".join(lines)
        print(text)
        return text
