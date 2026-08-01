"""
tests/test_bgdt.py
--------------------
Basic sanity/unit tests for the BG-DT v1.0 package. Run with:
    python -m pytest tests/ -v
or, without pytest installed:
    python tests/test_bgdt.py
"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bgdt.config import BGDTConfig
from bgdt.physical import SensorNetwork
from bgdt import hydrology, hydraulics, vegetation, sediment, metrics
from bgdt.bayesian import EnsembleAssimilator
from bgdt.ml_model import SedimentYieldModel
from bgdt.scenario import scenario_simulation, sobol_indices
from bgdt.pipeline import BomoGullyDigitalTwin


def test_sensor_network_simulate():
    net = SensorNetwork.simulate(random_state=1)
    assert len(net) > 100
    assert net.rainfall_mm.sum() > 0


def test_hydrology_eq2_4():
    cfg = BGDTConfig().hydrology
    net = SensorNetwork.simulate(random_state=1)
    out = hydrology.discharge_from_rainfall(net.rainfall_mm, cfg)
    assert out["soil_moisture"].min() >= 0.05
    assert out["soil_moisture"].max() <= cfg.theta_max + 1e-9
    assert out["discharge"].min() >= 0.02
    assert len(out["discharge"]) == len(net)


def test_hydraulics_eq5_7():
    cfg = BGDTConfig().hydraulics
    depth = np.array([0.3, 0.6, 1.0])
    ndvi = np.array([0.2, 0.5, 0.8])
    n_v = hydraulics.vegetation_adjusted_manning_n(ndvi, np.array([10, 20, 30]), cfg)
    assert (n_v >= cfg.manning_n0).all()
    v = hydraulics.manning_velocity(depth, 0.02, n_v)
    assert (v > 0).all()
    tau = hydraulics.bed_shear_stress(depth, cfg)
    assert (tau > 0).all()
    omega = hydraulics.unit_stream_power(v, depth, cfg)
    assert (omega > 0).all()


def test_vegetation_eq8_9():
    cfg = BGDTConfig().vegetation
    rld = np.array([5.0, 20.0])
    depth = np.array([0.5, 0.5])
    S_R = vegetation.root_reinforced_shear_strength(rld, cfg)
    assert S_R[1] > S_R[0]  # more roots -> more reinforcement
    fs = vegetation.factor_of_safety(depth, rld, cfg)
    assert fs[1] > fs[0]    # more roots -> higher factor of safety


def test_sediment_eq10():
    cfg = BGDTConfig().sediment
    a_base = sediment.rusle_soil_loss(cfg, biocontrol=False)
    a_bio = sediment.rusle_soil_loss(cfg, biocontrol=True)
    assert a_bio < a_base  # biocontrol must reduce modelled soil loss


def test_bayesian_eq11():
    cfg = BGDTConfig().bayesian
    rng = np.random.default_rng(0)
    prior = np.cumsum(rng.normal(0, 0.1, 50)) + 5
    obs = prior + rng.normal(0, 0.2, 50)
    filt = EnsembleAssimilator(cfg, variable="discharge", random_state=0)
    mean, lo, hi = filt.run(prior, obs)
    assert len(mean) == 50
    assert (hi >= lo).all()


def test_ml_model_eq12_shapley_sums_to_prediction_minus_baseline():
    cfg = BGDTConfig().ml
    rng = np.random.default_rng(0)
    n = 200
    X = pd.DataFrame(rng.uniform(0, 1, size=(n, len(cfg.feature_names))), columns=cfg.feature_names)
    y = X.sum(axis=1).values + rng.normal(0, 0.05, n)
    model = SedimentYieldModel(cfg)
    metrics_out = model.fit(X, y)
    assert "R2" in metrics_out
    # Shapley efficiency property: sum(phi_i) == f(x) - f(baseline)
    x0 = X.values[0]
    phi = model.shapley_values(x0)
    f_x = model._f(x0, np.ones(len(x0), dtype=bool))
    f_baseline = model._f(x0, np.zeros(len(x0), dtype=bool))
    assert abs(phi.sum() - (f_x - f_baseline)) < 1e-6


def test_metrics_eq15_16():
    obs = np.array([1.0, 2.0, 3.0, 4.0])
    sim = np.array([1.1, 1.9, 3.2, 3.8])
    assert metrics.nse(obs, sim) > 0.9
    assert abs(metrics.pbias(obs, sim)) < 5.0


def test_scenario_and_sobol_eq14():
    cfg = BGDTConfig().scenario
    scen = scenario_simulation(cfg)
    assert (scen["peak_discharge_biocontrol_m3s"] < scen["peak_discharge_no_biocontrol_m3s"]).all()
    sobol = sobol_indices(cfg)
    assert set(sobol.columns) == {"parameter", "first_order", "total_order"}
    # The surrogate response is additive (no parameter interactions), so
    # total-order should approximately equal first-order for every
    # parameter; allow for expected Monte Carlo estimator noise at finite
    # sample size rather than asserting a strict inequality.
    assert (sobol["total_order"] >= sobol["first_order"] - 0.05).all()
    assert sobol.iloc[0]["parameter"] == "rainfall_intensity"  # dominant driver, per Table 10


def test_full_pipeline_runs_end_to_end():
    dt = BomoGullyDigitalTwin.from_default_config()
    dt.run()
    assert dt.state["discharge_m3s"] >= 0
    assert dt.scenario_table is not None
    assert dt.sobol_table is not None


if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items()) if name.startswith("test_")]
    passed, failed = 0, 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
