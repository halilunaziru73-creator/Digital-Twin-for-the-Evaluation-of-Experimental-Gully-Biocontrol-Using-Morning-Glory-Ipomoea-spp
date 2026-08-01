"""
bgdt.physical
--------------
Physical Layer: represents the field sensor network described in Section
3.4 of the manuscript (rain gauges, water-level loggers, soil-moisture
probes, discharge/turbidity sensor). Two data sources are supported:

  1. `SensorNetwork.simulate(...)` -- generates a physically plausible,
     stochastic storm-driven rainfall record for demonstration/testing
     when no live sensor feed is available (this is what backs the
     digital twin's continuous "synthetic" operating mode described in
     the manuscript's Data Availability statement).
  2. `SensorNetwork.from_csv(path)` -- ingests a real quality-controlled
     CSV export from the field telemetry pipeline (Section 4.2), with the
     same schema as `01_generate_data.py`'s output
     (`01_dt_state_estimation_timeseries.csv`) or a real field campaign
     export (Section 3.5's consolidated dataset).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


class SensorNetwork:
    """Represents the Physical-Layer sensor array of one monitoring reach."""

    def __init__(self, timestamps: pd.DatetimeIndex, rainfall_mm: np.ndarray):
        self.timestamps = pd.DatetimeIndex(timestamps)
        self.rainfall_mm = np.asarray(rainfall_mm, dtype=float)

    # ------------------------------------------------------------------
    @classmethod
    def simulate(cls, start: str = "2024-06-01", end: str = "2024-08-20",
                 freq: str = "1h", storm_prob: float = 0.018,
                 random_state: int = 42) -> "SensorNetwork":
        """Simulate a stochastic, storm-driven rainfall record (Poisson
        storm arrivals, Gaussian-shaped intensity profile), representative
        of a Sub-Saharan single-rainy-season regime."""
        rng = np.random.default_rng(random_state)
        timestamps = pd.date_range(start, end, freq=freq)
        n = len(timestamps)
        rain = np.zeros(n)
        i = 0
        while i < n:
            if rng.random() < storm_prob:
                dur = rng.integers(1, 5)
                peak = rng.gamma(shape=2.2, scale=9.0)
                profile = peak * np.exp(-0.5 * (np.linspace(-1.3, 1.3, dur)) ** 2)
                profile = np.clip(profile + rng.normal(0, 0.3, dur), 0, None)
                end_i = min(n, i + dur)
                rain[i:end_i] += profile[: end_i - i]
                i = end_i + rng.integers(2, 30)
            else:
                i += 1
        return cls(timestamps, np.clip(rain, 0, None))

    # ------------------------------------------------------------------
    @classmethod
    def from_csv(cls, path: str, time_col: str = "datetime",
                 rain_col: str = "rainfall_mm") -> "SensorNetwork":
        """Ingest a real (or previously-generated) quality-controlled CSV
        telemetry export."""
        df = pd.read_csv(path, parse_dates=[time_col])
        return cls(df[time_col], df[rain_col].values)

    # ------------------------------------------------------------------
    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame({"datetime": self.timestamps, "rainfall_mm": self.rainfall_mm})

    def __len__(self) -> int:
        return len(self.timestamps)

    def __repr__(self) -> str:
        return (f"<SensorNetwork n={len(self)} span={self.timestamps[0].date()} "
                f"to {self.timestamps[-1].date()} total_rain={self.rainfall_mm.sum():.1f} mm>")
