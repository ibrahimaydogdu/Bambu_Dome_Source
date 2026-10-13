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

Figure 2 shows the mean and best penalized weight over the function evaluations. On all three domes the mean curve of DO is the lowest at small NFE and flattens at the highest value. The mean curves of ABC and ACO end close to each other on Ribbed and Kiewitt. On Kiewitt the ACO mean curve approaches the ABC curve later than ABC does and ends 1.2 kN higher (Table 7).

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
