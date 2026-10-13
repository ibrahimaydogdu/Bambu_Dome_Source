# Open items

## Decisions for the authors

1. **ICE Educational V5.0.** The "Please Read First" document of the database states that it may not be used "in research or any carbon calculations, other than for the purposes of teaching or learning the subject of embodied carbon". The emission factors for connection steel (2.38), steel tube (2.51) and grout (0.18 kg CO₂e/kg) come from this database. The base value of the culm factor EC_b (0.30) and its lower bound (0.09) also depend on it, through the ICE value for softwood without carbon storage (0.2626 kg CO₂e/kg) used as the upper production bound in `EC_BAMBOO_METHOD.md`. A source that permits research use has to be chosen, or permission obtained, before submission. Changing the factors changes all carbon results.
2. **Weight–carbon relation.** The project documents (AGENTS.md rule 1, README, MEMORY) state a near-linear relation with R² = 0.81–0.97. Recomputed from all feasible evaluations with the current emission factors, the values are R² = 0.804 (Geodesic), 0.524 (Kiewitt) and 0.734 (Ribbed) (`04_Results/WEIGHT_CARBON_TRADEOFF.md`). The manuscript reports the recomputed values. The statement that no trade-off exists should be reworded in the project documents.
3. **Title and span wording.** The three domes have spans of 16, 32 and 40 m. Earlier project documents described all three as 40 m domes.
4. **Price scenarios.** The draft shows all four scenarios with their derivation. Three of them derive bamboo prices from the Indonesian prices. The authors may present the Indonesian scenario as the main case and the others as sensitivity cases.
5. **Population sizes.** The campaign used population sizes of 20, 40 and 40 for ABC, ACO and DO. The tuning study found other best sizes for some pairs of algorithm and dome. The basis of the campaign values has to be stated.

## Data needed from the authors

- Verbal definition of the design groups of Ribbed and Kiewitt (Section 2.1).
- Basis for the 24 (D, t) pairs of the catalogue (Section 2.2).
- Source of the load values and of the 354-member reference dome (Section 2.3, 2.1).
- Record of the IStructE joint calculation (3–5 kN per bolt) (Sections 2.5, 4.6).
- Parameter values of the dandelion optimizer (Section 2.6).
- Record of the check of the steel model against the literature (135–136 kN against 151.1–155.8 kN) (Section 3.6).
- Source file of the COP exchange rate (Section 2.9).
- Colombian Guadua price: diameter of the 6 m unit (38 500 COP), and the source of the Turkish bamboo price table mentioned in `MEMORY.md`.
- Archive of the raw campaign records (about 135 MB).

## Placeholders in the manuscript text (generated)

| File | Line | Placeholder |
|---|---|---|
| 00_title_abstract_highlights.md | 5 | [DECISION NEEDED: title. The domes have spans of 16, 32 and 40 m. The study excludes biogenic carbon and the stages after A3, so it cannot decide whether bamboo is "zero-carbon"; "large-span" and "decarbonization paradox" are the authors' choice of wording.] |
| 01_introduction.md | 3 | [REF NEEDED] |
| 01_introduction.md | 9 | [REF NEEDED: metaheuristic sizing optimization of steel domes; reference 354-member dome] |
| 02_methods.md | 15 | [REF NEEDED: source of the 354-member reference dome] |
| 02_methods.md | 19 | [DATA NEEDED: verbal description of the Ribbed and Kiewitt group definition] |
| 02_methods.md | 38 | [REF CHECK: Manual limit b₀ ≤ 0.02] |
| 02_methods.md | 46 | [DATA NEEDED: basis for the choice of the 24 (D, t) pairs] |
| 02_methods.md | 50 | [REF NEEDED: source of the dead, snow and wind values] |
| 02_methods.md | 65 | [REF NEEDED: benchmark] |
| 02_methods.md | 67 | [REF CHECK: ASCE 7-22 section number] |
| 02_methods.md | 100 | [DATA NEEDED: record of the IStructE joint calculation] |
| 02_methods.md | 116 | [REF NEEDED: original references of ABC, ACO and DO] |
| 02_methods.md | 116 | [DATA NEEDED: DO parameter values] |
| 02_methods.md | 124 | [REF NEEDED: Friedman, Mann–Whitney, Holm] |
| 02_methods.md | 124 | [REF NEEDED: Vargha and Delaney] |
| 02_methods.md | 132 | [REF NEEDED] |
| 02_methods.md | 136 | [LICENSE CHECK for the ICE term] |
| 02_methods.md | 137 | [LICENSE CHECK] |
| 02_methods.md | 138 | [LICENSE CHECK] |
| 02_methods.md | 139 | [LICENSE CHECK] |
| 02_methods.md | 141 | [LICENSE CHECK: the terms of use of ICE Educational V5.0 exclude research use; the source of the steel and grout factors has to be confirmed before submission.] |
| 02_methods.md | 156 | [DATA CHECK: visual verification against the pages is not recorded] |
| 02_methods.md | 156 | [DATA CHECK: source files of the rates] |
| 02_methods.md | 162 | [REF NEEDED: AISC ASD 1989] |
| 03_results.md | 142 | [DATA NEEDED: calculation record of the 135–136 kN check; REF NEEDED: literature values] |
| 04_discussion.md | 7 | [DATA NEEDED: basis for the population sizes used in the campaign] |
| 04_discussion.md | 35 | [DATA NEEDED: IStructE joint calculation record] |
| 04_discussion.md | 43 | [LICENSE CHECK] |
| 07_references.md | 3 | [REF NEEDED] |
| 07_references.md | 3 | [REF CHECK] |
| 07_references.md | 21 | [REF CHECK: year and publisher details] |
| 07_references.md | 25 | [REF CHECK: full title and publisher] |
| 07_references.md | 26 | [REF CHECK: title and publisher] |
| 07_references.md | 27 | [REF CHECK: authors; LICENSE CHECK: terms of use exclude research use] |
| 07_references.md | 28 | [REF NEEDED: full citation] |
| 07_references.md | 29 | [REF NEEDED] |
| 07_references.md | 30 | [REF NEEDED] |
| 07_references.md | 31 | [REF NEEDED] |
| 07_references.md | 32 | [REF NEEDED] |
| 07_references.md | 33 | [REF CHECK: report number, authors, year; file `Evidence/MOSO-Bamboo-products-LCA-TP35.pdf`] |

Count: 40
