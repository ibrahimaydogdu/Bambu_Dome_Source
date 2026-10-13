# 4. Results

This section presents the comparative optimization findings across the three dome topologies, detailing algorithmic convergence, statistical hypothesis testing, governing biomechanical limit states, bolt count requirements, embodied carbon balances, and international material cost trade-offs.

## 4.1 Metaheuristic algorithm convergence and statistical benchmark

All 270 optimization runs executed for the bamboo space domes successfully identified strictly feasible structural designs satisfying all normative strength, stability, slenderness, joint, and deflection constraints (Table 7). The lightest feasible design identified for each topology weighs 5.800 kN for the 16 m Geodesic dome, 41.058 kN for the 32 m Kiewitt dome, and 66.352 kN for the 40 m Ribbed dome. The ABC algorithm reached these absolute minimum weights in 5, 30, and 7 of its 30 runs, respectively. ACO attained the global minimum in 0, 14, and 1 runs, while DO did not locate the minimum on any dome. DO consistently produced the highest mean structural weight across all three models.

| Dome Topology | Optimizer | Feasible Runs | Best Weight [kN] | Median Weight [kN] | Mean Weight [kN] | Std. Dev. [kN] | Worst Weight [kN] | NFE Budget | Mean Execution Time [min] |
|---|---|---|---|---|---|---|---|---|---|
| Geodesic | ABC | 30/30 | 5.800 | 5.894 | 5.880 | 0.051 | 5.980 | 23,000 | 0.39 |
| Geodesic | ACO | 30/30 | 5.842 | 6.122 | 6.183 | 0.311 | 7.151 | 23,000 | 0.83 |
| Geodesic | DO | 30/30 | 6.178 | 6.448 | 6.488 | 0.209 | 7.168 | 23,000 | 0.54 |
| Kiewitt | ABC | 30/30 | 41.058 | 41.058 | 41.058 | 0.000 | 41.058 | 22,000 | 1.69 |
| Kiewitt | ACO | 30/30 | 41.058 | 41.761 | 42.281 | 1.393 | 45.422 | 22,000 | 2.13 |
| Kiewitt | DO | 30/30 | 41.348 | 43.045 | 42.922 | 0.876 | 44.482 | 22,000 | 1.84 |
| Ribbed | ABC | 30/30 | 66.352 | 66.365 | 66.452 | 0.194 | 67.000 | 43,000 | 12.16 |
| Ribbed | ACO | 30/30 | 66.352 | 67.050 | 66.908 | 0.474 | 67.741 | 43,000 | 13.77 |
| Ribbed | DO | 30/30 | 71.803 | 74.394 | 74.404 | 1.396 | 77.079 | 43,000 | 12.66 |

**Table 7.** Best structural weight statistics across 30 independent runs per algorithm and dome topology (seeds 1001–1030).

Figure 3 shows the mean and best penalized weight convergence profiles as a function of the number of function evaluations (NFE). The mean best penalized weight is given at fractions of the evaluation budget in the following. On the Geodesic dome, ABC is lower than DO from 5% of the budget onward (6.80 and 8.52 kN at 10% of the budget). On the Kiewitt and Ribbed domes, DO holds lower means than ABC at 5% of the budget (48.8 and 95.6 kN against 2419 and 395 kN), because ABC and ACO still hold infeasible designs at that stage; at 25% of the budget ABC is lower than DO on both domes (41.65 and 67.39 kN against 45.03 and 83.75 kN). The mean best weight of DO changes by less than 0.1% between 75% and 100% of the budget and ends above ABC on every dome (6.49, 42.92 and 74.40 kN against 5.88, 41.06 and 66.45 kN), whereas ABC still improves between 75% and 100% by 0.7%, 0.0% and 0.3%. ACO follows ABC closely and finishes about 1.2 kN above the mean weight of ABC on Kiewitt (Table 7).

The statistical dispersion of the best structural weights across the 30 independent seeds is illustrated in Figure 4. ABC shows zero variance on the Kiewitt dome across all 30 seeds and narrow interquartile ranges on both the Geodesic and Ribbed domes.

The seed-blocked Friedman test rejected the null hypothesis of equal algorithmic performance across all three topologies ($p < 10^{-8}$, Table 8). ABC achieved the lowest mean rank (1.100, 1.233, and 1.250), followed by ACO (2.000, 2.033, and 1.750) and DO (2.900, 2.733, and 3.000).

| Dome Topology | Friedman Statistic ($\chi^2_F$) | $p$-value | Mean Rank ABC | Mean Rank ACO | Mean Rank DO |
|---|---|---|---|---|---|
| Geodesic | 48.600 | $2.80 \times 10^{-11}$ | 1.1000 | 2.0000 | 2.9000 |
| Kiewitt | 38.264 | $4.91 \times 10^{-9}$ | 1.2333 | 2.0333 | 2.7333 |
| Ribbed | 49.160 | $2.11 \times 10^{-11}$ | 1.2500 | 1.7500 | 3.0000 |

**Table 8.** Seed-blocked Friedman non-parametric rank test results on optimal weights across 30 random seeds.

In the pairwise post-hoc Mann–Whitney U tests with Holm correction, ABC proved statistically superior to both ACO and DO across all domes at $\alpha = 0.05$ (Table 9). The maximum Holm-adjusted $p$-value was $5.53 \times 10^{-4}$ (ABC versus ACO on the 40 m Ribbed dome). The Vargha–Delaney effect size $A_{12} = 1.000$ confirmed that a random run of DO has a probability of 1.0 of being heavier than a run of ABC.

| Dome Topology | Pairwise Comparison | Median Difference [kN] | Mann–Whitney $U$ | Raw $p$-value | Effect Size $A_{12}$ | Holm-Adjusted $p$-value |
|---|---|---|---|---|---|---|
| Geodesic | ABC vs ACO | 0.2286 | 764.5 | $3.40 \times 10^{-6}$ | 0.8494 | $3.40 \times 10^{-6}$ |
| Geodesic | ABC vs DO | 0.5546 | 900.0 | $2.97 \times 10^{-11}$ | 1.0000 | $5.94 \times 10^{-11}$ |
| Kiewitt | ABC vs ACO | 0.7032 | 690.0 | $5.27 \times 10^{-6}$ | 0.7667 | $5.27 \times 10^{-6}$ |
| Kiewitt | ABC vs DO | 1.9872 | 900.0 | $1.21 \times 10^{-12}$ | 1.0000 | $2.42 \times 10^{-12}$ |
| Ribbed | ABC vs ACO | 0.6852 | 682.5 | $5.53 \times 10^{-4}$ | 0.7583 | $5.53 \times 10^{-4}$ |
| Ribbed | ABC vs DO | 8.0284 | 900.0 | $2.84 \times 10^{-11}$ | 1.0000 | $5.67 \times 10^{-11}$ |

**Table 9.** Two-sided Mann–Whitney U tests and Vargha–Delaney $A_{12}$ effect sizes for ABC against ACO and DO.

To verify computational integrity, the internal direct stiffness solver was benchmarked against CSI SAP2000 v24 for the lightest design of each dome (Table 10). Recomputed member forces and displacements matched to within machine precision (normalised differences $\le 1.31 \times 10^{-13}$), and maximum demand-to-capacity (D/C) ratios matched exactly to five decimal places.

| Dome Topology | Peak Axial Force [kN] | Normalised Axial Force Difference | Normalised Displacement Difference | Max D/C (Own Solver) | Max D/C (SAP2000) |
|---|---|---|---|---|---|
| Geodesic | 13.82 | $3.4 \times 10^{-15}$ | $7.3 \times 10^{-15}$ | 0.99589 | 0.99589 |
| Kiewitt | 26.76 | $1.7 \times 10^{-14}$ | $3.2 \times 10^{-14}$ | 0.99226 | 0.99226 |
| Ribbed | 39.77 | $6.2 \times 10^{-14}$ | $1.3 \times 10^{-13}$ | 0.99995 | 0.99995 |

**Table 10.** Numerical verification of the direct stiffness solver against CSI SAP2000 v24 for the lightest designs.

## 4.2 Lightest designs and governing biomechanical limit states

The cross-sectional profiles (outer diameter $D$ and wall thickness $t$) assigned to each design group in the lightest designs are shown in Figure 5. Sizing distributions reflect structural hierarchy, with heavier culms positioned along base rings and high-stress meridians.

Table 11 lists the maximum demand-to-capacity ratios across all active design checks for the lightest designs. Column buckling under axial compression is the critical limit state, reaching D/C ratios of 0.992 to 1.000 across all three domes. Maximum nodal displacements remain well below allowable thresholds ($u/u_{lim} = 0.060, 0.062$, and $0.129$).

| Dome Topology | Max Tension D/C | Max Compression D/C | Max Slenderness D/C | Max Joint D/C | Displacement Ratio $u/u_{lim}$ | Groups with D/C $\ge 0.95$ |
|---|---|---|---|---|---|---|
| Geodesic | 0.165 | 0.996 | 0.733 | 0.280 | 0.060 | 8 / 23 |
| Kiewitt | 0.361 | 0.992 | 0.532 | 0.543 | 0.062 | 6 / 22 |
| Ribbed | 0.430 | 1.000 | 0.664 | 0.807 | 0.129 | 9 / 43 |

**Table 11.** Peak demand-to-capacity (D/C) ratios by limit state and active constraint counts for the lightest designs.

Compression buckling governs the largest D/C ratio in 19 of 23 groups (Geodesic), 21 of 22 (Kiewitt), and 41 of 43 (Ribbed) in the lightest designs. Geometric slenderness governs the remaining groups (4, 1, and 2 groups, respectively). Pure tension and codified connection capacity do not govern any group in the optimal designs. Averaged across all 90 feasible runs per dome, compression governs 81.1%, 95.5%, and 93.4% of the groups, slenderness governs 18.9%, 4.5%, and 6.5%, and connection capacity governs 0.2% on the Ribbed dome. Figure 6 illustrates these governing limit state shares.

## 4.3 Connection detailing: required bolts and spatial constraints

Peak member axial forces in the lightest designs reach 13.82 kN (Geodesic), 26.76 kN (Kiewitt), and 39.77 kN (Ribbed) (Table 10), all remaining below the four-bolt capacity of $F_{j,Rd} = 49.3$ kN. Consequently, individual members require only one, two, or three bolts per end rather than four (Table 12). On the 40 m Ribbed dome, 813 members require 1 bolt, 591 require 2 bolts, and 60 require 3 bolts.

| Dome Topology | Members ($N_m$) | $n_{req} = 1$ | $n_{req} = 2$ | $n_{req} = 3$ | $n_{req} = 4$ | Members Too Short for Required Bolts | Share [%] | Shortest Member [m] | Peak Force in Short Members [kN] | Members $< 1.35$ m |
|---|---|---|---|---|---|---|---|---|---|---|
| Geodesic | 115 | 115 | 0 | 0 | 0 | 0 | 0.00% | 2.24 | 0.00 | 0 |
| Kiewitt | 456 | 388 | 68 | 0 | 0 | 0 | 0.00% | 2.09 | 0.00 | 0 |
| Ribbed | 1464 | 813 | 591 | 60 | 0 | 12 | 0.82% | 0.76 | 31.25 | 84 |

**Table 12.** Required bolt distribution per member end (NSR-10 allowable capacity of a #5 bolt interpolated for the culm diameter, group factor $C_g$ = 1.0, 1.0, 0.97, 0.93 for one to four bolts) and geometric spacing compliance.

The joint capacity of 49.3 kN used in the optimization is the value for a culm diameter of 100 mm. As a check, the force of every member of the lightest designs was also compared with the capacity of four #5 bolts interpolated for the diameter of the member in NSR-10 Table G.12.11-2 (11.54 kN per bolt at 80 mm to 19.80 kN at 150 mm, $C_g = 0.93$). The largest joint demand-to-capacity ratios are 0.20 (Geodesic), 0.36 (Kiewitt) and 0.58 (Ribbed), and no member exceeds its capacity. The catalogue contains diameters up to 160 mm, which are beyond the table; the 150 mm value is used for them.

Importantly, 12 members in the Ribbed dome (0.82%), each measuring 0.76 m, are geometrically too short to accommodate the three through-bolts required under NSR-10 minimum spacing provisions ($2 \times [100 + 2 \times 150] + 150 = 0.95$ m minimum length for compression members with an end distance of 100 mm). These members experience peak axial forces of 31.25 kN, highlighting that dense spatial grid topologies require specialized multi-culm or compact clamp detailing. In contrast, the Geodesic and Kiewitt domes exhibit zero length violations.

## 4.4 Embodied carbon of the optimal designs and connection dominance

Total cradle-to-gate embodied carbon emissions (A1–A3) of the lightest designs are 0.71 t CO₂e (Geodesic), 4.84 t CO₂e (Kiewitt), and 10.34 t CO₂e (Ribbed) (Table 13). Connection hardware (steel hubs, sleeve fittings, and cementitious grout infill) carries 79.64%, 78.97%, and 84.10% of the total structural carbon emissions. Connection steel alone accounts for 33.15%, 18.55%, 27.05% of total emissions and cementitious grout for 46.49%, 60.42%, 57.05%, while grout represents 57% to 67% of total structural mass.

| Dome Topology | Culm Mass [t] | Steel Hardware [t] | Grout Mass [t] | Total Mass [t] | Culm Carbon [%] | Steel Carbon [%] | Grout Carbon [%] | Joint Total Carbon [%] | Total Carbon [t CO₂e] |
|---|---|---|---|---|---|---|---|---|---|
| Geodesic | 0.59 | 0.21 | 1.06 | 1.86 | 20.36% | 33.15% | 46.49% | 79.64% | 0.71 |
| Kiewitt | 4.19 | 0.79 | 9.43 | 14.41 | 21.03% | 18.55% | 60.42% | 78.97% | 4.84 |
| Ribbed | 6.76 | 2.47 | 19.02 | 28.26 | 15.90% | 27.05% | 57.05% | 84.10% | 10.34 |

**Table 13.** Structural mass and embodied carbon breakdown of the lightest bamboo space dome designs (baseline: $EC_b = 0.243, EC_s = 1.13, EC_m = 0.310\text{ kg CO}_2\text{e/kg}, \beta = 2.5$).

Table 14 summarizes parametric sensitivity sweeps across culm emission factors ($EC_b$), steel emissions ($EC_s$), grout length ratios ($\beta$), and a combined low-joint-carbon scenario. The steel factor is varied between 0.5 and 2 times the declared value of 1.13 kg CO₂e/kg, which is the range between the electric arc furnace and blast furnace routes stated in the source EPD [39]; the other ranges are parameter assumptions of the study.

| Dome Topology | Baseline | $\beta = 1.5$ | $\beta = 3.5$ | $EC_{steel} = 0.565$ | $EC_{steel} = 2.26$ | $EC_{bamboo} = 0.0324$ | $EC_{bamboo} = 1.23$ | Combined Scenario |
|---|---|---|---|---|---|---|---|---|
| Geodesic | 79.64% | 74.99% | 82.83% | 75.59% | 84.71% | 96.70% | 43.59% | 42.1% |
| Kiewitt | 78.97% | 72.27% | 83.06% | 76.82% | 82.26% | 96.57% | 42.59% | 38.8% |
| Ribbed | 84.10% | 79.40% | 87.05% | 81.61% | 87.48% | 97.54% | 51.10% | 48.4% |

**Table 14.** Parametric sensitivity of connection carbon share [%] across individual and combined parameter sweeps. Combined scenario assumes $\beta = 1.5, EC_s = 0.565, EC_b = 0.50, EC_m = 0.155$.

The bamboo culm emission factor exerts the single largest influence. At the lower-bound factor ($EC_b = 0.0324\text{ kg CO}_2\text{e/kg}$), connection hardware accounts for 96.57% to 97.54% of total structure emissions. When culm emissions are increased to the highest value tested ($EC_b = 1.23$), connections represent 42.59% to 51.10% of total emissions. Across all single-parameter sweeps the connection share lies between 42.6% and 97.5%.

## 4.5 Optimum-versus-optimum comparison with steel space domes

When comparing optimal bamboo designs with equivalent structural steel domes, the bamboo culm members weigh 0.509, 0.677, and 0.634 of the structural steel tubes, representing a 32% to 49% reduction in member weight (Table 15 and Table 16). Furthermore, the complete bamboo structural systems generate 0.319, 0.424, and 0.493 of the embodied carbon of the steel domes at baseline emission factors (rising to 0.583, 0.785, and 0.812 under $EC_b = 1.23$).

However, when full connection hardware and grout infill are included, the bamboo systems are heavier than the steel systems (Table 15): total system weights reach 18.21 kN, 141.32 kN, and 277.22 kN for bamboo versus 13.43 kN, 68.46 kN, and 128.96 kN for steel (weight ratios of 1.36, 2.06, and 2.15). On the 40 m Ribbed dome, injected grout alone contributes 19.02 t (186.6 kN) out of the 28.26 t total system mass.

| Structural System | Members ($N_m$) | Member Weight [kN] | Total System Weight [kN] | Embodied Carbon [t CO₂e] |
|---|---|---|---|---|
| Steel - Reference (354 members) | 354 | 129.012 | 134.976 | 23.057 |
| Steel - Ribbed (1464 members) | 1464 | 104.685 | 128.955 | 20.947 |
| Steel - Kiewitt (456 members) | 456 | 60.666 | 68.456 | 11.416 |
| Steel - Geodesic (115 members) | 115 | 11.404 | 13.434 | 2.211 |
| Bamboo - Geodesic (115 members) | 115 | 5.800 | 18.211 | 0.706 |
| Bamboo - Kiewitt (456 members) | 456 | 41.058 | 141.320 | 4.836 |
| Bamboo - Ribbed (1464 members) | 1464 | 66.352 | 277.222 | 10.336 |

**Table 15.** Optimum structural mass and embodied carbon comparison between steel and bamboo space domes.

| Dome Topology | Bamboo / Steel Member Weight Ratio | Bamboo / Steel Total CO₂e Ratio |
|---|---|---|
| Geodesic | 0.509 | 0.319 |
| Kiewitt | 0.677 | 0.424 |
| Ribbed | 0.634 | 0.493 |

**Table 16.** Ratios of optimal bamboo to steel domes for member weight and system embodied carbon.

Figure 7 illustrates the comparative member weight (Figure 7a) and component-level embodied carbon breakdown (Figure 7b) across all structural configurations.

## 4.6 International material cost evaluation

Table 17 documents the ratio of bamboo to steel material cost across diameter-price scaling exponents $\alpha \in [1.5, 3.0]$ in the primary Indonesian market.

| Exponent $\alpha$ | Geodesic Cost Ratio | Kiewitt Cost Ratio | Ribbed Cost Ratio | Geodesic Grout [%] | Kiewitt Grout [%] | Ribbed Grout [%] |
|---|---|---|---|---|---|---|
| 1.5 | 0.612 | 0.869 | 0.981 | 59.6% | 73.4% | 69.7% |
| 2.0 | 0.639 | 0.926 | 1.021 | 57.1% | 68.9% | 67.0% |
| 2.5 | 0.676 | 1.010 | 1.076 | 54.0% | 63.1% | 63.5% |
| 3.0 | 0.724 | 1.137 | 1.154 | 50.4% | 56.1% | 59.2% |

**Table 17.** Ratio of bamboo to steel material cost ($C_{bamboo}/C_{steel}$) and grout cost share in the Indonesian baseline scenario.

For the nominal 16 m Geodesic dome, bamboo is cheaper across all scaling exponents (ratios 0.612–0.724). For the 32 m Kiewitt dome, bamboo remains cost-competitive for $\alpha \le 2.0$ (0.869–0.926). For the 40 m Ribbed dome, bamboo is cheaper only at $\alpha = 1.5$ (0.981) and becomes more expensive at $\alpha \ge 2.0$ due to heavy grout volumes. Grout represents 50.4% to 73.4% of total bamboo material expenditure. The cost ratios of the India and Türkiye scenarios are within 1% of the Indonesian ratios (Table 18), because their bamboo prices are derived from the Indonesian prices; the Colombian ratios are higher (0.868, 1.248 and 1.297 at $\alpha = 2.0$). In all scenarios the cost ratio increases with member count and grout infill length.

| Scenario | Geodesic ($\alpha = 2.0$) | Kiewitt ($\alpha = 2.0$) | Ribbed ($\alpha = 2.0$) |
|---|---|---|---|
| Indonesia 2024 | 0.639 | 0.926 | 1.021 |
| India 2023 | 0.637 | 0.922 | 1.016 |
| Türkiye 2026 | 0.638 | 0.924 | 1.019 |
| Colombia 2026 | 0.868 | 1.248 | 1.297 |

**Table 18.** Sensitivity of cost ratios across international economic market scenarios ($\alpha = 2.0$).
