# Reproducible Numerical Datasets & Benchmark Tables

This directory contains the machine-readable CSV datasets corresponding to the optimization benchmarks, limit state analyses, non-parametric statistical hypothesis tests, parametric LCA sensitivity sweeps, cost inventories, and convergence trajectories presented in the manuscript.

---

## 📊 Summary of Structured Datasets

### 1. Metaheuristic Optimization Benchmarks & Best Solutions
- `T1_optimization_results.csv`: Structural mass and statistical performance across all 270 optimization runs (3 domes × 3 algorithms × 30 seeds).
- `T2_best_solutions.csv`: Summary characteristics of the global best design vectors for each dome topology.
- `T2_best_profile_geodesic16.csv`: Discrete culm diameter ($D$) and wall thickness ($t$) profiles for the 16 m Geodesic dome.
- `T2_best_profile_kiewitt32.csv`: Discrete culm profile assignments for the 32 m Kiewitt dome.
- `T2_best_profile_ribbed40.csv`: Discrete culm profile assignments for the 40 m Ribbed dome.

### 2. Statistical Hypothesis Testing & Algorithmic Rankings (Tables 8–9)
- `T_stats_descriptive.csv`: Summary descriptive statistics (Best, Median, Mean, Standard Deviation, Carbon, NFE, Runtime) across 30 independent seeds per algorithm.
- `T_stats_friedman_ranks.csv`: Asymptotic $p$-values, $\chi_F^2$ test statistics, and mean rank orders from the seed-blocked Friedman test.
- `T_stats_wilcoxon_pairwise.csv`: Pairwise Mann–Whitney U statistics, rank-sum differences, Holm-adjusted $p$-values, and Vargha–Delaney $A_{12}$ non-parametric effect sizes.

### 3. Structural Mechanics, Limit States, and Joint Capacities (Table 11, Table S1.1, Figure 6)
- `T4_limit_states.csv`: Governing limit state distributions and peak D/C ratios for the lightest designs.
- `T_governing_limit_shares.csv`: Member group breakdown governed by column buckling, member slenderness, axial tension, and joint bearing capacity.
- `T10_joint_bolt_requirement.csv`: Member-end force distributions, required bolt numbers ($n_{bolt}$), and spatial member length clearance verification.
- `T_tuning_study_summary.csv`: Hyperparameter tuning study evaluating population size sensitivity across algorithms.

### 4. Material Comparison, Post-Optimization LCA & Sensitivity Sweeps (Table 13–15)
- `T5_material_comparison.csv`: Direct structural mass and cradle-to-gate embodied carbon comparison between Guadua bamboo and AISC steel domes.
- `T6_same_geometry_ratio.csv`: Weight and carbon ratios under identical geometric layouts.
- `T7_bamboo_component_breakdown.csv`: Component-wise mass and carbon breakdown (culms, connection steel, cementitious grout infill).
- `T_lca_base_case_breakdown.csv`: Baseline cradle-to-gate carbon footprint breakdown across all three dome topologies.
- `T_lca_sensitivity_grout_length.csv`: Sensitivity sweep of grout infill length ratio ($\beta = L_{inj}/D \in [1.5, 3.5]$).
- `T_lca_sensitivity_steel_ec.csv`: Sensitivity sweep across steel emission factors ($EC_s \in [0.565, 2.26]\text{ kg CO}_2\text{e/kg}$).
- `T_lca_sensitivity_bamboo_ec.csv`: Sensitivity sweep across bamboo culm emission factors ($EC_b \in [0.0324, 1.23]\text{ kg CO}_2\text{e/kg}$).
- `T8_material_sensitivity.csv`: Summary comparative carbon sensitivity of bamboo/steel ratios.

### 5. International Material Cost Scenarios (Tables 16–18)
- `T9_price_scenarios_cost.csv`: Total structural expenditure across four international market scenarios (Indonesia, India, Türkiye, Colombia) and culm pricing exponents ($\alpha \in [1.5, 3.0]$).
- `T9a_price_scenario_inputs_USD.csv`: Unit prices for structural culms, steel hardware, and grout in USD equivalent.

### 6. Raw Convergence Trajectories (Figure 3)
- `T_convergence_curves_history.csv`: Continuous NFE evaluation grid (300 interpolated evaluation points per algorithm and dome) containing mean, best, and standard deviation penalized weights across all 30 replicated runs.
