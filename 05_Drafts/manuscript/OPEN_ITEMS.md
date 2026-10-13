# Open items

Status of 2026-10-13 (after the revision that removed the ICE database). The manuscript text contains no placeholders at present; the points below must be settled before submission. Stage 5 has not been approved by the lead author.

## Decisions taken by the authors

1. **Emission factors.** ICE Database Educational V5.0 is no longer used (its terms exclude research use). Baseline factors are declared EPD values: connection steel 1.13 (bauforumstahl EPD), steel pipe 1.701 (Welded Tube of Canada EPD), grout 0.310 kg CO₂e/kg (SikaGrout-312 HP EPD); culm 0.243 kg CO₂e/kg (INBAR TR35 Table 1 plus 300 km road delivery). Sensitivity ranges: steel 0.5–2 times the plate value; grout 0.5–2 times (assumption); culm 0.0324–1.23.
2. **Title.** Plain descriptive title by the lead author's authority.
3. **Price scenarios.** The Indonesian scenario is the main case; the Indian, Türkiye and Colombian scenarios are sensitivity cases and are partly derived or proxy values (stated in Table 6).
4. **Population sizes.** 20, 40, 40, justified by the ratio to the number of design variables and by [Taymuş et al. 2025].
5. **Structure.** Section 2 formulation only; Section 3 numerical examples; numbered references with the citation at the end of the sentence.

## Points that need the author's attention

The verification of the references and of the steel model against the literature is carried out by the author and is not listed here.

- **Emission factor sources.** The plate EPD expired on 24.10.2023; the pipe EPD is a single Canadian producer; the freight factor 0.185 kg CO₂e/(t·km) is the authors' value within the DEFRA 2023 range 0.1782–0.2146; the upper bound 1.23 of the culm factor is derived from Zea Escamilla and Habert 2014 (Table 8) and not verified against the full source tables.
- **Literature gap statement (Section 1).** The statement that structure-level comparisons of bamboo with steel are limited has no search protocol behind it; a search (Scopus or Web of Science, see `REFERENCE_SEARCH_GUIDE.md`) is needed.
- **Prices.** The OCR-read Indonesian and Indian prices were not compared with the page images; the Colombian bamboo quotation and the proxy steel and grout prices are not verified.
- **Design groups, densification, catalogue basis.** Verbal definition of the groups of Ribbed and Kiewitt, the reason for the frequency-2 densification and the basis of the 24 (D, t) pairs are not documented.
- **Declarations.** The statement on the use of AI tools is checked by the author. The data availability statement points to `https://github.com/ibrahimaydogdu/BambuDome-reproducibility`, where all structured CSV datasets (Tables 8–9 stats, LCA sensitivity, tuning, and Figure 3 convergence series), FEA solver, optimization routines, and SAP2000 models are synchronized and published.
- **Stale columns.** `campaign_final/summary.csv` and `global_best*.json` contain carbon columns computed with factors different from the manuscript (the campaign configuration used 0.35, 2.1 and 0.18); they are not used in the manuscript.

## Placeholders in the manuscript text (generated)

| File | Line | Placeholder |
|---|---|---|

Count: 0
