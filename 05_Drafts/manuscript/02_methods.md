# 2. Methods

## 2.1 Dome models

Three dome models are analysed (Table 1). They differ in span, topology and member count. They are not scaled copies of one geometry.

| Dome | Code name | Span [m] | Rise [m] | Nodes | Members | Design groups | Supported nodes | Member length [m] | u_lim [mm] |
|---|---|---|---|---|---|---|---|---|---|
| Geodesic | geodesic16 | 16 (nominal) | 3.72 | 46 | 115 | 23 | 20 | 2.24-2.96 | 107 |
| Kiewitt | kiewitt32 | 32 | 6.60 | 169 | 456 | 22 | 48 | 2.09-3.55 | 213 |
| Ribbed | ribbed40 | 40 | 8.28 | 505 | 1464 | 43 | 48 | 0.76-3.08 | 267 |

**Table 1.** Dome models. The Geodesic dome has a nominal span of 16 m; twice the largest horizontal distance of a node from the vertical axis is 16.77 m. The rise is the height of the highest node above the lowest support. The displacement limit u_lim is the span divided by 150, rounded to 1 mm in the code.

- **Ribbed:** ribbed dome (called Schwedler type in the code). It is a frequency-2 densification of a 354-member reference steel dome with a 40 m span and a crown height of 8.28 m [REF NEEDED: source of the 354-member reference dome]. The reference dome has members up to 5.97 m long. The densified model has members of 0.76–3.08 m.
- **Kiewitt:** spherical cap with 8 sectors and 6 rings.
- **Geodesic:** icosahedral geodesic dome (class I, frequency 5) truncated at a colatitude of 50°. All nodes on the zigzag boundary are supported.

Members are assigned to design groups by geometric class. For Geodesic, a group contains members with the same length, the same latitude and the same position in the 72° sector; mirror images form separate groups. For Ribbed and Kiewitt, the classes are defined in the dome generators of the code (`truss_model.py`, `dome_types.py`) [DATA NEEDED: verbal description of the Ribbed and Kiewitt group definition].

Members are pin-jointed axial-force elements. Supported nodes are restrained in all three translations. Member forces and nodal displacements are computed with a direct stiffness solver written for this study. For the lightest design of each dome, the results were compared with SAP2000 (Section 3.1).

## 2.2 Material and section catalogue

Table 2 lists the material and design parameters.

| Quantity | Value | Basis |
|---|---|---|
| Density ρ | 700 kg/m³ | IStructE Manual Table 4.4; mean Guadua value 680 kg/m³ (Table A3.9) |
| Design modulus E_k | 10 GPa | Manual Table 4.4 gives 10 or 15 GPa (15 GPa for tropical bamboo with D/t ≥ 10, a mean value with 75% confidence). 10 GPa is used for all sections, a conservative choice |
| Tension strength f_t,0,k | 40 MPa | Manual Table 4.4, schematic. For Guadua, Table A3.9 gives only a mean tension strength (121 MPa, COV 0.18) and no characteristic value |
| Compression strength f_c,0,k | 37.8 MPa | Manual Table A3.4 (Guadua, n = 922) |
| Factor of safety FS | 2.0 | axial members (Manual Appendix A3.6) |
| Redundancy factor C_R | 0.90 | Manual: a single culm is non-redundant, C_R = 0.9. Applied to all members, which assumes single-culm members |
| Temperature factor C_T | 1.0 | service temperature below 38 °C (Manual) |
| Duration factor C_DF, Service Class 2 | 0.55 / 0.65 / 0.85 | permanent / transient / instantaneous loads; values from worked examples in the Manual (PDF pp. 153 and 163). The choice of Service Class 2 and the assignment of snow to transient and wind to instantaneous loads are assumptions |
| Ylinen constant c | 0.8 | Manual Annex A6.2 |
| Initial curvature b₀ | 0.01 | assumed [REF CHECK: Manual limit b₀ ≤ 0.02]; C_bow = 1 − b₀/0.02 = 0.5 |
| Effective length factor K | 1.0 | Manual Table 6.1 |
| Slenderness limit λ_max | 150 | NSR-10 G.12.9.2.6 and G.12.9.2.7 prescribe 150 for compression members; applied here to all members |
| Displacement limit u_lim | span/150 | example in the IStructE Manual |
| Joint capacity F_j,Rd | 49.3 kN | NSR-10 Tabla G.12.11-2 and G.12.11-3 (Section 2.5) |

**Table 2.** Material and design parameters. C_R, b₀, the Service Class and load-duration assignment, the choice E_k = 10 GPa and the use of λ_max for tension members are choices or assumptions of this study.

The catalogue has 24 hollow circular sections with outer diameter D = 80–160 mm and wall thickness t = 6–22 mm (Supplementary Table S1) [DATA NEEDED: basis for the choice of the 24 (D, t) pairs]. The culm weight is W = g ρ Σ A_i L_i, with g = 9.81 m/s².

## 2.3 Loads and load combinations

The load values are those of the 354-member reference dome [REF NEEDED: source of the dead, snow and wind values]. The same values, including the pressure coefficients of the 40 m reference dome, are used for all three domes. For Geodesic, S is the nominal span of 16 m.

- **Dead load D:** 0.20 kN/m² on the horizontal projection, downward.
- **Snow load S:** 0.83 kN/m² on the horizontal projection, downward.
- **Wind loads:** pressure normal to the surface, p = q_h G C_p − q_h GC_pi, with q_h = 1.115 kN/m², G = 0.85 and C_p = 0.0105, −0.907 and −0.5 in three zones along the wind direction x (x < −S/4, |x| ≤ S/4, x > S/4, where S is the span). The internal pressure term is GC_pi = −0.18 for pattern W_N and +0.18 for W_P. The resulting pressures are listed in Table 3.

| Pattern | Zone x < -S/4 | Zone -S/4 <= x <= S/4 | Zone x > S/4 |
|---|---|---|---|
| W_N | +0.211 | -0.659 | -0.273 |
| W_P | -0.191 | -1.060 | -0.675 |

**Table 3.** Wind pressures [kN/m²] computed from the constants above. Positive values act toward the surface.

Surface loads are distributed to the nodes by triangular faces, one third of each face to each of its nodes. For Ribbed and Kiewitt, the projected area is normalised so that the total equals the area of a circle of diameter S. This normalisation is not applied to Geodesic. The wind zone of a face is selected from the x-coordinate of its centroid.

The culm self-weight, the connection hardware and the grout are not applied as loads. The permanent load is the surface load D only. This follows the reference benchmark [REF NEEDED: benchmark].

Eight ASD combinations are evaluated without load factors (ASCE 7-22 Section 2.4.1) [REF CHECK: ASCE 7-22 section number]. The duration class of a combination is that of its shortest-duration load.

| No. | Combination | Duration class | C_DF | k = C_R C_DF C_T / FS |
|---|---|---|---|---|
| 1 | D | permanent | 0.55 | 0.2475 |
| 2 | D+S | transient | 0.65 | 0.2925 |
| 3 | D+0.6W_N | instantaneous | 0.85 | 0.3825 |
| 4 | D+0.6W_P | instantaneous | 0.85 | 0.3825 |
| 5 | D+0.75S+0.45W_N | instantaneous | 0.85 | 0.3825 |
| 6 | D+0.75S+0.45W_P | instantaneous | 0.85 | 0.3825 |
| 7 | 0.6D+0.6W_N | instantaneous | 0.85 | 0.3825 |
| 8 | 0.6D+0.6W_P | instantaneous | 0.85 | 0.3825 |

**Table 4.** Load combinations, duration classes and capacity factors k.

## 2.4 Design checks

For member i and combination j, let N_ij be the axial force (tension positive). The scaled force is Ñ_ij = N_ij / k_j with k_j = C_R C_DF,j C_T / FS (Table 4). Four demand-to-capacity ratios are computed per member from the envelope over the eight combinations:

- Tension: DC_t = max_j(Ñ_ij) / (A_i f_t,0,k), taken as zero if no combination gives tension.
- Compression: DC_c = max_j(−Ñ_ij) / (A_i f_cr,i), taken as zero if no combination gives compression. The Ylinen compressive strength is

$$f_{e} = \frac{\pi^{2} E_k C_{bow}}{(K L_i / r_i)^{2}}, \qquad f_{cr} = \frac{f_{c,0,k}+f_e}{2c} - \sqrt{\left(\frac{f_{c,0,k}+f_e}{2c}\right)^{2} - \frac{f_{c,0,k}\, f_e}{c}}$$

- Slenderness: DC_s = λ_i / 150 with λ_i = K L_i / r_i, for all members.
- Joint: DC_j = max_j |N_ij| / F_j,Rd, using the unscaled force.

The member ratio is DC_i = max(DC_t, DC_c, DC_s, DC_j). The serviceability measure is u_max, the largest absolute nodal displacement over all nodes, all three translation components and all eight combinations. The limit is u_lim = S/150 (Table 1).

## 2.5 Connection model

The joint capacity is F_j,Rd = n_bolt F_bolt,adm C_g = 4 × 13.25 kN × 0.93 = 49.3 kN. F_bolt,adm is the allowable load of one #5 (5/8 in) bolt in double shear, parallel to the fibre, for a culm diameter of 100 mm (NSR-10 Tabla G.12.11-2). C_g is the group factor for four bolts (Tabla G.12.11-3). The number of bolts n_bolt = 4 is a design decision of the authors. The same capacity is used for every member, independent of the section.

A calculation with the joint procedure of the IStructE Manual gave about 3–5 kN per bolt. The factor K of that procedure could not be verified, so the NSR-10 value is used [DATA NEEDED: record of the IStructE joint calculation].

The carbon model uses a fixed joint hardware definition: a steel hub of 2.0 kg per node, 0.5 kg of steel per member end (stud, nut and washer) and a grout infill at each member end (Section 2.8). These masses are assumptions. They do not depend on the member force and are not designed against F_j,Rd.

Section 3.3 reports the number of bolts that each member requires and the members that are too short to hold them under the NSR-10 spacing rules (bolt spacing of at least 150 mm; end distance of more than 150 mm for tension members and more than 100 mm for compression members). The required length of a member with n bolts at each end is L ≥ 2 (e + (n − 1) · 150 mm) + 150 mm, where e is the end distance: 150 mm for tension members and 100 mm for compression members (NSR-10 G.12.11.3.13). With e = 150 mm, three bolts require a member length of about 1.05 m, and four bolts at both ends about 1.35 m.

## 2.6 Optimization problem and algorithms

The design vector x contains one section index (1–24) per design group, so the number of variables N_g equals the number of groups (Table 1). The objective is the penalized weight

$$\min_{x}\; f_{pen}(x) = W(x)\,\bigl(1+P(x)\bigr)^{\varepsilon}, \qquad \varepsilon = 2,$$

$$P(x) = \sum_{g=1}^{N_g} \max\bigl(DC_g - 1,\,0\bigr) + \max\!\left(\frac{u_{max}}{u_{lim}} - 1,\,0\right), \qquad DC_g = \max_{i\in g} DC_i .$$

For a feasible design P = 0 and f_pen = W. Carbon is not part of the objective.

Three algorithms were used: the artificial bee colony (ABC), ant colony optimization (ACO) and the dandelion optimizer (DO; Zhao et al., 2022) [REF NEEDED: original ABC and ACO papers]. The application of these algorithms to steel structures is documented (Aydogdu and Saka, 2012; Aydogdu et al., 2016; Saka and Aydogdu, 2021; Taymuş et al., 2025). They were implemented for this study (`metaheuristic_optimizers.py`). The campaign used the default parameters of the implementation. For ABC, the abandonment limit is the population size times N_g. For ACO, α = 1, β = 0.5, the evaporation rate is 0.2 and the elite fraction is 0.2; its heuristic is 1/s for section index s, which favours small sections. DO has a rising stage, a descending stage and a landing stage with a Lévy-flight step (β = 1.5, scaled by 0.1); a new design replaces the current one only if it is better.

Each run stopped after NFE = 1000 N_g function evaluations: 43 000 (Ribbed), 22 000 (Kiewitt) and 23 000 (Geodesic). The population sizes were 20 for ABC and 40 for ACO and DO, that is, 0.5–1.8 times the number of design variables (N_g = 22–43). Taymuş et al. (2025) set the memory size of the algorithms they compared, including an enhanced dandelion optimizer, equal to the number of design variables. Each algorithm was run with 30 independent seeds (1001–1030) on each dome, giving 270 runs.

Algorithm selection used a separate tuning study with seeds 2001–2005 (three seeds for Ribbed), population sizes of 20, 40 and 80, and the candidates ABC, ACO, DO, GWO, WOA and TLBO. Each candidate was ranked at its own best population size by mean penalized weight (`TUNING_STUDY.md`). GWO, WOA and TLBO were not run on Ribbed, so the mean ranks are taken over the domes on which an algorithm was run. ABC and ACO had the lowest mean ranks (1.00 and 2.00); DO had 3.33, but GWO had a lower mean weight than DO on Geodesic. DO was included by study design, as one recent algorithm next to two older ones (ABC, ACO); it is not shown to be among the three best candidates. The campaign used population sizes of 20, 40 and 40, whereas the tuning table lists the best sizes [20, 20, 40] (ABC), [80, 20, 80] (ACO) and [40, 80, 40] (DO) for Geodesic, Kiewitt and Ribbed.

## 2.7 Statistical comparison

For each dome, the best weights of the 30 seeds were compared with a seed-blocked Friedman test over the three algorithms. ABC, which had the lowest Friedman mean rank on every dome, was compared with ACO and with DO by two-sided Mann–Whitney U tests with Holm correction over the two comparisons of a dome, at a significance level of 0.05 [REF NEEDED: Friedman, Mann–Whitney, Holm]. ACO and DO were not compared with each other. The effect size A12 is the probability that a run of the competing algorithm gives a heavier design than a run of ABC, with ties counted as 0.5 [REF NEEDED: Vargha and Delaney].

## 2.8 Embodied carbon

Embodied carbon covers the stages A1–A3. Biogenic carbon storage, use, demolition and recycling are not included. It is computed after the optimization for the lightest design of each dome:

$$E = EC_b\, m_b + EC_s\, m_s + EC_m\, m_m .$$

The culm mass is m_b = ρ Σ A_i L_i. The connection steel mass is m_s = 2.0 N_n + 0.5 · 2 N_m, with N_n nodes and N_m members. The grout mass is m_m = Σ_i 2 ρ_m (π/4)(D_i − 2 t_i)² (2.5 D_i), with ρ_m = 2100 kg/m³ (assumed density of non-shrink grout [REF NEEDED]), that is, a grout column of length 2.5 D_i in the bore at each end of member i. The factor 2.5 and the hardware masses are assumptions.

| Factor | Value [kg CO₂e/kg] | Basis |
|---|---|---|
| Bamboo culm EC_b | 0.30 (range 0.09–1.23) | derived in `EC_BAMBOO_METHOD.md`: production 0.092 plus 300 km road transport 0.21. The production lower bound uses data for laminated bamboo panels and is an assumption. The production term uses the ICE value for softwood without carbon storage (0.2626) as its upper bound. The upper value 1.23 is derived from Zea Escamilla and Habert (2014) and is an import-to-Europe scenario that does not suit local use |
| Connection steel EC_s | 2.38 | ICE Educational V5.0 "Steel, Plate" |
| Grout EC_m | 0.18 | ICE Educational V5.0 mortar 1:3, used as a proxy for non-shrink grout |
| Steel tube (steel reference only) | 2.51 | ICE Educational V5.0 "Steel, welded pipe" |

**Table 5.** Emission factors.

The sensitivity of the joint share (steel plus grout) was evaluated for the lightest designs by changing one parameter at a time: L_inj/D from 1.5 to 3.5, EC_s from 1.2 to 3.0 kg CO₂e/kg and EC_b from 0.09 to 1.23 kg CO₂e/kg. A combined case applies L_inj/D = 1.5, EC_s = 1.2, EC_b = 0.47 and EC_m = 0.12 together.

## 2.9 Material cost

Only material cost is considered. Labour, erection and life-cycle costs are not included, for bamboo and for steel. The price of bamboo per metre is taken at a reference culm diameter and scaled to the section diameter with (D/D_ref)^α for α = 1.5, 2, 2.5 and 3. Connection steel is priced at the steel material price, and grout at the grout price. The steel reference is priced with the same steel material price for tubes and connection steel. The Indonesian scenario is the main case, because its prices of bamboo, steel and grout come from one document; the Indian, Türkiye and Colombian scenarios are sensitivity cases.

| Scenario | Steel material [USD/kg] | Grout [USD/kg] | Bamboo at reference diameter [USD/m] | Reference diameter [mm] |
|---|---|---|---|---|
| Indonesia 2024 (Jateng HSD) | 1.141 | 0.5388 | 0.2304 | 70 |
| India 2023 (CPWD DSR) | 0.7222 | 0.339 | 0.1459 | 70 |
| Turkiye 2026 (CSB, August) | 0.6894 | 0.3246 | 0.1392 | 70 |
| Colombia 2026 (Guadua, D_ref assumed) | 0.9315 | 0.4389 | 1.583 | 120 |

**Table 6.** Price inputs in USD. The Indonesian prices of bamboo, steel and grout come from one document (Jawa Tengah HSD 2024) and are means over four regencies; the bamboo price is for culms of 6–8 cm diameter and 6 m length. The Jateng HSD and CPWD DSR prices were read from scanned pages [DATA CHECK: visual verification against the pages is not recorded]. The Indian steel and grout prices come from CPWD DSR 2023, where the steel price is the base price of structural steel sections and is applied to tubes, bolts and connection steel; the Indian bamboo price is derived from the Indonesian ratio of bamboo to steel price. The Türkiye steel price is derived from the erected-steel price of ÇŞB (August 2026) with the Indian ratio of erected to material price; its grout and bamboo prices are derived from ratios. The Colombian bamboo price is a 6 m Guadua unit price of 38 500 COP from a supplier web page (2026); the diameter is not stated and D_ref = 120 mm is assumed; its steel and grout prices are the mean of the Indonesian and Indian values. Exchange rates: 82.60 INR (2023), 15 855 IDR (2024) and 47.4925 TRY (mean of two TCMB quotes of 3 August 2026) per USD; 4 053 COP (2025) per USD. The INR, IDR and COP rates are annual averages [DATA CHECK: source files of the rates].

The bamboo prices of the Indian and Türkiye scenarios are derived from the Indonesian prices, and the Colombian steel and grout prices are proxies. The sensitivity scenarios are therefore not independent checks of the main case.

## 2.10 Steel reference

Each dome and the 354-member reference dome were also sized in steel with the same geometry, load patterns, combinations and displacement limit. The steel members are circular hollow sections from a catalogue of 37 AISC pipe sections, with F_y = 248.2 MPa and E = 205 GPa. Tension is limited to 0.6 F_y and compression to the AISC ASD 1989 allowable stress [REF NEEDED: AISC ASD 1989]. The slenderness limits are 200 in compression and 300 in tension. No joint capacity check is made for steel. The steel connection hardware uses the same masses per node and per member end as the bamboo model, without grout. The steel structures were optimized with ABC (population 20, NFE = 1000 N_g, seeds 1001–1030), 30 runs per structure and 120 runs in total.

## Supplementary tables

| Section | D [mm] | t [mm] |
|---|---|---|
| 1 | 80 | 6 |
| 2 | 80 | 9 |
| 3 | 80 | 12 |
| 4 | 90 | 7 |
| 5 | 90 | 10 |
| 6 | 90 | 14 |
| 7 | 100 | 7 |
| 8 | 100 | 10 |
| 9 | 100 | 14 |
| 10 | 110 | 8 |
| 11 | 110 | 11 |
| 12 | 110 | 15 |
| 13 | 120 | 8 |
| 14 | 120 | 12 |
| 15 | 120 | 16 |
| 16 | 130 | 9 |
| 17 | 130 | 13 |
| 18 | 130 | 18 |
| 19 | 140 | 10 |
| 20 | 140 | 15 |
| 21 | 140 | 20 |
| 22 | 160 | 10 |
| 23 | 160 | 15 |
| 24 | 160 | 22 |

**Table S1.** The 24 hollow circular sections of the catalogue.
