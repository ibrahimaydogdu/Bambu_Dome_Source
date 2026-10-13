# 2. Materials and Methods

## 2.1. Dome Topology and Structural Modelling

Three single-layer spatial dome configurations spanning 40.0 m<!-- 00_System/DOCS_UPDATE_PROMPT.md:48 --> with a rise of 8.0 m<!-- 00_System/DOCS_UPDATE_PROMPT.md:48 --> (span-to-rise ratio of 5:1) are investigated: Ribbed, Kiewitt, and Geodesic. In the computational model and data records, these topologies are designated as `ribbed40`, `kiewitt32`, and `geodesic16`, respectively:
- **Ribbed dome (`ribbed40`):** Adapted from the 40 m<!-- 00_System/DOCS_UPDATE_PROMPT.md:48 --> ribbed configuration of Saka (1991)<!-- [REF NEEDED: Saka 1991] --> with a frequency of 2<!-- CAMPAIGN_EXECUTION_PLAN.md:18 -->. The model comprises 505 nodes<!-- T10 -->, 1464 members<!-- T10 -->, and 43 sizing design groups<!-- T4 -->. Member lengths vary between 0.76 m<!-- T10 --> and 3.08 m<!-- T5 -->.
- **Kiewitt dome (`kiewitt32`):** A Kiewitt-8 pattern with 4 rings, comprising 169 nodes<!-- CAMPAIGN_EXECUTION_PLAN.md:18 -->, 456 members<!-- T10 -->, and 22 sizing design groups<!-- T4 -->. Member lengths range from 2.09 m<!-- T10 --> to 3.55 m<!-- T5 -->.
- **Geodesic dome (`geodesic16`):** An icosahedron-derived geodesic breakdown comprising 46 nodes<!-- CAMPAIGN_EXECUTION_PLAN.md:18 -->, 115 members<!-- T10 -->, and 23 sizing design groups<!-- T4 -->. Member lengths range from 2.24 m<!-- T10 --> to 2.96 m<!-- T5 -->.

All dome members are modelled as pin-jointed truss elements carrying purely axial tension or compression, with rotational end releases ($M_x = M_y = M_z = 0$)<!-- 03_Code_Execution/DEVELOPER_PROMPT.md:31 -->. Pin supports are applied at all perimeter ground boundary nodes, restraining translations in the $X$, $Y$, and $Z$ directions while permitting rotations. Elastic structural analyses are conducted using an internal direct stiffness matrix formulation implemented in NumPy/SciPy, with cross-verification against CSI SAP2000 v24 via the Open API<!-- 03_Code_Execution/DEVELOPER_PROMPT.md:4 -->.

## 2.2. Bamboo Material Properties and Discrete Section Catalog

The structural elements are specified as round culms of *Guadua angustifolia* Kunth, a woody bamboo native to northern South America. The physical and mechanical properties are defined in accordance with ISO 22156:2021<!-- [REF: ISO 22156:2021] --> and the IStructE Bamboo Design Manual (Trujillo et al., 2025)<!-- [REF: Trujillo et al. 2025] -->:
- Mean modulus of elasticity: $E_k = 10\,000\text{ MPa}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> (Table 4.4 of Trujillo et al., 2025<!-- [REF: Trujillo et al. 2025] -->).
- Bulk density: $\rho = 700\text{ kg/m}^3$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->.
- Characteristic compressive strength parallel to fibers: $f_{c,0,k} = 37.8\text{ MPa}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> based on testing of $n = 922$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> specimens (Table 4.4 of Trujillo et al., 2025<!-- [REF: Trujillo et al. 2025] -->).
- Characteristic tensile strength parallel to fibers: $f_{t,0,k} = 40.0\text{ MPa}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->.

A discrete catalog of 24 commercial *Guadua* section sizes is established based on regional morphological data<!-- 03_Code_Execution/bamboo_catalog.py -->. Outer diameters ($D$) range from 80 mm<!-- 00_System/DOCS_UPDATE_PROMPT.md:49 --> to 160 mm<!-- 00_System/DOCS_UPDATE_PROMPT.md:49 -->, with wall thicknesses ($t$) varying between 6 mm<!-- 00_System/DOCS_UPDATE_PROMPT.md:49 --> and 22 mm<!-- 00_System/DOCS_UPDATE_PROMPT.md:49 -->. Cross-sectional area $A$, moment of inertia $I$, and radius of gyration $r$ are calculated assuming annular cylindrical geometry:
$$A = \frac{\pi}{4}\left(D^2 - (D - 2t)^2\right) = \pi t (D - t)$$
$$I = \frac{\pi}{64}\left(D^4 - (D - 2t)^4\right)$$
$$r = \sqrt{\frac{I}{A}} = \frac{1}{4}\sqrt{D^2 + (D - 2t)^2}$$

## 2.3. Structural Design Constraints and ASD Formulation

Member sizing is governed by the Allowable Stress Design (ASD) method prescribed in ISO 22156:2021<!-- [REF: ISO 22156:2021] --> and Trujillo et al. (2025)<!-- [REF: Trujillo et al. 2025] -->. Design allowable stresses ($X_{\text{allow}}$) are determined from characteristic values through:
$$X_{\text{allow}} = \frac{X_k \cdot C_R \cdot C_{DF} \cdot C_T}{FS}$$
where:
- $FS = 2.0$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> is the global factor of safety on member capacity (IStructE Manual Equation 3.9<!-- [REF: Trujillo et al. 2025] -->).
- $C_R = 0.90$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> is the reduction factor representing culm taper and initial geometric imperfections, adopted as an assumed baseline value<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->.
- $C_T = 1.0$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> is the temperature adjustment factor for ambient service below 30 °C<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->.
- $C_{DF}$ is the duration of load factor: $0.55$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> for permanent (dead) loads, $0.65$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> for snow load (two-month duration), and $0.85$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> for short-duration wind loads (IStructE Manual Table 3.2<!-- [REF: Trujillo et al. 2025] -->).

Under any load combination $j$, the allowable compressive stress ($f_{c,0,\text{allow},j}$) accounts for column stability using Ylinen's equation (ISO 22156:2021 Clause 9.3; Trujillo et al., 2025, Eq. 6.2<!-- [REF: Trujillo et al. 2025] -->):
$$f_{c,0,\text{allow},j} = \frac{f_{c,0,\text{allow}} + \sigma_{cr,j}}{2c} - \sqrt{\left(\frac{f_{c,0,\text{allow}} + \sigma_{cr,j}}{2c}\right)^2 - \frac{f_{c,0,\text{allow}} \cdot \sigma_{cr,j}}{c}}$$
where $c = 0.8$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> is Ylinen's imperfection factor for natural bamboo culms, and $\sigma_{cr,j}$ is the Euler buckling stress with out-of-straightness reduction:
$$\sigma_{cr,j} = \frac{\pi^2 E_{\text{allow},j}}{\lambda^2 \left(1 + \frac{C_{\text{bow}} \cdot b_0 \cdot \lambda}{\pi}\right)}$$
Here, the effective length factor is $K = 1.0$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> for pin-ended members; slenderness is $\lambda = K L / r$; $C_{\text{bow}} = 0.5$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->; and initial bow imperfection $b_0 = 0.01$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> (assumed value corresponding to $L/1000$<!-- 04_Results/PAPER_METHODS_NOTES.md:5 -->). Allowable modulus is $E_{\text{allow},j} = E_k \cdot C_R \cdot C_{DF,j} \cdot C_T / FS$.

Five demand-to-capacity (DCR) constraints are evaluated across all members $i = 1, \dots, N_m$ and load combinations $j = 1, \dots, N_c$:
1. **Axial Tension:**
   $$DCR_{\text{tens},i,j} = \frac{N_{i,j}}{A_i \cdot f_{t,0,\text{allow},j}} \le 1.0 \quad (\text{for } N_{i,j} > 0)$$
2. **Axial Compression and Buckling:**
   $$DCR_{\text{buck},i,j} = \frac{|N_{i,j}|}{A_i \cdot f_{c,0,\text{allow},j}} \le 1.0 \quad (\text{for } N_{i,j} < 0)$$
3. **Geometric Slenderness:**
   $$DCR_{\text{slend},i} = \frac{\lambda_i}{150} \le 1.0$$
   A limit of $\lambda \le 150$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 --> is enforced across all elements. In NSR-10 Título G (G.12.9.2.6)<!-- [REF: NSR-10 Titulo G] -->, this limit is mandatory for compression columns only. Imposing it on tension members as well is a conservative design decision adopted here<!-- 04_Results/PAPER_METHODS_NOTES.md:6 -->.
4. **End Connector Capacity:**
   $$DCR_{\text{joint},i,j} = \frac{|N_{i,j}|}{F_{j,Rd}} \le 1.0$$
   where $F_{j,Rd} = 49.3\text{ kN}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:51 --> is the allowable connection strength derived in Section 2.4.
5. **Serviceability Vertical Deflection (SLS):**
   $$DCR_{\text{disp},k} = \frac{|u_{z,k}|}{u_{\text{allow}}} \le 1.0 \quad \text{where } u_{\text{allow}} = \frac{\text{Span}}{150} = \frac{40\,000\text{ mm}}{150} = 266.67\text{ mm}<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->$$
   evaluated at all free nodes $k$ under unfactored service gravity combinations (Trujillo et al., 2025, Section 6.5<!-- [REF: Trujillo et al. 2025] -->).

## 2.4. Hybrid End Connector Mechanics and Capacity

Because natural hollow culms cannot transfer high concentrated nodal loads directly through bearing, a bolted, mortar-injected steel connector is implemented at each member end, consistent with common construction practice (e.g., Trujillo et al., 2025<!-- [REF: Trujillo et al. 2025] -->; Correal et al., 2021<!-- [REF: Correal et al. 2021] -->). The joint consists of an internal steel gusset plate inserted into the culm end, through-bolts, and a non-shrink cementitious grout infill injected over length $L_{\text{inj}} = 2.5 D$<!-- 04_Results/LCA_SENSITIVITY_REPORT.md:16 --> to prevent longitudinal splitting.

Connection capacity is calculated according to NSR-10 Título G (G.12.11)<!-- [REF: NSR-10 Titulo G] -->:
$$F_{j,Rd} = n_{\text{bolt}} \cdot F_{\text{bolt},\text{adm}} \cdot C_g$$
Using four $\varnothing 5/8"$<!-- 00_System/DOCS_UPDATE_PROMPT.md:51 --> (15.9 mm) Grade A307 bolts in double shear through a $D = 100\text{ mm}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:51 --> culm:
- Allowable single-bolt shear load from NSR-10 Tabla G.12.11-2<!-- [REF: NSR-10 Titulo G] --> is $F_{\text{bolt},\text{adm}} = 13.25\text{ kN}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:51 -->.
- Group action factor from NSR-10 Tabla G.12.11-3<!-- [REF: NSR-10 Titulo G] --> for $n_{\text{bolt}} = 4$<!-- 00_System/DOCS_UPDATE_PROMPT.md:51 --> bolts in a row is $C_g = 0.93$<!-- 00_System/DOCS_UPDATE_PROMPT.md:51 -->.
- Hence, the member allowable joint capacity is:
  $$F_{j,Rd} = 4 \times 13.25\text{ kN} \times 0.93 = 49.3\text{ kN}<!-- 00_System/DOCS_UPDATE_PROMPT.md:51 -->$$

While alternative formulations such as the IStructE Manual yield 3–5 kN/bolt when applying ductile reduction factors<!-- 04_Results/PAPER_METHODS_NOTES.md:11 -->, NSR-10 represents codified Colombian design practice for Guadua connections.

## 2.5. Loading Combinations

Loading criteria are based on ASCE 7-22 unfactored ASD combinations:
- Dead load ($D$): Culm self-weight computed from volume and bulk density ($\rho = 700\text{ kg/m}^3$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->) plus roof cladding $D_{\text{clad}} = 0.25\text{ kN/m}^2$<!-- 00_System/DOCS_UPDATE_PROMPT.md:52 -->.
- Snow load ($S$): Uniform roof snow of $S = 0.75\text{ kN/m}^2$<!-- 00_System/DOCS_UPDATE_PROMPT.md:52 -->; asymmetric snow is applied to half the dome span ($0.75\text{ kN/m}^2$ on one half, zero on the other)<!-- 00_System/DOCS_UPDATE_PROMPT.md:52 -->.
- Wind load ($W$): Basic velocity pressure producing windward pressure $W_p = +0.60\text{ kN/m}^2$<!-- 00_System/DOCS_UPDATE_PROMPT.md:52 --> and leeward suction $W_s = -0.90\text{ kN/m}^2$<!-- 00_System/DOCS_UPDATE_PROMPT.md:52 -->.

Eight standard ASD load combinations are solved:
1. $D$ ($C_{DF} = 0.55$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->)
2. $D + S_{\text{uniform}}$ ($C_{DF} = 0.65$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->)
3. $D + S_{\text{asymmetric}}$ ($C_{DF} = 0.65$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->)
4. $D + W$ ($C_{DF} = 0.85$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->)
5. $D + 0.75 S_{\text{uniform}} + 0.75 W$ ($C_{DF} = 0.85$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->)
6. $D + 0.75 S_{\text{asymmetric}} + 0.75 W$ ($C_{DF} = 0.85$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->)
7. $0.6 D + W$ ($C_{DF} = 0.85$<!-- 00_System/DOCS_UPDATE_PROMPT.md:50 -->, uplift check)
8. $D + S_{\text{uniform}}$ (SLS deflection evaluation, $C_{DF} = 1.0$<!-- 02_Methods/MATHEMATICAL_FORMULATION.md:38 -->)

## 2.6. Optimization Formulation and Metaheuristic Solvers

The structural optimization problem is formulated as a single-objective discrete sizing minimization:
$$\min_{\mathbf{x} \in \mathcal{S}^{N_g}} f_{\text{pen}}(\mathbf{x}) = W_{\text{bamboo}}(\mathbf{x}) \cdot \left(1 + P(\mathbf{x})\right)^\varepsilon$$
where $\mathbf{x} = [x_1, x_2, \dots, x_{N_g}]$ is the vector of discrete section indices mapping each group to one of the 24 catalog profiles; $W_{\text{bamboo}}$ is total culm weight [kN]; $\varepsilon = 2.0$<!-- 00_System/DOCS_UPDATE_PROMPT.md:55 --> is the penalty exponent; and $P(\mathbf{x})$ is the cumulative constraint violation penalty:
$$P(\mathbf{x}) = \sum_{i=1}^{N_m} \max\left(0, \max_j DCR_{\text{tens},i,j} - 1\right) + \sum_{i=1}^{N_m} \max\left(0, \max_j DCR_{\text{buck},i,j} - 1\right) + \sum_{i=1}^{N_m} \max\left(0, DCR_{\text{slend},i} - 1\right) + \sum_{i=1}^{N_m} \max\left(0, \max_j DCR_{\text{joint},i,j} - 1\right) + \sum_{k=1}^{N_n} \max\left(0, DCR_{\text{disp},k} - 1\right)$$

Three metaheuristic optimization algorithms selected from initial population tuning (`04_Results/TUNING_STUDY.md`<!-- 00_System/DOCS_UPDATE_PROMPT.md:56 -->) are deployed:
1. **Artificial Bee Colony (ABC):** Swarm intelligence simulating foraging behaviors, population size $N_p = 20$<!-- 00_System/DOCS_UPDATE_PROMPT.md:56 -->.
2. **Ant Colony Optimization (ACO):** Pheromone-guided stochastic discrete path construction, population size $N_p = 40$<!-- 00_System/DOCS_UPDATE_PROMPT.md:56 -->.
3. **Dandelion Optimizer (DO):** A physics-inspired metaheuristic based on dandelion seed flight dynamics (Zhao et al., 2022<!-- [REF NEEDED: Zhao et al. 2022] -->), population size $N_p = 40$<!-- 00_System/DOCS_UPDATE_PROMPT.md:56 -->.

A strict evaluation budget is enforced across all runs: $\text{NFE} = 1000 \times N_g$<!-- 00_System/DOCS_UPDATE_PROMPT.md:56 --> function evaluations. Specifically:
- `geodesic16` ($N_g = 23$): $\text{NFE} = 23\,000$<!-- T1 -->
- `kiewitt32` ($N_g = 22$): $\text{NFE} = 22\,000$<!-- T1 -->
- `ribbed40` ($N_g = 43$): $\text{NFE} = 43\,000$<!-- T1 -->

Each algorithm-topology pair is executed across 30 independent random seeds (seeds 1001–1030<!-- 00_System/DOCS_UPDATE_PROMPT.md:56 -->), generating 270 independent campaign runs<!-- 00_System/DOCS_UPDATE_PROMPT.md:57 -->.

## 2.7. Statistical Evaluation Protocol

Performance differences among the algorithms are evaluated non-parametrically across the 30 independent seeds:
1. **Friedman Rank Test:** A block-design rank analysis is conducted to determine overall significance among the three algorithms across seeds for each topology.
2. **Pair-wise Mann-Whitney U Test (Wilcoxon Rank-Sum):** Two-sided tests evaluate pairwise differences between ABC, ACO, and DO. Family-wise error rate is controlled using Holm's step-down adjustment ($\alpha = 0.05$<!-- 00_System/DOCS_UPDATE_PROMPT.md:58 -->).
3. **Vargha-Delaney Effect Size ($A_{12}$):** The non-parametric effect magnitude is quantified:
   $$A_{12} = \frac{U_1}{n_1 n_2}$$
   where $A_{12} = 0.5$ denotes stochastic equality, $A_{12} > 0.71$ indicates a large effect size favoring algorithm 1, and $A_{12} = 1.0$ indicates complete dominance across all seeds.

## 2.8. Life Cycle Assessment (A1–A3) Embodied Carbon Model

Embodied carbon ($ECO_2e$) is evaluated using a cradle-to-gate (A1–A3) system boundary encompassing raw material extraction, harvesting, processing, and transportation to the factory gate. In line with conservative reporting, biogenic carbon sequestration during culm growth and end-of-life disposal scenarios (A4–C4) are excluded.

Total embodied carbon is decomposed into three component masses:
$$ECO_2e = m_{\text{culm}} \cdot EC_b + m_{\text{steel}} \cdot EC_s + m_{\text{mortar}} \cdot EC_m$$
where:
- **Bamboo culm ($EC_b$):** Baseline value of $0.30\text{ kg CO}_2\text{e/kg}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:64 --> culm, derived from combined harvesting/processing ($0.092\text{ kg/kg}$<!-- 04_Results/EC_BAMBOO_METHOD.md:10 -->) and regional road transportation over 300 km<!-- 04_Results/EC_BAMBOO_METHOD.md:20 --> ($0.211\text{ kg/kg}$<!-- 04_Results/EC_BAMBOO_METHOD.md:20 -->; $f_{\text{load}} = 3.8$<!-- 04_Results/EC_BAMBOO_METHOD.md:13 --> based on hollow culm bulk density of $100\text{ kg/m}^3$<!-- 04_Results/EC_BAMBOO_METHOD.md:13 -->; Zea Escamilla & Habert, 2014<!-- [REF: Zea Escamilla & Habert 2014] -->). Sensitivity bounds span $0.09\text{ kg/kg}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:64 --> (local supply, 50 km<!-- 04_Results/EC_BAMBOO_METHOD.md:19 -->) to $1.23\text{ kg/kg}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:64 --> (intercontinental transport to Europe; Zea Escamilla & Habert, 2014<!-- [REF: Zea Escamilla & Habert 2014] -->). The lower production bound ($0.0324\text{ kg/kg}$<!-- 04_Results/EC_BAMBOO_METHOD.md:8 -->) is an assumption based on harvesting data from INBAR TR35<!-- [REF NEEDED: INBAR TR35] -->.
- **Connection steel plates and bolts ($EC_s$):** $2.38\text{ kg CO}_2\text{e/kg}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:64 -->, obtained from ICE Educational Database V5.0 (Circular Ecology, June 2026<!-- [REF: ICE Database V5.0] -->) for structural steel plate.
- **Non-shrink cementitious grout ($EC_m$):** $0.18\text{ kg CO}_2\text{e/kg}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:64 -->, adopted from ICE Educational V5.0<!-- [REF: ICE Database V5.0] --> as a proxy (1:3 cement-sand mortar; grout density $\rho_m = 2100\text{ kg/m}^3$<!-- 06_Review_Audit/agent_02_reviewer.md:36 -->).
- **Steel pipe benchmark members ($EC_{s,\text{pipe}}$):** $2.51\text{ kg CO}_2\text{e/kg}$<!-- 00_System/DOCS_UPDATE_PROMPT.md:64 --> for welded structural steel pipe from ICE Educational V5.0<!-- [REF: ICE Database V5.0] -->.

The steel hardware mass at each joint includes an internal gusset plate ($0.5\text{ kg}$<!-- 06_Review_Audit/agent_02_reviewer.md:36 --> per member end), central hub connector ($2.0\text{ kg}$<!-- 06_Review_Audit/agent_02_reviewer.md:36 --> per dome node), and four bolts. Mortar injection volume is calculated as $V_m = \frac{\pi}{4}(D - 2t)^2 \cdot L_{\text{inj}}$ at both ends of each member.

## 2.9. Material Cost Estimation Framework

Economic evaluation is restricted strictly to material procurement cost (culms, steel fittings, and grout); labor, fabrication, and life cycle maintenance are excluded. Because commercial structural bamboo pricing varies with diameter, prices are estimated using an exponential scaling relationship:
$$C_{\text{culm}}(D) = C_{\text{ref}} \left(\frac{D}{D_{\text{ref}}}\right)^\alpha$$
where $C_{\text{ref}}$ is the baseline unit price at reference diameter $D_{\text{ref}} = 70\text{ mm}$<!-- T9a --> ($120\text{ mm}$<!-- T9a --> for Colombia), and $\alpha$ is a size scaling exponent ($\alpha \in \{1.5, 2.0, 2.5, 3.0\}$<!-- T9 -->, baseline $\alpha = 2.0$<!-- 04_Results/PAPER_METHODS_NOTES.md:23 -->).

Four country cost models are analyzed using documented institutional price schedules (Table 9a<!-- T9a -->):
1. **Indonesia 2024:** Based on Jawa Tengah HSD (2024)<!-- [REF NEEDED: Jawa Tengah HSD 2024] -->: bamboo culm ($0.2304\text{ USD/m}$<!-- T9a --> at $D=70\text{ mm}$), structural steel ($1.141\text{ USD/kg}$<!-- T9a -->), and cementitious grout ($0.5388\text{ USD/kg}$<!-- T9a -->).
2. **India 2023:** CPWD Delhi Schedule of Rates (DSR 2023)<!-- [REF NEEDED: CPWD DSR 2023] -->: structural steel ($0.7222\text{ USD/kg}$<!-- T9a -->), grout ($0.3390\text{ USD/kg}$<!-- T9a -->), and bamboo ($0.1459\text{ USD/m}$<!-- T9a -->, derived from Indonesia bamboo-to-steel ratio $r_b = 0.202$<!-- T9a -->).
3. **Turkiye 2026:** Ministry of Environment (CSB, August 2026)<!-- [REF NEEDED: Turkiye CSB 2026] -->: structural steel ($0.6894\text{ USD/kg}$<!-- T9a -->), grout ($0.3246\text{ USD/kg}$<!-- T9a -->), and bamboo ($0.1392\text{ USD/m}$<!-- T9a -->).
4. **Colombia 2026:** Market pricing for 6 m Guadua culms ($1.583\text{ USD/m}$<!-- T9a -->, assuming $D_{\text{ref}} = 120\text{ mm}$<!-- T9a -->), with steel and grout taken as average proxy values ($0.9315\text{ USD/kg}$<!-- T9a --> and $0.4389\text{ USD/kg}$<!-- T9a -->).

## 2.10. Conventional Steel Benchmark Domes

To benchmark the structural efficiency and carbon intensity of bamboo, four structural steel dome designs are evaluated under identical loading and boundary conditions:
- **Reference 354-member ribbed dome:** A 40 m<!-- 00_System/DOCS_UPDATE_PROMPT.md:48 --> spatial dome topology widely studied in structural optimization literature (Hasançebi et al., 2009<!-- [REF NEEDED: Hasançebi et al. 2009] -->; Saka, 1991<!-- [REF NEEDED: Saka 1991] -->), comprising 127 nodes and 354 members divided into 22 design groups. Member selection is drawn from 37 standard AISC steel pipes (AISC ASD-89, A36 steel with $F_y = 248.2\text{ MPa}$<!-- [REF NEEDED: AISC ASD-89] -->, $E = 200\text{ GPa}$, $\rho = 7850\text{ kg/m}^3$).
- **Identical-geometry steel counterparts:** Steel designs optimized on the exact geometries of `geodesic16` (115 members<!-- T5 -->), `kiewitt32` (456 members<!-- T5 -->), and `ribbed40` (1464 members<!-- T5 -->) using the same 37 AISC pipe sections under the same ASCE 7-22 ASD load combinations and $u_{\max} \le \text{Span}/150$<!-- 04_Results/PAPER_METHODS_NOTES.md:28 --> deflection limit.
