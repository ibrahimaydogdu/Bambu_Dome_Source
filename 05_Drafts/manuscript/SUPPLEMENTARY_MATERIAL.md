# Supplementary Material: Sizing Optimization of Guadua Bamboo Space Domes and the Share of Connection Steel and Grout in Embodied Carbon

---

## Table of Contents

- [Appendix S1: Metaheuristic Optimization Algorithms and Execution Protocols](#appendix-s1-metaheuristic-optimization-algorithms-and-execution-protocols)
  - [S1.1 Artificial Bee Colony (ABC) Algorithm](#s11-artificial-bee-colony-abc-algorithm)
  - [S1.2 Ant Colony Optimization (ACO)](#s12-ant-colony-optimization-aco)
  - [S1.3 Dandelion Optimizer (DO)](#s13-dandelion-optimizer-do)
  - [S1.4 Algorithmic Parameter Tuning Study](#s14-algorithmic-parameter-tuning-study)
- [Appendix S2: Non-parametric Statistical Hypothesis Testing Framework](#appendix-s2-non-parametric-statistical-hypothesis-testing-framework)
  - [S2.1 Seed-Blocked Friedman Rank-Sum Test](#s21-seed-blocked-friedman-rank-sum-test)
  - [S2.2 Two-Sided Mann–Whitney U Test with Holm-Bonferroni Correction](#s22-two-sided-mannwhitney-u-test-with-holm-bonferroni-correction)
  - [S2.3 Vargha–Delaney Non-parametric Effect Size ($A_{12}$)](#s23-varghadelaney-non-parametric-effect-size-a_12)
- [Appendix S3: Codified Structural Design Formulations and Biomechanical Mechanics](#appendix-s3-codified-structural-design-formulations-and-biomechanical-mechanics)
  - [S3.1 Allowable Stress Design (ASD) Framework (ISO 22156 / IStructE 2025)](#s31-allowable-stress-design-asd-framework-iso-22156--istructe-2025)
  - [S3.2 Non-linear Ylinen Column Buckling Theory](#s32-non-linear-ylinen-column-buckling-theory)
  - [S3.3 Bolted Connection Load Capacity and Geometric Spacing Rules (NSR-10 Title G)](#s33-bolted-connection-load-capacity-and-geometric-spacing-rules-nsr-10-title-g)
  - [S3.4 Discrete Cross-Sectional Culm Catalogue](#s34-discrete-cross-sectional-culm-catalogue)
- [Appendix S4: Space Dome Topological Geometries, Coordinates, and Design Groups](#appendix-s4-space-dome-topological-geometries-coordinates-and-design-groups)
  - [S4.1 Space Dome Topologies and High-Resolution Visual Layouts](#s41-space-dome-topologies-and-high-resolution-visual-layouts)
  - [S4.2 Nodal Geometric Generation Algorithms](#s42-nodal-geometric-generation-algorithms)
  - [S4.3 Wind Pressure Aerodynamic Zoning and Tributary Loading](#s43-wind-pressure-aerodynamic-zoning-and-tributary-loading)
- [Appendix S5: Life Cycle Assessment (LCA) and Regional Cost Inventories](#appendix-s5-life-cycle-assessment-lca-and-regional-cost-inventories)
  - [S5.1 Cradle-to-Gate (A1–A3) Embodied Carbon Inventory](#s51-cradle-to-gate-a1a3-embodied-carbon-inventory)
  - [S5.2 International Economic Market Cost Inventories](#s52-international-economic-market-cost-inventories)

### List of Supplementary Tables
- **Table S1.1:** Summary of the preliminary parameter tuning study
- **Table S1:** Discrete structural catalogue of hollow circular *Guadua angustifolia* culms ($n_s = 24$)

---

# Appendix S1: Metaheuristic Optimization Algorithms and Execution Protocols

This section details the theoretical background, mathematical update operators, and discrete adaptation of the three metaheuristic algorithms evaluated in the study: the Artificial Bee Colony (ABC) algorithm, Ant Colony Optimization (ACO), and the Dandelion Optimizer (DO).

## S1.1 Artificial Bee Colony (ABC) Algorithm

The Artificial Bee Colony algorithm, introduced by Karaboga and Basturk [26], mimics the intelligent foraging behavior of honeybee swarms. In the discrete structural optimization formulation, the food sources correspond to candidate discrete design vectors $\mathbf{x} = [x_1, x_2, \dots, x_{N_g}]$, where each $x_\ell \in \{1, 2, \dots, n_s\}$ represents a discrete profile index. The colony consists of three functional groups: employed bees, onlooker bees, and scout bees.

### Employed Bee Phase
Each employed bee is associated with a specific food source $\mathbf{x}_m$ ($m = 1, \dots, N_p$, where $N_p$ is the population size). An employed bee explores the discrete neighborhood by perturbing a randomly chosen design variable $k \in \{1, \dots, N_g\}$ according to:

$$v_{m,k} = \text{round}\left( x_{m,k} + \phi_{m,k}\,(x_{m,k} - x_{r,k}) \right) \tag{S1}$$

where $r \in \{1, \dots, N_p\}$ is a randomly selected distinct food source ($r \ne m$), and $\phi_{m,k}$ is a uniform random real number drawn from $[-1, 1]$. The perturbed value $v_{m,k}$ is clamped to the discrete catalogue bounds $[1, n_s]$. A greedy selection is performed between $\mathbf{x}_m$ and the candidate vector $\mathbf{v}_m$: if the penalized weight $F(\mathbf{v}_m) \le F(\mathbf{x}_m)$, the food source is updated to $\mathbf{v}_m$ and its trial counter is reset to 0; otherwise, the trial counter is incremented by 1.

### Onlooker Bee Phase
Onlooker bees wait in the hive and select food sources based on their relative fitness values $fit_m$:

$$fit_m = \begin{cases} \dfrac{1}{1 + F(\mathbf{x}_m)} & \text{if } F(\mathbf{x}_m) \ge 0 \\[8pt] 1 + |F(\mathbf{x}_m)| & \text{if } F(\mathbf{x}_m) < 0 \end{cases} \tag{S2}$$

The probability $p_m$ of selecting food source $m$ is evaluated via roulette-wheel selection:

$$p_m = \frac{fit_m}{\sum_{j=1}^{N_p} fit_j} \tag{S3}$$

Once an onlooker bee selects a food source based on $p_m$, it produces a neighbor solution using the identical neighborhood operator, followed by greedy selection.

### Scout Bee Phase and Abandonment Limit
If a food source cannot be improved over a predefined threshold known as the abandonment limit:

$$limit = N_p \times N_g \tag{S4}$$

it is abandoned. The associated employed bee becomes a scout bee and initializes a completely new food source uniformly at random across the discrete search space:

$$x_{m,\ell} = \text{rand\_int}(1, n_s), \qquad \ell = 1, \dots, N_g \tag{S5}$$

## S1.2 Ant Colony Optimization (ACO)

Ant Colony Optimization, formalized by Dorigo et al. [27], simulates the collective foraging dynamics of ant colonies using indirect chemical communication mediated by artificial pheromone trails.

### Pheromone Representation and Heuristic Desirability
For each design group $\ell \in \{1, \dots, N_g\}$ and available discrete section candidate $s \in \{1, \dots, n_s\}$, a pheromone level $\tau_{\ell,s} \ge 0$ is maintained. The heuristic desirability $\eta_{\ell,s}$ is inversely proportional to the profile index $s$, favoring lighter, smaller cross-sections:

$$\eta_{\ell,s} = \frac{1}{s} \tag{S6}$$

### Ant Path Construction
Each artificial ant constructs a complete structural design vector $\mathbf{x} = [x_1, \dots, x_{N_g}]$ by selecting a profile for each design group sequentially according to the probability distribution:

$$p_{\ell,s} = \frac{\left[\tau_{\ell,s}\right]^\alpha \left[\eta_{\ell,s}\right]^\beta}{\sum_{k=1}^{n_s} \left[\tau_{\ell,k}\right]^\alpha \left[\eta_{\ell,k}\right]^\beta} \tag{S7}$$

where $\alpha$ is the pheromone sensitivity exponent ($\alpha = 1.0$), and $\beta$ is the heuristic visibility exponent ($\beta = 0.5$).

### Pheromone Evaporation and Global Update
After all ants in the population have constructed their design solutions and their penalized objective weights $F(\mathbf{x})$ have been evaluated, pheromone levels evaporate at rate $\rho = 0.20$:

$$\tau_{\ell,s} \leftarrow \max\left((1 - \rho)\,\tau_{\ell,s},\, \tau_{\min}\right) \tag{S8}$$

where $\tau_{\min} = 0.01$ is the lower pheromone threshold enforced to avoid search stagnation.

Pheromone reinforcement is deposited exclusively by the elite fraction (top 20% best-performing ants) of the current generation, alongside the global best solution found since the start of search:

$$\Delta\tau_{\ell,s} = \sum_{k \in \text{Elite}} \frac{Q}{F(\mathbf{x}_k)}, \qquad \tau_{\ell,s} \leftarrow \tau_{\ell,s} + \Delta\tau_{\ell,s} \tag{S9}$$

where $Q$ is an arbitrary scaling constant.

## S1.3 Dandelion Optimizer (DO)

The Dandelion Optimizer, proposed by Zhao et al. [28], is a recent bio-inspired metaheuristic that models the long-distance seed dispersal of dandelions across atmospheric airflow layers.

### Rising Stage (Ascent in Wind Fields)
Depending on weather humidity and wind turbulence, dandelion seeds ascend under laminar or turbulent wind conditions. Under clear conditions with convective updrafts, the position update is modeled as:

$$\mathbf{x}_{m}^{t+1} = \mathbf{x}_{m}^{t} + \alpha \cdot v_x \cdot v_y \cdot \ln Y \cdot (\mathbf{x}_s^{t} - \mathbf{x}_{m}^{t}) \tag{S10}$$

where $\mathbf{x}_s^{t}$ is a randomly selected position, $v_x, v_y$ are wind lift coefficients, and $\ln Y$ is a log-normal perturbation. Under windy conditions, ascent is governed by turbulent eddy vortices.

### Descending Stage (Descent in Still Air)
In the descending stage, seeds drift downward following an adjusted trajectory that reflects the average swarm location:

$$\mathbf{x}_{m}^{t+1} = \mathbf{x}_{m}^{t} - \beta_t \cdot \left( \frac{1}{N_p}\sum_{j=1}^{N_p}\mathbf{x}_j^t - \alpha_t \cdot \mathbf{x}_m^t \right) \tag{S11}$$

### Landing Stage (Lévy Flight Search)
Upon approaching the terrain, landing sites are explored using a Lévy flight random walk to avoid premature trapping:

$$\mathbf{x}_{m}^{t+1} = \mathbf{x}_{best}^{t} + 0.1 \cdot \text{Lévy}(\beta) \cdot \alpha_t \cdot \left( \mathbf{x}_{best}^{t} - \mathbf{x}_{m}^{t} \cdot \frac{2 t}{T} \right) \tag{S12}$$

where $\beta = 1.5$ is the Lévy exponent. After each continuous position update, coordinates are rounded to the nearest integer index and bounded within $[1, n_s]$.

## S1.4 Algorithmic Parameter Tuning Study

Prior to the production optimization campaign, an independent algorithmic parameter tuning investigation was conducted across three population sizes ($N_p \in \{20, 40, 80\}$) and six metaheuristic candidates (ABC, ACO, DO, Grey Wolf Optimizer [GWO], Whale Optimization Algorithm [WOA], and Teaching-Learning-Based Optimization [TLBO]). The Geodesic and Kiewitt domes used seeds 2001–2005; the Ribbed dome used seeds 2001–2003 and only ABC, ACO and DO. Table S1.1 gives the mean best penalized weight of each algorithm at its best population size and the resulting rank.

| Candidate Algorithm | Geodesic (16 m): mean best penalized weight [kN] (rank, best pop) | Kiewitt (32 m): mean best penalized weight [kN] (rank, best pop) | Ribbed (40 m): mean best penalized weight [kN] (rank, best pop) | Mean rank | Selected for Campaign |
|---|---|---|---|---|---|
| ABC | 5.894 (1, pop 20) | 41.058 (1, pop 20) | 66.359 (1, pop 40) | 1.00 | **Yes** |
| ACO | 6.111 (2, pop 80) | 41.956 (2, pop 20) | 66.592 (2, pop 80) | 2.00 | **Yes** |
| DO | 6.426 (4, pop 40) | 42.769 (3, pop 80) | 73.652 (3, pop 40) | 3.33 | **Yes (recent benchmark)** |
| GWO | 6.221 (3, pop 80) | 43.828 (5, pop 80) | not run | 4.00 | No |
| WOA | 6.511 (5, pop 80) | 43.128 (4, pop 40) | not run | 4.50 | No |
| TLBO | 7.264 (6, pop 80) | 83.226 (6, pop 80) | not run | 6.00 | No |

**Table S1.1.** Summary of the preliminary parameter tuning study (Geodesic and Kiewitt: five seeds; Ribbed: three seeds). The production campaign used population sizes of 20 for ABC and 40 for ACO and DO.

---

# Appendix S2: Non-parametric Statistical Hypothesis Testing Framework

To systematically evaluate the performance differences among stochastic search algorithms, non-parametric statistical hypothesis testing was implemented in accordance with guidelines by Derrac et al. [32].

## S2.1 Seed-Blocked Friedman Rank-Sum Test

The Friedman test evaluates whether statistically significant differences exist across multiple algorithms applied to the identical set of 30 independent random starting seeds (matched seed-blocked design). Let $r_i^j$ be the rank of algorithm $j$ on seed $i$ ($i = 1, \dots, n$; $j = 1, \dots, k$, with $n = 30$ and $k = 3$). The average rank of algorithm $j$ is:

$$R_j = \frac{1}{n}\sum_{i=1}^{n} r_i^j \tag{S13}$$

The Friedman test statistic $\chi_F^2$ is evaluated as:

$$\chi_F^2 = \frac{12\,n}{k(k+1)}\left[ \sum_{j=1}^{k} R_j^2 - \frac{k(k+1)^2}{4} \right] \tag{S14}$$

Under the null hypothesis $H_0$ that all algorithms perform equivalently, $\chi_F^2$ follows a chi-square distribution with $k - 1 = 2$ degrees of freedom. A $p$-value less than $\alpha = 0.05$ leads to the rejection of $H_0$.

## S2.2 Two-Sided Mann–Whitney U Test with Holm-Bonferroni Correction

When the Friedman test detects significant differences, post-hoc pairwise comparisons between the control algorithm (ABC) and competing methods (ACO, DO) are conducted using the two-sided Mann–Whitney U test. The test statistic $U$ evaluates the ranks of combined sample runs:

$$U_1 = R_1 - \frac{n_1(n_1 + 1)}{2}, \qquad U = \min(U_1, n_1 n_2 - U_1) \tag{S15}$$

To control the family-wise error rate across multiple pairwise comparisons ($m = 2$ per dome), the Holm-Bonferroni step-down correction is applied. Raw $p$-values are sorted in ascending order $p_{(1)} \le p_{(2)}$. Each $p_{(i)}$ is compared against:

$$\alpha_{(i)} = \frac{\alpha}{m - i + 1} \tag{S16}$$

If $p_{(1)} < \alpha / 2$, the first hypothesis is rejected and testing proceeds to $p_{(2)} < \alpha$.

## S2.3 Vargha–Delaney Non-parametric Effect Size ($A_{12}$)

The Vargha–Delaney $A_{12}$ statistic [33] quantifies the probability that a random run of algorithm $A$ yields a heavier structural weight than a random run of algorithm $B$:

$$A_{12} = \frac{R_1 - \dfrac{n_1(n_1 + 1)}{2}}{n_1\,n_2} \tag{S17}$$

where $R_1$ is the rank sum of algorithm $A$. An effect size of $A_{12} = 0.50$ indicates stochastic equality; $A_{12} > 0.50$ indicates that algorithm $A$ is stochastically heavier (inferior) than algorithm $B$. In Table 9 the effect size of 'ABC vs X' is reported as $A_{12}$ with the competing algorithm X as $A$, i.e. the probability that X gives the heavier design.

---

# Appendix S3: Codified Structural Design Formulations and Biomechanical Mechanics

## S3.1 Allowable Stress Design (ASD) Framework (ISO 22156 / IStructE 2025)

The allowable load capacity for axial bamboo members is formulated in accordance with Equation 3.9 of the IStructE Bamboo Design Manual [1]:

$$X_{allow} = \frac{x_k\,C_R\,C_{DF}\,C_T}{FS} \tag{S18}$$

where:
- $x_k$ = characteristic material capacity ($f_{c,0,k} = 37.8$ MPa, $f_{t,0,k} = 40.0$ MPa),
- $C_R = 0.90$ = structural redundancy factor (applied assuming single-culm primary members without structural load sharing, pursuant to IStructE Manual Section 6.3 and ISO 22156:2021 Clause 5.4),
- $C_T = 1.00$ = temperature factor for ambient service temperatures $\le 38^\circ\text{C}$,
- $FS = 2.00$ = global factor of safety for axial load-carrying culms,
- $C_{DF}$ = load duration factor, taking values of 0.55 for permanent dead load ($D$), 0.65 for transient snow load ($S$), and 0.85 for instantaneous wind actions ($W$).

## S3.2 Non-linear Ylinen Column Buckling Theory

Because natural bamboo culms are anisotropic, thin-walled biological cylinders, flexural column buckling deviates from classical Euler theory. Ylinen's formulation [1, 36] incorporates elastoplastic material nonlinearity:

$$f_{cr} = \frac{f_{c,0,k} + f_e}{2c} - \sqrt{\left(\frac{f_{c,0,k} + f_e}{2c}\right)^2 - \frac{f_{c,0,k}\,f_e}{c}} \tag{S19}$$

$$f_e = \frac{\pi^2 E_k\,C_{bow}}{\lambda^2}, \qquad \lambda = \frac{K\,L}{r}, \qquad C_{bow} = 1 - \frac{b_0}{0.02} \tag{S20}$$

where:
- $c = 0.80$ is the Ylinen interaction parameter (empirically calibrated for full-culm Guadua),
- $b_0 = 0.01$ is the non-dimensional initial culm crookedness ratio,
- $K = 1.00$ is the effective length factor for pinned-ended truss members,
- $r = \sqrt{I/A} = \sqrt{(D^2 + (D - 2t)^2)} / 4$ is the radius of gyration.

## S3.3 Bolted Connection Load Capacity and Geometric Spacing Rules (NSR-10 Title G)

Connection load-carrying capacity is evaluated following Title G of the Colombian building code NSR-10 [37]. For a culm with mortar-filled ends connected by $n_{bolt}$ through-bolts in double shear:

$$F_{j,Rd} = n_{bolt} \cdot F_{bolt,adm} \cdot C_g \tag{S21}$$

where $F_{bolt,adm} = 13.25$ kN is the codified allowable load for a single 5/8 in (#5, 15.9 mm diameter) steel bolt in a 100 mm diameter Guadua culm (Table G.12.11-2; note that for $D = 80$ mm NSR-10 specifies 11.54 kN), and $C_g = 0.93$ is the group modification factor for four consecutive fasteners (Table G.12.11-3). The design allowable connection capacity is thus $F_{j,Rd} = 4 \times 13.25 \times 0.93 = 49.3$ kN.

### Spacing Requirements
To prevent longitudinal splitting along parallel fibers, NSR-10 mandates:
- Minimum bolt pitch parallel to fiber: $p \ge 150$ mm,
- Minimum end distance for tension members: $e_t \ge 150$ mm,
- Minimum end distance for compression members: $e_c \ge 100$ mm.

The codified minimum culm length required to house $n$ bolts at both member ends without overlapping is:

$$L_{min,code} = 2 \left[ e + (n - 1)\,p \right] \tag{S22}$$

For $n = 4$ bolts with $e = 150$ mm and $p = 150$ mm, $L_{min,code} = 2 \times [150 + 3 \times 150] = 1200$ mm ($1.20$ m); for $n = 3$ bolts, $L_{min,code} = 2 \times [150 + 2 \times 150] = 900$ mm ($0.90$ m). In actual construction, maintaining a nominal unperforated mid-span clearance of $p_{mid} \approx 150$ mm between the two end grout cores expands the practical required member lengths to approximately $1.35$ m and $1.05$ m, respectively.

## S3.4 Discrete Cross-Sectional Culm Catalogue

Table S1 lists the geometric properties of the 24 discrete *Guadua angustifolia* culm sections utilized in the optimization campaign.

| Profile Index ($s$) | Outer Diameter $D$ [mm] | Wall Thickness $t$ [mm] | Inner Diameter $d$ [mm] | Cross-Section Area $A$ [mm²] | Moment of Inertia $I$ [$10^4$ mm⁴] | Radius of Gyration $r$ [mm] |
|---|---|---|---|---|---|---|
| 1 | 80 | 6 | 68 | 1394.9 | 96.1 | 26.25 |
| 2 | 80 | 9 | 62 | 2007.5 | 128.5 | 25.30 |
| 3 | 80 | 12 | 56 | 2563.5 | 152.8 | 24.41 |
| 4 | 90 | 7 | 76 | 1825.3 | 158.3 | 29.45 |
| 5 | 90 | 10 | 70 | 2513.3 | 204.2 | 28.50 |
| 6 | 90 | 14 | 62 | 3342.7 | 249.5 | 27.32 |
| 7 | 100 | 7 | 86 | 2045.2 | 222.4 | 32.97 |
| 8 | 100 | 10 | 80 | 2827.4 | 289.8 | 32.02 |
| 9 | 100 | 14 | 72 | 3782.5 | 359.0 | 30.81 |
| 10 | 110 | 8 | 94 | 2563.5 | 335.4 | 36.17 |
| 11 | 110 | 11 | 88 | 3421.2 | 424.3 | 35.22 |
| 12 | 110 | 15 | 80 | 4476.8 | 517.6 | 34.00 |
| 13 | 120 | 8 | 104 | 2814.9 | 443.6 | 39.70 |
| 14 | 120 | 12 | 96 | 4071.5 | 601.0 | 38.42 |
| 15 | 120 | 16 | 88 | 5227.6 | 723.5 | 37.20 |
| 16 | 130 | 9 | 112 | 3421.2 | 629.6 | 42.90 |
| 17 | 130 | 13 | 104 | 4778.4 | 827.7 | 41.62 |
| 18 | 130 | 18 | 94 | 6333.5 | 1018.7 | 40.11 |
| 19 | 140 | 10 | 120 | 4084.1 | 867.9 | 46.10 |
| 20 | 140 | 15 | 110 | 5890.5 | 1167.1 | 44.51 |
| 21 | 140 | 20 | 100 | 7539.8 | 1394.9 | 43.01 |
| 22 | 160 | 10 | 140 | 4712.4 | 1331.2 | 53.15 |
| 23 | 160 | 15 | 130 | 6833.0 | 1815.0 | 51.54 |
| 24 | 160 | 22 | 116 | 9537.9 | 2328.2 | 49.41 |

**Table S1.** Discrete structural catalogue of hollow circular *Guadua angustifolia* culms ($n_s = 24$).

---

# Appendix S4: Space Dome Topological Geometries, Coordinates, and Design Groups

## S4.1 Space Dome Topologies and High-Resolution Visual Layouts

The three benchmark space dome topologies evaluated in this research represent standard structural forms spanning varying geometric scales:
1. **16 m Geodesic Dome (geodesic16):** 46 nodes, 115 members, 23 design groups, 20 pinned base supports, span-to-rise ratio $L_d/H = 4.30$.
2. **32 m Kiewitt Dome (kiewitt32):** 169 nodes, 456 members, 22 design groups, 48 pinned base supports, span-to-rise ratio $L_d/H = 4.85$.
3. **40 m Ribbed Dome (ribbed40):** 505 nodes, 1464 members, 43 design groups, 48 pinned base supports, span-to-rise ratio $L_d/H = 4.83$.

The high-resolution isometric 3D perspectives, orthogonal plan views, elevation profiles, and the optimal culm outer diameter allocations obtained from the metaheuristic optimization campaign are illustrated in Figure 2 of the main manuscript (panels a, b, and c).

## S4.2 Nodal Geometric Generation Algorithms

### Geodesic Dome Generation
The geodesic geometry is constructed by subdividing the triangular faces of a regular spherical icosahedron using Class I alternate breakdown at frequency $\nu = 5$, projecting intermediate vertices onto a sphere of radius $R = 10.45$ m. The sphere is truncated at a colatitude of $\theta = 50^\circ$, creating a zigzag perimeter base boundary with 20 support nodes.

### Kiewitt Dome Generation
The Kiewitt cap is generated on a spherical cap of radius $R = 22.70$ m spanning a base diameter of 32.0 m and rise of 6.60 m. The geometry is partitioned into 8 cyclic radial sectors and 6 concentric horizontal latitude rings. Diagonal bracing is arranged in alternating orientations within each sector to ensure kinematic triangulated stability.

### Ribbed (Schwedler-type) Dome Generation
The 40 m ribbed dome geometry is generated on a spherical surface of radius $R = 28.29$ m with a crown rise of 8.28 m. The structure features 24 meridional ribs and 10 horizontal rings. In the frequency-2 densified model, each original trapezoidal grid quadrilateral is subdivided into four triangulated sub-panels, reducing peak member lengths from 5.97 m to 3.08 m to comply with structural culm transportability.

## S4.3 Wind Pressure Aerodynamic Zoning and Tributary Loading

Wind loads are distributed across three distinct aerodynamic pressure zones along the wind axis $x$:
- **Windward Zone ($x < -L_d/4$):** Characterized by positive pressure / slight suction, $C_p = +0.0105$.
- **Central Crest Zone ($|x| \le L_d/4$):** Dominated by intense aerodynamic uplift suction over the crown, $C_p = -0.907$.
- **Leeward Zone ($x > L_d/4$):** Characterized by wake vortex suction, $C_p = -0.500$.

Combined with velocity pressure $q_h = 1.115$ kN/m², gust effect factor $G = 0.85$, and internal pressure coefficients $GC_{pi} = \pm 0.18$, the nodal tributary loads are calculated by integrating surface pressures over triangular facets and assigning one-third of the resultant facet load to each of its three vertex nodes.

---

# Appendix S5: Life Cycle Assessment (LCA) and Regional Cost Inventories

## S5.1 Cradle-to-Gate (A1–A3) Embodied Carbon Inventory

The cradle-to-gate life cycle stages (EN 15978) evaluated in this study encompass raw material extraction (A1), transport to processing facility (A2), and structural component manufacturing (A3). 

### Bamboo Culm Emission Factor ($EC_b$)
The baseline culm carbon intensity ($EC_b = 0.243$ kg CO₂e/kg) is derived as:

$$EC_b = EC_{proc} + EC_{trans} \tag{S23}$$

1. **Cultivation, harvesting and local hauling ($EC_{proc} = 0.0324$ kg CO₂e/kg):** In INBAR Technical Report No. 35 (MOSO TP35 [38], Table 1), cultivation and harvesting from the plantation contribute $0.0156$ kg CO₂e/kg and transport from the plantation to the strip manufacturing facility contributes $0.0168$ kg CO₂e/kg. The sum is $EC_{proc} = 0.0324$ kg CO₂e/kg. The table refers to a laminated bamboo board; the two upstream steps are taken here as the upstream burden of the culm.
2. **Regional delivery to the construction site ($EC_{trans} = 0.211$ kg CO₂e/kg):** The delivery of the culms from a regional processing site to the construction site is assumed to take place over 300 km by road. The freight factor of $0.185$ kg CO₂e per t·km is a value of the author close to the factors of $0.1782$ (average load) and $0.2146$ kg CO₂e per t·km (50% load) given for rigid goods vehicles in the UK DESNZ/DEFRA 2023 conversion factors [42]; the factor for a 100% load is $0.1251$. The correction factor of 3.8 accounts for the low bulk density of bamboo poles (about 100 kg/m³), which fills the lorry in volume before the load capacity is reached: the lorry carries 2.5 t instead of 9.5 t [2].

$$EC_{trans} = 0.185 \times \frac{300}{1000} \times 3.8 = 0.2109 \approx 0.211\text{ kg CO}_2\text{e/kg} \tag{S24}$$

The two terms describe different transport legs: the plantation-to-factory leg in $EC_{proc}$ and the delivery to the site in $EC_{trans}$. The sum is $0.0324 + 0.211 = 0.243$ kg CO₂e/kg. The sensitivity analysis uses a lower bound of $0.0324$ kg CO₂e/kg (upstream steps only, no delivery) and a highest value of $1.23$ kg CO₂e/kg. This value is obtained from Table 8 of Zea Escamilla and Habert [2] for bamboo poles: 12.37 mPt per m³ of poles, converted with the normalization factor of 9.95 t CO₂e per point given in [2] and divided by the bulk density of 100 kg/m³. The inventory includes drying, treatment and the mean transport of that study; the value is used as the highest culm factor tested and is not a physical bound.

### Steel Hardware and Grout Factors
- Connection steel plates, threaded studs and sleeves: $EC_s = 1.13$ kg CO₂e/kg. This is the A1–A3 global warming potential of 1 t of structural steel plates and open sections ($1.13 \times 10^{3}$ kg CO₂e) in the EPD of bauforumstahl e.V. [39, p. 7]. The EPD states that the results of single plants range from 0.5 times (electric arc furnace route) to 2 times (blast furnace route) of this average, which is the basis of the range of the steel factor in the sensitivity analysis. The EPD was valid until 24.10.2023.
- Structural steel pipe: $EC_{pipe} = 1.701$ kg CO₂e/kg, the A1–A3 value of 1701.06 kg CO₂e per tonne of welded hollow structural sections of one producer [40, p. 7].
- Cementitious non-shrink grout: $EC_m = 0.310$ kg CO₂e/kg, the A1–A3 value for 1 kg of SikaGrout-312 HP [41, p. 10].
- The sensitivity range of the steel factor (0.565 to 2.26 kg CO₂e/kg) is 0.5 to 2 times the declared value of the plate. The same range is applied to the grout factor (0.155 to 0.62 kg CO₂e/kg) as an assumption of the study; the EPD does not give a range for grout.


## S5.2 International Economic Market Cost Inventories

Direct structural material expenditures are surveyed across four international economic regions:
- **Indonesia (Baseline Market):** Jawa Tengah Harmonized Unit Rate Schedule (HSD 2024; exchange rate 15,855 IDR/USD), reporting regional government-verified unit rates for bamboo culms (6–8 cm diameter, 6 m length: 0.2304 USD/m), structural steel (1.141 USD/kg), and packaged cement grout (0.5388 USD/kg).
- **India:** Central Public Works Department Delhi Schedule of Rates (CPWD DSR 2023; exchange rate 82.60 INR/USD), with structural steel at 0.7222 USD/kg and grout at 0.3390 USD/kg. Bamboo culm price (0.1459 USD/m) is scaled using the baseline Indonesian bamboo-to-steel price ratio.
- **Türkiye:** Ministry of Environment, Urbanisation and Climate Change (CSB August 2026 unit prices; exchange rate 47.49 TRY/USD), with structural steel at 0.6894 USD/kg and grout at 0.3246 USD/kg. Bamboo culm price (0.1392 USD/m) is scaled using the baseline Indonesian bamboo-to-steel price ratio.
- **Colombia:** Regional Guadua market quotations (2026; exchange rate 4,053 COP/USD), reporting 38,500 COP per 6 m pole ($D_{ref} \approx 120$ mm), yielding $38,500 / (6 \times 4,053) = 1.583$ USD/m. Structural steel (0.9315 USD/kg) and cement grout (0.4389 USD/kg) represent an emerging-market proxy calculated as the unweighted mean of Indonesian and Indian rates.


