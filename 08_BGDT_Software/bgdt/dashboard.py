"""
bgdt.dashboard
---------------
Service Layer: renders the live-state dashboard snapshot described in
Section 5.6 of the manuscript (Fig. 14) -- as a plain-text console panel
by default, and optionally as a matplotlib figure image.
"""
from __future__ import annotations

from datetime import datetime
from typing import Dict

import numpy as np


def render_text_dashboard(state: Dict[str, float], status: str = "NORMAL") -> str:
    """Render a plain-text snapshot of the current assimilated digital-twin
    state, in the same spirit as the live dashboard cards in Fig. 14B."""
    lines = [
        "=" * 56,
        "  BOMO GULLY DIGITAL TWIN (BG-DT) v1.0 -- LIVE STATE",
        "=" * 56,
        f"  Timestamp:            {datetime.now().isoformat(timespec='seconds')}",
        f"  Rainfall intensity:   {state.get('rainfall_mm', float('nan')):.1f} mm/h",
        f"  Water level:          {state.get('water_level_m', float('nan')):.2f} m",
        f"  Discharge:            {state.get('discharge_m3s', float('nan')):.1f} m3/s",
        f"  Soil moisture:        {state.get('soil_moisture', float('nan')):.2f} m3/m3",
        f"  Sediment conc.:       {state.get('sediment_conc_mgL', float('nan')):.1f} mg/L",
        f"  System status:        {status}",
        "-" * 56,
    ]
    return "\n".join(lines)


def render_figure_dashboard(history: "pandas.DataFrame", save_path: str = None):
    """Render a matplotlib panel (hydrograph + status) mirroring Fig. 14C.
    Import matplotlib lazily so the core package has no hard plotting
    dependency."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(history["datetime"], history["discharge_obs_m3s"], color="#1a1a2e", lw=1.0, label="Observed")
    if "discharge_sim_m3s" in history.columns:
        ax.plot(history["datetime"], history["discharge_sim_m3s"], color="#e63946", lw=0.9,
                 alpha=0.85, label="Digital Twin (assimilated)")
    ax.set_xlabel("Time"); ax.set_ylabel("Discharge (m$^3$ s$^{-1}$)")
    ax.legend(frameon=False)
    ax.set_title("BG-DT Live Hydrograph")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=200)
    return fig
