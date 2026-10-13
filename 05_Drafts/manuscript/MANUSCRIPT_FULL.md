# Sizing Optimization of Guadua Bamboo Space Domes and the Share of Connection Steel and Grout in Embodied Carbon

> Working draft. Open placeholders in the text: 30. Sources of numbers: `NUMBERS_TRACE.md`. Open decisions and data requests: `OPEN_ITEMS.md`. Source search instructions: `REFERENCE_SEARCH_GUIDE.md`.

## Highlights

- Bamboo and steel space domes sized to their own optimum for a fair comparison
- Single-objective ASD sizing with three metaheuristic algorithms and repeated runs
- Connection steel and grout carry 74–82% of the baseline carbon of the bamboo domes
- The joint carbon share falls to 41–53% at the highest culm emission factor tested
- For these three domes, bamboo systems with grout weigh more than steel systems

## Abstract

Structural bamboo is promoted as a low-carbon alternative to steel, yet comparisons in which both materials are sized to their own optimum under design-code constraints, including the connection hardware, are scarce. This study asks whether Guadua bamboo space domes are lighter, lower in embodied CO₂ and cheaper than steel domes of the same geometry. Three domes with spans of 16, 32 and 40 m were sized in bamboo under allowable stress design based on ISO 22156 and in steel under AISC allowable stress design. The weight was minimized with three metaheuristic algorithms run repeatedly from independent random starts, and the embodied carbon (A1–A3) and the material cost were evaluated for the optimum designs. The bamboo members weigh 0.51–0.68 of the steel members, and the bamboo systems carry 0.25–0.35 of the steel carbon at baseline emission factors. However, the connection steel and the grout carry 74–82% of the carbon of the bamboo domes, and the grout makes the bamboo systems heavier than the steel systems. The carbon share of the connections falls to 41–53% when the emission factor of the culm is raised to the highest value tested, so the conclusion depends on this factor. In the main price scenario, the bamboo dome costs 0.64–1.02 times the steel dome at a diameter-price exponent of 2. A fair assessment of bamboo space structures therefore has to include the connection design.

## Keywords

bamboo structures; Guadua; space truss; sizing optimization; metaheuristic algorithms; embodied carbon

# 1. Introduction

Bamboo culms reach full height within 3–6 months and then mature over 3–6 years, and bamboo fixes carbon in its leaves, stem, roots and surrounding soil. The life cycle of bamboo is described as an attractive resource in the context of the climate emergency [1]. Life-cycle studies of bamboo materials and products are available [2–4]. Bamboo culms have been compared with steel, concrete and timber on environmental and financial grounds [5], and bamboo-based buildings have been compared with brick and concrete buildings [6]. In the latter study, steel and the transport of construction materials accounted for 34.7% and 49.0% of the CO₂-equivalent of a single-storey bamboo house, and the bamboo poles for 6.4% [6].

These studies compare materials or whole buildings. They do not compare load-bearing structures in which bamboo and steel are each sized to their own optimum for the same geometry, loads and design rules. The comparison matters because the weight, cost and carbon of a structure depend on how efficiently each material is used, and for a space structure also on the connection hardware, since such a structure has many member ends. A concrete, structure-level comparison of bamboo with conventional alternatives such as steel and concrete, in cost and CO₂ emission, is, to the authors' knowledge, missing from the literature [REF-S1]. This is the research gap; the present study addresses it for steel.

Connections are a known difficulty of structural bamboo. Bolted–mortar-infill connections are described as one of the most challenging aspects of the design and construction of bamboo structures, because of the uncertainty in the connection strength [7]. Plain bolted connections in tests on Kao Jue culms failed early by brittle splitting, and mortar infill increased the strength but reduced the ductility [8]. The Manual refers to flowable infill, typically cementitious grout [1]. These studies address the strength and ductility of single joints. The mass and carbon that the steel hardware and the grout add to a whole structure, and how they grow with the number of members, are rarely quantified [REF-S2]. Whether the lower weight and carbon of the bamboo members are kept once the connections are included is therefore an open question for space structures.

A fair comparison of two materials needs an objective rule that sizes both. Optimization provides this rule: each structure is brought to its own optimum cross-sections under the same design philosophy, and the optima are compared. Metaheuristic algorithms are widely used for the discrete sizing of steel skeletal structures, including real-size pin-jointed structures [9, 10]. Ant colony optimization and artificial bee colony algorithms have been applied to steel frames and space frames [11–13], and an enhanced dandelion optimizer has been used for steel buildings with reinforced concrete shear cores [14]. Their use for bamboo space structures is not documented [REF-S1].

The research question of this study is: if a Guadua bamboo space dome and a steel dome of the same geometry are each sized to their own optimum under allowable stress design, is the bamboo dome lighter, lower in embodied CO₂ and cheaper once the connection hardware is included? The contribution is threefold: a code-based discrete sizing formulation for bamboo space domes that includes the joint capacity and the connection hardware; an optimum-versus-optimum comparison with steel in weight, embodied carbon and material cost; and a sensitivity analysis of the share of the connection hardware in the embodied carbon.

The aim of the study is to compare bamboo with steel in weight, embodied CO₂ and material cost for space domes. To reach this aim, the following tasks were carried out: (i) the size optimization problem of bamboo and steel domes was formulated with design-code constraints; (ii) the problem was solved on three domes with three metaheuristic algorithms, each run repeatedly from independent random starts; (iii) the embodied carbon and the material cost of the optimum designs were evaluated, including connection steel and grout, and their sensitivity to the assumptions was examined; (iv) bamboo and steel were compared.

Three algorithms and repeated runs were used for the following reasons. Metaheuristic algorithms are stochastic, and their performance varies with the type of problem. The true optimum of these problems is not known in advance. Three different algorithms therefore allow the best design to be cross-checked: confidence in a design increases when independent algorithms reach it. A single run is not sufficient, because the result of one run depends on the random numbers drawn. Each algorithm was therefore run 30 times from independent random seeds. This measures not only the best design that an algorithm can find, but also its stability, consistency and repeatability, which are compared with statistical tests (Section 2.5).

Section 2 states the optimization problem and the evaluation methods. Section 3 describes the numerical examples: the domes, materials, loads and settings. Section 4 gives the results, Section 5 discusses them and their limits, and Section 6 lists the conclusions.

# 2. Optimization problem formulation and solution method

This section states the size optimization problem of a bamboo dome and of the corresponding steel dome, the algorithms and statistical tests used to solve and compare it, and the evaluation of embodied carbon and material cost after the optimization. The domes, materials, loads and numerical settings are given in Section 3.

## 2.1 Design variables

The geometry (nodes, member connectivity and supports) and the loads are fixed. Only the member cross-sections are sized (size optimization). The members are collected into $N_g$ design groups, and all members of a group have the same section. The design vector is

$$\mathbf{x}=[x_1,x_2,\dots,x_{N_g}],\qquad x_\ell\in\{1,2,\dots,n_s\},\tag{1}$$

where $x_\ell$ is the index of the profile of group $\ell$ in a discrete catalogue of $n_s$ sections. The bamboo catalogue has $n_s = 24$ hollow circular Guadua sections and the steel catalogue has $n_s = 37$ AISC pipe sections (Section 3.2). The members are pin-jointed axial-force elements.

## 2.2 Objective function

The objective is the weight of the members (culms for bamboo, tubes for steel):

$$W(\mathbf{x})=g_0\,\rho\sum_{i=1}^{N_m}A_i(\mathbf{x})\,L_i,\tag{2}$$

where $g_0 = 9.81$ m/s² is the acceleration of gravity, $\rho$ is the material density, $A_i$ is the cross-section area of member $i$ (given by the profile index of its group), $L_i$ is its length and $N_m$ is the number of members. The single-objective problem is

$$\min_{\mathbf{x}}\;W(\mathbf{x})\quad\text{subject to}\quad g_k(\mathbf{x})\le 0,\;k=1,\dots,N_c,\tag{3}$$

with the constraints $g_k$ defined in Sections 2.3 and 2.4. Weight is chosen as the objective because it does not depend on price or emission-factor assumptions, which are uncertain and differ between scenarios. The embodied carbon and the material cost are evaluated for the optimum designs (Sections 2.6 and 2.7), and their sensitivity to the assumptions is examined in Section 4.

## 2.3 Constraints of the bamboo dome

All constraints are written in the form $g=\text{demand}/\text{capacity}-1\le 0$. Member $i$ is checked for each of the eight load combinations $j$ (Section 3.3). Let $N_{ij}$ be the axial force (tension positive). The design follows allowable stress design. The allowable member capacity is

$$X_{allow}=\frac{x_k\,C_R\,C_{DF}\,C_T}{FS},\tag{4}$$

where $x_k$ is the characteristic capacity, $C_R$ the redundancy factor, $C_{DF}$ the duration factor of the load combination, $C_T$ the temperature factor and $FS$ the factor of safety (Equation 3.9 of the Manual [1]). Instead of reducing the capacity, the force is divided by the factor $k_j$, which gives the same ratio:

$$k_j=\frac{C_R\,C_{DF,j}\,C_T}{FS},\qquad \tilde N_{ij}=\frac{N_{ij}}{k_j}.\tag{5}$$

**Tension constraints.** The scaled tension is compared with the characteristic tension strength $f_{t,0,k}$ [1]:

$$g^{t}_{ij}(\mathbf{x})=\frac{\max(\tilde N_{ij},0)}{A_i\,f_{t,0,k}}-1\le 0.\tag{6}$$

**Compression and buckling constraints.** The scaled compression is compared with the characteristic Ylinen buckling stress $f_{cr,i}$:

$$g^{c}_{ij}(\mathbf{x})=\frac{\max(-\tilde N_{ij},0)}{A_i\,f_{cr,i}}-1\le 0,\tag{7}$$

$$f_{cr,i}=\frac{f_{c,0,k}+f_{e,i}}{2c}-\sqrt{\left(\frac{f_{c,0,k}+f_{e,i}}{2c}\right)^{2}-\frac{f_{c,0,k}\,f_{e,i}}{c}},\qquad f_{e,i}=\frac{\pi^{2}E_k\,C_{bow}}{\lambda_i^{2}},\tag{8}$$

$$\lambda_i=\frac{K\,L_i}{r_i},\qquad C_{bow}=1-\frac{b_0}{0.02}.\tag{9}$$

Here $f_{c,0,k}$ is the characteristic compression strength, $E_k$ the design modulus, $c$ the Ylinen constant, $\lambda_i$ the slenderness, $K$ the effective length factor, $r_i$ the radius of gyration and $b_0$ the initial bow of the culm. Equation 8 is the Ylinen equation of the Manual (Equations 6.1–6.3, divided by the area), Equation 9 gives the slenderness and the bow reduction factor (Equation 6.4), and the factors of Equation 4 are applied through $k_j$ as in Equation 6.5 [1].

**Slenderness constraint.**

$$g^{s}_{i}(\mathbf{x})=\frac{\lambda_i}{\lambda_{max}}-1\le 0.\tag{10}$$

The limit $\lambda_{max}=150$ is taken from NSR-10 (G.12.9.2.6 and G.12.9.2.7), which prescribes it for compression members [15]. It is applied to all members here.

**Connection constraints.** The joint capacity is checked with the unscaled force, because the allowable bolt loads of the code are already allowable values:

$$g^{n}_{ij}(\mathbf{x})=\frac{|N_{ij}|}{F_{j,Rd}}-1\le 0,\qquad F_{j,Rd}=n_{bolt}\,F_{bolt,adm}\,C_g.\tag{11}$$

$F_{bolt,adm}$ is the allowable load of one bolt in double shear (Table G.12.11-2 of NSR-10), $n_{bolt}$ the number of bolts per member end and $C_g$ the group factor (Table G.12.11-3 of NSR-10) [15]. The values are given in Section 3.2. The same capacity is used for every member.

**Serviceability constraint.**

$$g^{u}(\mathbf{x})=\frac{u_{max}(\mathbf{x})}{u_{lim}}-1\le 0,\tag{12}$$

where $u_{max}$ is the largest absolute nodal displacement over all nodes, all three translation components and all load combinations, and $u_{lim}$ is the displacement limit (Section 3.1).

## 2.4 Constraints of the steel dome

The steel dome is sized with the same objective (Equation 2, $\rho = 7850$ kg/m³), the same design variables and the same load combinations, with unfactored forces and allowable stress design [REF-S6]. Tension, compression, slenderness and serviceability constraints are written in the same form:

$$g^{t}_{ij}=\frac{\max(N_{ij},0)}{0.6\,F_y\,A_i}-1\le 0,\qquad g^{c}_{ij}=\frac{\max(-N_{ij},0)}{F_{a,i}\,A_i}-1\le 0,\qquad g^{s}_{i}=\frac{\lambda_i}{\lambda_{max}}-1\le 0,\tag{13}$$

with $\lambda_{max}=300$ for members in tension and $200$ for members in compression, and $g^{u}$ as in Equation 12. The allowable compressive stress is

$$F_{a}=\frac{\left[1-\dfrac{\lambda^{2}}{2C_c^{2}}\right]F_y}{\dfrac53+\dfrac{3\lambda}{8C_c}-\dfrac{\lambda^{3}}{8C_c^{3}}}\ \ (\lambda<C_c),\qquad F_a=\frac{12\pi^{2}E}{23\,\lambda^{2}}\ \ (\lambda\ge C_c),\qquad C_c=\sqrt{\frac{2\pi^{2}E}{F_y}},\tag{14}$$

where $F_y$ is the yield stress and $E$ the modulus of elasticity [REF-S6]. No connection constraint is imposed on the steel dome.

## 2.5 Constraint handling, algorithms and statistical evaluation

**Penalty function.** The constraints are handled with a penalty that is kept separate from the objective of Equation 3. For member $i$, let $\hat g_i$ be the largest value of $g^t_{ij}$, $g^c_{ij}$, $g^n_{ij}$ (over all combinations $j$) and $g^s_i$. The penalty collects the violation of the most critical member of each group and the violation of the displacement limit:

$$P(\mathbf{x})=\sum_{\ell=1}^{N_g}\max\!\Bigl(0,\max_{i\in\ell}\hat g_i\Bigr)+\max\bigl(0,g^{u}\bigr),\tag{15}$$

and the algorithms minimize the penalized weight

$$F(\mathbf{x})=W(\mathbf{x})\,\bigl(1+P(\mathbf{x})\bigr)^{\varepsilon},\qquad\varepsilon=2.\tag{16}$$

For a feasible design $P=0$ and $F=W$.

**Algorithms.** Three metaheuristic algorithms solve the problem: the artificial bee colony (ABC), ant colony optimization (ACO) and the dandelion optimizer (DO) [16] [REF-S3]. They were implemented in-house for the discrete index vector of Equation 1. Their application to steel structures is documented [11–14]. Because metaheuristics are stochastic, each algorithm is run from 30 independent random seeds on each dome. The best design of all runs is the optimum design of the dome. The 30 values of the best weight of an algorithm show its stability, consistency and repeatability.

**Statistical evaluation.** For each dome, the best weights of the 30 seeds are compared with a seed-blocked Friedman test over the three algorithms [REF-S5]. The algorithm with the lowest mean Friedman rank (ABC in all domes) is compared with each of the other two by a two-sided Mann–Whitney U test with Holm correction over the two comparisons of a dome, at a significance level of 0.05 [REF-S5]. The effect size A12 is the probability that a run of the competing algorithm gives a heavier design than a run of the control algorithm, with ties counted as 0.5 [REF-S5].

## 2.6 Embodied carbon

Embodied carbon covers the stages A1–A3 (cradle to gate). Biogenic carbon storage, use, demolition and recycling are not included. It is evaluated for the optimum design of each dome:

$$E_{CO_2}=EC_b\,m_b+EC_s\,m_s+EC_m\,m_m,\tag{17}$$

where $EC_b$, $EC_s$ and $EC_m$ are the emission factors of the bamboo culm, the connection steel and the grout, and $m_b$, $m_s$ and $m_m$ are the corresponding masses. The culm mass is $m_b=\rho\sum_i A_iL_i$. The connection steel mass is $m_s=m_{hub}N_n+m_{end}\cdot 2N_m$, with a hub mass $m_{hub}$ per node, a hardware mass $m_{end}$ per member end, $N_n$ nodes and $N_m$ members. The grout mass is

$$m_m=\sum_{i=1}^{N_m}2\,\rho_m\,\frac{\pi}{4}\,(D_i-2t_i)^2\,(\beta D_i),\tag{18}$$

which is a grout column of length $\beta D_i$ in the bore of the culm at each end of member $i$, with outer diameter $D_i$, wall thickness $t_i$ and grout density $\rho_m$. For the steel dome, $E_{CO_2}=EC_{tube}m_{tube}+EC_s\,m_s$ with the same connection steel model and no grout. The values of the parameters are given in Section 3.5. The sensitivity of the joint share $(EC_sm_s+EC_mm_m)/E_{CO_2}$ is evaluated for the optimum designs by changing one parameter at a time ($\beta$, $EC_s$, $EC_b$), and in one combined case in which $\beta$, $EC_s$, $EC_b$ and $EC_m$ are changed together in the direction that lowers the joint share.

## 2.7 Material cost

Only material cost is considered; labour, erection and life-cycle costs are not included, for bamboo and for steel. For bamboo,

$$C_{bamboo}=\sum_{i=1}^{N_m}L_i\,p_b(D_i)+p_s\,m_s+p_g\,m_m,\qquad p_b(D)=p_{ref}\left(\frac{D}{D_{ref}}\right)^{\alpha},\tag{19}$$

where $p_b$ is the price of bamboo per metre, scaled from the price $p_{ref}$ at a reference diameter $D_{ref}$ with the exponent $\alpha$, $p_s$ is the steel material price and $p_g$ the grout price. For steel, $C_{steel}=p_s\,(m_{tube}+m_{conn})$. The exponent $\alpha$ is varied between 1.5 and 3. The price inputs are given in Section 3.5.

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

# 4. Results

## 4.1 Algorithm performance

All 270 runs ended with feasible designs (Table 7). The lightest design of each dome weighs 5.800 kN (Geodesic), 41.058 kN (Kiewitt) and 66.352 kN (Ribbed). ABC reached this weight in 5, 30 and 7 of its 30 runs, ACO in 0, 14 and 1 runs, and DO in none. DO gave the heaviest mean weight on every dome.

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

## 4.2 Lightest designs and governing limit states

Table 11 gives the largest demand-to-capacity ratio of each check for the lightest designs. Compression reaches a ratio of 0.992–1.000 in all three designs. The displacement ratio is 0.060, 0.062 and 0.129 of the limit.

| Dome | Tension | Compression | Slenderness | Joint | u/u_lim | Groups with D/C >= 0.95 |
|---|---|---|---|---|---|---|
| Geodesic | 0.165 | 0.996 | 0.733 | 0.280 | 0.060 | 8/23 |
| Kiewitt | 0.361 | 0.992 | 0.532 | 0.543 | 0.062 | 6/22 |
| Ribbed | 0.430 | 1.000 | 0.664 | 0.807 | 0.129 | 9/43 |

**Table 11.** Largest D/C ratio per check in the lightest design of each dome, displacement ratio and number of design groups with D/C ≥ 0.95.

Compression determines the largest D/C ratio in 19 of 23 groups (Geodesic), 21 of 22 (Kiewitt) and 41 of 43 (Ribbed) in the lightest designs. Slenderness determines the remaining groups: 4, 1 and 2. Tension and the joint check determine no group of the lightest designs. Averaged over the 90 feasible runs of each dome, compression determines 81.1%, 95.5% and 93.4% of the groups, slenderness 18.9%, 4.5% and 6.5%, and the joint check 0.2% on Ribbed. Figure 4 shows these shares. The profiles of the lightest designs are in Figure 1.

![Figure 4](../../04_Results/figures/F4_governing_limit_states.png)

**Figure 4.** Share of design groups in which each check gives the largest D/C ratio. Left: lightest design of each dome. Right: mean of the 90 feasible runs of each dome. The checks are tension, compression, slenderness and joint capacity.

![Figure 1](../../04_Results/figures/F1_best_profiles.png)

**Figure 1.** Lightest design of each dome: the lightest feasible design among the 90 runs per dome (3 algorithms × 30 seeds). Bars give the outer diameter D [mm] of each design group (left axis); the line gives the wall thickness t [mm] (right axis). The panel titles give the algorithm that found the design and its weight. ABC found the lightest design of each dome; ACO reached the same weight on Kiewitt and Ribbed.

## 4.3 Bolts required per member

The largest member forces of the lightest designs are 13.82, 26.76 and 39.77 kN (Table 10), below F_j,Rd = 49.3 kN, so most members need one or two bolts (Table 12). No member needs four. On Ribbed, 813 members need one bolt, 591 two and 60 three. Twelve Ribbed members (0.82%), all 0.76 m long, are too short to hold the three bolts they require under the NSR-10 spacing rules; the largest force in these members is 31.25 kN. Eighty-four Ribbed members are shorter than 1.35 m. Geodesic and Kiewitt have no such members; their shortest members are 2.24 m and 2.09 m long.

| Dome | Members | n_req=1 | n_req=2 | n_req=3 | n_req=4 | n_req>4 | Members too short for required bolts | Share [%] | Shortest member [m] | Max force in too-short members [kN] | Members < 1.35 m (4 bolts both ends) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Geodesic | 115 | 115 | 0 | 0 | 0 | 0 | 0 | 0.00 | 2.24 | 0.00 | 0 |
| Kiewitt | 456 | 388 | 68 | 0 | 0 | 0 | 0 | 0.00 | 2.09 | 0.00 | 0 |
| Ribbed | 1464 | 813 | 591 | 60 | 0 | 0 | 12 | 0.82 | 0.76 | 31.25 | 84 |

**Table 12.** Number of bolts required per member end (NSR-10 allowable load, #5 bolt) and members too short to hold them. Lengths and forces in the last columns are in m and kN.

## 4.4 Embodied carbon of the lightest designs

The embodied carbon of the lightest designs is 0.86 t CO₂e (Geodesic), 4.84 t (Kiewitt) and 11.34 t (Ribbed) (Table 13). Connection steel and grout together account for 79.39%, 74.07% and 82.11% of this carbon; connection steel alone accounts for 57.25%, 39.03% and 51.92%. The grout mass is 57%, 65% and 67% of the total mass of culm, steel and grout (derived from Table 13).

| Dome | Bamboo [t] | Steel [t] | Grout [t] | Total [t] | Culm [%] | Steel [% CO2e] | Grout [% CO2e] | Joint (steel+grout) [% CO2e] | Total CO2e [t] |
|---|---|---|---|---|---|---|---|---|---|
| Geodesic | 0.59 | 0.21 | 1.06 | 1.86 | 20.61 | 57.25 | 22.13 | 79.39 | 0.86 |
| Kiewitt | 4.19 | 0.79 | 9.43 | 14.41 | 25.93 | 39.03 | 35.04 | 74.07 | 4.84 |
| Ribbed | 6.76 | 2.47 | 19.02 | 28.26 | 17.89 | 51.92 | 30.19 | 82.11 | 11.34 |

**Table 13.** Mass and carbon breakdown of the lightest design of each dome (baseline parameters: EC_b = 0.30, EC_s = 2.38, EC_m = 0.18 kg CO₂e/kg; β = 2.5).

Table 14 shows the joint share (steel plus grout) when parameters are changed.

| Dome | Base | β = 1.5 | β = 3.5 | EC_steel = 1.2 | EC_steel = 3.0 | EC_bamboo = 0.09 | EC_bamboo = 1.23 | Combined case |
|---|---|---|---|---|---|---|---|---|
| Geodesic | 79.39 | 77.38 | 81.06 | 71.22 | 82.06 | 92.77 | 48.43 | 53.9 |
| Kiewitt | 74.07 | 69.84 | 77.26 | 67.85 | 76.46 | 90.50 | 41.06 | 45.3 |
| Ribbed | 82.11 | 79.65 | 84.04 | 75.91 | 84.24 | 93.86 | 52.82 | 57.7 |

**Table 14.** Joint share of the embodied carbon [%] for the lightest designs. Each column changes one parameter from the baseline; the last column changes β = 1.5, EC_s = 1.2, EC_b = 0.47 and EC_m = 0.12 together. β is the ratio of the grout length to the culm diameter.

The emission factor of the bamboo culm has the largest effect. With EC_b = 0.09 the joint share is 90.50–93.86%; with EC_b = 1.23 it is 41.06–52.82%. The share changes by less than 10 percentage points with β or EC_s alone. The joint share is below 50% for Kiewitt in the combined case (45.3%) and for Kiewitt (41.06%) and Geodesic (48.43%) with EC_b = 1.23.

## 4.5 Comparison with steel

For the same geometry, the weight of the bamboo members is 0.509, 0.677 and 0.634 of the weight of the steel members, and the embodied carbon of the bamboo systems (culm, connection steel and grout) is 0.252, 0.278 and 0.347 of that of the steel systems at the baseline emission factors (Table 16). With EC_b = 1.23 kg CO₂e/kg the three ratios are 0.414, 0.502 and 0.540. With a steel emission factor of 1.6 kg CO₂e/kg they are 0.396, 0.436 and 0.545. The system weights, which include connection steel and grout, are higher for bamboo than for steel (Table 15): 18.211, 141.320 and 277.222 kN for bamboo against 13.434, 68.456 and 128.955 kN for steel (ratios 1.36, 2.06 and 2.15, derived).

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

## 4.6 Material cost

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

# 5. Discussion

## 5.1 Algorithm comparison

ABC had the lowest mean weight and the lowest mean Friedman rank on all three domes. On Kiewitt, all 30 ABC runs ended at the same weight. ACO reached the best weight of ABC on Kiewitt and Ribbed in at least one run, and DO had the highest mean weight on every dome.

The ranking applies to the settings used: NFE = 1000 N_g and population sizes of 20 (ABC), 40 (ACO) and 40 (DO). The tuning study found different best population sizes for some pairs of algorithm and dome (ABC: 20, 20 and 40; ACO: 80, 20 and 80; DO: 40, 80 and 40 for Geodesic, Kiewitt and Ribbed). The ranking may change with other population sizes or budgets. ACO and DO were not tested against each other.

## 5.2 Joint share of the embodied carbon

In the baseline case, connection steel and grout carry 74.1–82.1% of the embodied carbon of the lightest designs (Table 13). This share depends on assumptions. In the one-at-a-time sweeps it ranges from 41.1% to 93.9% (Table 14). The parameter with the largest effect is the emission factor of the bamboo culm, whose lower value (0.09 kg CO₂e/kg) rests on data for laminated bamboo panels (Section 3.5). In the combined case, in which the parameters are changed together in the direction that lowers the joint share, the share is 45.3–57.7%.

The share also depends on the hardware definition of the model: 2.0 kg of steel per node, 0.5 kg per member end and a grout length of 2.5 D. These values are assumptions, and a different joint design would change the share. The grout is 57–67% of the total mass of culm, steel and grout (Section 4.4).

For a single-storey bamboo house, steel accounts for 34.7% and the transport of construction materials for 49.0% of the CO₂-equivalent, and the bamboo poles for 6.4% (Table 2 of [6]). That study has a different structure, functional unit and system boundary, so the values cannot be compared directly. In both studies, most of the CO₂-equivalent does not come from the culms.

## 5.3 Bamboo and steel

In member weight and in embodied carbon, the bamboo designs are lower than the steel designs of the same geometry (Table 16). The carbon ratio of 0.25–0.35 holds for the baseline emission factors; it rises to 0.41–0.54 with EC_b = 1.23 (Section 4.5). With connection steel and grout included, the bamboo systems are heavier (Table 15). The grout alone is 19.02 t of the 28.26 t of the Ribbed system.

The comparison has limits. The steel structures were sized with a different design rule (AISC ASD 1989), a catalogue of 37 pipe sections, slenderness limits of 200 and 300, and no joint capacity check, and they were optimized with one algorithm. The ratios compare optimum designs under different rules and catalogues and are indicative only.

## 5.4 Material cost

In the Indonesian scenario, the main case, the bamboo structure is cheaper than the steel structure for Geodesic at all values of the diameter exponent α, cheaper for Kiewitt for α ≤ 2, and more expensive for Ribbed for α ≥ 2 (Table 17). The bamboo price at structural diameters is not taken directly from a source: it is scaled from a reference diameter, and the ratios depend on α. The grout is a large part of the bamboo material cost. The sensitivity scenarios give higher ratios, the highest for Colombia, where the reference diameter is assumed (Table 18). The Indian and Türkiye bamboo prices are derived from the Indonesian prices, so those scenarios are not independent checks. Labour, erection and life-cycle costs are not included.

## 5.5 Connections

The joint capacity of 49.3 kN follows NSR-10. The IStructE Manual procedure gave about 3–5 kN per bolt in a preliminary calculation (Section 3.2), against 13.25 kN allowable per bolt in NSR-10. If the lower capacity applied, more bolts per member end would be needed, and the hardware masses of the carbon model would no longer hold [DATA NEEDED: IStructE joint calculation record]. The 12 Ribbed members of 0.76 m cannot hold the bolts required under the NSR-10 spacing rules; their joints need a different detail.

## 5.6 Limitations

- The three domes have different spans, topologies and member counts; the results hold for these three models and the 24-section catalogue.
- The culm self-weight, the connection hardware and the grout are not part of the loads.
- C_R = 0.90 (single-culm members) and b₀ = 0.01 are assumptions; λ ≤ 150 is applied to tension members, although NSR-10 prescribes it for compression members only.
- The hub (2.0 kg per node), the hardware at member ends (0.5 kg) and the grout length (2.5 D) are assumptions and are not designed against the member forces.
- The emission factor of the culm has an assumed lower bound, and the grout factor is a proxy for non-shrink grout.
- Only stages A1–A3 are considered; biogenic carbon is excluded.
- The cost covers materials only. The bamboo price at structural diameters is scaled from a reference diameter, and the four price scenarios are not independent.
- The steel reference was designed with different rules and catalogue than the bamboo structures (Section 5.3).
- Connections are modelled as pin joints; joint stiffness and eccentricity are not considered.
- The three algorithms were run with one population size each and one evaluation budget.

# 6. Conclusions

The results hold for the three dome models (spans of 16, 32 and 40 m), the 24-section catalogue, the assumed joint hardware and the stated emission factors.

1. Single-objective ASD sizing gave feasible designs in all 270 runs. The lightest designs weigh 5.800 kN (Geodesic, 115 members), 41.058 kN (Kiewitt, 456 members) and 66.352 kN (Ribbed, 1464 members).
2. ABC had the lowest mean rank on every dome (Friedman p ≤ 4.91 × 10⁻⁹) and was lighter than ACO and DO with Holm-adjusted p ≤ 5.53 × 10⁻⁴. The ranking holds for the population sizes and the evaluation budget used.
3. Compression determines the largest D/C ratio in 19 of 23, 21 of 22 and 41 of 43 design groups of the lightest designs. Tension and the joint check determine none.
4. In the baseline case, connection steel and grout account for 74.1–82.1% of the embodied carbon (A1–A3, biogenic carbon excluded). Changing one parameter at a time gives 41.1–93.9%. The emission factor of the culm has the largest effect. The share is below 50% for Kiewitt in the combined case and for Kiewitt and Geodesic with EC_b = 1.23 kg CO₂e/kg.
5. For the same geometry, the bamboo members weigh 0.51–0.68 of the steel members, and the bamboo systems carry 0.25–0.35 of the steel-system carbon at baseline emission factors (0.41–0.54 with EC_b = 1.23). With connection steel and grout, the bamboo systems weigh 1.36–2.15 times the steel systems.
6. In the Indonesian price scenario, the ratio of bamboo to steel material cost is 0.64 (Geodesic), 0.93 (Kiewitt) and 1.02 (Ribbed) for α = 2, and 0.61–1.15 for α = 1.5–3. Across four price scenarios the ratio ranges from 0.610 to 1.394. The sensitivity scenarios are not independent of the main case.

Future work: a joint design that follows from the member forces, and the inclusion of biogenic carbon and of labour and life-cycle costs.

# References

Entries without a mark were checked against the source document (authors, title, journal, volume, pages, DOI). Entries marked † were taken from the reference list of another document (the paper of Taymuş et al. or the Manual) and have not been checked against the original papers. Placeholders [REF-S#] in the text are explained in the reference search guide.

[1] Trujillo, D., Harries, K., Kaminski, S., Lopez, L.-F., 2025. Manual for the design of bamboo structures to ISO 22156:2021. The Institution of Structural Engineers, London. Version 1.0, November 2025. ISBN 978-1-906335-97-7 (print).

[2] Zea Escamilla, E., Habert, G., 2014. Environmental impacts of bamboo-based construction materials representing global production diversity. Journal of Cleaner Production 69, 117–127. https://doi.org/10.1016/j.jclepro.2014.01.067

[3] Vogtländer, J., van der Lugt, P., Brezet, H., 2010. The sustainability of bamboo products for local and Western European applications. LCAs and land-use. Journal of Cleaner Production 18, 1260–1269. https://doi.org/10.1016/j.jclepro.2010.04.015

[4] Restrepo, A., Becerra, R., Tibaquira G., J.E., 2016. Energetic and carbon footprint analysis in manufacturing process of bamboo boards in Colombia. Journal of Cleaner Production 126, 563–571. https://doi.org/10.1016/j.jclepro.2016.02.144

[5] van der Lugt, P., van den Dobbelsteen, A.A.J.F., Janssen, J.J.A., 2006. An environmental, economic and practical assessment of bamboo as a building material for supporting structures. Construction and Building Materials 20, 648–656. https://doi.org/10.1016/j.conbuildmat.2005.02.023

[6] Zea Escamilla, E., Habert, G., Correal Daza, J.F., Archilla, H.F., Echeverry Fernández, J.S., Trujillo, D., 2018. Industrial or traditional bamboo construction? Comparative life cycle assessment (LCA) of bamboo-based buildings. Sustainability 10 (9), 3096. https://doi.org/10.3390/su10093096

[7] Correal, J.F., Prada, E., Suárez, A., Moreno, D., 2021. Bearing capacity of bolted-mortar infill connections in bamboo and yield model formulation. Construction and Building Materials 305, 124597. https://doi.org/10.1016/j.conbuildmat.2021.124597

[8] Paraskeva, T., Pradhan, N.P.N., Stoura, C.D., Dimitrakopoulos, E.G., 2019. Monotonic loading testing and characterization of new multi-full-culm bamboo to steel connections. Construction and Building Materials 201, 473–483. https://doi.org/10.1016/j.conbuildmat.2018.12.198

[9] Hasançebi, O., et al., 2009. Performance evaluation of metaheuristic search techniques in the optimum design of real size pin jointed structures. Computers & Structures 87 (5–6), 284–302. †

[10] Saka, M.P., Geem, Z.W., 2013. Mathematical and metaheuristic applications in design optimization of steel frame structures: an extensive review. Mathematical Problems in Engineering 2013, 1–33. †

[11] Aydogdu, I., Saka, M.P., 2012. Ant colony optimization of irregular steel frames including elemental warping effect. Advances in Engineering Software 44 (1), 150–169. †

[12] Aydogdu, I., Akin, A., Saka, M.P., 2016. Design optimization of real world steel space frames using artificial bee colony algorithm with Levy flight distribution. Advances in Engineering Software 92, 1–14. †

[13] Saka, M., Aydogdu, I., 2021. Performance evaluation of artificial bee colony algorithm and its variants in the optimum design of steel skeletal structures. Asian Journal of Civil Engineering 22, 73–91. †

[14] Taymuş, R.B., Aydoğdu, İ., Saka, M.P., Kim, S., Geem, Z.W., 2025. Impact of connection types on metaheuristic-based optimum design of 3D steel buildings with RC shear core. International Journal of Steel Structures 25 (5), 1097–1116. https://doi.org/10.1007/s13296-025-00994-0

[15] Ministerio de Ambiente, Vivienda y Desarrollo Territorial, Colombia. Reglamento Colombiano de Construcción Sismo Resistente NSR-10, Título G — Estructuras de madera y estructuras de guadua. [year and publisher details needed]

[16] Zhao, S., et al., 2022. Dandelion optimizer: a nature-inspired metaheuristic algorithm for engineering applications. Engineering Applications of Artificial Intelligence 114, 105075. † [full author list needed]

[17] International Standards Organization, 2021. ISO 22156:2021: Bamboo structures — Bamboo culms — Structural design. ISO, Geneva. † (as listed in the Manual)

[18] American Society of Civil Engineers, 2022. ASCE/SEI 7-22: Minimum design loads and associated criteria for buildings and other structures. [REF-S11]

[19] Circular Ecology, 2026. ICE Database Educational Version 5.0 (June 2026). [REF-S12]
