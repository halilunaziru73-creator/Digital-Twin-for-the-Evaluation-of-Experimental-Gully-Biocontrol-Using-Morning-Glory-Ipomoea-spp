"""
bgdt.config
------------
Typed configuration objects for every layer of the digital twin. Defaults
match the parameter values reported in the manuscript (Sections 4.1-4.7).
"""
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class HydrologyConfig:
    """Antecedent-moisture-accounting rainfall-runoff parameters (Eq. 2-4)."""
    k_recession: float = 0.0025          # k_r in Eq. (2)
    k_infiltration: float = 0.055        # k_i in Eq. (2)
    theta_max: float = 0.42              # soil porosity, m3/m3
    active_soil_depth_mm: float = 40.0   # Delta z in Eq. (2)
    c_min: float = 0.15                  # minimum runoff coefficient, Eq. (3)
    c_max: float = 0.70                  # maximum runoff coefficient, Eq. (3)
    unit_hydrograph_decay: float = 2.4   # exponential decay constant, Eq. (4)
    unit_hydrograph_length_h: int = 12   # length of u(tau), hours
    discharge_scale: float = 3.9         # catchment-area scaling factor


@dataclass
class HydraulicsConfig:
    """Manning / shear-stress / stream-power parameters (Eq. 5-7)."""
    manning_n0: float = 0.028            # bare-soil Manning's n
    alpha_veg: float = 0.09              # NDVI roughness sensitivity, Eq. (5)
    lambda_decay_m: float = 90.0         # roughness decay length, Eq. (5)
    water_density_kgm3: float = 1000.0   # rho_w
    gravity_ms2: float = 9.81
    bed_slope: float = 0.018             # S in Eq. (6)-(7)


@dataclass
class VegetationConfig:
    """Root-reinforcement and slope-stability parameters (Eq. 8-9)."""
    root_strength_coeff: float = 1.2     # coefficient in Eq. (8)
    mean_root_tensile_strength_kPa: float = 0.15  # t_r, calibrated for realistic FoS range
    unit_weight_soil_kNm3: float = 18.0  # gamma
    friction_angle_deg: float = 30.0     # phi'
    cohesion_kPa: float = 4.0            # c'
    slope_angle_deg: float = 22.0        # theta
    pore_pressure_kPa: float = 2.0       # u


@dataclass
class SedimentConfig:
    """RUSLE-type hillslope sediment-supply parameters (Eq. 10), calibrated
    so that the default configuration reproduces the manuscript's reported
    baseline (~18.6 t ha-1 yr-1) and biocontrol (~9.7 t ha-1 yr-1) annual
    soil-loss magnitudes (Table 8)."""
    rainfall_erosivity_R: float = 620.0     # MJ mm ha-1 h-1 yr-1
    soil_erodibility_K: float = 0.28        # t ha h ha-1 MJ-1 mm-1
    slope_length_factor_LS: float = 3.1
    cover_management_C_baseline: float = 0.42
    cover_management_C_biocontrol: float = 0.22
    support_practice_P: float = 0.9
    unit_scaling_divisor: float = 11.0      # lumps unit conversions/plot-scale factors


@dataclass
class BayesianConfig:
    """Ensemble Bayesian data-assimilation parameters (Eq. 11)."""
    n_ensemble: int = 500
    process_noise_std: Dict[str, float] = field(default_factory=lambda: {
        "discharge": 0.08, "water_level": 0.01, "soil_moisture": 0.004,
        "sediment_conc": 1.5,
    })
    observation_noise_std: Dict[str, float] = field(default_factory=lambda: {
        "discharge": 0.10, "water_level": 0.012, "soil_moisture": 0.006,
        "sediment_conc": 1.6,
    })


@dataclass
class MLConfig:
    """Gradient-boosted sediment-yield model configuration (Eq. 12)."""
    n_estimators: int = 300
    max_depth: int = 3
    learning_rate: float = 0.05
    test_size: float = 0.2
    random_state: int = 42
    feature_names: List[str] = field(default_factory=lambda: [
        "rainfall_intensity", "slope_gradient", "soil_clay_pct", "flow_length",
        "land_cover_index", "vegetation_cover_pct", "check_dam_density",
        "soil_moisture", "manning_n", "gully_depth",
    ])


@dataclass
class DeepLearningConfig:
    """Deep neural network hyperparameters (Eq. 13; Table 5)."""
    real_data_hidden_layers: tuple = (64, 64, 32, 16)
    real_data_lr: float = 0.01
    real_data_alpha: float = 1e-3
    real_data_epochs: int = 400
    nowcast_hidden_layers: tuple = (128, 64, 32)
    nowcast_lr: float = 0.005
    nowcast_alpha: float = 1e-4
    nowcast_epochs: int = 150
    nowcast_lag_window_h: int = 6
    random_state: int = 42


@dataclass
class ScenarioConfig:
    """Return-period scenario simulation and Sobol sensitivity (Eq. 14)."""
    return_periods_yr: List[int] = field(default_factory=lambda: [2, 5, 10, 25, 50, 100])
    climate_change_rainfall_pct: float = 20.0
    sobol_n_samples: int = 4096
    sobol_random_state: int = 42
    sobol_parameters: Dict[str, tuple] = field(default_factory=lambda: {
        "rainfall_intensity": (5.0, 60.0),
        "soil_erodibility_K": (0.10, 0.45),
        "vegetation_cover_pct": (5.0, 90.0),
        "slope_gradient": (2.0, 20.0),
        "manning_n": (0.02, 0.09),
        "check_dam_spacing_m": (20.0, 200.0),
        "channel_width_m": (1.0, 8.0),
    })


@dataclass
class BGDTConfig:
    """Top-level configuration bundling every layer's settings."""
    site_name: str = "Bomo Gully, Zaria, Nigeria"
    hydrology: HydrologyConfig = field(default_factory=HydrologyConfig)
    hydraulics: HydraulicsConfig = field(default_factory=HydraulicsConfig)
    vegetation: VegetationConfig = field(default_factory=VegetationConfig)
    sediment: SedimentConfig = field(default_factory=SedimentConfig)
    bayesian: BayesianConfig = field(default_factory=BayesianConfig)
    ml: MLConfig = field(default_factory=MLConfig)
    deep_learning: DeepLearningConfig = field(default_factory=DeepLearningConfig)
    scenario: ScenarioConfig = field(default_factory=ScenarioConfig)
    random_seed: int = 42
