# 3. Numerical examples

This section establishes the benchmark structural applications, material inventories, external action profiles, algorithmic tuning configurations, and life cycle cost/carbon inventories. Three distinct single-layer space dome topologies spanning 16 m to 40 m are evaluated under identical geometry, external loading combinations, and boundary restraints for both bamboo and steel systems, ensuring that differences in structural performance stem strictly from material mechanics and normative design philosophies.

## 3.1 Space dome topologies, geometry, and design grouping

To investigate scale effects and geometric sensitivity, three benchmark space domes encompassing diverse structural typologies were selected: a 16 m geodesic dome, a 32 m Kiewitt dome, and a 40 m ribbed (Schwedler-type) dome. The geometric characteristics, grid layouts, and structural configurations are summarized in Table 1, with the generation algorithms and the wind pressure zoning given in Supplementary Material Appendix S4.

| Dome Topology | Code Designation | Span [m] | Rise [m] | Nodes ($N_n$) | Members ($N_m$) | Design Groups ($N_g$) | Supported Nodes | Member Length Range [m] | $u_{lim}$ [mm] |
|---|---|---|---|---|---|---|---|---|---|
| Geodesic | geodesic16 | 16.0 (nominal) | 3.72 | 46 | 115 | 23 | 20 | 2.24–2.96 | 107 |
| Kiewitt | kiewitt32 | 32.0 | 6.60 | 169 | 456 | 22 | 48 | 2.09–3.55 | 213 |
| Ribbed | ribbed40 | 40.0 | 8.28 | 505 | 1464 | 43 | 48 | 0.76–3.08 | 267 |

**Table 1.** Geometric parameters and modeling properties of the benchmark space domes. $u_{lim} = \text{span}/150$.

The spatial layout of each dome configuration reflects standard spatial truss typologies established in the structural optimization literature [20, 30, 31]:
- **Geodesic Dome (16 m span):** Based on an icosahedral spherical geometry (Class I, subdivision frequency 5) truncated at a colatitude of 50°. The structure features 46 joints and 115 members categorized into 23 independent cross-sectional sizing groups based on latitude rings and 72° five-fold rotational symmetry. All 20 perimeter base joints along the zigzag boundary are pinned in all translational degrees of freedom. Member lengths range between 2.24 m and 2.96 m.
- **Kiewitt Dome (32 m span):** Formed as a spherical cap divided into 8 symmetric circumferential sectors with 6 concentric horizontal rings, encompassing 169 nodes and 456 members. Members are partitioned into 22 design groups according to ring position and radial orientation. The 48 outermost perimeter base nodes are pinned. Member lengths vary from 2.09 m to 3.55 m.
- **Ribbed (Schwedler-type) Dome (40 m span):** Derived from the well-established 40 m, 354-member benchmark space dome extensively investigated in steel optimization literature [20, 30, 31]. The original 354-member geometry has member lengths of 2.94 m to 5.97 m. With the constraints of this study no feasible bamboo design was found for it: with the largest catalogue section in all groups the sum of the normalized constraint violations is P = 9.12, the largest member force of 75.5 kN exceeds the joint capacity of 49.3 kN in 66 members, and three ABC runs from different seeds ended at P = 9.32. A frequency-2 topological densification was therefore applied, generating 505 nodes, 1464 members, and 43 design groups with member lengths strictly constrained between 0.76 m and 3.08 m. The 48 foundation support nodes are pinned.
- **Classical 354-Member Steel Reference Dome:** In addition to the three bio-structural benchmark domes, the classical 40 m span, 354-member, 22-group Schwedler-type steel dome [20, 30, 31] was analyzed under identical loading conditions as an external literature calibration anchor.

Figure 2 illustrates the spatial layouts, plan projections, elevation profiles, and optimal cross-sectional diameter allocations across the three benchmark space domes: (a) 16 m Geodesic dome, (b) 32 m Kiewitt dome, and (c) 40 m Ribbed dome, where each dome panel depicts (i) 3D perspective view, (ii) plan view, and (iii) side elevation view. The generation algorithms of the node coordinates are given in Supplementary Material Appendix S4.

Elastic structural analysis is performed using an in-house direct stiffness solver verified against commercial finite element software (CSI SAP2000 v24). Serviceability displacement thresholds are adopted as an engineering design assumption set to $u_{lim} = \text{span}/150$, adapted from general flexural member serviceability guidance in the IStructE design manual [1] (since neither ISO 22156 nor NSR-10 specifies global roof deflection limits for reticulated spatial structures), yielding limits of 107 mm, 213 mm, and 267 mm, respectively.

## 3.2 Material mechanical properties and discrete profile catalogues

Material properties, allowable stress limits, and design factors for *Guadua angustifolia* bamboo are established in strict accordance with ISO 22156:2021 [36], the IStructE bamboo design manual [1], and NSR-10 Title G [37]. Table 2 presents the material parameters and design factors adopted in the analysis.

| Mechanical / Design Property | Design Value | Codified Source and Justification |
|---|---|---|
| Material density $\rho$ | 700 kg/m³ | ISO 22156 / IStructE Manual Table 4.4; Guadua mean is 680 kg/m³ |
| Characteristic elastic modulus $E_k$ | 10,000 MPa | Conservative baseline from Table 4.4 of [1] |
| Characteristic tensile strength $f_{t,0,k}$ | 40.0 MPa | Table 4.4 of [1] |
| Characteristic compressive strength $f_{c,0,k}$ | 37.8 MPa | Table A3.4 of [1] (Guadua angustifolia database, $n = 922$) |
| Safety factor $FS$ | 2.0 | Appendix A3.6 of [1] for axial truss members |
| Redundancy factor $C_R$ | 0.90 | IStructE Manual Section 6.3 and ISO 22156:2021 Clause 5.4 for single-culm primary members |
| Temperature adjustment factor $C_T$ | 1.00 | Service temperatures $\le 38^\circ\text{C}$ [1] |
| Load duration factors $C_{DF}$ | 0.55 / 0.65 / 0.85 | Permanent (D) / Transient (S) / Instantaneous (W) [1] |
| Ylinen non-linear interaction constant $c$ | 0.80 | Appendix A6.2 of [1] |
| Dimensionless initial culm crookedness $b_0$ | 0.01 | Typical natural bow, yielding $C_{bow} = 0.50$ [1] |
| Effective column length factor $K$ | 1.00 | Table 6.1 of [1] for pin-jointed space truss members |
| Maximum slenderness limit $\lambda_{max}$ | 150 | NSR-10 Section G.12.9.2.6 [37] applied to all members |
| Codified connection joint capacity $F_{j,Rd}$ | 49.3 kN | Nominal baseline from NSR-10 Tables G.12.11-2 and G.12.11-3 for $D \ge 100$ mm ($F_{bolt,adm} = 13.25\text{ kN}$, $n_{bolt} = 4$, $C_g = 0.93$; for $D = 80$ mm NSR-10 specifies 11.54 kN) |
| Maximum nodal deflection limit $u_{lim}$ | $\text{span}/150$ | Engineering design assumption adapted from IStructE Manual guidance [1] (Section 3.1) |

**Table 2.** Mechanical properties, partial factors, and design parameters for the Guadua bamboo space domes.

The discrete bamboo catalogue comprises $n_s = 24$ commercially viable Guadua culm cross-sections, with outer diameters ranging from $D = 80$ mm to $160$ mm and wall thicknesses from $t = 6$ mm to $22$ mm (detailed in Supplementary Material Table S1). 

The baseline joint design specifies four through-bolts ($n_{bolt} = 4$) of grade #5 (5/8 in / 15.9 mm diameter) embedded in an injected mortar/grout core at each member end, providing an allowable design capacity of $F_{j,Rd} = 4 \times 13.25 \times 0.93 = 49.3$ kN pursuant to NSR-10 Title G [37]. Standard bolt spacing requirements in NSR-10 Title G prescribe a minimum pitch of 150 mm between successive bolts and end distances of 150 mm for tension members and 100 mm for compression members. Housing four bolts across both member ends requires $2 \times [e + (n_{bolt}-1)p] = 2 \times [150 + 3 \times 150] = 1.20$ m of culm length, which expands to approximately 1.35 m when maintaining a nominal 150 mm unperforated mid-span clearance between opposite connection zones.

For the benchmark steel domes, the discrete catalogue consists of 37 standard AISC steel pipe sections with yield strength $F_y = 248.2$ MPa, Young's modulus $E = 205$ GPa, and steel density $\rho = 7850$ kg/m³ [20, 34], designed under AISC ASD specifications.

## 3.3 Design loads and ASD load combinations

Applied nominal design load magnitudes (dead, snow, and wind velocity pressure) are adapted from benchmark space dome literature [20, 30, 31]. While classical literature studies evaluated three simplified loading cases under historical ASCE 7-98 provisions, the present study establishes a design basis by evaluating eight unfactored ASD load combinations in strict accordance with ASCE 7-22 [35] (Table 4) applied identically to both bamboo and steel dome configurations:
- **Nominal Dead Load ($D$):** 0.20 kN/m² applied vertically downward on the horizontal projected area.
- **Nominal Snow Load ($S$):** 0.83 kN/m² applied vertically downward on the horizontal projected area.
- **Wind Actions ($W$):** Computed using wind velocity pressure $q_h = 1.115$ kN/m², gust factor $G = 0.85$, and aerodynamic pressure coefficients $C_p$ distributed across three spatial windward, leeward, and crest zones along the wind axis $x$: $C_p = +0.0105$ for $x < -L_d/4$, $C_p = -0.907$ for $|x| \le L_d/4$, and $C_p = -0.50$ for $x > L_d/4$ ($L_d$ is the dome span). Internal pressure coefficients are taken as $GC_{pi} = -0.18$ (pattern $W_N$) and $+0.18$ (pattern $W_P$), producing the net surface pressures documented in Table 3.

| Wind Load Pattern | Windward Zone ($x < -L_d/4$) | Central Crest Zone ($|x| \le L_d/4$) | Leeward Zone ($x > L_d/4$) |
|---|---|---|---|
| Pattern $W_N$ ($GC_{pi} = -0.18$) | $+0.211\text{ kN/m}^2$ | $-0.659\text{ kN/m}^2$ | $-0.273\text{ kN/m}^2$ |
| Pattern $W_P$ ($GC_{pi} = +0.18$) | $-0.191\text{ kN/m}^2$ | $-1.060\text{ kN/m}^2$ | $-0.675\text{ kN/m}^2$ |

**Table 3.** Distributed aerodynamic wind surface pressures. Positive values denote inward pressure.

Surface tributary loads are lumped onto structural joints via surface triangular discretization. Eight unfactored ASD load combinations are systematically evaluated in accordance with ASCE 7-22 [35], as summarized in Table 4.

| No. | Load Combination | Governing Duration Class | $C_{DF}$ | Combined ASD Scaling Factor $k_j$ |
|---|---|---|---|---|
| 1 | $D$ | Permanent | 0.55 | 0.2475 |
| 2 | $D + S$ | Transient | 0.65 | 0.2925 |
| 3 | $D + 0.6W_N$ | Instantaneous | 0.85 | 0.3825 |
| 4 | $D + 0.6W_P$ | Instantaneous | 0.85 | 0.3825 |
| 5 | $D + 0.75S + 0.45W_N$ | Instantaneous | 0.85 | 0.3825 |
| 6 | $D + 0.75S + 0.45W_P$ | Instantaneous | 0.85 | 0.3825 |
| 7 | $0.6D + 0.6W_N$ | Instantaneous | 0.85 | 0.3825 |
| 8 | $0.6D + 0.6W_P$ | Instantaneous | 0.85 | 0.3825 |

**Table 4.** ASD load combinations, duration categories, and resulting capacity factors $k_j$ (Equation 5).

## 3.4 Optimization algorithm execution settings

To ensure equitable computational budgets across topologies of varying dimensionality, each algorithmic run terminates strictly after $NFE = 1000\,N_g$ structural analyses: 23,000 evaluations for the 16 m Geodesic dome, 22,000 for the 32 m Kiewitt dome, and 43,000 for the 40 m Ribbed dome. Population sizes were set to 20 for ABC and 40 for ACO and DO, in relation to the number of design variables (23 to 43) and in line with the practice in [25]. A preliminary tuning study with three to five seeds per setting (Supplementary Material S1.4) ranked ABC first, ACO second and DO third; for the three methods it also found other best-performing sizes on some domes (Table S1.1), and the production runs kept one size for each of the two methods on all domes. 

Every algorithm was independently executed across 30 random seeds (1001–1030) per dome, resulting in 270 full optimization runs for the bamboo domes (3 topologies × 3 algorithms × 30 seeds). For the benchmark steel domes, the ABC algorithm was executed under identical evaluation budgets across the same 30 random seeds for all three benchmark domes and the classical 354-member reference dome, totaling 120 steel optimization runs (4 models × 30 seeds).

## 3.5 Embodied carbon factors and international material cost inventories

**Connection detailing hardware.** The baseline spatial truss connection detailing incorporates a central spherical steel hub of $m_{hub} = 2.0$ kg per node, member-end steel connector assemblies of $m_{end} = 0.5$ kg per member end (threaded stud, washers, nuts, and insert sleeve), and an injected non-shrink cementitious grout infill column of length $L_{grout} = \beta\,D$ with baseline ratio $\beta = 2.5$ and density $\rho_m = 2100$ kg/m³.

**Cradle-to-gate carbon emission factors.** Embodied carbon intensity coefficients (stages A1–A3) are drawn from verified life cycle databases and international technical reports, as summarized in Table 5.

| Structural Component | Emission Factor [kg CO₂e/kg] | Reference Basis and Derivation |
|---|---|---|
| Bamboo culm ($EC_b$) | 0.243 (sensitivity range: 0.0324–1.23) | Author's baseline derivation: cultivation, harvesting and local hauling 0.0324 (0.0156 + 0.0168, INBAR TR35 Table 1 [38]) + regional delivery to site 0.211 ($0.185 \times \frac{300}{1000} \times 3.8$ [2, 42]); sum 0.243; highest value tested 1.23 [2] |
| Connection steel hardware ($EC_s$) | 1.13 | Structural steel plates and sections, A1–A3, declared average of the producing plants [39] |
| Non-shrink cementitious grout ($EC_m$) | 0.310 | SikaGrout-312 HP, A1–A3, declared unit 1 kg [41] |
| Structural steel pipe ($EC_{pipe}$) | 1.701 | Welded hollow structural sections, A1–A3, declared unit 1 tonne [40] |

**Table 5.** Cradle-to-gate embodied carbon emission factors. The steel and grout factors are the values declared in environmental product declarations (EPD) [39–41]. The freight factor of 0.185 kg CO₂e/(t·km) is a value of the author close to the values of 0.1782 (average load) and 0.2146 kg CO₂e/(t·km) (50% load) given for rigid goods vehicles in the UK DESNZ/DEFRA 2023 conversion factors [42] (100% load: 0.1251); the factor 3.8 corrects for the low bulk density of culms (100 kg/m³) relative to the load capacity of the lorry in the inventory [2]. The connection steel factor is the average of the plants of one EPD [39] that expired on 24.10.2023, and the pipe factor is the value of one producer [40]; the plants of [39] range from 0.5 to 2 times its average. The culm factor adds the cultivation, harvesting and plantation-to-factory transport of a laminated bamboo board (0.0156 + 0.0168 kg CO₂e/kg [38]) to the delivery to the site (0.185 × 0.3 × 3.8 = 0.211). The highest culm value tested, 1.23 kg CO₂e/kg, is derived from Table 8 of [2] for bamboo poles including drying, treatment and transport and is not a physical bound.

**Methodological notes on LCI inventory assumptions.** Several inventory assumptions in Table 5 are highlighted for transparency: (i) The European structural steel plate EPD [39] (validity ended October 2023) represents an average across producing plants; to account for plant-level variations between electric arc and blast furnace routes, a broad sensitivity range of 0.5× to 2.0× ($EC_s = 0.565$ to $2.26\text{ kg CO}_2\text{e/kg}$) is evaluated in the parametric sweeps. (ii) The steel pipe factor [40] represents a single North American manufacturer (Welded Tube of Canada) as an indicative baseline for hollow structural sections. (iii) The road freight factor of $0.185\text{ kg CO}_2\text{e/(t}\cdot\text{km)}$ is selected within the UK DEFRA [42] interval ($0.1782$ to $0.2146\text{ kg CO}_2\text{e/(t}\cdot\text{km)}$ for rigid goods vehicles). (iv) The upper-bound culm factor ($1.23\text{ kg CO}_2\text{e/kg}$) is derived from the life-cycle inventory of industrial bamboo poles in [2], incorporating preservation, kiln drying, and transport. The sensitivity sweeps in Section 4.4 evaluate the influence of each assumption across these ranges.




**International material cost scenarios.** Direct material cost parameters are compiled across four developing and emerging market regions to capture geographic cost variations (Table 6). Indonesia serves as the baseline empirical reference market, where regional government schedules of rates (Jawa Tengah HSD 2024, mean of the four regencies Cilacap, Banyumas, Purbalingga and Banjarnegara; exchange rate 15,855 IDR/USD) provide simultaneous local unit rates for bamboo culms, structural steel, and cementitious materials. For sensitivity analysis, illustrative cost models are developed for India (CPWD DSR 2023; 82.60 INR/USD), Türkiye (CSB 2026; 47.49 TRY/USD), and Colombia (price list for immunized Guadua of 27 June 2026, p. 4: 38,500 COP per 6 m unit; exchange rate 4,053 COP/USD, giving 1.583 USD/m; the list gives no diameter). The reference culm prices refer to poles of 60–80 mm diameter (Indonesia, with 70 mm taken as the reference) or to an unspecified diameter assumed as 120 mm (Colombia), and they are scaled to the diameters of the designs with the exponent $\alpha$. In these sensitivity scenarios, Indian and Turkish culm prices are scaled from the empirical Indonesian bamboo-to-steel price ratio; the Turkish steel material price is the erected steel price of the schedule (106.70 TRY/kg) divided by the ratio of the Indian erected to material steel price (3.26), and the Turkish and Indian grout and culm prices follow from Indonesian ratios where the schedule has no item, whereas Colombian steel and grout prices represent an emerging-market proxy (mean of Indonesian and Indian rates) combined with Colombian commercial Guadua pole quotes (Table 6).

| Economic Market Scenario | Structural Steel [$p_s$, USD/kg] | Grout [$p_g$, USD/kg] | Bamboo at $D_{ref}$ [$p_{ref}$, USD/m] | Reference Culm Diameter [$D_{ref}$, mm] |
|---|---|---|---|---|
| Indonesia 2024 (Jateng HSD) | 1.141 | 0.5388 | 0.2304 | 70 |
| India 2023 (CPWD DSR) | 0.7222 | 0.3390 | 0.1459 | 70 |
| Türkiye 2026 (CSB August) | 0.6894 | 0.3246 | 0.1392 | 70 |
| Colombia 2026 (Guadua national) | 0.9315 | 0.4389 | 1.5830 | 120 |

**Table 6.** International material cost inventory in USD. Note: India and Türkiye culm rates are scaled using the baseline Indonesian bamboo-to-steel price ratio; Colombia steel and grout rates represent an emerging-market proxy (Indonesia–India average) paired with Colombian commercial Guadua market quotes.
