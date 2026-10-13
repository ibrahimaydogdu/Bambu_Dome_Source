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
