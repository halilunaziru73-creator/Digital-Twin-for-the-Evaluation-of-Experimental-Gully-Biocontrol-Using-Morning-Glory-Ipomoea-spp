# Photo-to-Plate Verification Method

Figure 2 (panels E-F) uses two real photographs from the source thesis
(`06_Data_Real_Field/Source_Thesis_Halilu_2024.docx`). Rather than guessing
which embedded image corresponds to which "Plate" caption, this was
determined **precisely** by parsing the document's underlying XML
structure directly:

1. Extracted `word/document.xml` from the .docx (a zip archive).
2. Parsed the document into its ordered sequence of paragraphs.
3. For each paragraph, recorded (a) any image relationship IDs
   (`r:embed="rIdNN"`) it contains, and (b) its text content.
4. Cross-referenced `word/_rels/document.xml.rels` to map each `rId` to
   its actual image filename (e.g. `rId56` → `media/image30.jpg`).
5. Walked the paragraph sequence to find, for every "Plate N ..." caption,
   the image embed that immediately precedes it in document order (this
   is how Word captions are structurally associated with their figures).

This produced an exact, verifiable mapping (not a guess based on color
statistics or visual similarity):

| Plate | Image file | Caption (verbatim from thesis) |
|-------|-----------|--------------------------------|
| I     | image12.jpg | Spot 1 along the Watercourse |
| II    | image13.jpg | Spot 2 along the Watercourse |
| III   | image14.jpg | Establishment of Current situation along Watercourse |
| IV    | image16.jpg | Planting of morning glory stems along the stream banks |
| V     | image17.jpg | Planting of morning glory at the upstream spot |
| VI    | image18.jpg | Planting of morning glory at downstream spots |
| VII   | image22.jpg | Established morning glory in the watercourse to control gully erosion |
| VIII  | image23.jpg | Established morning glory in the watercourse to control stream bank erosion |
| VIII* | image28.jpg | Gully spot along the watercourse before intervention (*the thesis reuses "Plate VIII" for a second, different photo — likely a numbering slip in the original document) |
| IX    | image29.jpg | Gully spot along the watercourse after intervention |
| **X** | **image30.jpg** | **Gully development before intervention of morning glory in the watercourse** |
| **XI** | **image31.jpg** | **Gully spot after intervention of morning glory** |

**Figure 2 panels E and F use Plate X and Plate XI** — the thesis's own
clearest, most explicit "before intervention" / "after intervention" pair
— copied to this package as:
- `05_Source_Images/plate_X_before_intervention.jpg`
- `05_Source_Images/plate_XI_after_intervention.jpg`

If you want to swap in a different pair of plates (e.g. VII/VIII showing
the established-vegetation stage instead of the gully-development stage),
the table above gives you the exact, verified filename for every plate in
the thesis, so you can make that substitution with full confidence in
what each image actually shows.
