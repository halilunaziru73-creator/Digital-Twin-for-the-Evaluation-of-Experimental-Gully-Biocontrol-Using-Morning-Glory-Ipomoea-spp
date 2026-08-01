# Digital Twin for the Evaluation of Experimental Gully Biocontrol
### Morning Glory (Ipomoea spp. / Ipomoea carnea) — Bomo Gully, Zaria, Nigeria
### Author: Naziru Halilu — 35-page manuscript, 14 figures, 10 tables, 16 equations

## Summary of what's in this package
A full Elsevier-format manuscript (*Environmental Modelling & Software*)
for a digital-twin framework evaluating Morning Glory (Ipomoea spp.)
gully-erosion biocontrol, combining synthetic-but-consistent continuous
digital-twin data with **real, field-measured data extracted from the
author's B.Eng. thesis**, plus two genuinely trained deep-learning models,
real statistical significance tests, and the complete reproducible code
and data pipeline.

## Change log

### Round 1
- Fixed a photo mix-up (poster PNGs mistakenly used instead of real field
  photos); corrected Figure 2 to use the actual PXL_*.jpg site photos.
- Renumbered all figures to strict order of appearance; removed all
  overlaid/floating panel labels (letters are now part of each panel's
  own title/caption text, never stamped over plot or photo content).
- Added a realistic sensor-installation illustration (Figure 3) with
  recognizable instrument shapes (tipping-bucket rain gauge, capacitance
  soil-moisture probes, PVC stilling well, area-velocity/turbidity probe,
  weatherproof logger enclosure with solar panel and antenna).
- Added a digital-twin dashboard/3-D visualization figure (Figure 14).
- Added 14 numbered equations (Eq. (1)-(14) at the time) across the
  hydrological, hydraulic, vegetation, geotechnical, Bayesian, ML, and
  statistical methods.
- Author block updated to Naziru Halilu with four affiliations (Ahmadu
  Bello University Zaria / Public University of Navarre / UTAD Portugal /
  Federal University Dutse) and corresponding e-mail
  halilu.175366@e.unavarra.es.

### Round 2 — real data, deep learning, and expansion to 30+ pages
- **Real thesis data incorporated.** Your uploaded B.Eng. project —
  *"The Use of Morning Glory (Ipomoea carnea) for Controlling Gully
  Erosion within the Watercourse of Ahmadu Bello University Dam"*
  (Halilu, 2024, U18AE2018) — was mined for genuine field data: channel
  geometry at 20 real stations, and sediment transport/velocity/soil
  shear under 5 real experimental conditions (baseline; 1.0 m and 1.5 m
  ponding, pre- and post-Morning-Glory). 100 real records, now Section
  3.5, Figure 4, and Tables 1-2 of the manuscript.
- **Real gully photographs** added to Figure 2 (panels E-F).
- **Deep learning, genuinely trained** (scikit-learn MLPRegressor, 4
  hidden layers): a real-data DNN on the 100 real thesis records
  (honest R²≈0.26-0.34, beating the thesis's own linear-regression
  benchmark), and a discharge-nowcasting DNN on 1,559 synthetic
  time-series windows (R²=0.87). Both are genuinely computed, not
  fabricated — training curves, predictions, and metrics are all real.
- **Data processing/storage/visualization architecture** (Section 4.2,
  Figure 6, Table 4): pipeline, database ERD, storage volumes, dashboard
  tech stack. **Deep-learning architecture** (Section 4.5, Figure 7,
  Table 5).
- Manuscript expanded to **34 pages** at this point.

### Round 3 — precise photo verification and statistical rigor
- **Precisely verified photo-plate matching.** Rather than guessing which
  thesis photo matched which "Plate" caption (as Round 2 did, using color
  statistics), I parsed the thesis .docx's underlying XML structure
  directly — reading `word/document.xml` paragraph-by-paragraph and
  cross-referencing `word/_rels/document.xml.rels` — to build an exact,
  verifiable table of all 12 Plates and their image files. Figure 2
  (panels E-F) now uses the thesis's own explicit "before intervention" /
  "after intervention" pair: **Plate X** (`image30.jpg`) and **Plate XI**
  (`image31.jpg`). Full mapping and method documented in
  `06_Data_Real_Field/PHOTO_VERIFICATION_METHOD.md`.
- **Real statistical significance testing added** (new Table 3, Section
  3.5): paired Wilcoxon signed-rank tests and paired t-tests on the real
  field data, comparing pre- vs. post-control at each ponding depth. This
  is a genuine, nuanced finding — velocity reduction is highly
  significant at both 1.0 m and 1.5 m ponding (p<0.001), but the
  sediment-transport reduction, while significant at 1.0 m (p=0.004), is
  **not** statistically significant at 1.5 m (p=0.19) — an honestly
  reported limitation suggesting Morning Glory alone may need pairing
  with structural measures under more severe hydraulic loading.
- Manuscript now **35 pages, 14 figures, 10 tables, 16 equations**,
  re-verified end-to-end: every figure/table caption is in strict
  numerical order with matching in-text references (checked by full-text
  extraction, not just visual spot-checks).

## Contents
- `01_Manuscript/` — Full manuscript (.docx + .pdf).
- `02_Code/` — Full reproducible pipeline:
  - `00_real_thesis_data.py` — transcribes the real thesis data tables.
  - `01_generate_data.py` — generates the synthetic continuous digital-twin
    dataset.
  - `01b_statistical_tests.py` — runs the real Wilcoxon/paired-t-test
    analysis on the real field data.
  - `02_generate_figures.py` — builds all 13 generated figures (300 dpi).
  - `03_train_deep_learning_model.py` — trains the real-data DNN.
  - `04_train_dl_nowcasting_model.py` — trains the discharge-nowcasting DNN.
  - `03_build_manuscript.js` — assembles the manuscript .docx.
- `03_Data_Synthetic/` — synthetic-but-physically-consistent continuous
  digital-twin datasets (hydrology, DEM-of-Difference grid, ML training
  set, scenario simulations, etc.) — 15 CSV/NPZ files.
- `04_Figures/` — all 13 generated PNG figures (Figure 1 is the
  author-supplied map, used directly — see `05_Source_Images/`).
- `05_Source_Images/` — the Bomo Basin map, the 4 original site photos,
  and the 2 precisely-verified real thesis plates (X and XI) used in
  Figure 2.
- `06_Data_Real_Field/` — **the real data**: all 8 transcribed thesis
  tables, the consolidated 100-record real dataset, the real statistical
  test results, the real deep-learning training histories/predictions/
  metrics, the photo-verification method and mapping table, and a copy of
  your original thesis document as the data's source of truth.
- `07_Trained_Models/` — the actual trained model files (joblib):
  `dnn_sediment_transport.joblib`, `dnn_velocity.joblib`,
  `dnn_discharge_nowcast.joblib`, plus fitted `StandardScaler`s and a
  `feature_columns.txt` listing each model's exact expected input order.

## Reproducing everything end-to-end
```bash
pip install numpy pandas matplotlib pillow scikit-learn scipy joblib --break-system-packages
python3 02_Code/00_real_thesis_data.py            # -> 06_Data_Real_Field/*.csv
python3 02_Code/01b_statistical_tests.py          # -> real significance tests
python3 02_Code/01_generate_data.py               # -> 03_Data_Synthetic/*.csv
python3 02_Code/02_generate_figures.py            # -> 04_Figures/*.png
python3 02_Code/03_train_deep_learning_model.py   # -> 07_Trained_Models/, real-data DL results
python3 02_Code/04_train_dl_nowcasting_model.py    # -> 07_Trained_Models/, nowcast DL results
npm install docx                                   # (only if not already installed)
node 02_Code/03_build_manuscript.js               # -> manuscript .docx
```

## Loading a trained model yourself
```python
import joblib, numpy as np
model = joblib.load("07_Trained_Models/dnn_velocity.joblib")
scaler = joblib.load("07_Trained_Models/scaler_X.joblib")
# feature order: water_depth_m, slope_decimal, soil_shear_lb_ft2, biocontrol, ponding_depth_m
X_new = scaler.transform(np.array([[0.9, 0.01, 0.6, 1, 1.0]]))
print(model.predict(X_new))
```

## Verification performed
- All 14 figure captions appear in strict numerical order (1→14) and every
  in-text `Fig. N` reference matches its caption.
- All 10 table captions appear in strict numerical order (1→10) and every
  in-text `Table N` reference matches its caption.
- All subsections (2.1→5.8) are correctly nested and sequential.
- All 16 equation cross-references (`Eq. (N)`) were manually checked
  against what each equation actually is, after three rounds of
  insertion-driven renumbering.
- Photo-to-plate matching verified via direct XML parsing of the source
  thesis (not visual guessing) — see `PHOTO_VERIFICATION_METHOD.md`.
- Document is 35 pages (LibreOffice PDF export, Times New Roman, standard
  margins).

## IMPORTANT — before submission
1. **Only the data in `06_Data_Real_Field/` is real, measured data.**
   Everything in `03_Data_Synthetic/` is synthetic-but-consistent,
   generated to make the full continuous digital twin demonstrable
   end-to-end (real field campaigns are necessarily discrete/episodic,
   not continuous hourly telemetry). This distinction is stated
   explicitly in the manuscript (Section 3.5) — please keep it that way
   in any further edits, for scientific integrity.
2. **DL model performance on the real 100-record dataset is modest
   (R²≈0.26-0.34).** This is reported honestly rather than inflated. With
   only 100 real records split 75/25, this is a realistic and defensible
   result, but reviewers may ask for a larger real dataset if you want to
   push this number higher.
3. **The 1.5 m ponding sediment-transport non-significance (p=0.19) is a
   real, honest finding** — do not be tempted to remove or soften it; it
   is scientifically valuable and strengthens the paper's credibility.
4. **Verify every reference/DOI** in the reference list against CrossRef
   before submission, including the new `Halilu2024` thesis citation
   (currently formatted as an unpublished B.Eng. project reference —
   update if it becomes formally archived/published).
5. Regenerate the Graphical Abstract separately per the journal's Guide
   for Authors.
6. Deposit code/data/models to a permanent repository (e.g., Zenodo) and
   update the Data/Software availability statements with the real DOI.

## Author
Naziru Halilu, 2026 .
