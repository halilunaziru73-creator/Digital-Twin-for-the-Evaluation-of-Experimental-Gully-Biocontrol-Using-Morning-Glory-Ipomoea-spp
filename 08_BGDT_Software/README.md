# Bomo Gully Digital Twin (BG-DT) v1.0

A four-layer (Physical / Digital / Brain / Service) digital-twin software
package for evaluating experimental gully bioengineering (Morning Glory /
*Ipomoea* spp.) interventions, developed to accompany:

> Halilu, N. (2026). *Digital Twin for the Evaluation of Experimental
> Gully Biocontrol Using Morning Glory (Ipomoea spp.): A Coupled
> Hydro-Geomorphic, Bayesian, and Machine-Learning Framework for the Bomo
> Gully, Zaria, Nigeria.* Environmental Modelling & Software.

Every function in this package implements one of the manuscript's 16
numbered equations. See each module's docstring for the exact mapping.

## Architecture

| Layer | Module | Equations | What it does |
|---|---|---|---|
| Physical | `bgdt.physical` | — | Sensor network simulation/ingestion (rainfall) |
| Digital | `bgdt.hydrology` | Eq. 2-4 | Antecedent-moisture rainfall-runoff, unit hydrograph |
| Digital | `bgdt.hydraulics` | Eq. 5-7 | Vegetation-adjusted Manning velocity, shear stress, stream power |
| Digital | `bgdt.vegetation` | Eq. 8-9 | Root-reinforced shear strength, infinite-slope factor of safety |
| Digital | `bgdt.sediment` | Eq. 10 | RUSLE-type hillslope sediment supply |
| Brain | `bgdt.bayesian` | Eq. 11 | Ensemble (particle-filter) Bayesian data assimilation |
| Brain | `bgdt.ml_model` | Eq. 12 | Gradient-boosted sediment-yield model + **exact** Shapley-value explainer |
| Brain | `bgdt.deep_learning` | Eq. 13 | Deep neural networks (real-data model + discharge nowcaster) |
| Service | `bgdt.scenario` | Eq. 14 | Return-period scenario simulation + Saltelli/Jansen Sobol sensitivity |
| — | `bgdt.metrics` | Eq. 15-16 | NSE, PBIAS and other performance metrics |
| — | `bgdt.dashboard` | — | Live-state text/plot dashboard rendering |
| — | `bgdt.pipeline` | — | `BomoGullyDigitalTwin` orchestrator tying every layer together |

### A note on "no external ML-interpretability/sensitivity libraries"
`shap` and `SALib` are not required. Instead:
- `bgdt.ml_model.SedimentYieldModel.shapley_values()` computes the
  **exact** Shapley value from Eq. (12) by brute-force coalition
  enumeration (practical for the manuscript's 10-feature model). Its
  correctness is verified in `tests/test_bgdt.py` via the Shapley
  *efficiency property* (contributions sum exactly to
  `f(x) - f(baseline)`).
- `bgdt.scenario.sobol_indices()` computes first-order (Eq. 14) and
  total-order Sobol indices using the classic Saltelli (2002) / Jansen
  (1999) Monte-Carlo estimators, requiring only independent uniform
  sampling — no specialised sensitivity-analysis package.

## Installation

```bash
# Option A: install dependencies and run directly from this directory
pip install -r requirements.txt --break-system-packages   # or in a venv, drop the flag
python run_bgdt.py

# Option B: install as an editable package (requires internet access for
# setuptools/pip's build backend if not already cached)
pip install -e .
python -c "from bgdt import BomoGullyDigitalTwin; BomoGullyDigitalTwin.from_default_config().run().report()"
```

## Quick start

```python
from bgdt import BomoGullyDigitalTwin

dt = BomoGullyDigitalTwin.from_default_config()
dt.run()          # Physical -> Digital -> Brain -> Service, end to end
dt.report()        # prints a run summary

dt.state                     # current assimilated live state (dict)
dt.digital_layer_output       # full Digital-Layer trajectory
dt.assimilated                # Bayesian posterior mean + 95% CI per variable
dt.scenario_table             # Table 9-equivalent: return-period scenarios
dt.sobol_table                 # Table 10-equivalent: Sobol sensitivity indices
```

### Training the ML/DL models

```python
import pandas as pd
from bgdt.config import BGDTConfig
from bgdt.pipeline import BomoGullyDigitalTwin

dt = BomoGullyDigitalTwin.from_default_config()
dt.run()

# Gradient-boosted sediment-yield model + exact Shapley values (Eq. 12)
X = pd.DataFrame(...)   # 10 features, see BGDTConfig().ml.feature_names
y = ...                  # sediment yield target
metrics = dt.fit_ml_model(X, y)
importance = dt.ml_model.mean_abs_shap(X)

# Deep neural network on real field data (Eq. 13)
real_df = pd.read_csv("Real_field_dataset_consolidated.csv")
metrics = dt.fit_deep_learning(real_df, target="velocity_ms")

# Discharge-nowcasting deep neural network (Eq. 13)
metrics = dt.fit_nowcasting_dnn()
```

### Command-line usage

```bash
python run_bgdt.py --real-data Real_field_dataset_consolidated.csv --output-dir outputs
```

This runs the full pipeline and writes:
- `outputs/bgdt_assimilated_state.csv` — the Bayesian-assimilated state trajectory
- `outputs/bgdt_scenario_simulation.csv` — return-period scenario table
- `outputs/bgdt_sobol_sensitivity.csv` — Sobol sensitivity indices

## Running the tests

```bash
python tests/test_bgdt.py          # plain-Python runner, no pytest required
# or
python -m pytest tests/ -v
```

All 10 tests pass, including a genuine check that the Shapley-value
implementation satisfies the mathematical efficiency property required by
Eq. (12).

## Configuration

All parameters live in `bgdt/config.py` as typed dataclasses
(`HydrologyConfig`, `HydraulicsConfig`, `VegetationConfig`,
`SedimentConfig`, `BayesianConfig`, `MLConfig`, `DeepLearningConfig`,
`ScenarioConfig`), bundled into a single `BGDTConfig`. Defaults are
calibrated to reproduce the manuscript's reported magnitudes (e.g. ~18.6
t ha⁻¹ yr⁻¹ baseline / ~9.7 t ha⁻¹ yr⁻¹ post-biocontrol annual soil loss).
Override any field to explore a different site or scenario:

```python
from bgdt.config import BGDTConfig, SedimentConfig
cfg = BGDTConfig(sediment=SedimentConfig(rainfall_erosivity_R=800.0))
dt = BomoGullyDigitalTwin(cfg)
```

## License
MIT (see `pyproject.toml`).

## Author
Naziru Halilu, 2026.
