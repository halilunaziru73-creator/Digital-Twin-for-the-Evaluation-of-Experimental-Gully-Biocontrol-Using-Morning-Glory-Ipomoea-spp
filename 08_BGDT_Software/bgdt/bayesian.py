"""
bgdt.bayesian
--------------
Brain Layer: sequential ensemble Bayesian data assimilation.

Implements, verbatim, the manuscript's:
  Eq. (11)  p(x_t | y_1:t) proportional-to p(y_t | x_t) . p(x_t | y_1:t-1)

An ensemble (particle) filter is used rather than a linear Kalman filter
because gully hydro-sedimentological dynamics are threshold-driven and
non-Gaussian (Section 4.3), consistent with integrated data-assimilation
practice for hydrological uncertainty (Liu and Gupta, 2007).
"""
from __future__ import annotations

import numpy as np

from .config import BayesianConfig


class EnsembleAssimilator:
    """A simple sequential-importance-resampling (bootstrap) particle
    filter implementing Eq. (11) for one scalar state variable at a time.

    Usage
    -----
    >>> filt = EnsembleAssimilator(cfg, variable="discharge")
    >>> posterior_mean, ci_lo, ci_hi = filt.run(prior_series, observations)
    """

    def __init__(self, cfg: BayesianConfig, variable: str, random_state: int = 42):
        self.cfg = cfg
        self.variable = variable
        self.rng = np.random.default_rng(random_state)
        self.process_noise = cfg.process_noise_std[variable]
        self.obs_noise = cfg.observation_noise_std[variable]

    def run(self, prior_series: np.ndarray, observations: np.ndarray):
        """Propagate an n_ensemble-member particle set through the full
        time series, applying Eq. (11) at every step where an observation
        is available.

        Parameters
        ----------
        prior_series : deterministic (Digital-Layer) model trajectory,
            used as the process-model prediction at each step.
        observations : the corresponding streaming sensor observations
            (same length; NaN entries are treated as missing/no-update).

        Returns
        -------
        posterior_mean, ci_lower_95, ci_upper_95 : np.ndarray (same length)
        """
        n = len(prior_series)
        n_ens = self.cfg.n_ensemble
        ensemble = np.tile(prior_series[0], n_ens) + self.rng.normal(0, self.process_noise, n_ens)

        post_mean = np.zeros(n)
        ci_lo = np.zeros(n)
        ci_hi = np.zeros(n)

        for t in range(n):
            # --- process model propagation (prior) ---
            if t > 0:
                drift = prior_series[t] - prior_series[t - 1]
                ensemble = ensemble + drift + self.rng.normal(0, self.process_noise, n_ens)
                ensemble = np.clip(ensemble, 0, None)

            # --- Bayesian update (Eq. 11) if an observation is available ---
            if not np.isnan(observations[t]):
                # likelihood weights ~ p(y_t | x_t) under Gaussian obs noise
                residual = observations[t] - ensemble
                weights = np.exp(-0.5 * (residual / self.obs_noise) ** 2)
                weights += 1e-12
                weights /= weights.sum()
                # resample (bootstrap) to draw from the posterior p(x_t | y_1:t)
                idx = self.rng.choice(n_ens, size=n_ens, p=weights)
                ensemble = ensemble[idx]

            post_mean[t] = ensemble.mean()
            ci_lo[t] = np.percentile(ensemble, 2.5)
            ci_hi[t] = np.percentile(ensemble, 97.5)

        return post_mean, ci_lo, ci_hi


def assimilate_all_states(model_trajectories: dict, observations: dict,
                           cfg: BayesianConfig) -> dict:
    """Convenience wrapper running `EnsembleAssimilator` over every state
    variable in a digital-twin run (discharge, water_level, soil_moisture,
    sediment_conc), returning posterior mean + 95% credible interval for
    each.
    """
    out = {}
    for var in model_trajectories:
        filt = EnsembleAssimilator(cfg, variable=var)
        mean, lo, hi = filt.run(model_trajectories[var], observations[var])
        out[var] = {"posterior_mean": mean, "ci_lower": lo, "ci_upper": hi}
    return out
