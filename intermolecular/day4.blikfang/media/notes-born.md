# The Born energy from the solvent's point of view

**Picture.** Put an ion into a solvent. The molecules near it turn and distort so that
their negative ends face a cation. Each molecule is now a small dipole in the ion's field, and
each lowers the free energy a little. The solvation free energy is the sum of all these small
contributions.

**One molecule.** A molecule in a field $E$ acquires a dipole $\alpha_{\rm eff}E$ and gains the
free energy $-\tfrac12\alpha_{\rm eff}E^2$ (the ½ for the same reason as in charging: the dipole
builds up as the field grows). The effective polarizability has two parts from day 3:
electronic, $\alpha$, and orientational, $\mu^2/3k_BT$, from the thermal average of a permanent
dipole's alignment.

**All molecules.** The ion's field is $E = q/(4\pi\varepsilon_0 r^2)$. A shell of radius $r$
and thickness $dr$ contains $\rho\,4\pi r^2\,dr$ molecules, with $\rho$ the number density.
Assuming the solvent is uniform outside the ion ($r > a$),

$$\Delta G \approx -\frac{\rho\,\alpha_{\rm eff}}{2}\int_a^\infty
\left(\frac{q}{4\pi\varepsilon_0 r^2}\right)^2 4\pi r^2\,dr
= -\frac{q^2}{8\pi\varepsilon_0 a}\cdot\frac{\rho\,\alpha_{\rm eff}}{\varepsilon_0}.$$

The last factor is the electric susceptibility $\chi$, and for a dilute medium
$\chi = \varepsilon_r - 1$. Each shell contributes in proportion to $r^{-2}\,dr$, so the
integral converges, but slowly: half the energy comes from beyond $r = 2a$.

**Why this fails in a liquid.** For water $\chi \approx 77$, and the formula would win back
77 times the vacuum self-energy. That cannot be: the solvent can at most cancel the field
entirely. The flaw is that each molecule was assumed to feel the bare field of the ion. In a
dense liquid the other molecules have already screened the field to $E/\varepsilon_r$.

**Building the dielectric up.** Add solvent so that the permittivity grows from $\varepsilon_r$
to $\varepsilon_r + d\varepsilon_r$. The new material has susceptibility $d\varepsilon_r$ and feels
the screened field, whose energy density is smaller by $1/\varepsilon_r^2$. Taking the medium
around the ion from $\varepsilon_1$ to $\varepsilon_2$,

$$d\Delta G = -\frac{q^2}{8\pi\varepsilon_0 a}\,\frac{d\varepsilon_r}{\varepsilon_r^2}
\quad\Rightarrow\quad
\Delta G_{\rm Born} = -\frac{q^2}{8\pi\varepsilon_0 a}\int_{\varepsilon_1}^{\varepsilon_2}\frac{d\varepsilon_r}{\varepsilon_r^2}
= \frac{q^2}{8\pi\varepsilon_0 a}\left(\frac1{\varepsilon_2}-\frac1{\varepsilon_1}\right).$$

This is the Born energy: the free energy of moving an ion from a medium with dielectric
constant $\varepsilon_1$ into one with $\varepsilon_2$ (Dill Eq. 22.61). The solvation free
energy is the special case $\varepsilon_1 = 1$, from vacuum:
$-\frac{q^2}{8\pi\varepsilon_0 a}(1 - 1/\varepsilon_r)$.

**Check against the charging picture.** Charging the sphere in vacuum costs
$q^2/(8\pi\varepsilon_0 a)$; charging it in the solvent costs $q^2/(8\pi\varepsilon_0\varepsilon_r a)$.
The difference is exactly the Born energy from vacuum into the solvent. Dill derives it this way, with a thermodynamic cycle
(Fig. 22.14, Eq. 22.61).

**Numbers.** In units of $k_BT$, $\Delta G_{\rm Born}/k_BT = (z^2\ell_B^{\rm vacuum}/2a)(1/\varepsilon_2 - 1/\varepsilon_1)$.
From vacuum this is $-(z^2\ell_B^{\rm vacuum}/2a)(1 - 1/\varepsilon_r)$.
For a monovalent ion with $a = 2$ Å in water this is $-140 \times 0.99 = -138\,k_BT$, about
−340 kJ/mol. In oil ($\varepsilon_r = 2$) it is only $-70\,k_BT$.

**Assumptions to keep in mind.** The solvent is a uniform continuum right up to the ion's
surface; it responds linearly to the field (no saturation, although the field next to a small
ion is enormous); and only electrostatics counts. The radius $a$ therefore works as an
effective, fitted cavity radius rather than the crystal radius.

## Self-test

1. Which changes the Born energy more, doubling $z$ or doubling $a$?
   *Answer: doubling $z$ (×4); doubling $a$ only halves it.*
2. What is the solvation free energy (Born from vacuum) for $\varepsilon_r \to 1$ and for $\varepsilon_r \to \infty$?
   *Answer: 0, and $-z^2\ell_B^{\rm vacuum}/2a$ (the whole self-energy).*
3. Why does the dilute formula $-(q^2/8\pi\varepsilon_0 a)\chi$ fail for water?
   *Answer: it assumes every molecule feels the bare field; in a dense liquid the field is
   already screened to $E/\varepsilon_r$.*
