# Open items

References that are missing are listed with search instructions in `REFERENCE_SEARCH_GUIDE.md` (placeholders `[REF-S#]`).

## Decisions taken by the authors (2026-10-13)

1. **Emission factors.** The factors for connection steel (2.38), steel tube (2.51) and grout (0.18 kg CO₂e/kg) come from ICE Database Educational V5.0, and so does the production upper bound of the culm factor EC_b (softwood without carbon storage, 0.2626 kg CO₂e/kg). The authors decided to use these values. The "Please Read First" document of the database states that it may not be used "in research or any carbon calculations, other than for the purposes of teaching or learning the subject of embodied carbon". This licence note is kept here for the submission stage; it is not a blocker for the draft.
2. **Title.** The working title was changed by the lead author's authority to a plain descriptive title.
3. **Price scenarios.** The Indonesian scenario is the main case; the Indian, Türkiye and Colombian scenarios are sensitivity cases.
4. **Population sizes.** The sizes used (20, 40, 40) are justified by their ratio to the number of design variables and by the memory size equal to the number of design variables in [Taymuş et al. 2025]. Further papers of the authors can be added if their PDFs are placed in `Papers/`.
5. **Manuscript structure (revision of 2026-10-13).** Domes, materials and loads are in a separate section "Numerical examples" (Section 3); Section 2 contains only the optimization formulation and evaluation methods. References use the numbered style, with the citation at the end of the sentence.

## Points where the requested wording was narrowed

- The requested statement that concrete comparative studies of bamboo against steel and concrete in cost and CO₂ are missing is stated for the **structure level** (each material sized to its own optimum, connections included). Material-level and building-level comparisons exist: bamboo culms against steel, concrete and timber [van der Lugt et al. 2006], and bamboo buildings against brick and concrete buildings [Zea Escamilla et al. 2018]. The gap statement carries the placeholder `[REF-S1]` until a literature search confirms it.

## Data needed from the authors

- Verbal definition of the design groups of Ribbed and Kiewitt (Section 3.1).
- Reason for the frequency-2 densification of the ribbed dome (Section 3.1).
- Basis for the 24 (D, t) pairs of the catalogue (Section 3.2).
- Record of the IStructE joint calculation (3–5 kN per bolt) (Sections 3.2, 5.5).
- Record of the check of the steel model against the literature (135–136 kN against 151.1–155.8 kN) (Section 4.5).
- Source files of the exchange rates and visual verification of the OCR-read prices (Section 3.5).
- Colombian Guadua price: diameter of the 6 m unit (38 500 COP), and the source of the Turkish bamboo price table mentioned in `MEMORY.md`.
- Archive of the raw campaign records (about 135 MB).

## Placeholders in the manuscript text (generated)

| File | Line | Placeholder |
|---|---|---|
| 01_introduction.md | 5 | [REF-S1] |
| 01_introduction.md | 7 | [REF-S2] |
| 01_introduction.md | 9 | [REF-S1] |
| 02_methods.md | 69 | [REF-S6] |
| 02_methods.md | 77 | [REF-S6] |
| 02_methods.md | 91 | [REF-S3] |
| 02_methods.md | 93 | [REF-S5] |
| 02_methods.md | 93 | [REF-S5] |
| 02_methods.md | 93 | [REF-S5] |
| 03_numerical_examples.md | 7 | [REF-S4] |
| 03_numerical_examples.md | 7 | [DATA NEEDED: reason for the frequency-2 densification] |
| 03_numerical_examples.md | 7 | [REF-S8] |
| 03_numerical_examples.md | 21 | [DATA NEEDED: verbal description of the Ribbed and Kiewitt group definition] |
| 03_numerical_examples.md | 23 | [REF-S9] |
| 03_numerical_examples.md | 48 | [DATA NEEDED: basis for the choice of the 24 (D, t) pairs] |
| 03_numerical_examples.md | 50 | [DATA NEEDED: record of the IStructE joint calculation] |
| 03_numerical_examples.md | 52 | [REF-S4] |
| 03_numerical_examples.md | 52 | [REF-S6] |
| 03_numerical_examples.md | 52 | [REF-S4] |
| 03_numerical_examples.md | 56 | [REF-S4] |
| 03_numerical_examples.md | 69 | [REF-S4] |
| 03_numerical_examples.md | 96 | [REF-S10] |
| 03_numerical_examples.md | 109 | [REF-S7] |
| 03_numerical_examples.md | 109 | [REF-S7] |
| 03_numerical_examples.md | 120 | [DATA CHECK: visual verification against the pages is not recorded] |
| 03_numerical_examples.md | 120 | [DATA CHECK: source files of the rates] |
| 04_results.md | 130 | [DATA NEEDED: calculation record of the 135–136 kN check; REF NEEDED: literature values] |
| 05_discussion.md | 29 | [DATA NEEDED: IStructE joint calculation record] |
| 08_references.md | 39 | [REF-S11] |
| 08_references.md | 41 | [REF-S12] |

Count: 30
