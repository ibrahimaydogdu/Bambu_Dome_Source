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
