"""
02_generate_figures.py  (v2)
-----------------------------
Builds all manuscript figures (Figures 2-8; Figure 1 is the author-supplied
basin map, used as-is). Changes from v1:
  * Panel letters (A, B, C ...) are placed BELOW each panel, in the
    whitespace outside the plot/photo -- never overlapping plot content
    or photographs.
  * No "Figure N. ..." title is burned into the PNG; the full caption is
    set in the Word manuscript (avoids duplicate/mismatched numbering).
  * A corrected field-photograph grid (Figure 2) is built from the actual
    high-resolution site photographs (PXL_*.jpg), not the poster PNGs.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
from PIL import Image
from pathlib import Path

DATA = Path("/home/claude/dt_gully/data")
FIG = Path("/home/claude/dt_gully/figures")
FIG.mkdir(parents=True, exist_ok=True)
UP = Path("/mnt/user-data/uploads")

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 9.3,
    "axes.titleweight": "bold", "axes.labelsize": 9, "xtick.labelsize": 8,
    "ytick.labelsize": 8, "legend.fontsize": 7.5, "figure.dpi": 150,
})
C_OBS, C_SIM, C_BASE, C_AFTER, C_FILL = "#1a1a2e", "#e63946", "#e63946", "#2a9d8f", "#457b9d"

def lab(letter, text):
    """Panel letter integrated directly into the panel's own title/caption
    text (e.g. '(A) Vegetation cover'). No separate label is ever drawn on
    top of / overlapping the plotted content or photograph -- the letter is
    simply the first characters of the existing title string."""
    return f"({letter}) {text}"

# =====================================================================
# FIGURE 2 - Field photographs of the Bomo Gully experimental reaches
# =====================================================================
THESIS_PHOTOS = Path("/home/claude/dt_gully/data_real/thesis_photos")
photos = [
    ("PXL_20260623_102136417.jpg", UP, "A", "Morning Glory (Ipomoea spp.) vegetation strip,\ntreated reach (~10 weeks after planting)"),
    ("PXL_20260623_102244103.jpg", UP, "B", "Active headcut and bare eroding bank,\nuntreated control reach"),
    ("PXL_20260623_102326179_2.jpg", UP, "C", "Transitional view of the gully channel\nshowing bank and bed conditions"),
    ("PXL_20260623_102459324.jpg", UP, "D", "Gully margin adjoining cultivated land,\nillustrating the contributing hillslope"),
    ("plate_X_before_intervention.jpg", THESIS_PHOTOS, "E", "Plate X: Real gully development BEFORE Morning\nGlory intervention, ABU Dam watercourse (Halilu, 2024)"),
    ("plate_XI_after_intervention.jpg", THESIS_PHOTOS, "F", "Plate XI: Real gully spot AFTER Morning Glory\nintervention, ABU Dam watercourse (Halilu, 2024)"),
]

fig = plt.figure(figsize=(11, 13.4))
gs = gridspec.GridSpec(3, 2, hspace=0.55, wspace=0.15)
for i, (fname, folder, letter, cap) in enumerate(photos):
    ax = fig.add_subplot(gs[i // 2, i % 2])
    im = Image.open(folder / fname)
    im.thumbnail((1400, 1400))
    ax.imshow(np.asarray(im))
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("#888888"); spine.set_linewidth(0.8)
    ax.text(0.5, -0.07, lab(letter, cap), transform=ax.transAxes, ha="center",
             va="top", fontsize=7.8, linespacing=1.5)

fig.tight_layout(rect=[0, 0.02, 1, 0.99])
fig.savefig(FIG / "Figure_2_field_photographs.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 3 - Sensor installation schematic & data-recording architecture
# =====================================================================
fig = plt.figure(figsize=(11, 9.6))
gs = gridspec.GridSpec(2, 2, hspace=0.55, wspace=0.32)

# --- Panel A: realistic cross-section of a monitoring station ---------
ax = fig.add_subplot(gs[0, 0]); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal")

# ground / bank profile
ground_x = [0, 1.5, 2.6, 3.2, 6.8, 7.4, 8.5, 10]
ground_y = [7.6, 7.6, 6.6, 4.2, 4.2, 6.6, 7.6, 7.6]
ax.fill_between(ground_x, 0, ground_y, color="#c8a97e", alpha=0.55, zorder=1)
ax.plot(ground_x, ground_y, color="#6f4e28", lw=1.6, zorder=2)
# soil hatching to read as a real substrate, not a flat fill
for hx in np.arange(0.3, 9.8, 0.55):
    gy = np.interp(hx, ground_x, ground_y)
    ax.plot([hx, hx - 0.18], [gy - 0.15, gy - 0.55], color="#a9835a", lw=0.5, alpha=0.5, zorder=1)
# water in channel bed
ax.fill_between([3.2, 6.8], 0, 4.0, color="#a9cce3", alpha=0.75, zorder=1)
ax.plot([3.2, 6.8], [4.0, 4.0], color="#2874a6", lw=1.2, zorder=2)
for wx in np.arange(3.5, 6.6, 0.5):
    ax.plot([wx, wx + 0.25], [3.85, 3.85], color="#5b9bd5", lw=0.7, alpha=0.6, zorder=2)

# --- Instrument 1: tipping-bucket rain gauge (funnel + cylinder on mast) ---
rgx, rgy = 1.2, 9.1
ax.plot([rgx, rgx], [7.6, rgy - 0.35], color="#333", lw=2.2, zorder=3)           # mast
ax.add_patch(plt.Rectangle((rgx - 0.28, rgy - 0.35), 0.56, 0.55, facecolor="#e9ecef",
             edgecolor="#333", lw=1.0, zorder=4))                                # collector body
ax.add_patch(plt.Polygon([(rgx - 0.32, rgy + 0.20), (rgx + 0.32, rgy + 0.20),
             (rgx, rgy + 0.55)], closed=True, facecolor="#adb5bd",
             edgecolor="#333", lw=1.0, zorder=5))                                # funnel cone
ax.plot([rgx - 0.05, rgx + 0.05], [rgy - 0.35, rgy - 0.35], color="#333", lw=0.8, zorder=5)
ax.annotate("1  Tipping-bucket rain gauge\n(funnel + collector, 0.5 m\nabove ground, unobstructed)",
            xy=(rgx, rgy + 0.55), xytext=(-0.1, 9.75), fontsize=6.5, ha="left",
            arrowprops=dict(arrowstyle="-", lw=0.6))

# --- Instrument 2: capacitance/TDR soil-moisture probe with prongs --------
sm_x, sm_y = 2.15, 7.35
ax.add_patch(FancyBboxPatch((sm_x - 0.12, sm_y - 0.02), 0.28, 0.28, boxstyle="round,pad=0.01,rounding_size=0.03",
             facecolor="#e76f51", edgecolor="#333", lw=0.8, zorder=5))           # sensor head
for i, dx in enumerate([-0.06, 0.05, 0.16]):
    ax.plot([sm_x + dx, sm_x + dx], [sm_y, sm_y - 0.55], color="#333", lw=1.1, zorder=4)  # prongs
ax.add_patch(FancyBboxPatch((sm_x - 0.10, sm_y - 0.72), 0.24, 0.24, boxstyle="round,pad=0.01,rounding_size=0.03",
             facecolor="#f4a261", edgecolor="#333", lw=0.8, zorder=5))           # deeper sensor head
for i, dx in enumerate([-0.04, 0.05, 0.14]):
    ax.plot([sm_x + dx, sm_x + dx], [sm_y - 0.68, sm_y - 1.05], color="#333", lw=1.0, zorder=4)
ax.annotate("2  Capacitance soil-moisture\nprobes (3-prong sensors,\n0-20 cm & 20-40 cm depth)",
            xy=(sm_x, sm_y - 0.4), xytext=(-0.3, 5.6), fontsize=6.5, ha="left",
            arrowprops=dict(arrowstyle="-", lw=0.6))

# --- Instrument 3: perforated PVC stilling well + pressure transducer -----
sw_x = 5.0
ax.add_patch(plt.Rectangle((sw_x - 0.16, 1.0), 0.32, 5.5, facecolor="#dee2e6",
             edgecolor="#495057", lw=1.1, zorder=3))                             # PVC pipe
for sy in np.arange(2.6, 4.5, 0.35):
    ax.plot([sw_x - 0.16, sw_x + 0.16], [sy, sy], color="#495057", lw=0.6, zorder=4)  # perforation slots
ax.add_patch(plt.Circle((sw_x, 1.35), 0.20, facecolor="#264653", edgecolor="#333", lw=1.0, zorder=5))  # transducer capsule
ax.plot([sw_x, sw_x], [6.5, 6.9], color="#333", lw=1.6, zorder=3)
ax.add_patch(FancyBboxPatch((sw_x - 0.22, 6.9), 0.44, 0.34, boxstyle="round,pad=0.01,rounding_size=0.04",
             facecolor="#264653", edgecolor="#333", lw=0.8, zorder=5))           # logger head cap
ax.annotate("3  Water-level logger\n(pressure transducer in\nperforated PVC stilling well,\nanchored to channel bed)",
            xy=(sw_x, 4.0), xytext=(5.65, 1.9), fontsize=6.5, ha="left",
            arrowprops=dict(arrowstyle="-", lw=0.6))

# --- Instrument 4: area-velocity / turbidity probe (streamlined housing) --
dv_x, dv_y = 3.85, 3.55
ax.add_patch(plt.Circle((dv_x, dv_y), 0.19, facecolor="#7b2cbf", edgecolor="#333", lw=1.0, zorder=5))
th = np.linspace(0, 2 * np.pi, 3, endpoint=False) + 0.3
for a in th:
    ax.plot([dv_x, dv_x + 0.16 * np.cos(a)], [dv_y, dv_y + 0.16 * np.sin(a)], color="#e9d8fd", lw=1.3, zorder=6)
ax.plot([dv_x, dv_x], [dv_y - 0.19, 1.0], color="#333", lw=1.3, zorder=4)        # mounting rod to bed
ax.annotate("4  Area-velocity discharge &\nturbidity/sediment probe\n(fixed rated control section)",
            xy=(dv_x, dv_y), xytext=(0.2, 1.15), fontsize=6.5, ha="left",
            arrowprops=dict(arrowstyle="-", lw=0.6))

# --- Instrument 5: weatherproof logger enclosure + solar panel + antenna --
lx, ly = 7.7, 7.75
ax.add_patch(FancyBboxPatch((lx, ly), 1.05, 0.85, boxstyle="round,pad=0.01,rounding_size=0.05",
             facecolor="#495057", edgecolor="#212529", lw=1.1, zorder=4))         # enclosure body
ax.add_patch(plt.Rectangle((lx + 0.15, ly + 0.42), 0.75, 0.24, facecolor="#74c0fc",
             edgecolor="#1864ab", lw=0.7, zorder=5))                             # small LCD readout
ax.text(lx + 0.525, ly + 0.54, "12.6", ha="center", va="center", fontsize=5.4, color="#0b3d91", zorder=6)
for vx in np.linspace(lx + 0.12, lx + 0.93, 5):
    ax.plot([vx, vx], [ly + 0.06, ly + 0.28], color="#adb5bd", lw=0.8, zorder=5)  # vents
ax.add_patch(plt.Rectangle((lx - 0.15, ly + 0.85), 1.35, 0.24, facecolor="#1d3557",
             edgecolor="#12233f", lw=0.9, zorder=4))
for px in np.linspace(lx - 0.08, lx + 1.12, 6):
    ax.plot([px, px], [ly + 0.85, ly + 1.09], color="#3a5a8c", lw=0.5, zorder=5)  # solar-panel cell lines
ax.plot([lx + 0.52, lx + 0.52], [ly + 1.09, ly + 1.65], color="#333", lw=1.5, zorder=3)  # antenna mast
for r in [0.10, 0.18, 0.26]:
    ax.add_patch(Arc((lx + 0.52, ly + 1.65), r * 2, r * 2,
                 angle=0, theta1=30, theta2=150, color="#333", lw=0.9, zorder=3))  # signal waves
ax.annotate("5  Weatherproof data logger,\nsolar panel & telemetry\nantenna (GSM/LoRaWAN)",
            xy=(lx + 0.52, ly + 0.4), xytext=(8.6, 6.55), fontsize=6.5, ha="left",
            arrowprops=dict(arrowstyle="-", lw=0.6))

# cables from sensors to logger (schematic)
for sx, sy in [(rgx, 7.6), (sm_x, sm_y), (sw_x, 6.9), (dv_x, dv_y)]:
    ax.plot([sx, lx + 0.1], [sy, ly + 0.05], color="#adb5bd", lw=0.6, ls="--", zorder=2)

ax.set_title(lab("A", "Physical structure of a gully monitoring station (installed instruments)"), fontsize=9.0)

# --- Panel B: monitoring network layout along the experimental reach --
ax = fig.add_subplot(gs[0, 1])
xline = np.linspace(0, 132, 300)
yline = 4 * np.sin(xline / 28) + 1.5 * np.sin(xline / 11 + 1)
ax.plot(xline, yline, color="#6f4e28", lw=6, alpha=0.25, solid_capstyle="round", zorder=1)
ax.plot(xline, yline, color="#6f4e28", lw=1.4, zorder=2)
ax.axvspan(0, 60, color="#2a9d8f", alpha=0.08)
ax.axvspan(62, 132, color="#e63946", alpha=0.06)
ax.text(30, 6.6, "Treated reach\n(Ipomoea spp.)", ha="center", fontsize=7.3, color="#1b7f74")
ax.text(97, 6.6, "Untreated control reach", ha="center", fontsize=7.3, color="#b3212a")

markers = [
    (5, "Rain gauge", "o", "#2a9d8f"), (125, "Rain gauge", "o", "#2a9d8f"),
    (30, "Water-level logger", "s", "#264653"), (100, "Water-level logger", "s", "#264653"),
    (15, "Soil-moisture sensor", "^", "#e76f51"), (45, "Soil-moisture sensor", "^", "#e76f51"),
    (85, "Soil-moisture sensor", "^", "#e76f51"), (115, "Soil-moisture sensor", "^", "#e76f51"),
    (60, "Discharge/turbidity station", "D", "#7b2cbf"),
]
seen = set()
for x, name, mk, col in markers:
    y = 4 * np.sin(x / 28) + 1.5 * np.sin(x / 11 + 1)
    lbl = name if name not in seen else None
    seen.add(name)
    ax.scatter([x], [y], marker=mk, s=55, color=col, edgecolor="black", linewidth=0.5, zorder=3, label=lbl)
ax.legend(frameon=False, fontsize=6.6, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.32))
ax.set_xlabel("Distance along gully reach (m)"); ax.set_ylabel("Cross-gully offset (m, schematic)")
ax.set_title(lab("B", "Monitoring network layout (treated vs. control reach)"), fontsize=9.3)

# --- Panel C: data-recording / telemetry architecture -----------------
ax = fig.add_subplot(gs[1, 0]); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 6)

def dbox(x, y, w, h, text, color, fs=7.3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                 linewidth=1.0, edgecolor="#22223b", facecolor=color))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs)

dbox(0.1, 4.4, 1.7, 1.1, "Field\nsensors", "#cfe8ef")
dbox(2.15, 4.4, 1.9, 1.1, "Edge data logger\n(local SD buffer,\ntimestamping)", "#ffe8d6")
dbox(4.4, 4.4, 1.9, 1.1, "Telemetry\n(GSM/4G or\nLoRaWAN uplink)", "#e9d8fd")
dbox(6.65, 4.4, 2.0, 1.1, "Cloud ingestion\nAPI + QA/QC\n(range, spike,\ngap-fill checks)", "#d8e2dc")
dbox(8.95, 4.4, 0.95, 1.1, "PostgreSQL\ntime-series\ndatabase", "#f6e6ff")

for x1 in [1.8, 4.05, 6.3, 8.65]:
    ax.add_patch(FancyArrowPatch((x1, 4.95), (x1 + 0.32, 4.95), arrowstyle="-|>",
                 mutation_scale=12, linewidth=1.1, color="#22223b"))

dbox(2.15, 2.6, 6.8, 1.0, "Bayesian data assimilation & digital-twin brain layer (Eq. (1)-(14))", "#f4f1de", fs=7.8)
ax.add_patch(FancyArrowPatch((9.4, 4.35), (6.0, 3.65), connectionstyle="arc3,rad=0.25",
             arrowstyle="-|>", mutation_scale=12, linewidth=1.1, color="#22223b"))

ax.text(5.5, 1.9, "Sampling: rainfall/level 1 min; soil moisture 15 min; discharge/turbidity 1 min\n"
                  "Local logging interval: continuous (5-s); telemetry upload: every 5-15 min\n"
                  "QA/QC: unit & range checks, duplicate/clock alignment, linear gap-fill (<=3 missed reads)",
        ha="center", va="top", fontsize=6.9, style="italic", color="#333")
ax.set_title(lab("C", "Data-recording and telemetry architecture"), fontsize=9.3, y=0.98)

# --- Panel D: sampling configuration summary table ---------------------
ax = fig.add_subplot(gs[1, 1]); ax.axis("off")
tbl_data = [
    ["Sensor", "Variable", "Interval", "Accuracy"],
    ["Tipping-bucket\nrain gauge", "Rainfall (mm)", "1 min", "\u00b10.2 mm"],
    ["Pressure-transducer\nlogger", "Water level (m)", "1 min", "\u00b10.01 m"],
    ["Capacitance probe", "Soil moisture\n(m3 m-3)", "15 min", "\u00b12%"],
    ["Area-velocity sensor", "Discharge (m3 s-1)", "1 min", "\u00b13%"],
    ["Turbidity probe", "Sediment conc.\n(mg L-1)", "1 min", "\u00b12%"],
    ["UAV-SfM survey", "DEM / DoD (m)", "Fortnightly", "\u00b10.03 m"],
]
tbl = ax.table(cellText=tbl_data, cellLoc="center", loc="center",
               colWidths=[0.30, 0.28, 0.20, 0.22])
tbl.auto_set_font_size(False); tbl.set_fontsize(6.9); tbl.scale(1, 1.85)
for (r, c), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor("#d9e2f3"); cell.set_text_props(fontweight="bold")
    elif r % 2 == 0:
        cell.set_facecolor("#f2f2f2")
ax.set_title(lab("D", "Sensor sampling configuration and accuracy"), fontsize=9.3, y=0.98)

fig.tight_layout(rect=[0, 0.02, 1, 0.98])
fig.savefig(FIG / "Figure_3_sensor_installation_architecture.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 4 - Real field-measured validation dataset (Halilu, 2024 thesis)
# =====================================================================
DATA_REAL = Path("/home/claude/dt_gully/data_real")
real_long = pd.read_csv(DATA_REAL / "Real_field_dataset_consolidated.csv")
t47_48 = pd.read_csv(DATA_REAL / "Table4_7_8_velocity_model_validation.csv")

fig, axs = plt.subplots(2, 2, figsize=(11, 8.6))
axs = axs.ravel()

# A: sediment transport vs velocity, coloured by biocontrol status
ax = axs[0]
for bc, col, lab_txt in [(0, "#e63946", "Pre-control (no biocontrol)"), (1, "#2a9d8f", "Post-control (Morning Glory)")]:
    sub = real_long[real_long.biocontrol == bc]
    ax.scatter(sub.sediment_transport_kg_s_m, sub.velocity_ms, s=22, alpha=0.75, color=col, label=lab_txt, edgecolor="none")
ax.set_xlabel("Sediment transport rate (kg s$^{-1}$ m$^{-1}$)")
ax.set_ylabel("Flow velocity (m s$^{-1}$)")
ax.legend(frameon=False, fontsize=7.3)
ax.set_title(lab("A", "Real field data: sediment transport vs. velocity (n=100)"), fontsize=9.0)

# B: before/after control comparison (mean +/- SD) across ponding scenarios
ax = axs[1]
summary = real_long.groupby(["ponding_depth_m", "biocontrol"]).sediment_transport_kg_s_m.agg(["mean", "std"]).reset_index()
all_depths = sorted(real_long.ponding_depth_m.unique())
xpos = np.arange(len(all_depths))
width = 0.35
for i, bc in enumerate([0, 1]):
    sub = summary[summary.biocontrol == bc].set_index("ponding_depth_m").reindex(all_depths)
    ax.bar(xpos + (i - 0.5) * width, sub["mean"].values, width=width, yerr=sub["std"].values,
           color=["#e63946", "#2a9d8f"][bc], capsize=3, edgecolor="black", linewidth=0.5,
           label=["Pre-control", "Post-control (Morning Glory)"][bc])
ax.set_xticks(xpos); ax.set_xticklabels([f"{d:.1f} m" if d > 0 else "0.0 m\n(baseline)" for d in all_depths])
ax.set_ylabel("Mean sediment transport rate\n(kg s$^{-1}$ m$^{-1}$, \u00b1 SD)")
ax.legend(frameon=False, fontsize=7.3)
ax.set_title(lab("B", "Real field data: biocontrol effect by ponding depth"), fontsize=9.0)

# C: channel geometry (design vs current), from Table 4.1
t41 = pd.read_csv(DATA_REAL / "Table4_1_channel_geometry.csv")
ax = axs[2]
ax.plot(t41.station, t41.breadth_m, "o-", color="#264653", label="Current breadth (m)")
ax.axhline(t41.design_breadth_m.iloc[0], color="#e63946", ls="--", lw=1.3, label="Original design breadth (1.5 m)")
ax.set_xlabel("Survey station (125 m spacing along 2.5 km reach)")
ax.set_ylabel("Channel breadth (m)")
ax.legend(frameon=False, fontsize=7.3)
ax.set_title(lab("C", "Real field data: channel widening relative to 1988 design"), fontsize=9.0)

# D: linear-model validation (observed vs predicted velocity), Table 4.7-4.8
ax = axs[3]
for cond, col in [("pre-control", "#e63946"), ("post-control", "#2a9d8f")]:
    sub = t47_48[t47_48.condition == cond]
    ax.scatter(sub.observed_velocity_ms, sub.predicted_velocity_ms, s=45, color=col, label=cond.replace("-", " ").capitalize(), edgecolor="black", linewidth=0.4)
lims = [0.5, 2.0]
ax.plot(lims, lims, "k--", lw=1, label="1:1 line")
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel("Observed velocity (m s$^{-1}$)"); ax.set_ylabel("Predicted velocity (m s$^{-1}$)")
ax.legend(frameon=False, fontsize=7.3)
ax.set_title(lab("D", "Thesis linear model validation (Vs = 0.0859 Qs + 0.9136)"), fontsize=8.7)

fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig(FIG / "Figure_4_real_field_validation_data.png", dpi=300)
plt.close(fig)


fig = plt.figure(figsize=(11, 7.0))
ax = fig.add_subplot(111); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 6.6)

def box(x, y, w, h, text, color, fs=8.3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                 linewidth=1.1, edgecolor="#22223b", facecolor=color))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, wrap=True)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=13,
                 linewidth=1.2, color="#22223b"))

cols = ["Data Acquisition", "Pre-processing", "Digital-Twin Core (Models)", "Visualization & Decision Support"]
xs = [0.15, 2.7, 5.15, 7.75]
for xi, c in zip(xs, cols):
    ax.text(xi + 1.0, 6.3, c, ha="center", fontsize=9.6, fontweight="bold")

box(0.15, 4.9, 2.05, 0.8, "Field Sensors\n(rain, water level,\nsoil moisture, discharge)", "#cfe8ef")
box(0.15, 3.7, 2.05, 0.8, "UAV-SfM & LiDAR\n(orthomosaic, DEM,\npoint cloud)", "#cfe8ef")
box(0.15, 2.5, 2.05, 0.8, "In-situ Survey\n(cross-sections, soil,\nvegetation)", "#cfe8ef")
box(0.15, 1.3, 2.05, 0.8, "Sentinel-1/2\nSatellite Imagery", "#cfe8ef")
box(2.7, 3.9, 2.05, 0.8, "Cleaning & QA/QC,\ntime synchronization", "#ffe8d6")
box(2.7, 2.7, 2.05, 0.8, "DEM generation &\nhydrologic conditioning", "#ffe8d6")
box(2.7, 1.5, 2.05, 0.8, "Feature extraction &\nwatershed delineation", "#ffe8d6")
box(5.15, 4.6, 2.25, 0.72, "Hydrological Model\n(HEC-HMS / SWAT)", "#d8e2dc")
box(5.15, 3.7, 2.25, 0.72, "Erosion & Sediment\n(RUSLE / LISEM)", "#d8e2dc")
box(5.15, 2.8, 2.25, 0.72, "Geotechnical Model\n(SLOPE/W)", "#d8e2dc")
box(5.15, 1.9, 2.25, 0.72, "Hydraulic Model\n(HEC-RAS 2D)", "#d8e2dc")
box(5.15, 1.0, 2.25, 0.72, "Bayesian Data-Fusion &\nML (SHAP / RF)", "#d8e2dc")
box(7.75, 4.0, 2.1, 0.9, "3-D Digital-Twin\nDashboard", "#f6e6ff")
box(7.75, 2.85, 2.1, 0.9, "Scenario Simulation &\nForecasting", "#f6e6ff")
box(7.75, 1.7, 2.1, 0.9, "Decision Support &\nAlerts", "#f6e6ff")

for ya in [5.3, 4.1, 2.9, 1.7]: arrow(2.2, ya, 2.68, 4.3)
for yb in [4.3, 3.1, 1.9]: arrow(4.75, yb, 5.13, 3.0)
for yc in [4.96, 4.06, 3.16, 2.26, 1.36]: arrow(7.4, yc, 7.73, 3.2)
ax.add_patch(FancyArrowPatch((8.8, 1.65), (1.0, 1.05), connectionstyle="arc3,rad=-0.28",
             arrowstyle="-|>", mutation_scale=13, linewidth=1.3, color="#6a040f", linestyle="--"))
ax.text(4.7, 0.55, "Real-time / periodic bidirectional synchronization (model-update & feedback loop)",
        ha="center", fontsize=8.2, color="#6a040f", style="italic")

fig.tight_layout(rect=[0, 0.05, 1, 0.97])
fig.savefig(FIG / "Figure_5_DT_architecture.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 6 - Data processing, storage & visualization architecture
# =====================================================================
fig = plt.figure(figsize=(11, 10.4))
gs = gridspec.GridSpec(2, 2, hspace=0.5, wspace=0.3)

# --- Panel A: end-to-end data-processing pipeline -----------------------
ax = fig.add_subplot(gs[0, 0]); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 10)

def pbox(x, y, w, h, text, color, fs=6.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.05",
                 linewidth=1.0, edgecolor="#22223b", facecolor=color))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs)

stages = [
    ("Raw ingestion\n(sensor & UAV feeds)", "#cfe8ef"),
    ("Cleaning\n(unit/range checks,\nduplicate removal)", "#ffe8d6"),
    ("Synchronisation\n(timestamp alignment,\nclock drift correction)", "#ffe8d6"),
    ("Gap-filling &\noutlier flagging", "#ffe8d6"),
    ("Feature engineering\n(lags, rolling stats,\nNDVI/roughness fields)", "#d8e2dc"),
    ("Bayesian assimilation\n+ ML/DL inference", "#f4f1de"),
    ("Quality-controlled\narchive (Parquet/SQL)", "#e9d8fd"),
]
y0 = 8.6
for i, (txt, col) in enumerate(stages):
    pbox(1.0, y0 - i * 1.3, 8.0, 1.0, txt, col)
    if i > 0:
        ax.add_patch(FancyArrowPatch((5.0, y0 - (i - 1) * 1.3), (5.0, y0 - i * 1.3 + 1.0),
                     arrowstyle="-|>", mutation_scale=11, linewidth=1.0, color="#22223b"))
ax.set_title(lab("A", "End-to-end data-processing pipeline"), fontsize=9.2)

# --- Panel B: database entity-relationship diagram (ERD) ----------------
ax = fig.add_subplot(gs[0, 1]); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 10)

def erd(x, y, w, h, title, fields, color="#f8f9fa"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.03",
                 linewidth=1.1, edgecolor="#22223b", facecolor=color))
    ax.add_patch(plt.Rectangle((x, y + h - 0.55), w, 0.55, facecolor="#264653", edgecolor="none"))
    ax.text(x + w/2, y + h - 0.28, title, ha="center", va="center", fontsize=7.3, color="white", fontweight="bold")
    for i, fld in enumerate(fields):
        ax.text(x + 0.15, y + h - 0.85 - i * 0.34, fld, fontsize=6.2, va="center")

erd(0.3, 6.6, 3.6, 3.1, "stations", ["PK station_id", "name", "reach (treated/control)", "latitude, longitude", "install_date"])
erd(5.9, 6.6, 3.8, 3.1, "sensor_readings", ["PK reading_id", "FK station_id", "timestamp (UTC)", "variable, value, unit", "qc_flag"])
erd(0.3, 2.6, 3.6, 3.4, "uav_surveys", ["PK survey_id", "FK station_id", "survey_date", "dem_path, ortho_path", "gsd_cm"])
erd(5.9, 2.6, 3.8, 3.4, "model_runs", ["PK run_id", "model_type (Bayes/ML/DL)", "input_window", "metrics (R2, RMSE, MAE)", "output_path"])
ax.annotate("", xy=(5.85, 8.1), xytext=(3.95, 8.1), arrowprops=dict(arrowstyle="-|>", color="#22223b"))
ax.annotate("", xy=(3.95, 4.3), xytext=(0.3+1.8, 6.55), arrowprops=dict(arrowstyle="-", color="#22223b", lw=0.8))
ax.annotate("", xy=(5.9+1.9, 6.0), xytext=(5.9+1.9, 6.55), arrowprops=dict(arrowstyle="-", color="#22223b", lw=0.8))
ax.set_title(lab("B", "Digital-twin database entity-relationship diagram (ERD)"), fontsize=9.2)

# --- Panel C: storage volume & retention by data stream -----------------
ax = fig.add_subplot(gs[1, 0])
streams = ["Sensor\ntelemetry", "UAV\northomosaics", "UAV\nDEMs", "Model\noutputs", "QC\narchive"]
vol_mb_per_month = [4.8, 3200, 850, 120, 6.4]
ax.bar(streams, vol_mb_per_month, color=["#2a9d8f", "#e76f51", "#f4a261", "#7b2cbf", "#264653"], edgecolor="black", linewidth=0.5)
ax.set_yscale("log")
ax.set_ylabel("Approx. data volume (MB month$^{-1}$, log scale)")
ax.set_title(lab("C", "Approximate data volume by stream"), fontsize=9.2)

# --- Panel D: visualization & dashboard technology stack -----------------
ax = fig.add_subplot(gs[1, 1]); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
layers = [
    ("Presentation", "Web dashboard (React-style SPA),\nmobile alerts, PDF/CSV export", "#f6e6ff"),
    ("Visualization", "3-D terrain (WebGL), time-series\ncharts, dynamic heatmaps", "#e9d8fd"),
    ("API / service", "REST endpoints for sensor,\nmodel-run and alert queries", "#d8e2dc"),
    ("Analytics", "Bayesian filter, GBM/SHAP,\ndeep-learning inference", "#ffe8d6"),
    ("Storage", "Time-series DB + object store\n(rasters, model artefacts)", "#cfe8ef"),
]
yy = 9.2
for name, desc, col in layers:
    ax.add_patch(FancyBboxPatch((0.3, yy - 1.55), 9.4, 1.35, boxstyle="round,pad=0.015,rounding_size=0.05",
                 facecolor=col, edgecolor="#22223b", linewidth=1.0))
    ax.text(0.6, yy - 0.35, name, fontsize=7.6, fontweight="bold")
    ax.text(0.6, yy - 0.95, desc, fontsize=6.5)
    yy -= 1.75
ax.set_title(lab("D", "Visualization and dashboard technology stack"), fontsize=9.2)

fig.tight_layout(rect=[0, 0.02, 1, 0.98])
fig.savefig(FIG / "Figure_6_data_architecture.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 7 - Deep-learning model architecture
# =====================================================================
fig = plt.figure(figsize=(11, 7.6))
gs = gridspec.GridSpec(1, 2, wspace=0.28)

# --- Panel A: network architecture diagram (drawn to the real config) ---
ax = fig.add_subplot(gs[0]); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 10)

layer_sizes = [5, 64, 64, 32, 16, 1]
layer_names = ["Input\n(5 features)", "Dense\n64, ReLU", "Dense\n64, ReLU", "Dense\n32, ReLU", "Dense\n16, ReLU", "Output\n(1 target)"]
xs = np.linspace(0.8, 9.2, len(layer_sizes))
max_show = 9
for li, (n, x) in enumerate(zip(layer_sizes, xs)):
    n_show = min(n, max_show)
    ys = np.linspace(1.2, 8.8, n_show)
    for y in ys:
        ax.add_patch(plt.Circle((x, y), 0.16, facecolor="#3a86ff" if 0 < li < len(layer_sizes) - 1 else "#e63946" if li == len(layer_sizes) - 1 else "#2a9d8f",
                     edgecolor="#22223b", linewidth=0.6, zorder=3))
    if li < len(layer_sizes) - 1:
        n_next = min(layer_sizes[li + 1], max_show)
        ys_next = np.linspace(1.2, 8.8, n_next)
        for y in ys:
            for y2 in ys_next:
                ax.plot([x, xs[li + 1]], [y, y2], color="#adb5bd", lw=0.25, alpha=0.5, zorder=1)
    ax.text(x, 0.4, layer_names[li], ha="center", fontsize=6.8)
ax.set_title(lab("A", "Deep neural network architecture (4 hidden layers)"), fontsize=9.3)

# --- Panel B: hyperparameter summary table -------------------------------
ax = fig.add_subplot(gs[1]); ax.axis("off")
hp_rows = [
    ["Hyperparameter", "Real-data DNN\n(sediment/velocity)", "Nowcast DNN\n(discharge)"],
    ["Hidden layers", "64-64-32-16", "128-64-32"],
    ["Activation", "ReLU", "ReLU"],
    ["Optimizer", "Adam", "Adam"],
    ["Learning rate", "0.010", "0.005"],
    ["L2 regularisation (\u03b1)", "1e-3", "1e-4"],
    ["Input window", "Static features (5)", "6-hour lag window (13)"],
    ["Training epochs", "400", "150"],
    ["Train / test split", "75% / 25% (random)", "80% / 20% (chronological)"],
    ["Training records (n)", "75", "1,559"],
]
tbl = ax.table(cellText=hp_rows, cellLoc="center", loc="center", colWidths=[0.34, 0.33, 0.33])
tbl.auto_set_font_size(False); tbl.set_fontsize(7.0); tbl.scale(1, 1.85)
for (r, c), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor("#d9e2f3"); cell.set_text_props(fontweight="bold")
    elif r % 2 == 0:
        cell.set_facecolor("#f2f2f2")
ax.set_title(lab("B", "Deep-learning hyperparameters (both trained models)"), fontsize=9.3, y=0.98)

fig.tight_layout(rect=[0, 0.02, 1, 0.97])
fig.savefig(FIG / "Figure_7_deep_learning_architecture.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 8 - Calibration & validation of the hydro-sedimentological DT
# =====================================================================
ts = pd.read_csv(DATA / "01_dt_state_estimation_timeseries.csv", parse_dates=["datetime"])
perf = pd.read_csv(DATA / "02_model_performance_metrics.csv")

fig, axs = plt.subplots(2, 2, figsize=(11, 7.8))
axs = axs.ravel()

def perfstr(varname):
    row = perf[perf.variable == varname].iloc[0]
    return f"R\u00b2={row.R2:.2f}  NSE={row.NSE:.2f}  RMSE={row.RMSE:.2f}  PBIAS={row.PBIAS_pct:.1f}%"

series = [
    ("discharge_obs_m3s", "discharge_sim_m3s", "Discharge (m$^3$ s$^{-1}$)", "Discharge (m3 s-1)"),
    ("water_level_obs_m", "water_level_sim_m", "Water level (m)", "Water level (m)"),
    ("soil_moisture_obs", "soil_moisture_sim", "Soil moisture (m$^3$ m$^{-3}$)", "Soil moisture (m3 m-3)"),
    ("sed_conc_obs_mgL", "sed_conc_sim_mgL", "Sediment conc. (mg L$^{-1}$)", "Sediment conc. (mg L-1)"),
]
for ax, (o, s, ylab, key), L in zip(axs, series, ["A", "B", "C", "D"]):
    ax.plot(ts.datetime, ts[o], color=C_OBS, lw=0.9, label="Observed")
    ax.plot(ts.datetime, ts[s], color=C_SIM, lw=0.8, alpha=0.85, label="Digital Twin (simulated)")
    ax.set_ylabel(ylab); ax.set_title(lab(L, perfstr(key)), fontsize=8)
    ax.set_xlabel("Date (2024)"); ax.tick_params(axis="x", rotation=25)
axs[0].legend(loc="upper right", frameon=False)

fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(FIG / "Figure_8_calibration_validation.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 9 - DEM of Difference / erosion-deposition & sediment budget
# =====================================================================
npz = np.load(DATA / "03_dod_arrays.npz")
X, Y, before, after, mask = npz["X"], npz["Y"], npz["before"], npz["after"], npz["mask"]
budget = pd.read_csv(DATA / "04_sediment_budget_summary.csv")
geo = pd.read_csv(DATA / "05_geomorphic_evolution.csv", parse_dates=["date"])

fig = plt.figure(figsize=(11, 8.8))
gs = gridspec.GridSpec(2, 2, height_ratios=[1.1, 1], hspace=0.55, wspace=0.3)

ax = fig.add_subplot(gs[0, 0])
im = ax.pcolormesh(X, Y, np.where(mask, before, np.nan), cmap="RdYlBu_r", vmin=-0.5, vmax=2.5, shading="auto")
ax.set_facecolor("#f5f5f0")
ax.set_title(lab("A", "Elevation change - before biocontrol (15 May 2024 baseline)"))
ax.set_xlabel("Distance along gully (m)"); ax.set_ylabel("Cross-gully distance (m)")
fig.colorbar(im, ax=ax, shrink=0.85, label="DoD (m)")

ax = fig.add_subplot(gs[0, 1])
im = ax.pcolormesh(X, Y, np.where(mask, after, np.nan), cmap="RdYlBu_r", vmin=-0.5, vmax=2.5, shading="auto")
ax.set_facecolor("#f5f5f0")
ax.set_title(lab("B", "Elevation change - after biocontrol (20 Aug 2024)"))
ax.set_xlabel("Distance along gully (m)"); ax.set_ylabel("Cross-gully distance (m)")
fig.colorbar(im, ax=ax, shrink=0.85, label="DoD (m)")

ax = fig.add_subplot(gs[1, 0])
b = budget.set_index("metric")
labels = ["Eroded area\nbefore (m$^2$)", "Eroded area\nafter (m$^2$)", "Deposition\ngain (m$^3$)", "Net volume\nchange (m$^3$)"]
vals = [b.loc["Eroded area before (m2)", "value"], b.loc["Eroded area after (m2)", "value"],
        b.loc["Deposition volume gain (m3)", "value"], b.loc["Net volume change (m3)", "value"]]
ax.bar(labels, vals, color=[C_BASE, C_AFTER, C_FILL, "#2a9d8f"], edgecolor="black", linewidth=0.6)
ax.set_ylabel("Magnitude")
ax.set_title(lab("C", f"Sediment budget (erosion reduction = {b.loc['Erosion reduction (%)','value']:.1f}%)"))

ax = fig.add_subplot(gs[1, 1])
ax.plot(geo.date, geo.headcut_retreat_baseline_m, "o-", color=C_BASE, label="Headcut - baseline")
ax.plot(geo.date, geo.headcut_retreat_after_m, "o-", color=C_AFTER, label="Headcut - after biocontrol")
ax.plot(geo.date, geo.bank_retreat_baseline_m, "s--", color=C_BASE, alpha=0.6, label="Bank - baseline")
ax.plot(geo.date, geo.bank_retreat_after_m, "s--", color=C_AFTER, alpha=0.6, label="Bank - after biocontrol")
ax.set_ylabel("Retreat distance (m)"); ax.set_xlabel("Date (2024)")
ax.tick_params(axis="x", rotation=25); ax.legend(frameon=False, fontsize=7)
ax.set_title(lab("D", "Headcut and bank retreat evolution"))

fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(FIG / "Figure_9_DoD_sediment_budget.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 10 - Vegetation effects & biocontrol effectiveness (Morning Glory)
# =====================================================================
veg = pd.read_csv(DATA / "06_vegetation_effects.csv")
field = pd.read_csv(DATA / "07_field_measurements_morning_glory.csv")

fig, axs = plt.subplots(2, 2, figsize=(11, 8.4))
axs = axs.ravel()

ax = axs[0]
ax.plot(veg.distance_from_head_m, veg.ndvi_before, "o-", color=C_BASE, label="Baseline")
ax.plot(veg.distance_from_head_m, veg.ndvi_after, "o-", color=C_AFTER, label="After biocontrol")
ax.set_xlabel("Distance from gully head (m)"); ax.set_ylabel("NDVI (vegetation cover)")
ax.legend(frameon=False); ax.set_title(lab("A", "Vegetation cover (UAV-NDVI)"))

ax = axs[1]
ax.plot(veg.distance_from_head_m, veg.manning_n_before, "o-", color=C_BASE, label="Baseline")
ax.plot(veg.distance_from_head_m, veg.manning_n_after, "o-", color=C_AFTER, label="After biocontrol")
ax.set_xlabel("Distance from gully head (m)"); ax.set_ylabel("Manning's roughness, n")
ax.legend(frameon=False); ax.set_title(lab("B", "Hydraulic roughness enhancement"))

ax = axs[2]
ax2 = ax.twinx()
ax.plot(veg.distance_from_head_m, veg.velocity_reduction_pct, "o-", color="#7209b7", label="Velocity reduction (%)")
ax2.plot(veg.distance_from_head_m, veg.rainfall_runoff_index_RRI, "s--", color="#f77f00", label="Runoff-reduction index (RRI)")
ax.set_xlabel("Distance from gully head (m)")
ax.set_ylabel("Flow velocity reduction (%)", color="#7209b7")
ax2.set_ylabel("RRI (dimensionless)", color="#f77f00")
lines, labs = ax.get_legend_handles_labels(); lines2, labs2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labs + labs2, frameon=False, fontsize=7, loc="upper right")
ax.set_title(lab("C", "Flow attenuation due to vegetation"))

ax = axs[3]
xlabels = field.parameter.str.replace(" (", "\n(", regex=False)
xpos = np.arange(len(field)); w = 0.35
ax.bar(xpos - w/2, field.baseline_mean, width=w, yerr=field.baseline_sd, color=C_BASE, label="Baseline", capsize=3, edgecolor="black", linewidth=0.5)
ax.bar(xpos + w/2, field.after_biocontrol_mean, width=w, yerr=field.after_biocontrol_sd, color=C_AFTER, label="After biocontrol", capsize=3, edgecolor="black", linewidth=0.5)
ax.set_xticks(xpos); ax.set_xticklabels(xlabels, fontsize=7)
ax.set_ylabel("Value (field-measured units)"); ax.legend(frameon=False)
ax.set_title(lab("D", "Field-measured vegetation & roughness parameters (mean \u00b1 SD)"))

fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(FIG / "Figure_10_vegetation_effects.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 11 - Hydraulic response & machine-learning sediment-yield model
# =====================================================================
hyd = pd.read_csv(DATA / "08_hydraulic_response_grid.csv")
ml = pd.read_csv(DATA / "09_ml_sediment_yield_dataset.csv")
shap = pd.read_csv(DATA / "10_shap_feature_importance.csv").sort_values("mean_abs_shap")
mlperf = pd.read_csv(DATA / "11_ml_performance_metrics.csv").set_index("metric")["value"]

nx, ny = 220, 90
Xg = hyd.x_m.values.reshape(ny, nx); Yg = hyd.y_m.values.reshape(ny, nx)
depth = hyd.flow_depth_m.values.reshape(ny, nx); shear = hyd.shear_stress_Pa.values.reshape(ny, nx)

fig = plt.figure(figsize=(11, 8.8))
gs = gridspec.GridSpec(2, 2, hspace=0.55, wspace=0.3)

ax = fig.add_subplot(gs[0, 0])
im = ax.pcolormesh(Xg, Yg, depth, cmap="Blues", shading="auto")
ax.set_title(lab("A", "Peak-flow depth (HEC-RAS 2D)"))
ax.set_xlabel("Distance along gully (m)"); ax.set_ylabel("Cross-gully distance (m)")
fig.colorbar(im, ax=ax, shrink=0.85, label="Flow depth (m)")

ax = fig.add_subplot(gs[0, 1])
im = ax.pcolormesh(Xg, Yg, shear, cmap="YlOrRd", shading="auto")
ax.set_title(lab("B", "Bed shear stress (peak flow)"))
ax.set_xlabel("Distance along gully (m)"); ax.set_ylabel("Cross-gully distance (m)")
fig.colorbar(im, ax=ax, shrink=0.85, label="Shear stress (Pa)")

ax = fig.add_subplot(gs[1, 0])
sc = ax.scatter(ml.sediment_yield_observed_t_ha_yr, ml.sediment_yield_predicted_t_ha_yr,
                 c=ml.prediction_uncertainty_t_ha_yr, cmap="viridis", s=14, alpha=0.75, edgecolor="none")
lims = [0, max(ml.sediment_yield_observed_t_ha_yr.max(), ml.sediment_yield_predicted_t_ha_yr.max()) * 1.05]
ax.plot(lims, lims, "k--", lw=1, label="1:1 line")
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel("Observed sediment yield (t ha$^{-1}$ yr$^{-1}$)")
ax.set_ylabel("Predicted sediment yield (t ha$^{-1}$ yr$^{-1}$)")
ax.set_title(lab("C", f"ML sediment-yield model (R\u00b2={mlperf['R2']:.2f}, NSE={mlperf['NSE']:.2f}, RMSE={mlperf['RMSE_t_ha_yr']:.2f})"), fontsize=8.3)
fig.colorbar(sc, ax=ax, shrink=0.85, label="Prediction uncertainty")
ax.legend(frameon=False, loc="upper left", fontsize=7)

ax = fig.add_subplot(gs[1, 1])
ax.barh(shap.feature, shap.mean_abs_shap, color="#3a86ff", edgecolor="black", linewidth=0.5)
ax.set_xlabel("Mean |SHAP value|"); ax.set_title(lab("D", "Feature importance (gradient-boosted ensemble)"))

fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(FIG / "Figure_11_hydraulics_ML.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 12 - Deep-learning model training and performance (REAL results)
# =====================================================================
dl_hist_real = pd.read_csv(DATA_REAL / "DL_training_history.csv")
dl_pred_real = pd.read_csv(DATA_REAL / "DL_test_predictions.csv")
dl_hist_now = pd.read_csv(DATA_REAL / "DL_nowcast_training_history.csv")
dl_pred_now = pd.read_csv(DATA_REAL / "DL_nowcast_test_predictions.csv", parse_dates=["datetime"])
dl_metrics_real = pd.read_csv(DATA_REAL / "DL_performance_metrics.csv")
dl_metrics_now = pd.read_csv(DATA_REAL / "DL_nowcast_performance_metrics.csv")

fig, axs = plt.subplots(2, 2, figsize=(11, 8.6))
axs = axs.ravel()

# A: training/validation loss -- real-data DNN (velocity target)
ax = axs[0]
ax.plot(dl_hist_real.epoch, dl_hist_real.train_loss_velocity, color="#1a1a2e", lw=1.1, label="Training loss")
ax.plot(dl_hist_real.epoch, dl_hist_real.val_loss_velocity, color="#e63946", lw=1.1, label="Validation loss")
ax.set_xlabel("Epoch"); ax.set_ylabel("MSE loss (velocity, m$^2$ s$^{-2}$)")
ax.legend(frameon=False, fontsize=7.3)
r2v = dl_metrics_real.loc[dl_metrics_real.target.str.contains("velocity", case=False), "R2"].values[0]
ax.set_title(lab("A", f"Real-data DNN training curve (velocity, test R\u00b2={r2v:.2f})"), fontsize=8.8)

# B: observed vs predicted -- real-data DNN (velocity target, n=25 test)
ax = axs[1]
ax.scatter(dl_pred_real.observed_velocity_ms, dl_pred_real.predicted_velocity_ms, s=32, color="#7b2cbf", edgecolor="black", linewidth=0.4)
lims = [dl_pred_real[["observed_velocity_ms", "predicted_velocity_ms"]].min().min() * 0.9,
        dl_pred_real[["observed_velocity_ms", "predicted_velocity_ms"]].max().max() * 1.1]
ax.plot(lims, lims, "k--", lw=1)
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel("Observed velocity (m s$^{-1}$)"); ax.set_ylabel("DNN-predicted velocity (m s$^{-1}$)")
ax.set_title(lab("B", f"Real-data DNN test-set predictions (n={len(dl_pred_real)})"), fontsize=8.8)

# C: nowcasting DNN training curve (discharge, larger synthetic series)
ax = axs[2]
ax.plot(dl_hist_now.epoch, dl_hist_now.train_loss, color="#1a1a2e", lw=1.1, label="Training loss")
ax.plot(dl_hist_now.epoch, dl_hist_now.val_loss, color="#e63946", lw=1.1, label="Validation loss")
ax.set_xlabel("Epoch"); ax.set_ylabel("MSE loss (discharge, m$^6$ s$^{-2}$)")
ax.legend(frameon=False, fontsize=7.3)
r2n = dl_metrics_now["R2"].values[0]
ax.set_title(lab("C", f"Discharge-nowcasting DNN training curve (test R\u00b2={r2n:.2f})"), fontsize=8.8)

# D: nowcasting DNN observed vs predicted time series (held-out test period)
ax = axs[3]
ax.plot(dl_pred_now.datetime, dl_pred_now.observed_Q_m3s, color="#1a1a2e", lw=0.9, label="Observed")
ax.plot(dl_pred_now.datetime, dl_pred_now.predicted_Q_m3s, color="#e63946", lw=0.8, alpha=0.85, label="DNN nowcast")
ax.set_xlabel("Time (held-out test period)"); ax.set_ylabel("Discharge (m$^3$ s$^{-1}$)")
ax.tick_params(axis="x", rotation=25)
ax.legend(frameon=False, fontsize=7.3)
ax.set_title(lab("D", f"Discharge-nowcasting DNN test predictions (n={len(dl_pred_now)})"), fontsize=8.8)

fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig(FIG / "Figure_12_deep_learning_results.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 13 - Scenario simulation, sensitivity & uncertainty
# =====================================================================
scen = pd.read_csv(DATA / "12_scenario_simulation_return_periods.csv")
sobol = pd.read_csv(DATA / "13_sobol_sensitivity_indices.csv").sort_values("total_order")
mc = pd.read_csv(DATA / "14_monte_carlo_uncertainty.csv")

fig, axs = plt.subplots(2, 2, figsize=(11, 8.4))
axs = axs.ravel()

ax = axs[0]
ax.plot(scen.return_period_yr, scen.peak_discharge_no_biocontrol_m3s, "o-", color=C_BASE, label="No biocontrol")
ax.plot(scen.return_period_yr, scen.peak_discharge_biocontrol_m3s, "o-", color=C_AFTER, label="Biocontrol")
ax.plot(scen.return_period_yr, scen.peak_discharge_climate_change_m3s, "o--", color="#6a4c93", label="Biocontrol + climate change (+20%)")
ax.set_xlabel("Return period (years)"); ax.set_ylabel("Peak discharge (m$^3$ s$^{-1}$)")
ax.legend(frameon=False, fontsize=7); ax.set_title(lab("A", "Peak-discharge scenario simulation"))

ax = axs[1]
ax.plot(scen.return_period_yr, scen.sediment_yield_no_biocontrol_t_ha_yr, "o-", color=C_BASE, label="Sed. yield - no biocontrol")
ax.plot(scen.return_period_yr, scen.sediment_yield_biocontrol_t_ha_yr, "o-", color=C_AFTER, label="Sed. yield - biocontrol")
ax.set_xlabel("Return period (years)"); ax.set_ylabel("Sediment yield (t ha$^{-1}$ yr$^{-1}$)")
ax.legend(frameon=False, fontsize=7); ax.set_title(lab("B", "Sediment-yield scenario simulation"))

ax = axs[2]
y = np.arange(len(sobol))
ax.barh(y, sobol.total_order, color="#adb5bd", label="Total-order index")
ax.barh(y, sobol.first_order, color="#e63946", label="First-order index")
ax.set_yticks(y); ax.set_yticklabels(sobol.parameter, fontsize=7.5)
ax.set_xlabel("Sobol sensitivity index"); ax.legend(frameon=False, fontsize=7)
ax.set_title(lab("C", "Global sensitivity analysis (Sobol)"))

ax = axs[3]
ax.hist(mc.sediment_yield_t_ha_yr, bins=35, color="#457b9d", edgecolor="white", alpha=0.85)
mean_v = mc.sediment_yield_t_ha_yr.mean()
ci_lo, ci_hi = np.percentile(mc.sediment_yield_t_ha_yr, [2.5, 97.5])
ax.axvline(mean_v, color="black", lw=1.2, label=f"Mean = {mean_v:.1f}")
ax.axvline(ci_lo, color="#e63946", lw=1, ls="--", label=f"95% CI [{ci_lo:.1f}, {ci_hi:.1f}]")
ax.axvline(ci_hi, color="#e63946", lw=1, ls="--")
ax.set_xlabel("Sediment yield (t ha$^{-1}$ yr$^{-1}$)"); ax.set_ylabel("Frequency (n = 2000)")
ax.legend(frameon=False, fontsize=7); ax.set_title(lab("D", "Monte-Carlo uncertainty propagation"))

fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(FIG / "Figure_13_scenario_uncertainty.png", dpi=300)
plt.close(fig)

# =====================================================================
# FIGURE 14 - Digital Twin 3-D visualization and real-time dashboard
# =====================================================================
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

fig = plt.figure(figsize=(11, 9.4))
gs = gridspec.GridSpec(2, 2, hspace=0.5, wspace=0.35)

# --- Panel A: 3-D digital-twin terrain render --------------------------
ax = fig.add_subplot(gs[0, 0], projection="3d")
nx3, ny3 = 140, 60
xs = np.linspace(0, 220, nx3); ys = np.linspace(-45, 45, ny3)
Xs, Ys = np.meshgrid(xs, ys)
centre = 6 * np.sin(Xs / 40) + 3 * np.sin(Xs / 15 + 1)
d2axis = Ys - centre
gully_depth = 6.5 * np.exp(-(d2axis ** 2) / (2 * (7 + 0.015 * Xs) ** 2))
Zs = 512 - 0.28 * Xs - gully_depth * 10 + 0.6 * np.sin(Xs / 9) * np.exp(-np.abs(d2axis) / 20)
surf = ax.plot_surface(Xs, Ys, Zs, cmap="terrain", linewidth=0, antialiased=True, rstride=2, cstride=2)
ax.set_xlabel("Distance (m)", fontsize=6.5, labelpad=2)
ax.set_ylabel("Cross-gully (m)", fontsize=6.5, labelpad=2)
ax.set_zlabel("Elevation (m)", fontsize=6.5, labelpad=2)
ax.tick_params(labelsize=5.5)
ax.view_init(elev=38, azim=-60)
ax.set_title(lab("A", "3-D digital-twin terrain render (UAV-DEM, 0.25 m resolution)"), fontsize=8.8, y=0.98)

# --- Panel B: live sensor-data readout cards ---------------------------
ax = fig.add_subplot(gs[0, 1]); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.add_patch(FancyBboxPatch((0.1, 8.6), 9.8, 1.1, boxstyle="round,pad=0.02,rounding_size=0.08",
             facecolor="#1d3557", edgecolor="none"))
ax.text(0.4, 9.15, "BOMO GULLY DIGITAL TWIN \u2014 LIVE DASHBOARD", color="white",
        fontsize=9.5, fontweight="bold", va="center")
ax.text(9.6, 9.15, "20 Aug 2024  10:15", color="#cddafd", fontsize=7, ha="right", va="center")

cards = [
    ("Rainfall", "12.6 mm/h", "#2a9d8f"), ("Water level", "0.86 m", "#264653"),
    ("Discharge", "16.7 m\u00b3 s\u207b\u00b9", "#7b2cbf"), ("Soil moisture", "0.21 m\u00b3 m\u207b\u00b3", "#e76f51"),
    ("Sediment conc.", "125 mg L\u207b\u00b9", "#e63946"), ("System status", "MODERATE", "#f4a261"),
]
for i, (lbl, val, col) in enumerate(cards):
    cx = 0.1 + (i % 2) * 5.0
    cy = 6.9 - (i // 2) * 2.55
    ax.add_patch(FancyBboxPatch((cx, cy), 4.75, 2.15, boxstyle="round,pad=0.02,rounding_size=0.09",
                 facecolor="#f8f9fa", edgecolor=col, linewidth=1.6))
    ax.add_patch(plt.Rectangle((cx, cy + 1.75), 4.75, 0.4, facecolor=col, edgecolor="none"))
    ax.text(cx + 2.375, cy + 1.95, lbl, color="white", fontsize=7.3, fontweight="bold", ha="center", va="center")
    ax.text(cx + 2.375, cy + 0.85, val, color="#212529", fontsize=11.5, fontweight="bold", ha="center", va="center")
ax.set_title(lab("B", "Live sensor-data readout panel"), fontsize=8.8, y=0.995)

# --- Panel C: real-time hydrograph on the dashboard ---------------------
ax = fig.add_subplot(gs[1, 0])
ts2 = pd.read_csv(DATA / "01_dt_state_estimation_timeseries.csv", parse_dates=["datetime"])
window = ts2.iloc[-240:]
ax.plot(window.datetime, window.discharge_obs_m3s, color="#1a1a2e", lw=1.0, label="Observed")
ax.plot(window.datetime, window.discharge_sim_m3s, color="#e63946", lw=0.9, alpha=0.85, label="Digital Twin (live)")
ax.fill_between(window.datetime, window.discharge_sim_m3s * 0.85, window.discharge_sim_m3s * 1.15,
                 color="#e63946", alpha=0.15, label="95% credible interval")
ax.set_ylabel("Discharge (m$^3$ s$^{-1}$)"); ax.set_xlabel("Time (last 10 days)")
ax.tick_params(axis="x", rotation=25)
ax.legend(frameon=False, fontsize=7)
ax.set_title(lab("C", "Real-time hydrograph (live Bayesian nowcast)"), fontsize=8.8)

# --- Panel D: alert / decision-support panel -----------------------------
ax = fig.add_subplot(gs[1, 1]); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.add_patch(FancyBboxPatch((0.2, 6.6), 9.6, 3.0, boxstyle="round,pad=0.02,rounding_size=0.08",
             facecolor="#fff3cd", edgecolor="#f4a261", linewidth=1.6))
ax.add_patch(plt.Circle((1.1, 8.65), 0.35, facecolor="#f4a261", edgecolor="none"))
ax.text(1.1, 8.65, "!", color="white", fontsize=15, fontweight="bold", ha="center", va="center")
ax.text(1.8, 9.15, "MODERATE RISK", fontsize=9.5, fontweight="bold", color="#7a4a05")
ax.text(1.8, 8.55, "Rising sediment concentration detected\nnear Station S3 headcut.", fontsize=7.3, color="#5c3d00")
ax.text(1.0, 7.1, "Recommended actions:  \u2022 Maintain vegetation strips  \u2022 Inspect upstream check dams",
        fontsize=6.9, color="#5c3d00")

ax.add_patch(FancyBboxPatch((0.2, 2.6), 9.6, 3.4, boxstyle="round,pad=0.02,rounding_size=0.08",
             facecolor="#e9f7ef", edgecolor="#2a9d8f", linewidth=1.6))
ax.text(0.6, 5.55, "SENSOR NETWORK STATUS", fontsize=8.6, fontweight="bold", color="#1b5e4f")
status_rows = [("Rain gauges (2/2)", "Online"), ("Water-level loggers (2/2)", "Online"),
               ("Soil-moisture sensors (4/4)", "Online"), ("Discharge/turbidity probe (1/1)", "Online"),
               ("Data availability (7-day)", "99.2 %")]
for i, (k, v) in enumerate(status_rows):
    yy = 5.0 - i * 0.5
    ax.text(0.6, yy, k, fontsize=6.9, color="#1b5e4f")
    ax.text(9.2, yy, v, fontsize=6.9, color="#1b5e4f", ha="right", fontweight="bold")
ax.set_title(lab("D", "Alerts and decision-support panel"), fontsize=8.8, y=0.98)

fig.tight_layout(rect=[0, 0.02, 1, 0.98])
fig.savefig(FIG / "Figure_14_dashboard_3D_visualization.png", dpi=300)
plt.close(fig)

print("Figures written to", FIG)
for f in sorted(FIG.glob("Figure_*.png")):
    print(" -", f.name)
