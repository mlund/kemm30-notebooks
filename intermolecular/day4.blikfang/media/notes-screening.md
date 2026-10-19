# Salt screening, a first look

**Picture.** In salt water every ion is surrounded by a cloud of other ions. Ions of the
opposite sign are drawn in and ions of the same sign are pushed away, so the cloud carries a
net charge equal and opposite to the central ion. Far away, the ion and its cloud together look
neutral: the field has been *screened*.

**How far the cloud reaches.** The balance between electrostatic attraction (which pulls the
cloud in) and entropy (which spreads it out) sets the size of the cloud, the Debye length
$\kappa^{-1}$. For a solution of ionic strength $I$ (mol/L),

$$\kappa^2 = 8\pi\,\ell_B\,N_A I \cdot (1000\ \text{L/m}^3),$$

and in water at 25 °C this gives $\kappa^{-1} = 3.04\ \text{Å}/\sqrt{I/\text{M}}$. At 0.1 M the
Debye length is about 10 Å; at 150 mM, the salt level of blood, 8 Å. A lower dielectric
constant gives a longer Bjerrum length and hence a *shorter* Debye length at the same salt,
$\kappa^{-1} \propto \sqrt{\varepsilon_r}$.

**The screened potential.** Solving the linearized Poisson–Boltzmann (Debye–Hückel) equation
around an ion of radius $a$, from which other ions are excluded, gives

$$\frac{e\psi(r)}{k_BT} = z\,\ell_B\,\frac{e^{-\kappa(r-a)}}{(1+\kappa a)\,r}.$$

Close to the ion this is Coulomb's law; beyond a few Debye lengths it dies away exponentially.
For two ions or two charged particles this gives the screened Coulomb interaction used in
problem 2, with the effective valence $z_{\rm eff} = z\,e^{\kappa a}/(1+\kappa a)$:
$w(R)/k_BT = z_{1,\rm eff}\,z_{2,\rm eff}\,\ell_B\,e^{-\kappa R}/R$. Problem 2 writes the same with
charges, $Q_{\rm eff} = Q\,e^{\kappa a}/(1+\kappa a)$.

**Assumptions.** The linearized theory holds when $e\psi \ll k_BT$, so it works best for low
charge, high dielectric constant and moderate salt. That is why the explorable keeps
$\varepsilon_r$ between 20 and 80 (water is 78): in oil-like solvents the ion clouds are strongly nonlinear and
ions pair up instead (day 2).

**Day 5** derives the Debye length, the ion atmosphere and what it does to activity
coefficients (Dill ch. 23).

## Self-test

1. What is the Debye length in 0.01 M and in 1 M NaCl at 25 °C?
   *Answer: 30 Å and 3 Å.*
2. Adding 0.1 M salt, does the attraction between Na⁺ and Cl⁻ 10 Å apart get weaker or stronger?
   *Answer: weaker; the ion atmospheres cancel part of each field.*
3. At the same salt concentration, is the Debye length longer or shorter in ethanol than in water?
   *Answer: shorter, since $\kappa^{-1} \propto \sqrt{\varepsilon_r}$.*
