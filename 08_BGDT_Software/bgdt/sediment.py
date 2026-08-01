"""
bgdt.sediment
--------------
Digital Layer: hillslope-to-channel sediment supply.

Implements, verbatim, the manuscript's:
  Eq. (10)  A = R * K * LS * C * P  (RUSLE-type erosivity-erodibility formulation)
"""
from __future__ import annotations
import numpy as np

from .config import SedimentConfig


def rusle_soil_loss(cfg: SedimentConfig, biocontrol: bool = False) -> float:
    """Eq. (10):  A = R . K . LS . C . P

    Returns the average annual soil loss (t ha-1 yr-1) for either the
    baseline (biocontrol=False) or Morning-Glory-treated (biocontrol=True)
    cover-management factor C.
    """
    C = cfg.cover_management_C_biocontrol if biocontrol else cfg.cover_management_C_baseline
    return (cfg.rainfall_erosivity_R * cfg.soil_erodibility_K *
            cfg.slope_length_factor_LS * C * cfg.support_practice_P) / cfg.unit_scaling_divisor


def sediment_trapping_efficiency(soil_loss_baseline: float, soil_loss_biocontrol: float,
                                   deposition_fraction: float = 0.621) -> float:
    """Fraction of the erosion reduction that is retained on-site as
    deposition within vegetation strips, rather than exported downstream
    (calibrated against the manuscript's reported 62.1% trapping
    efficiency, Section 5.2)."""
    reduction = soil_loss_baseline - soil_loss_biocontrol
    return deposition_fraction * reduction / soil_loss_baseline if soil_loss_baseline > 0 else 0.0
