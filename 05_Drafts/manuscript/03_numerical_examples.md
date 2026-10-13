# 3. Numerical examples

This section describes the examples to which the formulation of Section 2 is applied: three space domes of different span and topology (Section 3.1), the bamboo and steel materials and the design parameters (Section 3.2), the loads and load combinations (Section 3.3), the settings of the algorithms (Section 3.4) and the inputs of the carbon and cost evaluation (Section 3.5). The same geometry, loads and load combinations are used for bamboo and steel, so that only the material and its design rules differ.

## 3.1 Dome models

Three domes were chosen to cover a range of scale and topology (Table 1). The spans are 16, 32 and 40 m, the number of members is 115, 456 and 1464, and the number of design variables $N_g$ is 23, 22 and 43. The domes are not scaled copies of one geometry. The ribbed dome is a frequency-2 densification of a 354-member reference steel dome with a 40 m span and a crown height of 8.28 m, which has members up to 5.97 m long [REF-S4]; the densified model has members of 0.76–3.08 m [DATA NEEDED: reason for the frequency-2 densification]. The Kiewitt and geodesic domes are two further common dome topologies [REF-S8].

| Dome | Code name | Span [m] | Rise [m] | Nodes | Members | Design groups | Supported nodes | Member length [m] | u_lim [mm] |
|---|---|---|---|---|---|---|---|---|---|
| Geodesic | geodesic16 | 16 (nominal) | 3.72 | 46 | 115 | 23 | 20 | 2.24-2.96 | 107 |
| Kiewitt | kiewitt32 | 32 | 6.60 | 169 | 456 | 22 | 48 | 2.09-3.55 | 213 |
| Ribbed | ribbed40 | 40 | 8.28 | 505 | 1464 | 43 | 48 | 0.76-3.08 | 267 |

**Table 1.** Dome models. The Geodesic dome has a nominal span of 16 m; twice the largest horizontal distance of a node from the vertical axis is 16.77 m. The rise is the height of the highest node above the lowest support. The displacement limit $u_{lim}$ is the span divided by 150, rounded to 1 mm.

- **Ribbed:** ribbed dome (called Schwedler type in the analysis code).
- **Kiewitt:** spherical cap with 8 sectors and 6 rings.
- **Geodesic:** icosahedral geodesic dome (class I, frequency 5) truncated at a colatitude of 50°. All nodes on the zigzag boundary are supported.

Members are assigned to design groups by geometric class. For Geodesic, a group contains members with the same length, the same latitude and the same position in the 72° sector; mirror images form separate groups. For Ribbed and Kiewitt, the classes follow the structure of the dome generator [DATA NEEDED: verbal description of the Ribbed and Kiewitt group definition]. Supported nodes are restrained in all three translations. Member forces and nodal displacements are computed with a direct stiffness solver written for this study; for the optimum design of each dome the results were compared with SAP2000 (Section 4.1).

The displacement limit is $u_{lim}=\text{span}/150$. The Manual states a long-term deflection limit of L/150 for elements without plaster or plasterboard ceilings, taken from Table NA.5 of the UK National Annex to Eurocode 5 [1]. No displacement limit specific to domes was found [REF-S9]. The limit is applied here to the largest nodal displacement of the dome and, for comparability, also to the steel dome.

## 3.2 Materials, section catalogues and design parameters

The bamboo parameters follow the Manual [1], which presents the characteristic values and the design factors of ISO 22156:2021 [17] in a form for allowable stress design. Density, design modulus and tension strength are the schematic values of its Table 4.4, and the compression strength is the value for *Guadua angustifolia* in its Table A3.4. The factors $C_R$, $C_T$ and $C_{DF}$ and the factor of safety are those of Equation 4. The joint capacity and the slenderness limit come from the Colombian code NSR-10, Title G [15], because the catalogue sections are Guadua culms. Table 2 lists the parameters and their sources.

| Quantity | Value | Source and remark |
|---|---|---|
| Density ρ | 700 kg/m³ | [1] Table 4.4; mean value for Guadua 680 kg/m³ (Table A3.9) |
| Design modulus E_k | 10 GPa | [1] Table 4.4 gives 10 or 15 GPa (15 GPa for tropical bamboo with D/t ≥ 10; a mean value with 75% confidence). 10 GPa is used for all sections, a conservative choice |
| Tension strength f_t,0,k | 40 MPa | [1] Table 4.4, schematic. For Guadua, Table A3.9 gives only a mean tension strength (121 MPa, COV 0.18) and no characteristic value |
| Compression strength f_c,0,k | 37.8 MPa | [1] Table A3.4 (Guadua, n = 922) |
| Factor of safety FS | 2.0 | axial members, [1] Appendix A3.6 |
| Redundancy factor C_R | 0.90 | [1]: a single culm is non-redundant, C_R = 0.9; applied to all members, which assumes single-culm members |
| Temperature factor C_T | 1.0 | service temperature below 38 °C [1] |
| Duration factor C_DF, Service Class 2 | 0.55 / 0.65 / 0.85 | permanent / transient / instantaneous loads; values from worked examples in the Manual (PDF pp. 153 and 163). The choice of Service Class 2 and the assignment of snow to transient and wind to instantaneous loads are assumptions |
| Ylinen constant c | 0.8 | [1] Appendix A6.2 |
| Initial bow b₀ | 0.01 | assumed; C_bow = 0.5 (Equation 6.4 of the Manual gives C_bow = 0 at b₀ = 0.02) |
| Effective length factor K | 1.0 | [1] Table 6.1 |
| Slenderness limit λ_max | 150 | [15] G.12.9.2.6 and G.12.9.2.7 (compression members); applied here to all members |
| Joint capacity F_j,Rd | 49.3 kN | [15] Tables G.12.11-2 and G.12.11-3: F_bolt,adm = 13.25 kN, n_bolt = 4, C_g = 0.93 |
| Displacement limit u_lim | span/150 | Section 3.1 |

**Table 2.** Material and design parameters of the bamboo dome. C_R, b₀, the Service Class and load-duration assignment, the choice E_k = 10 GPa and the use of λ_max for tension members are choices or assumptions of this study.

The catalogue has 24 hollow circular sections with outer diameter $D = 80$–$160$ mm and wall thickness $t = 6$–$22$ mm (Table S1) [DATA NEEDED: basis for the choice of the 24 (D, t) pairs].

The joint capacity of Equation 11 is $F_{j,Rd}=4\times 13.25\times 0.93=49.3$ kN: $F_{bolt,adm}$ is the allowable load of one #5 (5/8 in) bolt in double shear, parallel to the fibre, for a culm diameter of 100 mm (Table G.12.11-2), and $C_g$ is the group factor for four bolts (Table G.12.11-3) [15]. The number of bolts $n_{bolt}=4$ is a design decision of the authors. A calculation with the joint procedure of the Manual gave about 3–5 kN per bolt; one factor of that procedure could not be verified, so the NSR-10 value is used [DATA NEEDED: record of the IStructE joint calculation]. Section 4.3 reports the number of bolts that each member requires and the members that are too short to hold them under the NSR-10 spacing rules: a bolt spacing of at least 150 mm, and an end distance of more than 150 mm for tension members and more than 100 mm for compression members. The length of a member with $n$ bolts at each end is then at least $2\,(e+(n-1)\cdot 150\ \text{mm})+150\ \text{mm}$, with $e$ the end distance; with $e=150$ mm, three bolts require about 1.05 m and four bolts about 1.35 m.

For the steel domes, the catalogue is a list of 37 AISC pipe sections [REF-S4], with $F_y=248.2$ MPa, $E=205$ GPa and $\rho=7850$ kg/m³; the design rules are those of Section 2.4 [REF-S6]. These settings follow the steel optimization of the 354-member dome in the literature [REF-S4], so that the steel model can be checked against it (Section 4.5).

## 3.3 Loads and load combinations

The load values are those of the 354-member reference dome [REF-S4]. The same values, including the pressure coefficients of the 40 m reference dome, are used for all three domes. For Geodesic, the span $L_d$ is the nominal span of 16 m.

- **Dead load D:** 0.20 kN/m² on the horizontal projection, downward.
- **Snow load S:** 0.83 kN/m² on the horizontal projection, downward.
- **Wind loads:** pressure normal to the surface, $p=q_hGC_p-q_hGC_{pi}$, with $q_h=1.115$ kN/m², $G=0.85$ and $C_p=0.0105$, $-0.907$ and $-0.5$ in three zones along the wind direction $x$ ($x<-L_d/4$, $|x|\le L_d/4$, $x>L_d/4$, with $L_d$ the span of the dome). The internal pressure term is $GC_{pi}=-0.18$ for pattern $W_N$ and $+0.18$ for $W_P$. The resulting pressures are listed in Table 3.

| Pattern | Zone x < -L_d/4 | Zone -L_d/4 <= x <= L_d/4 | Zone x > L_d/4 |
|---|---|---|---|
| W_N | +0.211 | -0.659 | -0.273 |
| W_P | -0.191 | -1.060 | -0.675 |

**Table 3.** Wind pressures [kN/m²] computed from the constants above. Positive values act toward the surface.

Surface loads are distributed to the nodes by triangular faces, one third of each face to each of its nodes. For Ribbed and Kiewitt, the projected area is normalised so that the total equals the area of a circle of diameter $L_d$; this normalisation is not applied to Geodesic. The wind zone of a face is selected from the $x$-coordinate of its centroid. The culm self-weight, the connection hardware and the grout are not applied as loads; the permanent load is the surface load D only. This follows the reference benchmark [REF-S4].

Eight allowable stress design combinations are evaluated without load factors, following ASCE 7-22 [18]. The duration class of a combination is that of its shortest-duration load.

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

**Table 4.** Load combinations, duration classes and capacity factors $k$ (Equation 5).

## 3.4 Settings of the algorithms

Each run stopped after $NFE = 1000\,N_g$ function evaluations: 43 000 (Ribbed), 22 000 (Kiewitt) and 23 000 (Geodesic). The population sizes were 20 for ABC and 40 for ACO and DO, that is, 0.5–1.8 times the number of design variables ($N_g$ = 22–43). In a comparison of algorithms that included an enhanced dandelion optimizer, the memory size was set equal to the number of design variables [14]. Each algorithm was run with 30 independent seeds (1001–1030) on each dome, giving 270 runs for bamboo. The steel domes were optimized with ABC (population 20, $NFE=1000\,N_g$, seeds 1001–1030), 30 runs per structure and 120 runs in total, because ABC gave the lightest bamboo designs.

The campaign used the default parameters of the implementation. For ABC, the abandonment limit is the population size times $N_g$. For ACO, $\alpha=1$, $\beta=0.5$, the evaporation rate is 0.2 and the elite fraction is 0.2; its heuristic is $1/s$ for section index $s$, which favours small sections. DO has a rising stage, a descending stage and a landing stage with a Lévy-flight step ($\beta=1.5$, scaled by 0.1); a new design replaces the current one only if it is better.

The algorithm selection used a separate tuning study with seeds 2001–2005 (three seeds for Ribbed), population sizes of 20, 40 and 80, and the candidates ABC, ACO, DO, GWO, WOA and TLBO. Each candidate was ranked at its own best population size by mean penalized weight. GWO, WOA and TLBO were not run on Ribbed, so the mean ranks are taken over the domes on which an algorithm was run. ABC and ACO had the lowest mean ranks (1.00 and 2.00); DO had 3.33, but GWO had a lower mean weight than DO on Geodesic. DO was included by study design, as one recent algorithm next to two older ones; it is not shown to be among the three best candidates. The campaign population sizes of 20, 40 and 40 differ from the best sizes of the tuning table, [20, 20, 40] (ABC), [80, 20, 80] (ACO) and [40, 80, 40] (DO) for Geodesic, Kiewitt and Ribbed.

## 3.5 Inputs of the carbon and cost evaluation

**Connection hardware.** The model uses a steel hub of $m_{hub}=2.0$ kg per node, steel hardware of $m_{end}=0.5$ kg per member end (stud, nut and washer) and a grout column of length $\beta D$ with $\beta=2.5$ and $\rho_m=2100$ kg/m³ (assumed density of non-shrink grout [REF-S10]). These values are assumptions. They do not depend on the member force and are not designed against $F_{j,Rd}$.

**Emission factors** (Table 5).

| Factor | Value [kg CO₂e/kg] | Basis |
|---|---|---|
| Bamboo culm EC_b | 0.30 (range 0.09–1.23) | production 0.092 plus 300 km road transport 0.21 (derivation below) |
| Connection steel EC_s | 2.38 | [19] "Steel, Plate" |
| Grout EC_m | 0.18 | [19] mortar 1:3, used as a proxy for non-shrink grout |
| Steel tube EC_tube (steel dome only) | 2.51 | [19] "Steel, welded pipe" |

**Table 5.** Emission factors.

No emission factor for round culms was found. $EC_b$ was derived as the sum of a production term and a transport term. The production term, 0.092, is the geometric mean of 0.0324 (harvest and haul to the processing plant of laminated bamboo panels, from an INBAR report [REF-S7]) and 0.2626 (kiln-dried softwood without carbon storage [19]); the lower value is an assumption, because it is not specific to culms. The transport term is 0.185 kg CO₂e per t·km [REF-S7] over 300 km, multiplied by a factor of 3.8 that accounts for the low bulk density of hollow culms (100 kg/m³ [2]), which gives 0.21. The lower value of the range, 0.09, uses a load factor of 1; the upper value, 1.23, is derived from the impact of bamboo poles reported in [2] and describes long-distance supply to Europe, which does not suit local use.

**Prices** (Table 6). The Indonesian scenario is the main case, because its prices of bamboo, steel and grout come from one document; the Indian, Türkiye and Colombian scenarios are sensitivity cases.

| Scenario | Steel material [USD/kg] | Grout [USD/kg] | Bamboo at reference diameter [USD/m] | Reference diameter [mm] |
|---|---|---|---|---|
| Indonesia 2024 (Jateng HSD) | 1.141 | 0.5388 | 0.2304 | 70 |
| India 2023 (CPWD DSR) | 0.7222 | 0.339 | 0.1459 | 70 |
| Turkiye 2026 (CSB, August) | 0.6894 | 0.3246 | 0.1392 | 70 |
| Colombia 2026 (Guadua, D_ref assumed) | 0.9315 | 0.4389 | 1.583 | 120 |

**Table 6.** Price inputs in USD. The Indonesian prices of bamboo, steel and grout come from one document (Jawa Tengah HSD 2024) and are means over four regencies; the bamboo price is for culms of 6–8 cm diameter and 6 m length. The Jateng HSD and CPWD DSR prices were read from scanned pages [DATA CHECK: visual verification against the pages is not recorded]. The Indian steel and grout prices come from CPWD DSR 2023, where the steel price is the base price of structural steel sections and is applied to tubes, bolts and connection steel; the Indian bamboo price is derived from the Indonesian ratio of bamboo to steel price. The Türkiye steel price is derived from the erected-steel price of ÇŞB (August 2026) with the Indian ratio of erected to material price; its grout and bamboo prices are derived from ratios. The Colombian bamboo price is a 6 m Guadua unit price of 38 500 COP from a supplier web page (2026); the diameter is not stated and $D_{ref}=120$ mm is assumed; its steel and grout prices are the mean of the Indonesian and Indian values. Exchange rates: 82.60 INR (2023), 15 855 IDR (2024) and 47.4925 TRY (mean of two TCMB quotes of 3 August 2026) per USD; 4 053 COP (2025) per USD. The INR, IDR and COP rates are annual averages [DATA CHECK: source files of the rates].

The bamboo prices of the Indian and Türkiye scenarios are derived from the Indonesian prices, and the Colombian steel and grout prices are proxies. The sensitivity scenarios are therefore not independent checks of the main case.

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

**Table S1.** The 24 hollow circular sections of the bamboo catalogue.
