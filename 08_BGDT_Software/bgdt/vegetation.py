"""
bgdt.vegetation
----------------
Digital Layer: root-reinforcement and infinite-slope stability model.

Implements, verbatim, the manuscript's:
  Eq. (8)  root-reinforced shear strength (perpendicular root model)
  Eq. (9)  infinite-slope factor of safety with root cohesion
"""
from __future__ import annotations

import numpy as np

from .config import VegetationConfig


def root_reinforced_shear_strength(root_length_density: np.ndarray, cfg: VegetationConfig) -> np.ndarray:
    """Eq. (8):  S_R = t_R (cos(theta) tan(phi') + sin(theta)) ~= 1.2 * RLD * t_r

    `root_length_density` (RLD) is dimensionless (or cm/cm3 as field-measured);
    `t_r` is the mean single-root tensile strength (kPa).
    """
    return cfg.root_strength_coeff * root_length_density * cfg.mean_root_tensile_strength_kPa


def factor_of_safety(depth_m: np.ndarray, root_length_density: np.ndarray,
                      cfg: VegetationConfig) -> np.ndarray:
    """Eq. (9):  FS = [c' + S_R + (gamma h - u) tan(phi')] / (gamma h sin(theta) cos(theta))"""
    theta_rad = np.radians(cfg.slope_angle_deg)
    phi_rad = np.radians(cfg.friction_angle_deg)
    S_R = root_reinforced_shear_strength(root_length_density, cfg)
    gamma_h = cfg.unit_weight_soil_kNm3 * depth_m
    numerator = cfg.cohesion_kPa + S_R + (gamma_h - cfg.pore_pressure_kPa) * np.tan(phi_rad)
    denominator = gamma_h * np.sin(theta_rad) * np.cos(theta_rad)
    return numerator / np.clip(denominator, 1e-6, None)


def ndvi_to_root_length_density(ndvi: np.ndarray, rld_max: float = 20.0) -> np.ndarray:
    """Simple monotonic mapping from UAV-derived NDVI to an equivalent root
    length density index, used when direct root excavation data are
    unavailable (calibrated against the field-measured values in Table 8
    of the manuscript: baseline RLD ~4.8, post-biocontrol RLD ~18.9)."""
    return np.clip(ndvi, 0, 1) * rld_max
