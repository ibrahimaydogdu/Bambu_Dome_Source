# Open Items Register (OPEN_ITEMS.md)

This document tracks all placeholders, required empirical parameters (`[DATA NEEDED]`), citations requiring formal external verification (`[REF NEEDED]`), and sources requiring bibliographic check (`[REF CHECK]`) across the draft manuscript.

---

## 1. Data Placeholders (`[DATA NEEDED]`)

The following numerical values represent minor secondary or derived parameters that were not directly tabulated in the primary summary tables and must be extracted from raw run files prior to journal submission:

| Location | Tag | Description | Current Estimated Value |
|---|---|---|---|
| `03_results.md:3.2` | `[DATA NEEDED: max force in geodesic]` | Maximum axial force in `geodesic16` (joint DCR = 0.280) | $\approx 13.80\text{ kN}$ ($0.280 \times 49.3\text{ kN}$) |
| `03_results.md:3.2` | `[DATA NEEDED: max force in kiewitt]` | Maximum axial force in `kiewitt32` (joint DCR = 0.543) | $\approx 26.77\text{ kN}$ ($0.543 \times 49.3\text{ kN}$) |
| `03_results.md:3.2` | `[DATA NEEDED: absolute deflections]` | Maximum apex vertical deflections under SLS for `geodesic16` and `kiewitt32` | $\approx 16.0\text{ mm}$ and $\approx 16.5\text{ mm}$ ($u/u_{\text{lim}} = 0.060, 0.062$) |
| `03_results.md:3.3` | `[DATA NEEDED: absolute culm CO2]` | Absolute cradle-to-gate embodied carbon of culm mass across domes | Calculated from Table 7 shares and totals |
| `03_results.md:3.3` | `[DATA NEEDED: absolute steel CO2]` | Absolute cradle-to-gate embodied carbon of connection steel | Calculated from Table 7 shares and totals |
| `03_results.md:3.3` | `[DATA NEEDED: absolute mortar CO2]` | Absolute cradle-to-gate embodied carbon of cementitious grout | Calculated from Table 7 shares and totals |
| `03_results.md:3.5` | `[DATA NEEDED: component weights]` | Exact dead weight breakdown between connector steel and mortar in `ribbed40` | Member: 66.35 kN, Total: 277.22 kN, Grout $\approx 186.6\text{ kN}$ |
| `04_discussion.md:4.1` | `[DATA NEEDED: culm CO2 ribbed]` | Absolute CO$_2$e of raw culm in `ribbed40` | $2.029\text{ t CO}_2\text{e}$ ($17.892\% \times 11.341\text{ t}$) |
| `04_discussion.md:4.1` | `[DATA NEEDED: joint CO2 ribbed]` | Absolute CO$_2$e of joint hardware in `ribbed40` | $9.312\text{ t CO}_2\text{e}$ ($82.108\% \times 11.341\text{ t}$) |
| `04_discussion.md:4.2` | `[DATA NEEDED: grout weight ribbed]` | Absolute dead weight of mortar infill in `ribbed40` | $\approx 186.6\text{ kN}$ |
| `04_discussion.md:4.4` | `[DATA NEEDED: alternative bolt size]` | Alternative bolt diameter for short member detailing | e.g., $\varnothing 3/4"$ or custom sleeve |
| `05_conclusions.md:3` | `[DATA NEEDED: grout weight]` | Absolute dead weight of mortar infill in `ribbed40` | $\approx 186.6\text{ kN}$ |

---

## 2. Unverified References (`[REF NEEDED]`)

The following citations are referenced for historical or comparative context but do not possess primary PDF verifications in `Papers/`. Full bibliographic details and DOIs must be verified before submission:

| Tag | Intended Source | Context / Section |
|---|---|---|
| `[REF NEEDED: Zhao et al. 2022]` | Zhao, S., Zhang, T., Ma, S., Chen, M. (2022). *Eng. Appl. Artif. Intell.*, 114, 105075. | Dandelion Optimizer algorithm formulation |
| `[REF NEEDED: Karaboga 2005]` | Karaboga, D. (2005). Technical Report TR06, Erciyes University. | Artificial Bee Colony algorithm formulation |
| `[REF NEEDED: Dorigo et al. 1996]` | Dorigo, M. et al. (1996). *IEEE Trans. Syst. Man Cybern. B*, 26(1), 29–41. | Ant Colony Optimization formulation |
| `[REF NEEDED: Saka 1991]` | Saka, M. P. (1991). Discrete sizing of pin-jointed structures. | Ribbed 40-m dome geometry origin |
| `[REF NEEDED: Hasançebi et al. 2009]` | Hasançebi, O. et al. (2009). *Comput. Struct.*, 87(5–6), 284–302. | 354-member benchmark steel dome |
| `[REF NEEDED: AISC ASD-89]` | AISC (1989). Specification for Structural Steel Buildings. | 37 steel pipe catalog design standard |
| `[REF NEEDED: INBAR TR35]` | INBAR (2014). Technical Report No. 35. | Lower-bound harvesting carbon value ($0.0324\text{ kg/kg}$) |
| `[REF NEEDED: Jawa Tengah HSD 2024]` | Pemerintah Provinsi Jawa Tengah (2024). HSD schedule. | Indonesian regional cost data |
| `[REF NEEDED: CPWD DSR 2023]` | CPWD (2023). Delhi Schedule of Rates. | Indian regional cost data |
| `[REF NEEDED: Turkiye CSB 2026]` | T.C. Çevre, Şehircilik ve İklim Değişikliği Bakanlığı (2026). | Turkish regional cost data |
| `[REF NEEDED: Colombia Guadua 2026]` | Comercializadora de Guadua y Bambú Colombia (2026). Web catalogue. | Colombian Guadua 6 m pricing |

---

## 3. Bibliographic Checks (`[REF CHECK]`)

| Tag | Source | Issue / Verification Required |
|---|---|---|
| `[REF CHECK: ICE Database V5.0]` | Circular Ecology, *Embodied Carbon – The Inventory of Carbon and Energy*, Educational V5.0 (June 2026). | Author order is not specified in the "Please Read First" introductory sheet; verify whether institutional author "Circular Ecology" or primary contributors (Jones & Hammond) should be cited. |
