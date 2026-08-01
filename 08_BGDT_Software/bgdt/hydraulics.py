"""
bgdt.hydraulics
----------------
Digital Layer: vegetation-adjusted hydraulic response.

Implements, verbatim, the manuscript's:
  Eq. (5)  vegetation-adjusted Manning velocity
  Eq. (6)  bed shear stress
  Eq. (7)  unit stream power
"""
from __future__ import annotations

import numpy as np

from .config import HydraulicsConfig


def vegetation_adjusted_manning_n(ndvi: np.ndarray, distance_from_head_m: np.ndarray,
                                    cfg: HydraulicsConfig) -> np.ndarray:
    """Eq. (5), roughness term:  n_v = n_0 + alpha * NDVI * exp(-x / lambda)"""
    return cfg.manning_n0 + cfg.alpha_veg * ndvi * np.exp(-distance_from_head_m / cfg.lambda_decay_m)


def manning_velocity(hydraulic_radius_m: np.ndarray, slope: np.ndarray,
                      manning_n: np.ndarray) -> np.ndarray:
    """Eq. (5), velocity term:  V = (1/n_v) R_h^(2/3) S^(1/2)"""
    return (1.0 / manning_n) * np.power(hydraulic_radius_m, 2.0 / 3.0) * np.sqrt(np.clip(slope, 1e-6, None))


def bed_shear_stress(depth_m: np.ndarray, cfg: HydraulicsConfig, slope: float | np.ndarray = None) -> np.ndarray:
    """Eq. (6):  tau_b = rho_w * g * h * S"""
    S = cfg.bed_slope if slope is None else slope
    return cfg.water_density_kgm3 * cfg.gravity_ms2 * depth_m * S


def unit_stream_power(velocity_ms: np.ndarray, depth_m: np.ndarray,
                       cfg: HydraulicsConfig, slope: float | np.ndarray = None) -> np.ndarray:
    """Eq. (7):  Omega = rho_w * g * V * h * S = tau_b * V"""
    tau_b = bed_shear_stress(depth_m, cfg, slope)
    return tau_b * velocity_ms


def froude_number(velocity_ms: np.ndarray, depth_m: np.ndarray, g: float = 9.81) -> np.ndarray:
    """Supplementary (not separately numbered in the manuscript, used in
    Fig. 8/Section 5.4 hydraulic characterisation): Fr = V / sqrt(g h)."""
    return velocity_ms / np.sqrt(g * np.clip(depth_m, 0.02, None))
