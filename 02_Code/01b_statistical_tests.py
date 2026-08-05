"""
01b_statistical_tests.py
--------------------------
Runs genuine statistical significance tests on the REAL field-measured
dataset (Halilu, 2024) to formally test whether Morning Glory biocontrol
produced a statistically significant reduction in sediment transport rate
and flow velocity, using the paired station-level design (the same 20
stations were measured under matched pre-/post-control conditions at each
ponding depth).

Tests used:
  - Paired (Wilcoxon signed-rank) test -- non-parametric, appropriate for
    n=20 paired samples without assuming normality.
  - Paired t-test -- reported alongside for comparison.
  - Shapiro-Wilk normality check on the paired differences, to justify
    the choice of non-parametric test.

Output: 06_Data_Real_Field/Statistical_significance_tests.csv
"""
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

DATA = Path(__file__).resolve().parent.parent / "06_Data_Real_Field"

t42 = pd.read_csv(DATA / "Table4_2_precontrol_baseline.csv")
t44 = pd.read_csv(DATA / "Table4_4_postcontrol_ponding_1_0m.csv")
t43 = pd.read_csv(DATA / "Table4_3_precontrol_ponding_1_0m.csv")
t45 = pd.read_csv(DATA / "Table4_5_precontrol_ponding_1_5m.csv")
t46 = pd.read_csv(DATA / "Table4_6_postcontrol_ponding_1_5m.csv")

rows = []


def paired_test(pre, post, label, variable):
    diff = post - pre
    # Shapiro-Wilk normality test on the paired differences
    sh_stat, sh_p = stats.shapiro(diff)
    # Wilcoxon signed-rank (non-parametric, robust choice given n=20)
    w_stat, w_p = stats.wilcoxon(pre, post)
    # Paired t-test (reported for comparison)
    t_stat, t_p = stats.ttest_rel(pre, post)
    rows.append(dict(
        comparison=label, variable=variable, n=len(pre),
        mean_pre=pre.mean(), mean_post=post.mean(),
        mean_reduction_pct=100 * (pre.mean() - post.mean()) / pre.mean(),
        shapiro_p=sh_p, wilcoxon_stat=w_stat, wilcoxon_p=w_p,
        paired_t_stat=t_stat, paired_t_p=t_p,
    ))


# 1.0 m ponding: pre-control (Table 4.3) vs post-control (Table 4.4)
paired_test(t43.sediment_transport_kg_s_m, t44.sediment_transport_kg_s_m,
            "1.0 m ponding: pre- vs post-control", "Sediment transport rate (kg s-1 m-1)")
paired_test(t43.velocity_ms, t44.velocity_ms,
            "1.0 m ponding: pre- vs post-control", "Flow velocity (m s-1)")

# 1.5 m ponding: pre-control (Table 4.5) vs post-control (Table 4.6)
paired_test(t45.sediment_transport_kg_s_m, t46.sediment_transport_kg_s_m,
            "1.5 m ponding: pre- vs post-control", "Sediment transport rate (kg s-1 m-1)")
paired_test(t45.velocity_ms, t46.velocity_ms,
            "1.5 m ponding: pre- vs post-control", "Flow velocity (m s-1)")

results = pd.DataFrame(rows)
results.to_csv(DATA / "Statistical_significance_tests.csv", index=False)

print(results.to_string(index=False))
print("\nWritten to", DATA / "Statistical_significance_tests.csv")
