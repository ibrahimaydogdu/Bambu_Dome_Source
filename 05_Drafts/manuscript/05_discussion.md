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
