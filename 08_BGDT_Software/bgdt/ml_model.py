"""
bgdt.ml_model
--------------
Brain Layer: interpretable gradient-boosted sediment-yield model.

Implements, verbatim, the manuscript's:
  Eq. (12)  phi_i = sum_{S subset F\\{i}} [|S|!(|F|-|S|-1)!/|F|!] . [f(S union {i}) - f(S)]

Because the `shap` package is not assumed to be installed, this module
provides a genuine, exact Shapley-value computation for small feature
sets (<= ~12 features) using the standard "interventional" convention
(missing features replaced by their training-set mean), which
reproduces Eq. (12) exactly rather than approximating it. For the
manuscript's 10-feature sediment-yield model this requires evaluating
2^10 = 1024 coalitions per explained instance, which is fast enough for
batch explanation of a full test set.
"""
from __future__ import annotations

import itertools
import math
from typing import List

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from .config import MLConfig


class SedimentYieldModel:
    """Gradient-boosted regressor for event-based sediment yield
    (t ha-1 yr-1), with an exact Shapley-value explainer (Eq. 12)."""

    def __init__(self, cfg: MLConfig):
        self.cfg = cfg
        self.model = GradientBoostingRegressor(
            n_estimators=cfg.n_estimators, max_depth=cfg.max_depth,
            learning_rate=cfg.learning_rate, random_state=cfg.random_state,
        )
        self._background_mean: np.ndarray | None = None
        self._is_fit = False

    # ------------------------------------------------------------------
    def fit(self, X: pd.DataFrame, y: np.ndarray) -> dict:
        """Fit the model and report held-out test performance."""
        X_train, X_test, y_train, y_test = train_test_split(
            X.values, y, test_size=self.cfg.test_size, random_state=self.cfg.random_state)
        self.model.fit(X_train, y_train)
        self._background_mean = X_train.mean(axis=0)
        self._is_fit = True

        pred = self.model.predict(X_test)
        metrics = dict(
            R2=r2_score(y_test, pred),
            NSE=1 - np.sum((y_test - pred) ** 2) / np.sum((y_test - y_test.mean()) ** 2),
            RMSE=np.sqrt(mean_squared_error(y_test, pred)),
            MAE=mean_absolute_error(y_test, pred),
        )
        self._X_test, self._y_test, self._pred_test = X_test, y_test, pred
        return metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X.values)

    # ------------------------------------------------------------------
    def _f(self, x_instance: np.ndarray, present_mask: np.ndarray) -> float:
        """Evaluate the model with only the features in `present_mask`
        'on' (interventional value function f(S) in Eq. 12); missing
        features are replaced by the training background mean."""
        x = np.where(present_mask, x_instance, self._background_mean)
        return float(self.model.predict(x.reshape(1, -1))[0])

    def shapley_values(self, x_instance: np.ndarray) -> np.ndarray:
        """Exact Shapley value phi_i for every feature, for one instance,
        computed directly from Eq. (12) by brute-force coalition
        enumeration. O(2^F) -- only practical for F <= ~14; the
        manuscript's model uses F=10.
        """
        if not self._is_fit:
            raise RuntimeError("Call .fit() before computing Shapley values.")
        n_features = len(x_instance)
        all_idx = list(range(n_features))
        phi = np.zeros(n_features)

        for i in all_idx:
            others = [j for j in all_idx if j != i]
            total = 0.0
            for r in range(len(others) + 1):
                for subset in itertools.combinations(others, r):
                    mask_S = np.zeros(n_features, dtype=bool)
                    mask_S[list(subset)] = True
                    mask_S_i = mask_S.copy()
                    mask_S_i[i] = True

                    f_S = self._f(x_instance, mask_S)
                    f_S_i = self._f(x_instance, mask_S_i)

                    weight = (math.factorial(len(subset)) *
                              math.factorial(n_features - len(subset) - 1) /
                              math.factorial(n_features))
                    total += weight * (f_S_i - f_S)
            phi[i] = total
        return phi

    def mean_abs_shap(self, X: pd.DataFrame, max_instances: int = 30) -> pd.Series:
        """Mean |Shapley value| per feature over (a sample of) instances,
        used for the global feature-importance ranking in Fig. 11D."""
        Xv = X.values[:max_instances]
        all_phi = np.array([self.shapley_values(row) for row in Xv])
        return pd.Series(np.abs(all_phi).mean(axis=0), index=X.columns).sort_values(ascending=False)
