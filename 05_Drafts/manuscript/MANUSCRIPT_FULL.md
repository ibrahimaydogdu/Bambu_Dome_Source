# Sizing Optimization of Guadua Bamboo Space Domes and the Share of Connection Steel and Grout in Embodied Carbon

> Working draft. Open placeholders in the text: 28. Sources of numbers: `NUMBERS_TRACE.md`. Open decisions and data requests: `OPEN_ITEMS.md`.

## Highlights

- Single-objective ASD sizing of bamboo space domes with a 24-section catalogue
- ABC ranked first on all three domes; all 270 runs were feasible
- Baseline joint steel and grout carry 74.1–82.1% of the embodied carbon
- One-at-a-time parameter sweeps give a joint share of 41.1–93.9%
- For these three domes, bamboo systems with grout weigh more than steel systems

## Abstract

This study sizes three Guadua bamboo space domes (spans 16, 32 and 40 m; 115, 456 and 1464 members) and accounts for the carbon of their connection steel and grout. Allowable stress design follows the IStructE Manual to ISO 22156:2021 and NSR-10. The objective is culm weight, with a multiplicative penalty for violated constraints; each design group takes one of 24 hollow circular sections. The artificial bee colony (ABC), ant colony optimization (ACO) and dandelion optimizer (DO) were run with 30 seeds per dome, 270 runs, all feasible. The lightest designs weigh 5.800, 41.058 and 66.352 kN. ABC had the lowest mean rank on every dome (Friedman p ≤ 4.91 × 10⁻⁹) and was lighter than ACO and DO (Holm-adjusted p ≤ 5.53 × 10⁻⁴). Embodied carbon (A1–A3, no biogenic carbon) was computed afterwards. Connection steel and grout account for 74.1–82.1% of the baseline carbon; changing one parameter at a time gives 41.1–93.9%, with the largest effect from the emission factor of the culm. For the same geometry, the bamboo members weigh 0.51–0.68 of the steel members and the bamboo systems carry 0.25–0.35 of the steel carbon at baseline factors, but the bamboo systems weigh more than the steel systems. In the Indonesian price scenario, the bamboo to steel material cost ratio is 0.64, 0.93 and 1.02 for α = 2 (0.61–1.15 for α = 1.5–3); the other scenarios give up to 1.39. The results hold for these three models and the stated assumptions.

## Keywords

bamboo structures; Guadua; space truss; sizing optimization; metaheuristic algorithms; embodied carbon

# 1. Introduction

Bamboo culms reach full height within 3–6 months and then mature over 3–6 years (Trujillo et al., 2025). Structural bamboo is promoted as a low-carbon alternative to steel [REF NEEDED]. The embodied carbon of a bamboo structure depends on all materials built into it, not only on the culms. In a life-cycle assessment of bamboo-based houses, steel accounted for 34.7% and the transport of construction materials for 49.0% of the CO₂-equivalent of a single-storey bamboo house, and the bamboo poles for 6.4% (Zea Escamilla et al., 2018, Table 2). Other life-cycle studies deal with bamboo materials and products such as poles, boards and laminated products (Zea Escamilla and Habert, 2014; Vogtländer et al., 2010; Restrepo et al., 2016; van der Lugt et al., 2006).

Connections are a known difficulty of structural bamboo. Correal et al. (2021) describe bolted–mortar-infill connections as one of the most challenging aspects of the design and construction of bamboo structures, because of the uncertainty in the connection strength. Paraskeva et al. (2019) report, for the Kao Jue culms they tested, that plain bolted connections fail early by brittle splitting of the culms, and that mortar infill increases the strength but reduces the ductility. The IStructE Manual refers to a flowable infill material, typically cementitious grout (Trujillo et al., 2025).

A space truss has many member ends. In the present model, each node carries a steel hub, and each member end carries steel hardware and a grout infill (Sections 2.5 and 2.8). The steel mass grows with the number of nodes and members, and the grout mass grows with the number of members and with the section size.

Metaheuristic algorithms are widely used for the discrete sizing optimization of steel skeletal structures, including real-size pin-jointed structures (Hasançebi et al., 2009; Saka and Geem, 2013). Ant colony optimization and artificial bee colony algorithms have been applied to steel frames and space frames (Aydogdu and Saka, 2012; Aydogdu et al., 2016; Saka and Aydogdu, 2021), and an enhanced dandelion optimizer has been used for steel buildings with reinforced concrete shear cores (Taymuş et al., 2025). This study applies single-objective sizing to bamboo space domes and reports the embodied carbon after the optimization. Its aims are:

1. to formulate the sizing of bamboo space domes with a discrete catalogue of 24 hollow circular sections under allowable stress design, with the IStructE Manual to ISO 22156:2021 and NSR-10 as the basis;
2. to compare three metaheuristic algorithms (ABC, ACO and DO) on three dome models over 30 independent seeds;
3. to compute the embodied carbon of the lightest designs, including the connection steel and the grout, and to test its sensitivity to the connection and emission-factor assumptions;
4. to compare the bamboo designs with steel designs of the same geometry in weight, carbon and material cost.

Section 2 describes the models, the design checks, the optimization, the carbon model and the cost model. Section 3 gives the results, Section 4 discusses them and their limits, and Section 5 lists the conclusions.

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

# 3. Results

## 3.1 Algorithm performance

All 270 runs ended with feasible designs (Table 7). The lightest design of each dome weighs 5.800 kN (Geodesic), 41.058 kN (Kiewitt) and 66.352 kN (Ribbed). ABC reached this weight in 5, 30 and 7 of its 30 runs, ACO in 0, 14 and 1 runs, and DO in none (`summary.csv`). DO gave the heaviest mean weight on every dome.

| Dome | Algorithm | Feasible runs | Best [kN] | Median [kN] | Mean [kN] | Std [kN] | Worst [kN] | NFE | Mean time [min] |
|---|---|---|---|---|---|---|---|---|---|
| Geodesic | ABC | 30/30 | 5.800 | 5.894 | 5.880 | 0.051 | 5.980 | 23000 | 0.39 |
| Geodesic | ACO | 30/30 | 5.842 | 6.122 | 6.183 | 0.311 | 7.151 | 23000 | 0.83 |
| Geodesic | DO | 30/30 | 6.178 | 6.448 | 6.488 | 0.209 | 7.168 | 23000 | 0.54 |
| Kiewitt | ABC | 30/30 | 41.058 | 41.058 | 41.058 | 0.000 | 41.058 | 22000 | 1.69 |
| Kiewitt | ACO | 30/30 | 41.058 | 41.761 | 42.281 | 1.393 | 45.422 | 22000 | 2.13 |
| Kiewitt | DO | 30/30 | 41.348 | 43.045 | 42.922 | 0.876 | 44.482 | 22000 | 1.84 |
| Ribbed | ABC | 30/30 | 66.352 | 66.365 | 66.452 | 0.194 | 67.000 | 43000 | 12.16 |
| Ribbed | ACO | 30/30 | 66.352 | 67.050 | 66.908 | 0.474 | 67.741 | 43000 | 13.77 |
| Ribbed | DO | 30/30 | 71.803 | 74.394 | 74.404 | 1.396 | 77.079 | 43000 | 12.66 |

**Table 7.** Best-weight statistics of the 30 runs per algorithm and dome (seeds 1001–1030). NFE is the number of function evaluations per run. The time is the mean wall-clock time per run.

The seed-blocked Friedman test rejected equal performance on every dome (Table 8). ABC had the lowest mean rank on every dome and ACO the second lowest.

| Dome | Friedman chi2_F | p | Mean rank ABC | Mean rank ACO | Mean rank DO |
|---|---|---|---|---|---|
| Geodesic | 48.600 | 2.7967e-11 | 1.1000 | 2.0000 | 2.9000 |
| Kiewitt | 38.264 | 4.9096e-09 | 1.2333 | 2.0333 | 2.7333 |
| Ribbed | 49.160 | 2.1140e-11 | 1.2500 | 1.7500 | 3.0000 |

**Table 8.** Friedman test on the best weights of the 30 seeds (lower rank is lighter).

In the pairwise Mann–Whitney U tests, ABC was lighter than ACO and than DO on every dome after Holm correction (Table 9). The largest Holm-adjusted p-value is 5.53 × 10⁻⁴ (ABC versus ACO on Ribbed).

| Dome | Comparison | Median difference [kN] | U | p (raw) | A12 | p_Holm |
|---|---|---|---|---|---|---|
| Geodesic | ABC vs ACO | 0.2286 | 764.5000 | 3.40e-06 | 0.8494 | 3.40e-06 |
| Geodesic | ABC vs DO | 0.5546 | 900.0000 | 2.97e-11 | 1.0000 | 5.94e-11 |
| Kiewitt | ABC vs ACO | 0.7032 | 690.0000 | 5.27e-06 | 0.7667 | 5.27e-06 |
| Kiewitt | ABC vs DO | 1.9872 | 900.0000 | 1.21e-12 | 1.0000 | 2.42e-12 |
| Ribbed | ABC vs ACO | 0.6852 | 682.5000 | 5.53e-04 | 0.7583 | 5.53e-04 |
| Ribbed | ABC vs DO | 8.0284 | 900.0000 | 2.84e-11 | 1.0000 | 5.67e-11 |

**Table 9.** Two-sided Mann–Whitney U tests of ABC against ACO and DO. The median difference is the median weight of the competitor minus that of ABC. A12 is the probability that a run of the competitor is heavier than a run of ABC.

![Figure 3](../../04_Results/figures/F3_boxplots.png)

**Figure 3.** Best weight of the 30 runs of each algorithm on each dome. Dots are individual runs, the orange line is the median, the green triangle is the mean, and hollow circles are outliers beyond 1.5 times the interquartile range. The box spans the interquartile range.

Figure 2 shows the mean and best penalized weight over the function evaluations. On all three domes the mean curve of DO is the lowest at small NFE and flattens at the highest value. The mean curves of ABC and ACO end close to each other on Ribbed and Kiewitt. On Kiewitt the ACO mean curve approaches the ABC curve later than ABC does and ends 1.2 kN higher (Table 7).

![Figure 2](../../04_Results/figures/F2_convergence.png)

**Figure 2.** Penalized weight against the number of function evaluations (NFE) for the three domes. Solid lines: mean of the 30 runs of an algorithm; dashed lines: best of the 30 runs. Logarithmic vertical axis, clipped to 0.9–4 times the final minimum of each dome. Markers: circle ABC, square ACO, triangle DO.

For the lightest design of each dome, member forces and nodal displacements were also computed with SAP2000 (Table 10). The differences are normalised by the largest value in the SAP2000 results. The D/C values recomputed from the SAP2000 forces equal those of the own solver to five decimals.

| Dome | Largest axial force [kN] | Axial-force difference (normalised) | Displacement difference (normalised) | max D/C (own solver) | max D/C (SAP2000 forces) |
|---|---|---|---|---|---|
| Geodesic | 13.82 | 3.4e-15 | 7.3e-15 | 0.99589 | 0.99589 |
| Kiewitt | 26.76 | 1.7e-14 | 3.2e-14 | 0.99226 | 0.99226 |
| Ribbed | 39.77 | 6.2e-14 | 1.3e-13 | 0.99995 | 0.99995 |

**Table 10.** Comparison of the own solver with SAP2000 for the lightest design of each dome.

## 3.2 Lightest designs and governing limit states

Table 11 gives the largest demand-to-capacity ratio of each check for the lightest designs. Compression reaches a ratio of 0.992–1.000 in all three designs. The displacement ratio is 0.060, 0.062 and 0.129 of the limit.

| Dome | Tension | Compression | Slenderness | Joint | u/u_lim | Groups with D/C >= 0.95 |
|---|---|---|---|---|---|---|
| Geodesic | 0.165 | 0.996 | 0.733 | 0.280 | 0.060 | 8/23 |
| Kiewitt | 0.361 | 0.992 | 0.532 | 0.543 | 0.062 | 6/22 |
| Ribbed | 0.430 | 1.000 | 0.664 | 0.807 | 0.129 | 9/43 |

**Table 11.** Largest D/C ratio per check in the lightest design of each dome, displacement ratio and number of design groups with D/C ≥ 0.95.

Compression determines the largest D/C ratio in 19 of 23 groups (Geodesic), 21 of 22 (Kiewitt) and 41 of 43 (Ribbed) in the lightest designs. Slenderness determines the remaining groups: 4, 1 and 2. Tension and the joint check determine no group of the lightest designs. Averaged over the 90 feasible runs of each dome, compression determines 81.1%, 95.5% and 93.4% of the groups, slenderness 18.9%, 4.5% and 6.5%, and the joint check 0.2% on Ribbed (`GOVERNING_LIMIT_SHARES.md`). Figure 4 shows these shares. The profiles of the lightest designs are in Figure 1.

![Figure 4](../../04_Results/figures/F4_governing_limit_states.png)

**Figure 4.** Share of design groups in which each check gives the largest D/C ratio. Left: lightest design of each dome. Right: mean of the 90 feasible runs of each dome. The checks are tension, compression, slenderness and joint capacity.

![Figure 1](../../04_Results/figures/F1_best_profiles.png)

**Figure 1.** Lightest design of each dome: the lightest feasible design among the 90 runs per dome (3 algorithms × 30 seeds). Bars give the outer diameter D [mm] of each design group (left axis); the line gives the wall thickness t [mm] (right axis). The panel titles give the algorithm that found the design and its weight. ABC found the lightest design of each dome; ACO reached the same weight on Kiewitt and Ribbed.

## 3.3 Bolts required per member

The largest member forces of the lightest designs are 13.82, 26.76 and 39.77 kN (Table 10), below F_j,Rd = 49.3 kN, so most members need one or two bolts (Table 12). No member needs four. On Ribbed, 813 members need one bolt, 591 two and 60 three. Twelve Ribbed members (0.82%), all 0.76 m long, are too short to hold the three bolts they require under the NSR-10 spacing rules; the largest force in these members is 31.25 kN. Eighty-four Ribbed members are shorter than 1.35 m. Geodesic and Kiewitt have no such members; their shortest members are 2.24 m and 2.09 m long.

| Dome | Members | n_req=1 | n_req=2 | n_req=3 | n_req=4 | n_req>4 | Members too short for required bolts | Share [%] | Shortest member [m] | Max force in too-short members [kN] | Members < 1.35 m (4 bolts both ends) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Geodesic | 115 | 115 | 0 | 0 | 0 | 0 | 0 | 0.00 | 2.24 | 0.00 | 0 |
| Kiewitt | 456 | 388 | 68 | 0 | 0 | 0 | 0 | 0.00 | 2.09 | 0.00 | 0 |
| Ribbed | 1464 | 813 | 591 | 60 | 0 | 0 | 12 | 0.82 | 0.76 | 31.25 | 84 |

**Table 12.** Number of bolts required per member end (NSR-10 allowable load, #5 bolt) and members too short to hold them. Lengths and forces in the last columns are in m and kN.

## 3.4 Embodied carbon of the lightest designs

The embodied carbon of the lightest designs is 0.86 t CO₂e (Geodesic), 4.84 t (Kiewitt) and 11.34 t (Ribbed) (Table 13). Connection steel and grout together account for 79.39%, 74.07% and 82.11% of this carbon; connection steel alone accounts for 57.25%, 39.03% and 51.92%. The grout mass is 57%, 65% and 67% of the total mass of culm, steel and grout (derived from Table 13).

| Dome | Bamboo [t] | Steel [t] | Grout [t] | Total [t] | Culm [%] | Steel [% CO2e] | Grout [% CO2e] | Joint (steel+grout) [% CO2e] | Total CO2e [t] |
|---|---|---|---|---|---|---|---|---|---|
| Geodesic | 0.59 | 0.21 | 1.06 | 1.86 | 20.61 | 57.25 | 22.13 | 79.39 | 0.86 |
| Kiewitt | 4.19 | 0.79 | 9.43 | 14.41 | 25.93 | 39.03 | 35.04 | 74.07 | 4.84 |
| Ribbed | 6.76 | 2.47 | 19.02 | 28.26 | 17.89 | 51.92 | 30.19 | 82.11 | 11.34 |

**Table 13.** Mass and carbon breakdown of the lightest design of each dome (baseline parameters: EC_b = 0.30, EC_s = 2.38, EC_m = 0.18 kg CO₂e/kg; L_inj = 2.5 D).

Table 14 shows the joint share (steel plus grout) when parameters are changed.

| Dome | Base | L_inj/D = 1.5 | L_inj/D = 3.5 | EC_steel = 1.2 | EC_steel = 3.0 | EC_bamboo = 0.09 | EC_bamboo = 1.23 | Combined case |
|---|---|---|---|---|---|---|---|---|
| Geodesic | 79.39 | 77.38 | 81.06 | 71.22 | 82.06 | 92.77 | 48.43 | 53.9 |
| Kiewitt | 74.07 | 69.84 | 77.26 | 67.85 | 76.46 | 90.50 | 41.06 | 45.3 |
| Ribbed | 82.11 | 79.65 | 84.04 | 75.91 | 84.24 | 93.86 | 52.82 | 57.7 |

**Table 14.** Joint share of the embodied carbon [%] for the lightest designs. Each column changes one parameter from the baseline; the last column changes L_inj/D = 1.5, EC_s = 1.2, EC_b = 0.47 and EC_m = 0.12 together.

The emission factor of the bamboo culm has the largest effect. With EC_b = 0.09 the joint share is 90.50–93.86%; with EC_b = 1.23 it is 41.06–52.82%. The share changes by less than 10 percentage points with L_inj/D or EC_s alone. The joint share is below 50% for Kiewitt in the combined case (45.3%) and for Kiewitt (41.06%) and Geodesic (48.43%) with EC_b = 1.23.

## 3.5 Comparison with steel

For the same geometry, the weight of the bamboo members is 0.509, 0.677 and 0.634 of the weight of the steel members, and the embodied carbon of the bamboo systems (culm, connection steel and grout) is 0.252, 0.278 and 0.347 of that of the steel systems at the baseline emission factors (Table 16). With EC_b = 1.23 kg CO₂e/kg the three ratios are 0.414, 0.502 and 0.540. With a steel emission factor of 1.6 kg CO₂e/kg they are 0.396, 0.436 and 0.545 (`T8_material_sensitivity.csv`). The system weights, which include connection steel and grout, are higher for bamboo than for steel (Table 15): 18.211, 141.320 and 277.222 kN for bamboo against 13.434, 68.456 and 128.955 kN for steel (ratios 1.36, 2.06 and 2.15, derived).

| Structure | Members | Member weight [kN] | System weight [kN] | Embodied carbon [t CO2e] |
|---|---|---|---|---|
| Steel - Reference (354 members) | 354 | 129.012 | 134.976 | 34.456 |
| Steel - Ribbed | 1464 | 104.685 | 128.955 | 32.673 |
| Steel - Kiewitt | 456 | 60.666 | 68.456 | 17.412 |
| Steel - Geodesic | 115 | 11.404 | 13.434 | 3.410 |
| Bamboo - Geodesic | 115 | 5.800 | 18.211 | 0.861 |
| Bamboo - Kiewitt | 456 | 41.058 | 141.320 | 4.842 |
| Bamboo - Ribbed | 1464 | 66.352 | 277.222 | 11.341 |

**Table 15.** Steel and bamboo structures. Member weight is the culm weight (bamboo) or tube weight (steel). System weight adds connection steel and, for bamboo, grout. Reference is the 354-member steel dome. Bamboo values are for the lightest of the 90 runs of the dome; steel values are for the best of 30 runs.

| Dome | Bamboo/Steel member weight | Bamboo/Steel CO2e |
|---|---|---|
| Geodesic | 0.509 | 0.252 |
| Kiewitt | 0.677 | 0.278 |
| Ribbed | 0.634 | 0.347 |

**Table 16.** Bamboo to steel ratios for the same geometry: member weight and embodied carbon of the systems, at the baseline emission factors.

Figure 5 shows the member weight and the embodied carbon of all structures of Table 15. Under the load condition of the literature study, the present steel model gives 135–136 kN for the 354-member dome, against 151.1–155.8 kN reported there [DATA NEEDED: calculation record of the 135–136 kN check; REF NEEDED: literature values].

![Figure 5a](../../04_Results/figures/F5_material_weight.png)

**Figure 5a.** Member weight [kN] of the steel structures (best of 30 runs) and of the lightest bamboo designs. Reference is the 354-member steel dome.

![Figure 5b](../../04_Results/figures/F5_material_co2.png)

**Figure 5b.** Embodied carbon [t CO₂e] of the structures of Figure 5a, by component: tube (steel) or culm (bamboo), connection steel and grout (labelled "mortar" in the figure).

## 3.6 Material cost

Table 17 gives the ratio of the bamboo material cost to the steel material cost for the same geometry in the Indonesian scenario, the main case. With α = 2 the ratios are 0.639 (Geodesic), 0.926 (Kiewitt) and 1.021 (Ribbed). Over α = 1.5–3 they range from 0.612 to 0.724, 0.869 to 1.137 and 0.981 to 1.154. A ratio above 1 means that the bamboo structure costs more. The ratio is below 1 for Geodesic at all α, below 1 for Kiewitt for α ≤ 2, and below 1 for Ribbed only at α = 1.5 (0.981). The grout accounts for 50.4-59.6%, 56.1-73.4%, 59.2-69.7% of the bamboo material cost (Geodesic, Kiewitt, Ribbed).

| alpha | Geodesic ratio | Kiewitt ratio | Ribbed ratio | Geodesic grout [%] | Kiewitt grout [%] | Ribbed grout [%] |
|---|---|---|---|---|---|---|
| 1.5 | 0.612 | 0.869 | 0.981 | 59.6 | 73.4 | 69.7 |
| 2 | 0.639 | 0.926 | 1.021 | 57.1 | 68.9 | 67.0 |
| 2.5 | 0.676 | 1.010 | 1.076 | 54.0 | 63.1 | 63.5 |
| 3 | 0.724 | 1.137 | 1.154 | 50.4 | 56.1 | 59.2 |

**Table 17.** Ratio of bamboo to steel material cost in the Indonesian scenario for the lightest bamboo and best steel designs, by diameter exponent α, and the grout share of the bamboo material cost.

The other three scenarios are sensitivity cases (Table 18). Over all four scenarios and α = 1.5–3, the ratio ranges from 0.610 to 0.875 (Geodesic), 0.865 to 1.394 (Kiewitt) and 0.977 to 1.342 (Ribbed). The Colombian scenario gives the highest ratios and is above 1 for Kiewitt and Ribbed at all α.

| Price scenario | Geodesic | Kiewitt | Ribbed |
|---|---|---|---|
| India 2023 (CPWD DSR) | 0.637 (0.610-0.721) | 0.922 (0.865-1.133) | 1.016 (0.977-1.150) |
| Türkiye 2026 (CSB, August) | 0.638 (0.611-0.723) | 0.924 (0.867-1.135) | 1.019 (0.979-1.152) |
| Colombia 2026 (Guadua, D_ref = 120 mm assumed) | 0.868 (0.862-0.875) | 1.248 (1.191-1.394) | 1.297 (1.279-1.342) |

**Table 18.** Sensitivity of the cost ratio to the price scenario: ratio at α = 2, with the range over α = 1.5–3 in brackets.

# 4. Discussion

## 4.1 Algorithm comparison

ABC had the lowest mean weight and the lowest mean Friedman rank on all three domes. On Kiewitt, all 30 ABC runs ended at the same weight. ACO reached the best weight of ABC on Kiewitt and Ribbed in at least one run, and DO had the highest mean weight on every dome.

The ranking applies to the settings used: NFE = 1000 N_g and population sizes of 20 (ABC), 40 (ACO) and 40 (DO). The tuning study found different best population sizes for some pairs of algorithm and dome (ABC: 20, 20 and 40; ACO: 80, 20 and 80; DO: 40, 80 and 40 for Geodesic, Kiewitt and Ribbed; `TUNING_STUDY.md`). The ranking may change with other population sizes or budgets. ACO and DO were not tested against each other.

## 4.2 Joint share of the embodied carbon

In the baseline case, connection steel and grout carry 74.1–82.1% of the embodied carbon of the lightest designs (Table 13). This share depends on assumptions. In the one-at-a-time sweeps it ranges from 41.1% to 93.9% (Table 14). The parameter with the largest effect is the emission factor of the bamboo culm, whose lower value (0.09 kg CO₂e/kg) rests on data for laminated bamboo panels (Section 2.8). In the combined case, in which the parameters are changed together in the direction that lowers the joint share, the share is 45.3–57.7%.

The share also depends on the hardware definition of the model: 2.0 kg of steel per node, 0.5 kg per member end and a grout length of 2.5 D. These values are assumptions, and a different joint design would change the share. The grout is 57–67% of the total mass of culm, steel and grout (Section 3.4).

Zea Escamilla et al. (2018, Table 2) report that, for a single-storey bamboo house, steel accounts for 34.7% and the transport of construction materials for 49.0% of the CO₂-equivalent, and the bamboo poles for 6.4%. That study has a different structure, functional unit and system boundary, so the values cannot be compared directly. In both studies, most of the CO₂-equivalent does not come from the culms.

## 4.3 Bamboo and steel

In member weight and in embodied carbon, the bamboo designs are lower than the steel designs of the same geometry (Table 17). The carbon ratio of 0.25–0.35 holds for the baseline emission factors; it rises to 0.41–0.54 with EC_b = 1.23 (Section 3.5). With connection steel and grout included, the bamboo systems are heavier (Table 16). The grout alone is 19.02 t of the 28.26 t of the Ribbed system.

The comparison has limits. The steel structures were sized with a different design rule (AISC ASD 1989), a catalogue of 37 pipe sections, slenderness limits of 200 and 300, and no joint capacity check, and they were optimized with one algorithm. The ratios compare optimum designs under different rules and catalogues and are indicative only.

## 4.4 Material cost

In the Indonesian scenario, the main case, the bamboo structure is cheaper than the steel structure for Geodesic at all values of the diameter exponent α, cheaper for Kiewitt for α ≤ 2, and more expensive for Ribbed for α ≥ 2 (Table 17). The bamboo price at structural diameters is not taken directly from a source: it is scaled from a reference diameter, and the ratios depend on α. The grout is a large part of the bamboo material cost. The sensitivity scenarios give higher ratios, the highest for Colombia, where the reference diameter is assumed (Table 18). The Indian and Türkiye bamboo prices are derived from the Indonesian prices, so those scenarios are not independent checks. Labour, erection and life-cycle costs are not included.

## 4.5 Connections

The joint capacity of 49.3 kN follows NSR-10. The IStructE Manual procedure gave about 3–5 kN per bolt in a preliminary calculation (Section 2.5), against 13.25 kN allowable per bolt in NSR-10. If the lower capacity applied, more bolts per member end would be needed, and the hardware masses of the carbon model would no longer hold [DATA NEEDED: IStructE joint calculation record]. The 12 Ribbed members of 0.76 m cannot hold the bolts required under the NSR-10 spacing rules; their joints need a different detail.

## 4.6 Limitations

- The three domes have different spans, topologies and member counts; the results hold for these three models and the 24-section catalogue.
- The culm self-weight, the connection hardware and the grout are not part of the loads.
- C_R = 0.90 (single-culm members) and b₀ = 0.01 are assumptions; λ ≤ 150 is applied to tension members, although NSR-10 prescribes it for compression members only.
- The hub (2.0 kg per node), the hardware at member ends (0.5 kg) and the grout length (2.5 D) are assumptions and are not designed against the member forces.
- The emission factor of the culm has an assumed lower bound, and the grout factor is a proxy for non-shrink grout.
- Only stages A1–A3 are considered; biogenic carbon is excluded.
- The cost covers materials only. The bamboo price at structural diameters is scaled from a reference diameter, and the four price scenarios are not independent.
- The steel reference was designed with different rules and catalogue than the bamboo structures (Section 4.3).
- Connections are modelled as pin joints; joint stiffness and eccentricity are not considered.
- The three algorithms were run with one population size each and one evaluation budget.

# 5. Conclusions

The results hold for the three dome models (spans of 16, 32 and 40 m), the 24-section catalogue, the assumed joint hardware and the stated emission factors.

1. Single-objective ASD sizing gave feasible designs in all 270 runs. The lightest designs weigh 5.800 kN (Geodesic, 115 members), 41.058 kN (Kiewitt, 456 members) and 66.352 kN (Ribbed, 1464 members).
2. ABC had the lowest mean rank on every dome (Friedman p ≤ 4.91 × 10⁻⁹) and was lighter than ACO and DO with Holm-adjusted p ≤ 5.53 × 10⁻⁴. The ranking holds for the population sizes and the evaluation budget used.
3. Compression determines the largest D/C ratio in 19 of 23, 21 of 22 and 41 of 43 design groups of the lightest designs. Tension and the joint check determine none.
4. In the baseline case, connection steel and grout account for 74.1–82.1% of the embodied carbon (A1–A3, biogenic carbon excluded). Changing one parameter at a time gives 41.1–93.9%. The emission factor of the culm has the largest effect. The share is below 50% for Kiewitt in the combined case and for Kiewitt and Geodesic with EC_b = 1.23 kg CO₂e/kg.
5. For the same geometry, the bamboo members weigh 0.51–0.68 of the steel members, and the bamboo systems carry 0.25–0.35 of the steel-system carbon at baseline emission factors (0.41–0.54 with EC_b = 1.23). With connection steel and grout, the bamboo systems weigh 1.36–2.15 times the steel systems.
6. In the Indonesian price scenario, the ratio of bamboo to steel material cost is 0.64 (Geodesic), 0.93 (Kiewitt) and 1.02 (Ribbed) for α = 2, and 0.61–1.15 for α = 1.5–3. Across four price scenarios the ratio ranges from 0.610 to 1.394. The sensitivity scenarios are not independent of the main case.

Future work: a joint design that follows from the member forces, and the inclusion of biogenic carbon and of labour and life-cycle costs.

# References

Entries without a mark were checked against the PDF in `Papers/` (authors, title, journal, volume, pages, DOI). Entries marked † were taken from the reference list of Taymuş et al. (2025) and have not been checked against the original papers.

Aydogdu, I., Akin, A., Saka, M.P., 2016. Design optimization of real world steel space frames using artificial bee colony algorithm with Levy flight distribution. Advances in Engineering Software 92, 1–14. †

Aydogdu, I., Saka, M.P., 2012. Ant colony optimization of irregular steel frames including elemental warping effect. Advances in Engineering Software 44 (1), 150–169. †

Correal, J.F., Prada, E., Suárez, A., Moreno, D., 2021. Bearing capacity of bolted-mortar infill connections in bamboo and yield model formulation. Construction and Building Materials 305, 124597. https://doi.org/10.1016/j.conbuildmat.2021.124597

Hasançebi, O., et al., 2009. Performance evaluation of metaheuristic search techniques in the optimum design of real size pin jointed structures. Computers & Structures 87 (5–6), 284–302. †

Paraskeva, T., Pradhan, N.P.N., Stoura, C.D., Dimitrakopoulos, E.G., 2019. Monotonic loading testing and characterization of new multi-full-culm bamboo to steel connections. Construction and Building Materials 201, 473–483. https://doi.org/10.1016/j.conbuildmat.2018.12.198

Restrepo, A., Becerra, R., Tibaquira G., J.E., 2016. Energetic and carbon footprint analysis in manufacturing process of bamboo boards in Colombia. Journal of Cleaner Production 126, 563–571. https://doi.org/10.1016/j.jclepro.2016.02.144

Saka, M., Aydogdu, I., 2021. Performance evaluation of artificial bee colony algorithm and its variants in the optimum design of steel skeletal structures. Asian Journal of Civil Engineering 22, 73–91. †

Saka, M.P., Geem, Z.W., 2013. Mathematical and metaheuristic applications in design optimization of steel frame structures: an extensive review. Mathematical Problems in Engineering 2013, 1–33. †

Taymuş, R.B., Aydoğdu, İ., Saka, M.P., Kim, S., Geem, Z.W., 2025. Impact of connection types on metaheuristic-based optimum design of 3D steel buildings with RC shear core. International Journal of Steel Structures 25 (5), 1097–1116. https://doi.org/10.1007/s13296-025-00994-0

Trujillo, D., Harries, K., Kaminski, S., Lopez, L.-F., 2025. Manual for the design of bamboo structures to ISO 22156:2021. The Institution of Structural Engineers, London. Version 1.0, November 2025. ISBN 978-1-906335-97-7 (print).

van der Lugt, P., van den Dobbelsteen, A.A.J.F., Janssen, J.J.A., 2006. An environmental, economic and practical assessment of bamboo as a building material for supporting structures. Construction and Building Materials 20, 648–656. https://doi.org/10.1016/j.conbuildmat.2005.02.023

Vogtländer, J., van der Lugt, P., Brezet, H., 2010. The sustainability of bamboo products for local and Western European applications. LCAs and land-use. Journal of Cleaner Production 18, 1260–1269. https://doi.org/10.1016/j.jclepro.2010.04.015

Zea Escamilla, E., Habert, G., 2014. Environmental impacts of bamboo-based construction materials representing global production diversity. Journal of Cleaner Production 69, 117–127. https://doi.org/10.1016/j.jclepro.2014.01.067

Zea Escamilla, E., Habert, G., Correal Daza, J.F., Archilla, H.F., Echeverry Fernández, J.S., Trujillo, D., 2018. Industrial or traditional bamboo construction? Comparative life cycle assessment (LCA) of bamboo-based buildings. Sustainability 10 (9), 3096. https://doi.org/10.3390/su10093096

Zhao, S., et al., 2022. Dandelion optimizer: a nature-inspired metaheuristic algorithm for engineering applications. Engineering Applications of Artificial Intelligence 114, 105075. † [REF CHECK: full author list]

Circular Ecology, ICE Database Educational V5.0, June 2026. [REF CHECK: authors]

Ministerio de Ambiente, Vivienda y Desarrollo Territorial, Colombia. Reglamento Colombiano de Construcción Sismo Resistente NSR-10, Título G — Estructuras de madera y estructuras de guadua. [REF CHECK: year and publisher details]

## Placeholders in the text

- ISO 22156:2021 [REF CHECK: full title and publisher].
- ASCE 7-22 [REF CHECK: title and publisher].
- Original references of ABC and ACO [REF NEEDED].
- The 354-member reference dome and its loads [REF NEEDED].
- AISC ASD 1989 [REF NEEDED].
- Friedman, Mann–Whitney, Holm and Vargha–Delaney [REF NEEDED].
- INBAR report with the emission data for laminated bamboo panels, used for the lower bound of EC_b [REF CHECK: report number, authors, year; file `Evidence/MOSO-Bamboo-products-LCA-TP35.pdf`].
