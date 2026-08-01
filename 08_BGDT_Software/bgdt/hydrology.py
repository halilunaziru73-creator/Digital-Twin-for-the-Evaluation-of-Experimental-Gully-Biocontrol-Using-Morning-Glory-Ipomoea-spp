"""
bgdt.hydrology
---------------
Digital Layer: antecedent-moisture-accounting rainfall-runoff model.

Implements, verbatim, the manuscript's:
  Eq. (2)  soil-moisture infiltration balance
  Eq. (3)  moisture-dependent runoff coefficient
  Eq. (4)  unit-hydrograph convolution to discharge
"""
from __future__ import annotations

import numpy as np

from .config import HydrologyConfig


def soil_moisture_update(rainfall_mm: np.ndarray, cfg: HydrologyConfig) -> np.ndarray:
    """Eq. (2):  theta_t = theta_{t-1}(1 - k_r) + [k_i P_t (1 - theta_{t-1}/theta_max)] / dz

    Parameters
    ----------
    rainfall_mm : hourly rainfall series (mm)
    cfg : HydrologyConfig

    Returns
    -------
    theta : hourly soil-moisture series (m3/m3)
    """
    n = len(rainfall_mm)
    theta = np.zeros(n)
    theta[0] = 0.22
    for t in range(1, n):
        infil = cfg.k_infiltration * rainfall_mm[t] * (1 - theta[t - 1] / cfg.theta_max)
        theta[t] = theta[t - 1] * (1 - cfg.k_recession) + infil / cfg.active_soil_depth_mm
        theta[t] = np.clip(theta[t], 0.05, cfg.theta_max)
    return theta


def runoff_coefficient(theta: np.ndarray, cfg: HydrologyConfig) -> np.ndarray:
    """Eq. (3):  C(t) = C_min + (C_max - C_min) * theta_t / theta_max"""
    return cfg.c_min + (cfg.c_max - cfg.c_min) * theta / cfg.theta_max


def effective_rainfall(rainfall_mm: np.ndarray, theta: np.ndarray, cfg: HydrologyConfig) -> np.ndarray:
    """R_e(t) = C(t) * P(t), the moisture-dependent effective-rainfall term
    feeding Eq. (4)."""
    return runoff_coefficient(theta, cfg) * rainfall_mm


def unit_hydrograph(cfg: HydrologyConfig) -> np.ndarray:
    """Dimensionless exponential-decay unit hydrograph u(tau), normalised to
    unit volume, used in the convolution of Eq. (4)."""
    tau = np.arange(cfg.unit_hydrograph_length_h)
    u = np.exp(-tau / cfg.unit_hydrograph_decay)
    return u / u.sum()


def discharge_from_rainfall(rainfall_mm: np.ndarray, cfg: HydrologyConfig) -> dict:
    """Full Eq. (2)-(4) pipeline: rainfall -> soil moisture -> effective
    rainfall -> discharge via unit-hydrograph convolution.

    Returns a dict with keys 'soil_moisture', 'effective_rainfall',
    'discharge' (all same length as `rainfall_mm`).
    """
    theta = soil_moisture_update(rainfall_mm, cfg)
    r_eff = effective_rainfall(rainfall_mm, theta, cfg)
    uh = unit_hydrograph(cfg)
    q = np.convolve(r_eff, uh, mode="full")[: len(rainfall_mm)] * cfg.discharge_scale
    q = np.clip(q, 0.02, None)
    return {"soil_moisture": theta, "effective_rainfall": r_eff, "discharge": q}
