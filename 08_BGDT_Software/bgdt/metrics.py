"""
bgdt.metrics
-------------
Model-performance evaluation.

Implements, verbatim, the manuscript's:
  Eq. (15)  NSE = 1 - sum(O_i - S_i)^2 / sum(O_i - Obar)^2
  Eq. (16)  PBIAS = 100 * sum(S_i - O_i) / sum(O_i)
"""
from __future__ import annotations

import numpy as np


def nse(observed: np.ndarray, simulated: np.ndarray) -> float:
    """Eq. (15): Nash-Sutcliffe Efficiency."""
    observed, simulated = np.asarray(observed), np.asarray(simulated)
    return 1 - np.sum((observed - simulated) ** 2) / np.sum((observed - observed.mean()) ** 2)


def pbias(observed: np.ndarray, simulated: np.ndarray) -> float:
    """Eq. (16): Percent bias."""
    observed, simulated = np.asarray(observed), np.asarray(simulated)
    return 100 * np.sum(simulated - observed) / np.sum(observed)


def rmse(observed: np.ndarray, simulated: np.ndarray) -> float:
    observed, simulated = np.asarray(observed), np.asarray(simulated)
    return np.sqrt(np.mean((observed - simulated) ** 2))


def r_squared(observed: np.ndarray, simulated: np.ndarray) -> float:
    observed, simulated = np.asarray(observed), np.asarray(simulated)
    return np.corrcoef(observed, simulated)[0, 1] ** 2


def mae(observed: np.ndarray, simulated: np.ndarray) -> float:
    observed, simulated = np.asarray(observed), np.asarray(simulated)
    return np.mean(np.abs(observed - simulated))


def full_report(observed: np.ndarray, simulated: np.ndarray) -> dict:
    """Convenience wrapper returning every metric used throughout the
    manuscript's performance tables (Table 6)."""
    return dict(R2=r_squared(observed, simulated), NSE=nse(observed, simulated),
                RMSE=rmse(observed, simulated), MAE=mae(observed, simulated),
                PBIAS=pbias(observed, simulated))
