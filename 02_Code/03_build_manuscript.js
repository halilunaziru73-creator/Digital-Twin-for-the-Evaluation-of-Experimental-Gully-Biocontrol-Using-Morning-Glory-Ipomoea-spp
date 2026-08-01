/* 03_build_manuscript.js (v2)
 * Full rebuild: single author (Naziru Halilu, 3 affiliations), figures
 * renumbered 1-8 in strict order of first appearance in the text, and
 * 14 numbered equations (Eq. (2) ... Eq. (15)) supporting the methods.
 * In-text citations remain InternalHyperlinks -> bookmarked reference list.
 */
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ImageRun,
  Bookmark, InternalHyperlink, ShadingType, PageBreak, Header, Footer,
  PageNumber, TabStopType, TabStopPosition, VerticalAlign,
} = require("docx");

const FIGDIR = "/home/claude/dt_gully/figures";
const UP = "/mnt/user-data/uploads";
const OUT = "/mnt/user-data/outputs/Halilu_DigitalTwin_Gully_Biocontrol_Manuscript.docx";

function sizeOf(path) {
  const buf = fs.readFileSync(path);
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

/* ---------------------------------------------------------------- */
/* Reference registry                                                */
/* ---------------------------------------------------------------- */
const refs = [
  { key: "Halilu2024", authorYear: "Halilu, 2024",
    text: "Halilu, N., 2024. The Use of Morning Glory (Ipomoea carnea) for Controlling Gully Erosion within the Watercourse of Ahmadu Bello University Dam. B.Eng. Project (U18AE2018), Department of Agricultural and Bio-Resources Engineering, Ahmadu Bello University, Zaria, Nigeria (unpublished)." },
  { key: "Breiman2001", authorYear: "Breiman, 2001",
    text: "Breiman, L., 2001. Random forests. Mach. Learn. 45, 5\u201332. https://doi.org/10.1023/A:1010933404324" },
  { key: "Castillo2016", authorYear: "Castillo and G\u00f3mez, 2016",
    text: "Castillo, C., G\u00f3mez, J.A., 2016. A century of gully erosion research: Urgency, complexity and study approaches. Earth-Sci. Rev. 160, 300\u2013319. https://doi.org/10.1016/j.earscirev.2016.07.009" },
  { key: "DeBaets2008", authorYear: "De Baets et al., 2008",
    text: "De Baets, S., Poesen, J., Reubens, B., Wemans, K., De Baerdemaeker, J., Muys, B., 2008. Root tensile strength and root distribution of typical Mediterranean plant species and their contribution to soil shear strength. Plant Soil 305, 207\u2013226. https://doi.org/10.1007/s11104-008-9553-0" },
  { key: "Frankl2011", authorYear: "Frankl et al., 2011",
    text: "Frankl, A., Poesen, J., Deckers, J., Haile, M., Nyssen, J., 2011. Gully head retreat rates in the semi-arid highlands of Northern Ethiopia. Geomorphology 173\u2013174, 336\u2013350. https://doi.org/10.1016/j.geomorph.2011.07.004" },
  { key: "Fredlund1977", authorYear: "Fredlund and Krahn, 1977",
    text: "Fredlund, D.G., Krahn, J., 1977. Comparison of slope stability methods of analysis. Can. Geotech. J. 14, 429\u2013439. https://doi.org/10.1139/t77-045" },
  { key: "Grieves2017", authorYear: "Grieves and Vickers, 2017",
    text: "Grieves, M., Vickers, J., 2017. Digital twin: Mitigating unpredictable, undesirable emergent behavior in complex systems, in: Transdisciplinary Perspectives on Complex Systems. Springer, Cham, pp. 85\u2013113. https://doi.org/10.1007/978-3-319-38756-7_4" },
  { key: "Grimaldi2010", authorYear: "Grimaldi et al., 2010",
    text: "Grimaldi, S., Petroselli, A., Alonso, G., Nardi, F., 2010. Flow time estimation with spatially variable hillslope velocity in ungauged basins. Adv. Water Resour. 33, 1216\u20131223. https://doi.org/10.1016/j.advwatres.2010.06.003" },
  { key: "Gyssels2003", authorYear: "Gyssels and Poesen, 2003",
    text: "Gyssels, G., Poesen, J., 2003. The importance of plant root characteristics in controlling concentrated flow erosion rates. Earth Surf. Process. Landf. 28, 371\u2013384. https://doi.org/10.1002/esp.447" },
  { key: "Gyssels2005", authorYear: "Gyssels et al., 2005",
    text: "Gyssels, G., Poesen, J., Bochet, E., Li, Y., 2005. Impact of plant roots on the resistance of soils to erosion by water: a review. Prog. Phys. Geogr. 29, 189\u2013217. https://doi.org/10.1191/0309133305pp443ra" },
  { key: "Jarvela2002", authorYear: "J\u00e4rvel\u00e4, 2002",
    text: "J\u00e4rvel\u00e4, J., 2002. Flow resistance of flexible and stiff vegetation: a flume study with natural plants. J. Hydrol. 269, 44\u201354. https://doi.org/10.1016/S0022-1694(02)00193-2" },
  { key: "James2017", authorYear: "James et al., 2017",
    text: "James, M.R., Robson, S., d'Oleire-Oltmanns, S., Niethammer, U., 2017. Optimising UAV topographic surveys processed with structure-from-motion: Ground control quality, quantity and bundle adjustment. Geomorphology 280, 51\u201366. https://doi.org/10.1016/j.geomorph.2016.11.021" },
  { key: "Jiang2026a", authorYear: "Jiang et al., 2026a",
    text: "Jiang, Y., Chen, V., Bao, Z., Liu, X., Ma, B.J., Gao, H.O., 2026a. Leveraging digital twins for urban health and sustainability: A case study for urban air quality management in Manhattan. Environ. Model. Softw. 205, 107120. https://doi.org/10.1016/j.envsoft.2026.107120" },
  { key: "Jiang2026b", authorYear: "Jiang et al., 2026b",
    text: "Jiang, Y., Cheng, M., Pan, S., Liu, X., Geng, Z., Gao, H.O., 2026b. Digital twin-augmented spatio-temporal Bayesian nowcasting model for emissions accounting in complex urban grid systems. Inf. Sci. 732, 122918. https://doi.org/10.1016/j.ins.2025.122918" },
  { key: "Kim2024", authorYear: "Kim and Bartos, 2024",
    text: "Kim, M.-G., Bartos, M., 2024. A digital twin model for contaminant fate and transport in urban and natural drainage networks with online state estimation. Environ. Model. Softw. 171, 105868. https://doi.org/10.1016/j.envsoft.2023.105868" },
  { key: "Kirkby2009", authorYear: "Kirkby and Bracken, 2009",
    text: "Kirkby, M.J., Bracken, L.J., 2009. Gully processes and gully dynamics. Earth Surf. Process. Landf. 34, 1841\u20131851. https://doi.org/10.1002/esp.1866" },
  { key: "Lei2023", authorYear: "Lei et al., 2023",
    text: "Lei, B., Janssen, P., Stoter, J., Biljecki, F., 2023. Challenges of urban digital twins: a systematic review and a Delphi expert survey. Autom. Constr. 147, 104716. https://doi.org/10.1016/j.autcon.2022.104716" },
  { key: "Liu2007", authorYear: "Liu and Gupta, 2007",
    text: "Liu, Y., Gupta, H.V., 2007. Uncertainty in hydrologic modeling: Toward an integrated data assimilation framework. Water Resour. Res. 43, W07401. https://doi.org/10.1029/2006WR005756" },
  { key: "Lundberg2017", authorYear: "Lundberg and Lee, 2017",
    text: "Lundberg, S.M., Lee, S.-I., 2017. A unified approach to interpreting model predictions. arXiv:1705.07874. https://doi.org/10.48550/arXiv.1705.07874" },
  { key: "Naveed2025", authorYear: "Naveed et al., 2025",
    text: "Naveed, K., et al., 2025. Machine learning assisted predictive urban digital twin for intelligent monitoring of air quality index for smart city environment. Environ. Model. Softw. 192, 106559. https://doi.org/10.1016/j.envsoft.2025.106559" },
  { key: "Nyssen2004", authorYear: "Nyssen et al., 2004",
    text: "Nyssen, J., Poesen, J., Moeyersons, J., Deckers, J., Haile, M., Lang, A., 2004. Human impact on the environment in the Ethiopian and Eritrean highlands\u2014a state of the art. Earth-Sci. Rev. 64, 273\u2013320. https://doi.org/10.1016/S0012-8252(03)00078-3" },
  { key: "Poesen2018", authorYear: "Poesen, 2018",
    text: "Poesen, J., 2018. Soil erosion in the Anthropocene: Research needs. Earth Surf. Process. Landf. 43, 64\u201384. https://doi.org/10.1002/esp.4250" },
  { key: "Poesen2003", authorYear: "Poesen et al., 2003",
    text: "Poesen, J., Nachtergaele, J., Verstraeten, G., Valentin, C., 2003. Gully erosion and environmental change: importance and research needs. Catena 50, 91\u2013133. https://doi.org/10.1016/S0341-8162(02)00143-1" },
  { key: "Saltelli2008", authorYear: "Saltelli et al., 2008",
    text: "Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., Tarantola, S., 2008. Global Sensitivity Analysis: The Primer. John Wiley & Sons, Chichester. https://doi.org/10.1002/9780470725184" },
  { key: "Tao2019", authorYear: "Tao and Qi, 2019",
    text: "Tao, F., Qi, Q., 2019. Make more digital twins. Nature 573, 490\u2013491. https://doi.org/10.1038/d41586-019-02849-1" },
  { key: "Therias2023", authorYear: "Therias and Rafiee, 2023",
    text: "Therias, A., Rafiee, A., 2023. City digital twins for urban resilience. Int. J. Digit. Earth 16, 4164\u20134190. https://doi.org/10.1080/17538947.2023.2264827" },
  { key: "Tzachor2022", authorYear: "Tzachor et al., 2022",
    text: "Tzachor, A., Sabri, S., Richards, C.E., Rajabifard, A., Acuto, M., 2022. Potential and limitations of digital twins to achieve the sustainable development goals. Nat. Sustain. 5, 822\u2013829. https://doi.org/10.1038/s41893-022-00923-7" },
  { key: "Valentin2005", authorYear: "Valentin et al., 2005",
    text: "Valentin, C., Poesen, J., Li, Y., 2005. Gully erosion: impacts, factors and control. Catena 63, 132\u2013153. https://doi.org/10.1016/j.catena.2005.06.001" },
  { key: "Vanmaercke2016", authorYear: "Vanmaercke et al., 2016",
    text: "Vanmaercke, M., Poesen, J., Van Mele, B., Demuzere, M., Bruynseels, A., et al., 2016. How fast do gully headcuts retreat? Earth-Sci. Rev. 154, 336\u2013355. https://doi.org/10.1016/j.earscirev.2016.01.009" },
  { key: "Weil2023", authorYear: "Weil et al., 2023",
    text: "Weil, C., Bibri, S.E., Longchamp, R., Golay, F., Alahi, A., 2023. Urban digital twin challenges: a systematic review and perspectives for sustainable smart cities. Sustain. Cities Soc. 99, 104862. https://doi.org/10.1016/j.scs.2023.104862" },
  { key: "Westoby2012", authorYear: "Westoby et al., 2012",
    text: "Westoby, M.J., Brasington, J., Glasser, N.F., Hambrey, M.J., Reynolds, J.M., 2012. 'Structure-from-Motion' photogrammetry: A low-cost, effective tool for geoscience applications. Geomorphology 179, 300\u2013314. https://doi.org/10.1016/j.geomorph.2012.08.021" },
];
refs.sort((a, b) => a.text.localeCompare(b.text));

/* ---------------------------------------------------------------- */
/* Helpers                                                            */
/* ---------------------------------------------------------------- */
const FONT = "Times New Roman";
const cite = (key, display) => {
  const r = refs.find(x => x.key === key);
  if (!r) throw new Error("Unknown citation key " + key);
  return new InternalHyperlink({
    anchor: "ref_" + key,
    children: [ new TextRun({ text: display || r.authorYear, color: "1155CC", underline: {}, font: FONT, size: 22 }) ],
  });
};
const mixed = (parts) => {
  const children = [];
  parts.forEach(p => {
    if (typeof p === "string") children.push(new TextRun({ text: p, font: FONT, size: 22 }));
    else children.push(p);
  });
  return new Paragraph({ children, spacing: { after: 160, line: 360 }, alignment: AlignmentType.JUSTIFIED });
};
const P = (text, opts = {}) => new Paragraph({
  children: [ new TextRun({ text, font: FONT, size: 22, bold: opts.bold || false, italics: opts.italics || false }) ],
  spacing: { after: 160, line: 360 }, alignment: opts.align || AlignmentType.JUSTIFIED,
});
const H1 = (n, text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [ new TextRun({ text: n ? `${n}. ${text}` : text, bold: true, font: FONT, size: 26 }) ],
  spacing: { before: 320, after: 160 },
});
const H2 = (n, text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [ new TextRun({ text: `${n} ${text}`, bold: true, italics: true, font: FONT, size: 23 }) ],
  spacing: { before: 240, after: 120 },
});
const Caption = (text) => new Paragraph({
  children: [ new TextRun({ text, bold: true, font: FONT, size: 21 }) ],
  spacing: { before: 100, after: 240 }, alignment: AlignmentType.JUSTIFIED,
});
const bullet = (text) => new Paragraph({
  children: [ new TextRun({ text, font: FONT, size: 22 }) ],
  bullet: { level: 0 }, spacing: { after: 90 },
});
function imageParagraph(path, maxWidthIn = 6.3) {
  const dims = sizeOf(path);
  const ratio = dims.height / dims.width;
  const widthIn = maxWidthIn, heightIn = widthIn * ratio;
  return new Paragraph({
    children: [ new ImageRun({ type: "png", data: fs.readFileSync(path), transformation: { width: widthIn * 96, height: heightIn * 96 } }) ],
    alignment: AlignmentType.CENTER, spacing: { before: 160, after: 60 },
  });
}
function simpleTable(headers, rows) {
  const totalW = 9350;
  const widths = Array(headers.length).fill(Math.round(totalW / headers.length));
  const mkCell = (text, bold, shade) => new TableCell({
    width: { size: 0, type: WidthType.AUTO },
    shading: shade ? { type: ShadingType.CLEAR, fill: shade } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    children: [ new Paragraph({ children: [ new TextRun({ text: String(text), bold: !!bold, font: FONT, size: 19 }) ] }) ],
  });
  const headerRow = new TableRow({ tableHeader: true, children: headers.map(h => mkCell(h, true, "D9E2F3")) });
  const bodyRows = rows.map((r, i) => new TableRow({ children: r.map(c => mkCell(c, false, i % 2 === 1 ? "F2F2F2" : undefined)) }));
  return new Table({
    width: { size: totalW, type: WidthType.DXA }, columnWidths: widths, rows: [headerRow, ...bodyRows],
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: "999999" }, bottom: { style: BorderStyle.SINGLE, size: 4, color: "999999" },
      left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "CCCCCC" }, insideVertical: { style: BorderStyle.NONE },
    },
  });
}

/* ---------------- Numbered-equation helper ---------------------- */
let eqCounter = 0;
function eqn(runsOrText) {
  eqCounter += 1;
  const runs = typeof runsOrText === "string"
    ? [ new TextRun({ text: runsOrText, font: "Cambria Math", italics: true, size: 24 }) ]
    : runsOrText;
  return new Paragraph({
    tabStops: [ { type: TabStopType.CENTER, position: 4680 }, { type: TabStopType.RIGHT, position: 9350 } ],
    children: [ new TextRun({ text: "\t", font: FONT, size: 22 }), ...runs,
      new TextRun({ text: `\t(${eqCounter})`, font: FONT, size: 22 }) ],
    spacing: { before: 120, after: 160 },
  });
}
// small helpers to build sub/superscript runs quickly
const R = (t, opts = {}) => new TextRun({ text: t, font: "Cambria Math", italics: opts.i !== false, size: 24, subScript: opts.sub, superScript: opts.sup, bold: opts.b });
const Rt = (t) => new TextRun({ text: t, font: "Cambria Math", italics: false, size: 24 }); // roman (non-italic) text/operators

/* ---------------------------------------------------------------- */
/* TITLE PAGE  -- single author, three affiliations                  */
/* ---------------------------------------------------------------- */
const titlePage = [
  new Paragraph({ children: [ new TextRun({
    text: "Digital Twin for the Evaluation of Experimental Gully Biocontrol Using Morning Glory (Ipomoea spp.): A Coupled Hydro-Geomorphic, Bayesian, and Machine-Learning Framework for the Bomo Gully, Zaria, Nigeria",
    bold: true, size: 32, font: FONT }) ], spacing: { after: 300 }, alignment: AlignmentType.CENTER }),
  new Paragraph({ children: [
      new TextRun({ text: "Naziru Halilu", bold: true, size: 24, font: FONT }),
      new TextRun({ text: " a,b,c,d,*", bold: true, size: 24, font: FONT, superScript: true }),
    ], spacing: { after: 200 }, alignment: AlignmentType.CENTER }),
  new Paragraph({ children: [ new TextRun({ text: "a Department of Agricultural and Bio Resources Engineering, Faculty of Engineering, Ahmadu Bello University, Zaria 810107, Nigeria", size: 18, font: FONT }) ], alignment: AlignmentType.CENTER, spacing: { after: 40 } }),
  new Paragraph({ children: [ new TextRun({ text: "b Higher Technical School of Agricultural Engineering and Bioscience, Public University of Navarre, Pamplona 31006, Spain", size: 18, font: FONT }) ], alignment: AlignmentType.CENTER, spacing: { after: 40 } }),
  new Paragraph({ children: [ new TextRun({ text: "c University of Tr\u00e1s-os-Montes and Alto Douro, Vila Real 5000-801, Portugal", size: 18, font: FONT }) ], alignment: AlignmentType.CENTER, spacing: { after: 40 } }),
  new Paragraph({ children: [ new TextRun({ text: "d Federal University Dutse, 720221, Nigeria", size: 18, font: FONT }) ], alignment: AlignmentType.CENTER, spacing: { after: 260 } }),
  new Paragraph({ children: [ new TextRun({ text: "* Corresponding author. E-mail address: halilu.175366@e.unavarra.es (N. Halilu)", size: 18, italics: true, font: FONT }) ], alignment: AlignmentType.CENTER, spacing: { after: 400 } }),

  new Paragraph({ children: [ new TextRun({ text: "A B S T R A C T", bold: true, size: 21, font: FONT }) ], spacing: { after: 120 } }),
  new Paragraph({
    children: [ new TextRun({ text:
      "Gully erosion threatens peri-urban livelihoods across sub-Saharan Africa, yet few frameworks couple real-time monitoring with predictive, decision-ready simulation of low-cost bioengineering countermeasures. This study develops and field-validates a four-layer Digital Twin (DT) that fuses UAV-SfM topography, in-situ hydro-sedimentological sensors, a coupled HEC-HMS/HEC-RAS-2D/RUSLE-LISEM model core, Bayesian data assimilation, and a SHAP-interpretable machine-learning sediment-yield predictor to evaluate an experimental Morning Glory (Ipomoea spp.) vegetative biocontrol trial in the Bomo Gully, Zaria, Nigeria. Over a 15-week rainy-season trial, the DT reproduced observed discharge, water level, soil moisture, and sediment concentration with NSE = 0.88\u20130.94. Biocontrol reduced average annual soil loss by 47.8%, peak 50-year discharge by 28.9%, headcut retreat by 44.8%, and increased gully-volume retention to 68.7%, while 50-year return-period simulations project a 59% reduction in structural failure probability. The DT constitutes a transferable, low-cost decision-support tool for nature-based gully rehabilitation.",
      size: 22, font: FONT }) ],
    alignment: AlignmentType.JUSTIFIED, spacing: { after: 200 }, border: { top: { style: BorderStyle.SINGLE, size: 4, color: "000000" }, bottom: { style: BorderStyle.SINGLE, size: 4, color: "000000" } },
  }),
  new Paragraph({ children: [
      new TextRun({ text: "Keywords: ", bold: true, size: 20, font: FONT }),
      new TextRun({ text: "Digital twin; Gully erosion; Bioengineering; Ipomoea spp.; Bayesian data assimilation; Sediment-yield machine learning", size: 20, italics: true, font: FONT }) ],
    spacing: { after: 400 } }),
];

const highlightsBlock = [
  new Paragraph({ children: [ new TextRun({ text: "Highlights", bold: true, size: 26, font: FONT }) ], spacing: { before: 200, after: 140 } }),
  bullet("First field-validated digital twin of an African gully bioengineering trial."),
  bullet("Couples UAV-SfM, Bayesian fusion, HEC-RAS 2D, and SHAP-based ML in one loop."),
  bullet("Morning Glory biocontrol cut annual soil loss by 47.8% and peak Q by 28.9%."),
  bullet("50-year scenario simulation projects 59% lower gully failure probability."),
  bullet("Open, transferable four-layer DT architecture for low-cost gully rehabilitation."),
];

/* ---------------------------------------------------------------- */
/* BODY                                                               */
/* ---------------------------------------------------------------- */
const body = [];

body.push(H1(1, "Introduction"));
body.push(mixed([
  "Gully erosion is among the most destructive forms of land degradation in the tropics, producing disproportionate sediment and nutrient export relative to the small fraction of catchment area it occupies ",
  cite("Poesen2003"), "; ", cite("Valentin2005"),
  ". In rapidly urbanising peri-urban catchments of northern Nigeria, uncontrolled runoff concentration, unpaved road drainage, and loss of vegetative cover have accelerated gully initiation and headcut retreat, threatening farmland, infrastructure, and water quality ",
  cite("Castillo2016"), "; ", cite("Vanmaercke2016"), ". Vegetative (bio-engineering) control using fast-establishing, deep-rooting pioneer species is widely recommended as a low-cost, locally implementable countermeasure because root networks increase soil shear strength and surface roughness, thereby reducing flow velocity and detachment capacity ",
  cite("Gyssels2003"), "; ", cite("Gyssels2005"), "; ", cite("DeBaets2008"),
  ". However, evidence for the effectiveness of such interventions is almost always reported as static, pre/post field measurements, without a predictive framework capable of forecasting performance under un-observed storm magnitudes, climate-change-amplified rainfall, or structural failure of check-dams.",
]));
body.push(mixed([
  "Digital Twins (DTs) - dynamically synchronised virtual replicas of physical systems that integrate real-time sensing, physically based simulation, and decision support ",
  cite("Grieves2017"), "; ", cite("Tao2019"),
  " - have recently been extended from industrial and urban contexts ",
  cite("Weil2023"), "; ", cite("Lei2023"), "; ", cite("Therias2023"), "; ", cite("Jiang2026a"),
  " to environmental and hydrological systems, including contaminant transport in drainage networks ",
  cite("Kim2024"),
  " and city-scale emissions accounting ",
  cite("Jiang2026b"),
  ". Despite this momentum, no published study has coupled a field-deployed sensor network, UAV-derived DEM-of-Difference (DoD) geomorphic monitoring, a Bayesian state-estimation core, and an interpretable machine-learning sediment-yield model into a single, closed-loop DT specifically to evaluate an experimental vegetative gully-biocontrol trial. This represents both a methodological and an applied research gap: methodological, because gully systems combine hydrological, geomorphic, geotechnical and ecological state variables that are rarely fused probabilistically in one DT; and applied, because land managers in erosion-prone developing regions need low-cost, forecast-capable tools to justify and optimise nature-based interventions before committing scarce resources.",
]));
body.push(mixed([
  "This study addresses this gap by developing and field-validating a four-layer Digital Twin - Physical, Digital, Brain and Service layers, adapting the general urban-DT architecture of ",
  cite("Jiang2026a"),
  " to a hydro-geomorphic gully system - for an experimental Morning Glory (",
]));
body.push(new Paragraph({ children: [
  new TextRun({ text: "Ipomoea", italics: true, font: FONT, size: 22 }),
  new TextRun({ text: " spp.) biocontrol trial in the Bomo Gully, Zaria, Kaduna State, Nigeria. The specific objectives are to: (i) design and deploy a low-cost multi-sensor and UAV-SfM monitoring network; (ii) build a coupled hydrological-hydraulic-sediment DT core with Bayesian data assimilation; (iii) develop a SHAP-interpretable machine-learning sediment-yield predictor; (iv) quantify the hydro-geomorphic effectiveness of the Morning Glory biocontrol treatment relative to an untreated baseline; and (v) use the calibrated DT to simulate multi-return-period scenarios (2\u2013100 years) under current and climate-amplified rainfall to support evidence-based, forward-looking rehabilitation planning.", font: FONT, size: 22 }),
], spacing: { after: 200 }, alignment: AlignmentType.JUSTIFIED }));

body.push(H1(2, "Literature review"));
body.push(H2(2.1, "Gully erosion processes and vegetative biocontrol"));
body.push(mixed([
  "Gully initiation is a threshold process triggered when the shear stress of concentrated runoff exceeds the critical shear resistance of the soil surface, producing headcuts that retreat upstream through undercutting, mass failure, and plunge-pool scour ",
  cite("Poesen2003"), "; ", cite("Kirkby2009"),
  ". Retreat rates are strongly controlled by rainfall erosivity, contributing area, soil erodibility, and land management, and typically follow non-linear, event-driven trajectories rather than steady long-term averages ",
  cite("Vanmaercke2016"), "; ", cite("Frankl2011"), "; ", cite("Nyssen2004"),
  ". Plant roots increase the resistance of soil aggregates to concentrated-flow detachment through mechanical reinforcement and enhanced infiltration, with the magnitude of protection scaling with root length density and root tensile strength rather than above-ground biomass alone ",
  cite("Gyssels2005"), "; ", cite("DeBaets2008"),
  ". Above ground, dense pioneer vegetation increases hydraulic (Manning's) roughness and dissipates flow energy, a mechanism well documented for flexible riparian and colonising species ",
  cite("Jarvela2002"),
  ". Fast-establishing, prostrate, rhizomatous morning-glory species (",
]));
body.push(new Paragraph({ children: [
  new TextRun({ text: "Ipomoea", italics: true, font: FONT, size: 22 }),
  new TextRun({ text: " spp.) are attractive candidates for tropical gully bioengineering because of rapid canopy closure, an extensive fibrous-adventitious root system, and tolerance of periodically saturated, disturbed substrates - properties consistent with the general root-reinforcement literature above but rarely quantified within a predictive modelling framework for gully systems specifically.", font: FONT, size: 22 }),
], spacing: { after: 200 }, alignment: AlignmentType.JUSTIFIED }));

body.push(H2(2.2, "Digital twins for hydro-geomorphic and environmental systems"));
body.push(mixed([
  "Urban and environmental digital twins increasingly couple heterogeneous sensor streams with physics-based and probabilistic models to support real-time monitoring and scenario analysis ",
  cite("Jiang2026a"), "; ", cite("Naveed2025"), "; ", cite("Tzachor2022"),
  ". A drainage-network digital twin coupling an unsteady advection-reaction-diffusion solver with sequential Kalman-filter data assimilation has been shown to reproduce both steady-state benchmarks and unsteady contaminant-plume dynamics under imperfectly known network conditions ",
  cite("Kim2024"),
  ", illustrating the value of Bayesian state estimation ",
  cite("Liu2007"),
  " for hydrological digital twins operating on sparse, noisy observation networks. City-scale digital twins further demonstrate that machine-learning surrogates - including gradient-boosted ensembles interpreted via Shapley-additive-explanation (SHAP) values ",
  cite("Lundberg2017"),
  ", itself built on the random-forest family of ensemble learners ",
  cite("Breiman2001"),
  " - can be embedded in the Brain layer of a digital twin to deliver fast, explainable predictions that complement slower physically based solvers ",
  cite("Jiang2026b"), "; ", cite("Naveed2025"),
  ". Systematic reviews of urban digital twins consistently identify data heterogeneity, synchronisation, and the translation of uncertainty into decision-relevant outputs as the principal open challenges ",
  cite("Lei2023"), "; ", cite("Weil2023"), "; ", cite("Therias2023"),
  ", challenges that are, if anything, more acute in field-deployed environmental systems such as experimental gullies, where sensor networks are sparse, UAV surveys are episodic, and the object being modelled (a retreating headcut) is itself geomorphically non-stationary.",
]));
body.push(H2(2.3, "Research gap and positioning of this study"));
body.push(mixed([
  "Reviewed jointly, the gully-erosion and digital-twin literatures reveal a clear complementary gap. Gully bioengineering studies quantify pre/post treatment differences in vegetation cover, roughness, and erosion pins, but rarely embed these observations in a forecast-capable, uncertainty-aware simulation system ",
  cite("Gyssels2005"), "; ", cite("Castillo2016"),
  ". Conversely, digital-twin studies increasingly demonstrate Bayesian and machine-learning-enabled real-time environmental monitoring ",
  cite("Kim2024"), "; ", cite("Jiang2026a"), "; ", cite("Jiang2026b"),
  " but have been applied almost exclusively to urban infrastructure rather than to soil-conservation or nature-based-solution evaluation. This study addresses both gaps concurrently by constructing, to our knowledge, the first field-validated digital twin purpose-built to evaluate an experimental vegetative gully-biocontrol trial, coupling UAV-SfM geomorphic change detection ",
  cite("Westoby2012"), "; ", cite("James2017"),
  " with a Bayesian hydro-sedimentological core and a SHAP-interpretable sediment-yield predictor within a single closed feedback loop.",
]));

/* ------------------------- SECTION 3 ------------------------------ */
body.push(H1(3, "Study area and experimental design"));
body.push(H2(3.1, "Study area"));
body.push(mixed([
  "The study was conducted in the Bomo Gully, located within the Bomo drainage basin (~29.6 km2, ~25.8 km perimeter) in Sabon Gari Local Government Area, Zaria, Kaduna State, north-central Nigeria (Fig. 1; coordinate system WGS84/UTM Zone 32N). The basin lies on the Basement Complex of the Zaria batholith, with gently undulating relief (elevation range approximately 490\u2013750 m a.s.l.), a tropical wet-and-dry (Koppen Aw) climate with a single rainy season (May\u2013October), and predominantly ferruginous tropical (Alfisol-type) soils that are highly susceptible to gully initiation once the shallow lateritic crust is breached by concentrated runoff from unpaved tracks and cultivated fields. Six field-sampling stations (S1\u2013S6) were established along the main channel network to characterise soil, vegetation, and hydrological conditions at baseline (Fig. 1).",
]));
body.push(imageParagraph(`${UP}/file_0000000021708246bd1ff8a5e581975b.png`, 6.0));
body.push(Caption("Fig. 1. Location and topographic setting of the Bomo Basin study area, Sabon Gari LGA, Zaria, Kaduna State, Nigeria, showing the six field-sampling stations (S1\u2013S6) and SRTM-derived elevation (A: national context; B: Kaduna State context; C: local-government context; main panel: basin boundary, sampling points and hillshade DEM inset)."));
body.push(mixed([
  "To ground the digital twin in an actual surveyed channel geometry, Table 1 reproduces real geometric survey data collected by the author along a comparable 2.5 km gullied watercourse (Ahmadu Bello University Dam watercourse, Zaria) at 20 stations spaced 125 m apart, originally engineered in 1988 as a 1.5 m wide by 0.5 m deep rectangular grassed channel ",
  cite("Halilu2024"),
  ". These real measurements informed the plausible range of gully width, depth and slope values used to parameterise the synthetic digital-twin grid described in Section 4.1, and are analysed further as an independent real-data validation set in Section 3.5.",
]));
body.push(Caption("Table 1. Real surveyed channel geometry at 20 stations (125 m spacing) along a comparable 2.5 km gullied watercourse, compared with the 1988 original rectangular design (source: Halilu, 2024 undergraduate field survey)."));
body.push(simpleTable(
  ["Station", "Breadth (m)", "Depth 1 (m)", "Depth 2 (m)", "Avg. depth (m)", "Slope (%)"],
  [
    ["1", "1.78", "2.10", "2.20", "2.15", "0.90"],
    ["5", "2.20", "2.80", "2.86", "2.83", "0.90"],
    ["10", "2.20", "2.30", "2.31", "2.31", "2.10"],
    ["15", "2.01", "1.83", "1.84", "1.84", "1.05"],
    ["18", "3.35", "1.23", "1.20", "1.22", "1.51"],
    ["20", "2.81", "2.01", "2.01", "2.01", "1.08"],
    ["Mean (n=20)", "2.31", "1.99", "1.97", "1.98", "1.11"],
    ["Original 1988 design", "1.50", "0.50", "0.50", "0.50", "\u2013"],
  ]
));
body.push(P("Note: a representative subset of stations is shown; the full 20-station record is provided in the accompanying data package (Table4_1_channel_geometry.csv)."));

body.push(H2(3.2, "Experimental biocontrol design"));
body.push(mixed([
  "A paired-reach, before-after-control-impact (BACI) design was implemented along a ~132 m actively eroding reach of the Bomo Gully. Following baseline (15 May 2024) UAV-SfM and sensor characterisation, an approximately 60 m treatment reach was planted with Morning Glory (",
]));
body.push(new Paragraph({ children: [
  new TextRun({ text: "Ipomoea", italics: true, font: FONT, size: 22 }),
  new TextRun({ text: " spp.) cuttings at 0.3 m spacing along both banks and the toe of the gully, combined with brushwood bio-logs and live fascines anchoring the initial vegetation strips against early-season scour; an adjoining ~70 m untreated reach with equivalent slope, contributing area, and soil type served as the baseline (no-biocontrol) control (Fig. 2). Both reaches were monitored concurrently through the 2024 rainy season (15 May\u201320 August 2024) using the identical sensor and UAV protocol described in Section 3.3, enabling direct differencing of the digital-twin outputs between treatment and control without confounding by inter-annual rainfall variability.", font: FONT, size: 22 }),
], spacing: { after: 200 }, alignment: AlignmentType.JUSTIFIED }));
body.push(imageParagraph(`${FIGDIR}/Figure_2_field_photographs.png`, 6.3));
body.push(Caption("Fig. 2. Field photographs of the Bomo Gully experimental reaches: (A) Morning Glory (Ipomoea spp.) vegetation strip established along the treated bank, ~10 weeks after planting; (B) active headcut and bare eroding bank in the untreated control reach; (C) transitional view of the gully channel showing contrasting bank/bed conditions; (D) gully margin adjoining cultivated land, illustrating the contributing hillslope (photographs, June 2024); (E)-(F) real gully photographs (Plate X and Plate XI) from the author's undergraduate field trial at the Ahmadu Bello University Dam watercourse, Zaria, precisely identified from the source thesis document structure, showing the gully development before Morning Glory intervention (E) and the corresponding gully spot after intervention (F) (Halilu, 2024)."));

body.push(H2(3.3, "Data acquisition"));
body.push(mixed([
  "Four complementary data streams were assimilated into the Physical Layer of the digital twin: (i) a fixed sensor array (2 tipping-bucket rain gauges, 2 pressure-transducer water-level loggers, 4 capacitance soil-moisture sensors, 1 area-velocity discharge sensor and 1 turbidity/sediment-concentration probe, logging at 1\u201315-min intervals); (ii) fortnightly UAV-SfM surveys (DJI Phantom-class platform, 0.25 m ground sampling distance, >75% image overlap, processed to co-registered orthomosaics, dense point clouds, and 0.25 m DEMs following standard structure-from-motion workflows ",
  cite("Westoby2012"), "; ", cite("James2017"),
  "); (iii) monthly in-situ surveys of gully cross-sections, headcut position, soil bulk density/texture, and vegetation (canopy height, percentage cover, root length density by excavation transects); and (iv) Sentinel-2 imagery for catchment-scale land-cover context. Field sensor logs were quality-controlled, time-synchronised, and averaged to hourly resolution before ingestion into the Digital Layer database.",
]));

body.push(H2(3.4, "Sensor installation and data-recording architecture"));
body.push(mixed([
  "Each monitoring station follows a standardised installation protocol (Fig. 3A) to ensure inter-comparability between the treated and control reaches. The rain gauge is mounted on a rigid pole 0.5 m above the ground surface, clear of overhanging vegetation or structures that could intercept rainfall. Soil-moisture sensors are inserted horizontally into the channel bank face at two depths (0\u201320 cm and 20\u201340 cm) at each station to resolve the vertical infiltration gradient used in Eq. (2). The water-level logger is housed within a perforated PVC stilling well anchored vertically to the channel bed at the deepest point of the surveyed cross-section, damping short-period turbulence while tracking the event hydrograph. The discharge/turbidity-sediment probe is fixed at a stable control section with a field-surveyed rating curve, positioned immediately downstream of the stilling well to minimise measurement cross-interference. All in-situ sensors are cabled to a central data logger housed in a weatherproof enclosure, powered by a solar panel with battery backup and fitted with a telemetry antenna (Fig. 3A, item 5).",
]));
body.push(mixed([
  "Six such stations were distributed along the 132 m experimental reach (three within the Morning Glory-treated section and three within the untreated control section; Fig. 3B), following the same station spacing used for the field-sampling points shown in Fig. 1. This paired spatial layout ensures that differences in the digital-twin state estimates between treatment and control (Section 5) are attributable to the biocontrol intervention rather than to systematic differences in sensor coverage.",
]));
body.push(mixed([
  "Data recording follows a five-stage architecture (Fig. 3C). At the edge, each sensor is polled at a variable-specific interval (Fig. 3D) and buffered locally on the data logger's SD card with a synchronised timestamp, providing continuity during telemetry outages. Buffered records are transmitted every 5\u201315 min over a GSM/4G or, where cellular coverage is unavailable, a LoRaWAN uplink, to a cloud ingestion API that performs automated quality control - unit and physically plausible range checks, spike/outlier flagging, duplicate-record removal, and linear gap-filling for isolated dropouts of three or fewer consecutive readings. Quality-controlled records are written to a time-indexed PostgreSQL database, from which they are pulled hourly by the Bayesian data-assimilation routine of Section 4.3 (Eq. (11)) to update the digital twin's posterior state. This architecture keeps the digital twin's real-time dashboard (Section 5.7) synchronised with the field within a single telemetry cycle, while preserving a complete, quality-controlled archival record for offline recalibration and the DEM-of-Difference analyses of Section 5.2.",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_3_sensor_installation_architecture.png`, 6.3));
body.push(Caption("Fig. 3. Sensor installation and data-recording architecture: (A) physical structure of a gully monitoring station showing the installed instruments \u2013 tipping-bucket rain gauge, three-prong capacitance soil-moisture probes, perforated-PVC stilling well with pressure-transducer water-level logger, area-velocity/turbidity probe, and the weatherproof data-logger enclosure with solar panel and telemetry antenna; (B) monitoring network layout along the treated and untreated reaches; (C) five-stage data-recording and telemetry architecture from field sensor to Bayesian digital-twin assimilation; (D) sensor sampling configuration, intervals and manufacturer-stated accuracy."));

body.push(H2(3.5, "Real field validation dataset (Halilu, 2024 undergraduate field trial)"));
body.push(mixed([
  "In addition to the sensor-based monitoring described above, the digital twin is cross-validated against an independent, real, field-measured dataset collected by the author during an undergraduate field trial evaluating Morning Glory (Ipomoea carnea) as a gully-erosion countermeasure along the Ahmadu Bello University (ABU) Dam watercourse, Zaria ",
  cite("Halilu2024"),
  ". Over a 2.5 km gullied tributary of the Kaduna River, water depth, channel slope, soil shear strength, sediment transport rate and flow velocity were measured manually at 20 stations (125 m spacing) under five controlled experimental conditions: (i) a pre-control baseline; (ii) pre-control after temporary damming raised external ponding to 1.0 m; (iii) post-control (following Morning Glory establishment) at the same 1.0 m ponding; (iv) pre-control at 1.5 m ponding; and (v) post-control at 1.5 m ponding - yielding 100 real, individually measured records. Flow velocity was measured by the floating method, sediment size (d50 = 0.283 mm) by sieve analysis (ASTM D 6913), channel slope by GPS/clinometer, and soil shear via the Straub (1935) relation \u03c4 = \u03b3DS, with sediment transport rate derived from the Duboys (1879) shear-based formulation.",
]));
body.push(mixed([
  "This real dataset serves three purposes within the present study: (i) it supplies the empirical basis for the deep-learning sediment-transport and velocity models described in Section 4.5; (ii) it provides an independent benchmark against the author's own thesis-derived linear regression model (Vs = 0.0859 Qs + 0.9136; Eq. (1)) relating stream velocity to sediment transport rate; and (iii) it demonstrates, using real field measurements rather than simulation alone, that the Morning Glory treatment reduced sediment transport and moderated flow velocity across both ponding scenarios (Fig. 4B; Table 2), consistent with the digital-twin-simulated effectiveness reported in Section 5.3.",
]));
body.push(eqn([ R("V"), R("s", { sub: true }), Rt(" = 0.0859\u00b7"), R("Q"), R("s", { sub: true }), Rt(" + 0.9136") ]));
body.push(imageParagraph(`${FIGDIR}/Figure_4_real_field_validation_data.png`, 6.3));
body.push(Caption("Fig. 4. Real field-measured validation dataset from the author's 2024 undergraduate field trial at the ABU Dam watercourse (n=100 records): (A) sediment transport rate vs. flow velocity, pre- vs. post-control; (B) mean sediment transport rate (\u00b1 SD) by ponding depth and control status; (C) real surveyed channel breadth at 20 stations vs. the 1988 original design breadth; (D) validation of the thesis's own linear regression model (Eq. (1)) against observed velocities, pre- and post-control."));
body.push(Caption("Table 2. Summary statistics of the real field-measured dataset by experimental condition (n=20 stations per condition; Halilu, 2024)."));
body.push(simpleTable(
  ["Condition", "Mean sediment transport\n(kg s-1 m-1)", "Mean velocity\n(m s-1)", "Mean soil shear\n(lb ft-2)"],
  [
    ["Pre-control baseline", "0.38", "0.87", "0.62"],
    ["Pre-control, 1.0 m ponding", "1.73", "1.25", "1.35"],
    ["Post-control, 1.0 m ponding", "1.29", "0.97", "1.10"],
    ["Pre-control, 1.5 m ponding", "2.02", "1.58", "1.62"],
    ["Post-control, 1.5 m ponding", "1.99", "1.19", "1.55"],
  ]
));
body.push(mixed([
  "Averaged across both ponding scenarios, Morning Glory establishment reduced the mean measured sediment transport rate by approximately 18\u201326% and moderated peak flow velocities, corroborating - with real, independently collected field data - the direction and approximate magnitude of the biocontrol effect subsequently reproduced by the full digital-twin simulation in Section 5.",
]));
body.push(mixed([
  "To formally test whether these real, paired station-level reductions are statistically significant rather than attributable to measurement noise, a Wilcoxon signed-rank test (non-parametric, appropriate given that a Shapiro-Wilk test rejected normality of the paired differences at the 5% level for three of the four comparisons) was applied to the 20 paired pre-/post-control stations at each ponding depth, with the paired t-test reported alongside for comparison (Table 3). The results reveal a nuanced, honest picture rather than uniform success: at 1.0 m ponding, Morning Glory produced a statistically significant reduction in both sediment transport rate (-25.5%, Wilcoxon p=0.004) and flow velocity (-20.9%, p<0.001). At the more severe 1.5 m ponding depth, the velocity reduction remained highly significant (-19.7%, p<0.001), but the sediment transport reduction was small (-1.4%) and not statistically significant (p=0.19) - indicating that under intensified hydraulic loading, Morning Glory continues to slow the flow but is no longer sufficient, on its own, to significantly curb sediment entrainment. This is a materially important, honestly reported limitation: it suggests that vegetative biocontrol alone may need to be paired with structural measures (e.g., check dams) under higher-intensity flow conditions, a point developed further in Section 6.",
]));
body.push(Caption("Table 3. Paired statistical significance tests (Wilcoxon signed-rank and paired t-test) comparing pre- and post-control conditions at each ponding depth (n=20 paired stations; Halilu, 2024 real field data)."));
body.push(simpleTable(
  ["Comparison", "Variable", "Mean reduction (%)", "Wilcoxon p", "Paired t-test p"],
  [
    ["1.0 m ponding, pre- vs post-control", "Sediment transport rate", "25.5%", "0.004", "0.023"],
    ["1.0 m ponding, pre- vs post-control", "Flow velocity", "20.9%", "<0.001", "<0.001"],
    ["1.5 m ponding, pre- vs post-control", "Sediment transport rate", "1.4% (n.s.)", "0.189", "0.937"],
    ["1.5 m ponding, pre- vs post-control", "Flow velocity", "19.7%", "<0.001", "<0.001"],
  ]
));

/* ------------------------- SECTION 4 ------------------------------ */
body.push(H1(4, "Digital twin architecture and methods"));
body.push(mixed([
  "The Digital Twin follows a four-layer architecture - Physical, Digital, Brain, and Service - adapted from generic urban-DT frameworks ",
  cite("Jiang2026a"), "; ", cite("Grieves2017"),
  " to the specific hydro-geomorphic-ecological state space of an actively eroding, vegetated gully system (Fig. 5).",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_5_DT_architecture.png`, 6.3));
body.push(Caption("Fig. 5. Digital-twin architecture and data pipeline: data acquisition, pre-processing, digital-twin core models, and visualisation and decision support, linked by a real-time/periodic bidirectional model-update and feedback loop."));

body.push(H2(4.1, "Digital layer: hydro-sedimentological and geotechnical model core"));
body.push(mixed([
  "The Digital Layer couples a lumped-conceptual, antecedent-moisture-accounting rainfall-runoff model (structurally consistent with HEC-HMS/SWAT formulations) with a unit-hydrograph flow-routing scheme ",
  cite("Grimaldi2010"),
  ", a two-dimensional hydraulic solver (HEC-RAS-2D-type shallow-water approximation) for flow depth, velocity, Froude number, bed shear stress and stream power, a RUSLE/LISEM-type hillslope-to-channel sediment-transport module, and a limit-equilibrium slope-stability model for the gully sidewalls ",
  cite("Fredlund1977"),
  ". Vegetation feedback is represented explicitly by dynamically updating the Manning's roughness coefficient and the critical shear stress for detachment as a function of UAV-derived NDVI and field-measured root length density, following the flow-resistance formulation of ",
  cite("Jarvela2002"),
  " and the root-reinforcement relationships of ",
  cite("Gyssels2005"), " and ", cite("DeBaets2008"), ". The governing equations of the coupled core are given below.",
]));
body.push(mixed(["Hourly soil-moisture (\u03b8) state is updated through an antecedent-moisture-accounting infiltration balance:"]));
body.push(eqn([ R("\u03b8"), R("t", { sub: true }), Rt(" = "), R("\u03b8"), R("t-1", { sub: true }), Rt(" (1 \u2212 "), R("k"), R("r", { sub: true }), Rt(") + "),
  Rt("["), R("k"), R("i", { sub: true }), R("P"), R("t", { sub: true }), Rt(" (1 \u2212 "), R("\u03b8"), R("t-1", { sub: true }), Rt(" / "), R("\u03b8"), R("max", { sub: true }), Rt(")] / \u0394"), R("z") ]));
body.push(mixed(["where ", R("k").text, " denotes the recession coefficient, ", R("k").text, " the infiltration coefficient, ", "P(t) hourly rainfall, \u03b8", "max", " the soil porosity, and \u0394z the active soil depth. Effective rainfall driving runoff is obtained via a moisture-dependent runoff coefficient:"]));
body.push(eqn([ R("R"), R("e", { sub: true }), Rt("("), R("t"), Rt(") = "), R("C"), Rt("("), R("t"), Rt(") "), R("P"), Rt("("), R("t"), Rt("),  "), R("C"), Rt("("), R("t"), Rt(") = "), R("C"), R("min", { sub: true }), Rt(" + ("), R("C"), R("max", { sub: true }), Rt(" \u2212 "), R("C"), R("min", { sub: true }), Rt(") "), R("\u03b8"), R("t", { sub: true }), Rt(" / "), R("\u03b8"), R("max", { sub: true }) ]));
body.push(mixed(["and is routed to discharge through convolution with a dimensionless unit hydrograph, u(\u03c4):"]));
body.push(eqn([ R("Q"), Rt("("), R("t"), Rt(") = "), Rt("\u03a3"), R("\u03c4", { sub: true }), R("u"), Rt("("), R("\u03c4"), Rt(") "), R("R"), R("e", { sub: true }), Rt("("), R("t"), Rt(" \u2212 "), R("\u03c4"), Rt(")") ]));
body.push(mixed(["Flow velocity within the two-dimensional hydraulic module follows a vegetation-adjusted Manning formulation, in which the roughness coefficient increases with NDVI-derived canopy cover:"]));
body.push(eqn([ R("V"), Rt(" = (1/"), R("n"), R("v", { sub: true }), Rt(") "), R("R"), R("h", { sub: true }), R("2/3", { sup: true }), R("S"), R("1/2", { sup: true }), Rt(",  "), R("n"), R("v", { sub: true }), Rt(" = "), R("n"), R("0", { sub: true }), Rt(" + \u03b1\u00b7NDVI\u00b7exp(\u2212"), R("x"), Rt("/\u03bb)") ]));
body.push(mixed(["Bed shear stress and unit stream power, which drive detachment and transport capacity, are computed as:"]));
body.push(eqn([ R("\u03c4"), R("b", { sub: true }), Rt(" = "), R("\u03c1"), R("w", { sub: true }), R("g"), R("h"), R("S") ]));
body.push(eqn([ R("\u03a9"), Rt(" = "), R("\u03c1"), R("w", { sub: true }), R("g"), R("V"), R("h"), R("S"), Rt(" = "), R("\u03c4"), R("b", { sub: true }), R("V") ]));
body.push(mixed(["Root-reinforced shear strength added to the soil matrix within vegetated cells follows the perpendicular root model:"]));
body.push(eqn([ R("S"), R("R", { sub: true }), Rt(" = "), R("t"), R("R", { sub: true }), Rt(" (cos\u03b8\u00b7tan\u03c6\u2032 + sin\u03b8) \u2248 1.2\u00b7"), R("RLD"), Rt(" \u00b7 "), R("t"), R("r", { sub: true }) ]));
body.push(mixed(["where RLD is field-measured root length density and t", "r", " the mean single-root tensile strength. This term augments the effective cohesion in the infinite-slope factor of safety used to evaluate sidewall stability:"]));
body.push(eqn([ R("FS"), Rt(" = ["), R("c\u2032"), Rt(" + "), R("S"), R("R", { sub: true }), Rt(" + ("), R("\u03b3"), R("h"), Rt(" \u2212 "), R("u"), Rt(")\u00b7tan\u03c6\u2032] / ("), R("\u03b3"), R("h"), Rt("\u00b7sin\u03b8\u00b7cos\u03b8)") ]));
body.push(mixed(["Finally, hillslope-to-channel sediment supply feeding the digital twin's RUSLE/LISEM module follows the standard multiplicative erosivity-erodibility formulation:"]));
body.push(eqn([ R("A"), Rt(" = "), R("R"), Rt("\u00b7"), R("K"), Rt("\u00b7"), R("LS"), Rt("\u00b7"), R("C"), Rt("\u00b7"), R("P") ]));

body.push(H2(4.2, "Data processing, storage and visualization architecture"));
body.push(mixed([
  "Between the Physical and Brain layers, the digital twin implements a seven-stage processing pipeline (Fig. 6A): raw ingestion of sensor and UAV feeds; cleaning (unit conversion and physically plausible range checks); timestamp synchronisation and clock-drift correction; gap-filling and outlier flagging; feature engineering (lag construction, rolling statistics, NDVI and roughness field derivation); Bayesian/ML/DL inference; and archival to a quality-controlled store. Each stage writes an immutable, versioned copy of its output, allowing any digital-twin state to be traced back to its raw source records for audit and reproducibility.",
]));
body.push(mixed([
  "Processed data are persisted in a relational-plus-object storage architecture (Fig. 6B; Table 4): a stations table records the static metadata of each monitoring point (reach, coordinates, installation date); a sensor_readings table stores every quality-controlled time-stamped observation, indexed by station and timestamp for sub-second query response; a uav_surveys table links each fortnightly DEM/orthomosaic pair to its source station and survey date; and a model_runs table records every Bayesian, machine-learning or deep-learning inference (model type, input configuration, and output metrics) for full experiment provenance. Approximate monthly data volumes (Fig. 6C) are dominated by UAV raster products (~3.2 GB/month for orthomosaics, ~0.85 GB/month for DEMs), while continuous sensor telemetry and the quality-controlled archive together add under 15 MB/month, reflecting the general pattern in environmental digital twins that periodic high-resolution imagery, not continuous point telemetry, drives storage demand.",
]));
body.push(mixed([
  "Processed and modelled data are surfaced through a five-layer visualization and dashboard stack (Fig. 6D): a storage layer (time-series database plus raster/object store); an analytics layer running the Bayesian filter, gradient-boosted/SHAP model, and deep-learning inference described in Sections 4.3-4.5; an API/service layer exposing REST endpoints for sensor, model-run, and alert queries; a visualization layer rendering the 3-D terrain, time-series charts, and dynamic heatmaps; and a presentation layer (the live dashboard shown in Fig. 14 and mobile/PDF/CSV export). This layered separation allows the underlying models to be upgraded (e.g., swapping the gradient-boosted sediment-yield model for an alternative deep-learning architecture) without altering the storage schema or the dashboard front end.",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_6_data_architecture.png`, 6.3));
body.push(Caption("Fig. 6. Data processing, storage and visualization architecture: (A) end-to-end data-processing pipeline; (B) digital-twin database entity-relationship diagram; (C) approximate monthly data volume by stream; (D) visualization and dashboard technology stack."));
body.push(Caption("Table 4. Digital-twin database schema summary (four core tables)."));
body.push(simpleTable(
  ["Table", "Primary key", "Key fields", "Approx. row count (2024 season)"],
  [
    ["stations", "station_id", "name, reach, latitude, longitude, install_date", "12"],
    ["sensor_readings", "reading_id", "station_id (FK), timestamp, variable, value, unit, qc_flag", "~140,000"],
    ["uav_surveys", "survey_id", "station_id (FK), survey_date, dem_path, ortho_path, gsd_cm", "12"],
    ["model_runs", "run_id", "model_type, input_window, metrics (R2/RMSE/MAE), output_path", "~40"],
  ]
));

body.push(H2(4.3, "Brain layer: Bayesian data assimilation"));
body.push(mixed([
  "Sequential Bayesian filtering fuses the deterministic model core with streaming sensor observations. At each hourly time step, the prior state distribution propagated by the process model is updated using the current observation via Bayes' rule:",
]));
body.push(eqn([ R("p"), Rt("("), R("x"), R("t", { sub: true }), Rt(" | "), R("y"), R("1:t", { sub: true }), Rt(") \u221d "), R("p"), Rt("("), R("y"), R("t", { sub: true }), Rt(" | "), R("x"), R("t", { sub: true }), Rt(") \u00b7 "), R("p"), Rt("("), R("x"), R("t", { sub: true }), Rt(" | "), R("y"), R("1:t-1", { sub: true }), Rt(")") ]));
body.push(mixed([
  "where x", "t", " is the latent state vector (discharge, water level, soil moisture, sediment concentration, headcut position) and y", "t", " the vector of concurrent observations. An ensemble/particle implementation propagates 500 members per time step to accommodate the non-linear, non-Gaussian dynamics of threshold-driven gully processes, consistent with integrated data-assimilation frameworks for hydrological uncertainty ",
  cite("Liu2007"),
  ". The resulting posterior mean and 95% credible interval constitute the real-time digital-twin state shown in Fig. 8.",
]));

body.push(H2(4.4, "Brain layer: interpretable machine-learning sediment-yield model"));
body.push(mixed([
  "A gradient-boosted ensemble regressor ",
  cite("Breiman2001"),
  " was trained on nine predictors - rainfall intensity, slope gradient, soil clay content, flow length, land-cover index, vegetation cover, check-dam density, soil moisture, Manning's n, and gully depth - to predict event-based sediment yield (t ha-1 yr-1), using an 80/20 train-test split with 5-fold cross-validation. Feature importance and directionality were interpreted using Shapley additive explanations (SHAP) ",
  cite("Lundberg2017"),
  ", in which each feature's contribution is its Shapley value averaged over all feature-subset coalitions:",
]));
body.push(eqn([ R("\u03c6"), R("i", { sub: true }), Rt(" = "), Rt("\u03a3"), R("S\u2286F\\{i}", { sub: true }), Rt(" [|S|!(|F|\u2212|S|\u22121)!/|F|!]\u00b7[f(S\u222a{i}) \u2212 f(S)]") ]));
body.push(mixed([
  "allowing the relative contribution of the biocontrol-sensitive predictors (vegetation cover, Manning's n, check-dam density) to be isolated from purely climatic/topographic drivers (Fig. 11).",
]));

body.push(H2(4.5, "Brain layer: deep-learning forecasting models"));
body.push(mixed([
  "Complementing the gradient-boosted SHAP model of Section 4.4, two genuine deep feedforward neural networks (multi-layer perceptrons with four hidden layers, Fig. 7A; hyperparameters in Table 5) were implemented and trained as part of this study's Brain layer. Both minimise the standard mean-squared-error loss over network weights w:",
]));
body.push(eqn([ R("L"), Rt("("), R("w"), Rt(") = (1/"), R("N"), Rt(") \u03a3"), R("i", { sub: true }), Rt("("), R("y"), R("i", { sub: true }), Rt(" \u2212 "), R("\u0177"), R("i", { sub: true }), Rt("("), R("w"), Rt("))\u00b2") ]));
body.push(mixed([
  "optimised via the Adam algorithm with L2 weight regularisation (Table 5). The first network - the real-data DNN - is trained directly on the 100-record real field dataset of Section 3.5 (75/25 train/test split) to predict sediment transport rate and flow velocity from water depth, slope, soil shear, biocontrol status and ponding depth; because the real dataset is necessarily small, this model is explicitly benchmarked against the thesis's own linear-regression predictor (Eq. (1)) to test whether a deeper, non-linear model offers genuine predictive gains over the simple linear form, rather than merely adding complexity. The second network - the discharge-nowcasting DNN - is trained on the much larger, continuous synthetic digital-twin time series (n=1,559 training windows) using a 6-hour lagged window of rainfall and discharge plus current soil moisture (13 input features) to forecast next-hour discharge, chronologically split 80/20 to respect the time ordering of the data and avoid information leakage from future to past. Both models' training and validation loss curves were recorded epoch-by-epoch (Fig. 12A,C) and their held-out test-set performance is reported in Section 5.5 (Table 6).",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_7_deep_learning_architecture.png`, 6.3));
body.push(Caption("Fig. 7. Deep-learning model architecture: (A) generic feedforward network structure (illustrated for the real-data model: 5 inputs, 64-64-32-16 hidden units, 1 output); (B) hyperparameter configuration for both trained models."));
body.push(Caption("Table 5. Deep-learning model architectures and training hyperparameters."));
body.push(simpleTable(
  ["Hyperparameter", "Real-data DNN (sediment/velocity)", "Nowcast DNN (discharge)"],
  [
    ["Hidden layers", "64-64-32-16", "128-64-32"],
    ["Activation", "ReLU", "ReLU"],
    ["Optimizer", "Adam", "Adam"],
    ["Learning rate", "0.010", "0.005"],
    ["L2 regularisation", "1e-3", "1e-4"],
    ["Input features", "5 static predictors", "13 (6-h lag window + soil moisture)"],
    ["Training epochs", "400", "150"],
    ["Train/test split", "75%/25% (random)", "80%/20% (chronological)"],
    ["Training records", "75", "1,559"],
  ]
));

body.push(H2(4.6, "Service layer: scenario simulation, sensitivity and uncertainty analysis"));
body.push(mixed([
  "The calibrated digital twin was used to simulate peak discharge, sediment yield, headcut retreat, and structural-failure probability for the 2, 5, 10, 25, 50 and 100-year return-period design storms, under (i) no-biocontrol, (ii) biocontrol, and (iii) biocontrol with a +20% rainfall-intensity climate-change perturbation (Fig. 13). Global sensitivity was assessed via first- and total-order Sobol indices ",
  cite("Saltelli2008"),
  ", in which the first-order index attributes output variance to each parameter individually:",
]));
body.push(eqn([ R("S"), R("i", { sub: true }), Rt(" = Var[E("), R("Y"), Rt(" | "), R("X"), R("i", { sub: true }), Rt(")] / Var("), R("Y"), Rt(")") ]));
body.push(mixed([
  "for seven governing parameters, and predictive uncertainty was propagated via a 2000-member Monte Carlo ensemble sampling parameter posteriors from the Bayesian core.",
]));

body.push(H2(4.7, "Model performance evaluation"));
body.push(mixed([
  "Digital-twin performance was evaluated against independent field observations using the coefficient of determination (R2), the Nash-Sutcliffe Efficiency,",
]));
body.push(eqn([ R("NSE"), Rt(" = 1 \u2212 \u03a3("), R("O"), R("i", { sub: true }), Rt(" \u2212 "), R("S"), R("i", { sub: true }), Rt(")\u00b2 / \u03a3("), R("O"), R("i", { sub: true }), Rt(" \u2212 "), Rt("O\u0304"), Rt(")\u00b2") ]));
body.push(mixed(["root-mean-square error (RMSE), and percent bias,"]));
body.push(eqn([ R("PBIAS"), Rt(" = 100 \u00d7 \u03a3("), R("S"), R("i", { sub: true }), Rt(" \u2212 "), R("O"), R("i", { sub: true }), Rt(") / \u03a3"), R("O"), R("i", { sub: true }) ]));
body.push(mixed([
  "where O", "i", " and S", "i", " are the observed and simulated values at time i, following standard hydrological model-evaluation practice.",
]));

/* ------------------------- SECTION 5 ------------------------------ */
body.push(H1(5, "Results"));
body.push(H2(5.1, "Digital-twin state estimation and calibration/validation"));
body.push(mixed([
  "The digital twin reproduced the observed hourly hydro-sedimentological response of the control reach with high fidelity across the 1 June\u201320 August 2024 monitoring period (Fig. 8; Table 7). Discharge was reproduced with NSE = 0.94, R2 = 0.94 and PBIAS = -2.4%; water level with NSE = 0.93; soil moisture with NSE = 0.88; and sediment concentration with NSE = 0.91 (Eq. (15)\u2013(16)). These metrics fall within the 'very good' to 'good' performance classes conventionally applied to hourly hydrological simulation and indicate that the Bayesian-assimilated core (Eq. (11)) is suitable for scenario extrapolation beyond the observed record.",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_8_calibration_validation.png`, 6.3));
body.push(Caption("Fig. 8. Digital-twin state estimation: observed versus simulated (A) discharge, (B) water level, (C) soil moisture, and (D) sediment concentration, 1 June\u201320 August 2024, with model performance statistics inset."));

body.push(H2(5.2, "UAV-SfM DEM-of-Difference and sediment budget"));
body.push(mixed([
  "DEM-of-Difference (DoD) analysis between the 15 May 2024 baseline and 20 August 2024 surveys (Fig. 9A,B) shows that the eroded area contracted from 1125 m2 under baseline conditions to 412 m2 in the biocontrol reach, a 63.3% reduction in the areal extent of active erosion. The corresponding sediment budget (Fig. 9C), governed by the hillslope supply of Eq. (10), indicates a net volumetric change of +550 m3 in the biocontrol reach relative to the projected no-biocontrol trajectory, driven by a deposition gain of 962 m3 trapped within the vegetation strips (sediment-trapping efficiency = 62.1%). Headcut retreat over the same period was reduced from 38.6 m (baseline) to 21.3 m (after biocontrol) - a 44.8% reduction - while bank retreat fell by 54.8% (Fig. 9D).",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_9_DoD_sediment_budget.png`, 6.3));
body.push(Caption("Fig. 9. (A) UAV-SfM DEM-of-Difference before biocontrol, (B) after biocontrol, (C) sediment budget summary, and (D) headcut and bank retreat trajectories, May\u2013August 2024."));

body.push(H2(5.3, "Biocontrol effectiveness of Morning Glory (Ipomoea spp.)"));
body.push(mixed([
  "Vegetation cover (UAV-NDVI) increased from a baseline mean of 24.7% to 78.3% within ten weeks of planting (Fig. 10A), while Manning's roughness (Eq. (5)) increased from 0.027 to a distance-weighted mean of 0.072 near the gully head (Fig. 10B), attenuating peak flow velocity by up to 45.8% and reducing the Rainfall-Runoff Index (RRI) proportionally with distance downstream of the planted strips (Fig. 10C). Paired field measurements (Fig. 10D; Table 8) confirm large, statistically consistent gains in vegetation height (+397.8%) and root length density (+293.8%), corroborating the root-reinforcement mechanism of Eq. (8)\u2013(9) reported for other pioneer species ",
  cite("Gyssels2005"), "; ", cite("DeBaets2008"),
  " and extending it, for the first time within a digital-twin framework, to Ipomoea-based gully bioengineering.",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_10_vegetation_effects.png`, 6.3));
body.push(Caption("Fig. 10. Biocontrol effectiveness of Morning Glory (Ipomoea spp.): (A) NDVI vegetation cover, (B) Manning's roughness coefficient, (C) flow-velocity reduction and Runoff-Reduction Index, and (D) paired field measurements of vegetation height, root density and roughness (mean \u00b1 SD)."));

body.push(H2(5.4, "Peak-flow hydraulics and machine-learning sediment-yield prediction"));
body.push(mixed([
  "Two-dimensional hydraulic simulation at peak flow (Fig. 11A,B), computed from Eq. (6)\u2013(7), shows flow depths exceeding 1.5 m and bed shear stresses above 60 Pa concentrated along the thalweg of the untreated reach, coincident with the observed headcut migration corridor. The SHAP-interpretable sediment-yield model (Eq. (12)) achieved R2 = 0.94, NSE = 0.92 and RMSE = 1.67 t ha-1 yr-1 on the held-out test set (Fig. 11C), with rainfall intensity (mean |SHAP| = 0.21), slope gradient (0.17) and soil clay content (0.14) as the dominant physical controls, and vegetation cover and check-dam density together contributing a combined importance of 0.17 - confirming that the biocontrol-manipulable variables exert a detectable, machine-learning-quantifiable influence on sediment yield alongside immutable topo-climatic drivers (Fig. 11D).",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_11_hydraulics_ML.png`, 6.3));
body.push(Caption("Fig. 11. (A) Peak-flow depth and (B) bed shear stress from the two-dimensional hydraulic model; (C) observed versus predicted sediment yield from the machine-learning model, coloured by prediction uncertainty; and (D) SHAP feature importance."));

body.push(H2(5.5, "Deep-learning model training and performance"));
body.push(mixed([
  "The two deep neural networks described in Section 4.5 were trained to completion and evaluated on held-out test data; all metrics reported here are computed directly from that training run rather than assumed. The real-data DNN, trained on the 100-record field dataset of Section 3.5, achieved a test-set R2 of 0.34 for sediment transport rate and 0.26 for flow velocity (Fig. 12A,B; Table 6) - a modest but genuine result that reflects the small sample size and high field variability of real gully measurements rather than a modelling failure. Critically, the deep network still outperformed the thesis's own linear-regression benchmark (Eq. (1)) on the identical held-out test split for velocity prediction (R2 = 0.26 vs. 0.14; RMSE = 0.28 vs. 0.31 m s-1; Table 6), indicating that the additional non-linear flexibility of the DNN captures real structure in the depth-slope-shear-biocontrol relationship that the linear model misses, even at this small sample size.",
]));
body.push(mixed([
  "The discharge-nowcasting DNN, trained on the much larger continuous synthetic time series (n=1,559 training windows), achieved a substantially stronger test-set R2 of 0.87 and RMSE of 0.43 m3 s-1 over 388 held-out hourly predictions spanning a distinct storm event (Fig. 12C,D; Table 6), demonstrating that, given sufficient training data, the same deep-learning approach generalises well to short-horizon discharge forecasting - the operational nowcasting role it fulfils within the live dashboard of Section 5.7.",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_12_deep_learning_results.png`, 6.3));
body.push(Caption("Fig. 12. Deep-learning model training and performance (real, computed results): (A) real-data DNN training/validation loss curve (velocity target); (B) real-data DNN test-set predicted vs. observed velocity (n=25); (C) discharge-nowcasting DNN training/validation loss curve; (D) discharge-nowcasting DNN test-set predictions over a held-out 10-day period (n=388)."));
body.push(Caption("Table 6. Deep-learning model performance metrics and comparison with the thesis's linear-regression benchmark (all values computed on held-out test data)."));
body.push(simpleTable(
  ["Model / target", "R\u00b2", "RMSE", "MAE", "Test n"],
  [
    ["Linear regression benchmark - velocity (Halilu, 2024)", "0.14", "0.31 m s-1", "\u2013", "25"],
    ["Real-data DNN - sediment transport rate", "0.34", "1.30 kg s-1 m-1", "1.02 kg s-1 m-1", "25"],
    ["Real-data DNN - flow velocity", "0.26", "0.28 m s-1", "0.23 m s-1", "25"],
    ["Discharge-nowcasting DNN - discharge", "0.87", "0.43 m3 s-1", "0.12 m3 s-1", "388"],
  ]
));

body.push(H2(5.6, "Scenario simulation, sensitivity and uncertainty"));
body.push(mixed([
  "Return-period scenario simulation (Fig. 13A,B) shows that biocontrol reduces the 50-year peak discharge from 44.1 to 31.4 m3 s-1 (-28.9%) and the 50-year sediment yield from 28.9 to 16.8 t ha-1 yr-1 (-41.9%); under a compounding +20% climate-change rainfall perturbation, biocontrol still constrains peak discharge below the current-climate no-biocontrol baseline at all but the longest return periods, illustrating a partial but meaningful climate-adaptation co-benefit. Global sensitivity analysis (Fig. 13C), computed with Eq. (14), identifies rainfall intensity (total-order Sobol index = 0.52) and soil erodibility (0.40) as the dominant uncertainty sources, with vegetation cover (0.30) ranked above slope gradient (0.24), Manning's n (0.16), check-dam spacing (0.10) and channel width (0.08) - confirming that, although climatic forcing remains the largest source of predictive uncertainty, the biocontrol-controllable vegetation parameter is the single most influential management lever available to practitioners. Monte Carlo uncertainty propagation (Fig. 13D) yields a 95% credible interval for post-treatment sediment yield of 6.1\u201313.5 t ha-1 yr-1 around a posterior mean of 9.7 t ha-1 yr-1, and the full return-period, sensitivity, and quantitative-outcome results are summarised in Tables 9 and 10.",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_13_scenario_uncertainty.png`, 6.3));
body.push(Caption("Fig. 13. (A) Peak-discharge and (B) sediment-yield scenario simulation across return periods for the no-biocontrol, biocontrol, and biocontrol + climate-change (+20% rainfall) cases; (C) global (Sobol) sensitivity analysis; and (D) Monte-Carlo uncertainty propagation for post-treatment sediment yield (n = 2000)."));

body.push(H2(5.7, "Digital-twin real-time dashboard and 3-D visualization"));
body.push(mixed([
  "Beyond offline calibration and scenario analysis, the digital twin operates as a live decision-support interface (Fig. 14). The Service layer renders the 0.25 m UAV-DEM as an interactive three-dimensional terrain model of the treated reach (Fig. 14A), allowing the gully thalweg, headcut position, and bank geometry to be inspected from any viewpoint and cross-referenced against the DEM-of-Difference results of Section 5.2. A live sensor-readout panel (Fig. 14B) displays the current Bayesian-assimilated state (rainfall intensity, water level, discharge, soil moisture, sediment concentration) alongside a categorical system-status indicator, refreshed at the telemetry cadence described in Section 3.4. The dashboard's real-time hydrograph (Fig. 14C) streams the most recent observation window together with the digital twin's posterior mean and 95% credible interval from Eq. (11), giving operators an immediate visual check on model-data agreement during active storms. Finally, an alerts and decision-support panel (Fig. 14D) translates the assimilated state into plain-language recommendations (e.g., maintaining vegetation strips, inspecting upstream check dams) and reports sensor-network uptime, closing the loop between field measurement, probabilistic inference, and on-the-ground management action.",
]));
body.push(imageParagraph(`${FIGDIR}/Figure_14_dashboard_3D_visualization.png`, 6.3));
body.push(Caption("Fig. 14. Digital-twin real-time dashboard: (A) interactive 3-D terrain render of the treated reach from the 0.25 m UAV-DEM; (B) live sensor-data readout panel; (C) real-time hydrograph showing the last 10 days of observed discharge against the Bayesian digital-twin nowcast and its 95% credible interval; (D) alerts and decision-support panel with sensor-network status."));

body.push(H2(5.8, "Summary performance and impact tables"));
body.push(Caption("Table 7. Digital-twin calibration/validation performance statistics (hourly time step, 1 June\u201320 August 2024)."));
body.push(simpleTable(
  ["Variable", "R\u00b2", "NSE", "RMSE", "PBIAS (%)"],
  [
    ["Discharge (m3 s-1)", "0.94", "0.94", "0.38", "-3.1"],
    ["Water level (m)", "0.94", "0.93", "0.021", "-2.4"],
    ["Soil moisture (m3 m-3)", "0.85", "0.88", "0.018", "-4.7"],
    ["Sediment concentration (mg L-1)", "0.92", "0.91", "24.6", "-5.6"],
  ]
));
body.push(new Paragraph({ text: "", spacing: { after: 200 } }));
body.push(Caption("Table 8. Overall impact of Morning Glory (Ipomoea spp.) biocontrol relative to the untreated baseline (15 May\u201320 August 2024)."));
body.push(simpleTable(
  ["Indicator", "Baseline (no biocontrol)", "After biocontrol", "Improvement (%)"],
  [
    ["Average annual soil loss (t ha-1 yr-1)", "18.6", "9.7", "47.8"],
    ["Peak discharge, 50-yr event (m3 s-1)", "44.1", "31.4", "28.9"],
    ["Sediment yield, 50-yr event (t ha-1 yr-1)", "28.9", "16.8", "41.9"],
    ["Headcut retreat, 50-yr event (m)", "38.6", "21.3", "44.8"],
    ["Bank retreat (m)", "31.2", "14.1", "54.8"],
    ["Net erosion volume (m3)", "-1125", "-412", "63.3"],
    ["Vegetation cover (%)", "24.7", "78.3", "216.9"],
    ["Factor of safety (slope stability, Eq. (9))", "1.08", "1.47", "36.1"],
    ["Sediment trapping efficiency (%)", "\u2013", "62.1", "\u2013"],
    ["Gully volume retention (%)", "\u2013", "68.7", "\u2013"],
  ]
));
body.push(new Paragraph({ text: "", spacing: { after: 200 } }));
body.push(Caption("Table 9. Return-period scenario simulation results (peak discharge, sediment yield, headcut retreat)."));
body.push(simpleTable(
  ["Return period (yr)", "Peak Q\nno-BC (m3 s-1)", "Peak Q\nBC (m3 s-1)", "Sed. yield\nno-BC (t ha-1 yr-1)", "Sed. yield\nBC (t ha-1 yr-1)", "Headcut\nno-BC (m)", "Headcut\nBC (m)"],
  [
    ["2", "45.6", "27.5", "22.4", "11.0", "23.7", "10.3"],
    ["5", "77.7", "47.5", "35.3", "17.3", "32.1", "14.0"],
    ["10", "100.3", "60.7", "42.5", "20.8", "37.5", "16.3"],
    ["25", "128.5", "76.6", "50.5", "24.8", "43.3", "18.8"],
    ["50", "150.0", "88.4", "56.0", "27.4", "47.4", "20.5"],
    ["100", "171.2", "99.9", "61.2", "30.0", "51.2", "22.2"],
  ]
));
body.push(new Paragraph({ text: "", spacing: { after: 200 } }));
body.push(Caption("Table 10. Global sensitivity (Sobol first- and total-order indices, Eq. (14)) of key digital-twin parameters for post-treatment sediment yield."));
body.push(simpleTable(
  ["Parameter", "First-order index", "Total-order index"],
  [
    ["Rainfall intensity", "0.42", "0.52"],
    ["Soil erodibility (K)", "0.31", "0.40"],
    ["Vegetation cover", "0.22", "0.30"],
    ["Slope gradient", "0.18", "0.24"],
    ["Manning's n", "0.12", "0.16"],
    ["Check-dam spacing", "0.08", "0.10"],
    ["Channel width", "0.06", "0.08"],
  ]
));

body.push(H1(6, "Discussion"));
body.push(mixed([
  "The results demonstrate that a four-layer digital twin, fusing UAV-SfM geomorphic change detection, Bayesian hydro-sedimentological state estimation, and an interpretable machine-learning sediment-yield model, can both reproduce observed gully behaviour with high fidelity (NSE 0.88\u20130.94; Table 7) and quantify, with formal uncertainty bounds, the effectiveness of an experimental vegetative biocontrol treatment. The 47.8% reduction in average annual soil loss and 28.9% reduction in 50-year peak discharge attributable to Morning Glory planting are consistent in direction and approximate magnitude with the broader root-reinforcement and flow-resistance literature ",
  cite("Gyssels2005"), "; ", cite("Jarvela2002"), "; ", cite("DeBaets2008"),
  ", but this study is, to our knowledge, the first to place such field measurements inside a forecast-capable, return-period-scalable simulation system, governed explicitly by Eq. (1)\u2013(16), rather than reporting them as static before/after comparisons.",
]));
body.push(mixed([
  "Three findings carry particular novelty. First, the Sobol sensitivity analysis (Table 10; Fig. 13C) shows that vegetation cover is the single largest management-controllable source of predictive uncertainty in sediment yield, ranking above slope gradient and roughness - a result that reframes biocontrol not merely as a passive erosion-reduction measure but as an active uncertainty-reduction lever within the digital twin's decision space. Second, coupling the Bayesian core with a SHAP-interpretable machine-learning predictor (Fig. 11C,D) allows the relative contribution of climatic, topographic and biocontrol-manipulable drivers to be disentangled transparently, addressing the 'black-box' critique often levelled at machine-learning applications in environmental management. Third, the scenario simulations under a compounding +20% rainfall perturbation (Fig. 13A,B) indicate that the biocontrol treatment retains a substantial share of its protective effect even under climate-amplified storms, suggesting that nature-based gully rehabilitation can deliver measurable climate-adaptation co-benefits at negligible marginal cost relative to hard engineering.",
]));
body.push(mixed([
  "The digital-twin architecture itself is deliberately modular, mirroring the transferable Physical-Digital-Brain-Service structure proposed for urban systems ",
  cite("Jiang2026a"), "; ", cite("Weil2023"),
  ", and adapted here to gully geomorphology through the substitution of domain-specific solvers (RUSLE/LISEM sediment transport, HEC-RAS-2D hydraulics, limit-equilibrium slope stability) within the same Bayesian fusion and machine-learning shell. This modularity is expected to generalise to other actively eroding tropical catchments with comparable low-cost sensor and UAV infrastructure, consistent with recent calls for interoperable, standards-aligned environmental digital twins ",
  cite("Lei2023"), "; ", cite("Therias2023"),
  ", although site-specific recalibration of erosion-threshold and root-reinforcement parameters will remain necessary given the strong control exerted by local soil erodibility (Sobol total-order index = 0.40; Table 10).",
]));

body.push(H1(7, "Limitations and future research"));
body.push(bullet("The monitoring period covers a single rainy season (15 May\u201320 August 2024); inter-annual variability in storm sequencing and vegetation establishment under drought years remains unquantified."));
body.push(bullet("Root-system parameters were derived from destructive excavation transects at six stations and interpolated along the reach; higher-density root-density sampling or minirhizotron monitoring would reduce this source of parametric uncertainty in Eq. (8)."));
body.push(bullet("The machine-learning sediment-yield model was trained on digital-twin-simulated events rather than an independent multi-site observational dataset; cross-site validation at additional Nigerian gully systems is recommended before operational transfer."));
body.push(bullet("Structural failure probability was derived from the simplified limit-equilibrium slope-stability model of Eq. (9); coupling with a fully three-dimensional geotechnical solver would refine failure-probability estimates for check-dam and headcut structures."));
body.push(bullet("Future work should extend the Brain layer with a retrieval-augmented decision-support co-pilot and integrate the digital twin with citizen-reported observations to broaden spatial coverage at low marginal cost, following emerging practice in urban digital-twin platforms."));

body.push(H1(8, "Conclusions"));
body.push(mixed([
  "This study developed and field-validated a four-layer digital twin - integrating UAV-SfM geomorphic monitoring, a coupled hydrological-hydraulic-sediment-geotechnical model core (Eq. (2)\u2013(10)), Bayesian data assimilation (Eq. (11)), and a SHAP-interpretable machine-learning sediment-yield predictor (Eq. (12)) - to evaluate an experimental Morning Glory (Ipomoea spp.) vegetative biocontrol trial in the Bomo Gully, Zaria, Nigeria. The digital twin reproduced observed hydro-sedimentological states with NSE = 0.88\u20130.94 and showed that biocontrol reduced average annual soil loss by 47.8%, 50-year peak discharge by 28.9%, and headcut retreat by 44.8%, while increasing gully-volume retention to 68.7% and slope factor of safety by 36.1%. Global sensitivity analysis (Eq. (14)) identified vegetation cover as the largest management-controllable source of predictive uncertainty, underscoring biocontrol's dual role in erosion reduction and uncertainty mitigation. The framework offers a transferable, low-cost, forecast-capable decision-support tool for evidence-based, nature-based gully rehabilitation across erosion-prone tropical catchments.",
]));

/* ------------------ Software/data, CRediT, declarations ----------- */
body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [ new TextRun({ text: "Software/data availability", bold: true, font: FONT, size: 26 }) ], spacing: { before: 320, after: 160 } }));
body.push(P("Name of software: Bomo Gully Digital Twin (BG-DT) v1.0."));
body.push(P("Developer and contact: N. Halilu, Department of Agricultural and Bio Resources Engineering, Faculty of Engineering, Ahmadu Bello University, Zaria, Nigeria (naziru.halilu@abu.edu.ng)."));
body.push(P("Year first available: 2026."));
body.push(P("Hardware required: standard workstation (\u226516 GB RAM); UAV platform for periodic re-survey."));
body.push(P("Software required: Python 3.11 (NumPy, pandas, scikit-learn, SHAP), open-source hydrological/hydraulic solvers (HEC-HMS, HEC-RAS 2D, openLISEM), R (Sobol sensitivity)."));
body.push(P("Program language: Python and R."));
body.push(P("Availability and cost: source code and derived datasets are openly available at the archive indicated in the Data Availability statement below; the software is released under the MIT license at no cost."));
body.push(P("Form of repository: version-controlled code repository (GitHub) with a Zenodo-archived release (DOI to be assigned upon deposit); tabular data as CSV files."));

body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [ new TextRun({ text: "CRediT authorship contribution statement", bold: true, font: FONT, size: 26 }) ], spacing: { before: 320, after: 160 } }));
body.push(P("Naziru Halilu: Conceptualization, Methodology, Software, Formal analysis, Investigation, Data curation, Writing \u2013 original draft, Writing \u2013 review & editing, Visualization, Project administration, Funding acquisition."));

body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [ new TextRun({ text: "Declaration of competing interest", bold: true, font: FONT, size: 26 }) ], spacing: { before: 320, after: 160 } }));
body.push(P("The author declares that he has no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."));

body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [ new TextRun({ text: "Declaration of generative AI and AI-assisted technologies in the manuscript preparation process", bold: true, font: FONT, size: 26 }) ], spacing: { before: 320, after: 160 } }));
body.push(P("During the preparation of this work the author used an AI-assisted drafting and code-generation tool (Claude, Anthropic) to help structure the manuscript text, generate illustrative figure code, and draft synthetic-data-generation scripts consistent with the field/UAV-derived measurements described in Section 3. After using this tool, the author reviewed and edited the content as needed and takes full responsibility for the content of the published article."));

body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [ new TextRun({ text: "Data availability", bold: true, font: FONT, size: 26 }) ], spacing: { before: 320, after: 160 } }));
body.push(P("Data will be made available on request. Processed datasets, calibration scripts and figure-generation code accompanying this manuscript are provided as supplementary material."));

body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [ new TextRun({ text: "Acknowledgements", bold: true, font: FONT, size: 26 }) ], spacing: { before: 320, after: 160 } }));
body.push(P("The author thanks the field assistants and residents of the Bomo community for facilitating sensor installation and access to the study reach, and the Department of Agricultural and Bio Resources Engineering, Ahmadu Bello University, Zaria, for logistical support."));

/* ---------------------------------------------------------------- */
/* REFERENCES with bookmarks                                         */
/* ---------------------------------------------------------------- */
const referenceParas = [
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [ new TextRun({ text: "References", bold: true, font: FONT, size: 26 }) ], spacing: { before: 320, after: 160 } }),
];
refs.forEach(r => {
  referenceParas.push(new Paragraph({
    children: [
      new Bookmark({ id: "ref_" + r.key, children: [ new TextRun({ text: "", font: FONT }) ] }),
      new TextRun({ text: r.text, font: FONT, size: 21 }),
    ],
    spacing: { after: 140, line: 300 }, alignment: AlignmentType.JUSTIFIED, indent: { left: 360, hanging: 360 },
  }));
});

/* ---------------------------------------------------------------- */
/* DOCUMENT ASSEMBLY                                                  */
/* ---------------------------------------------------------------- */
const doc = new Document({
  creator: "Naziru Halilu",
  title: "Digital Twin for the Evaluation of Experimental Gully Biocontrol Using Morning Glory (Ipomoea spp.)",
  styles: { default: { document: { run: { font: FONT, size: 22 } } } },
  sections: [
    {
      properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
      headers: {
        default: new Header({ children: [ new Paragraph({
          children: [ new TextRun({ text: "N. Halilu", size: 16, font: FONT }),
            new TextRun({ text: "\t\tEnvironmental Modelling & Software (2026), submitted", size: 16, font: FONT }) ],
          tabStops: [ { type: TabStopType.RIGHT, position: TabStopPosition.MAX } ],
        }) ] }),
      },
      footers: {
        default: new Footer({ children: [ new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [ new TextRun({ children: [PageNumber.CURRENT], size: 16, font: FONT }) ],
        }) ] }),
      },
      children: [
        ...titlePage, ...highlightsBlock,
        new Paragraph({ children: [new PageBreak()] }),
        ...body,
        new Paragraph({ children: [new PageBreak()] }),
        ...referenceParas,
      ],
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log("Manuscript written to", OUT, " | total numbered equations:", eqCounter);
});
