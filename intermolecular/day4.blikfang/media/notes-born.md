# The solvation free energy, two ways

**The model.** An ion is a sphere of radius $a$ with charge $q = ze$ on its surface, in a
uniform medium with dielectric constant $\varepsilon_r$. Only electrostatics counts: no cavity,
no dispersion, no hydrogen bonds.

## Step 0: charging a sphere

**Why charge it gradually.** The first bits of charge arrive at a neutral sphere and cost
nothing; the last are pushed against almost the full charge. So add the charge in small steps.
Let $\lambda$ run from 0 (neutral) to 1 (charged). With $\lambda q$ on the sphere, the surface
potential is $\psi(\lambda) = \lambda q/(4\pi\varepsilon_0\varepsilon_r a)$, and the next bit
$q\,d\lambda$ costs $\psi(\lambda)\,q\,d\lambda$:

$$\Delta G_{\rm charge} = \int_0^1 \frac{\lambda q}{4\pi\varepsilon_0\varepsilon_r a}\,q\,d\lambda
= \frac{q^2}{8\pi\varepsilon_0\varepsilon_r a} = \frac{z^2\ell_B}{2a}\,k_BT,
\qquad \ell_B = \frac{e^2}{4\pi\varepsilon_0\varepsilon_r k_BT}.$$

The ½ comes from $\int_0^1\lambda\,d\lambda$: on average a bit feels half the final potential
(Dill Ex. 22.10). In vacuum $\ell_B^{\rm vacuum} = 560$ Å, so a monovalent ion with $a = 2$ Å
costs $560/4 = 140\,k_BT$, about 350 kJ/mol.

## Route 1: charge in vacuum, then in the medium

Free energy depends only on the start and end states, so take a detour (Dill Fig. 22.14):

1. discharge the ion in vacuum: $-q^2/8\pi\varepsilon_0 a$;
2. move the neutral sphere into the medium: no electrostatic cost;
3. charge it in the medium: $+q^2/8\pi\varepsilon_0\varepsilon_r a$.

The sum is the solvation free energy,

$$\Delta G_{\rm solv} = \frac{q^2}{8\pi\varepsilon_0 a}\left(\frac1{\varepsilon_r} - 1\right).$$

The same detour between two media, discharging in medium 1 and charging in medium 2, gives the
Born energy $\frac{q^2}{8\pi\varepsilon_0 a}\left(\frac1{\varepsilon_2}-\frac1{\varepsilon_1}\right)$
(Dill Eq. 22.61): a transfer is the difference of two solvation free energies. This route is
quick, but it treats $\varepsilon_r$ as given and does not say what the solvent does.

## Route 2: add up the solvent's response

**One molecule.** A solvent molecule in a field $E$ acquires a dipole $\alpha_{\rm eff}E$ and
gains $-\tfrac12\alpha_{\rm eff}E^2$ (the ½ again because the dipole builds up with the field).
From day 3, $\alpha_{\rm eff} = \alpha + \mu^2/3k_BT$: electronic plus orientational.

**All molecules, dilute solvent.** The ion's field is $E = q/(4\pi\varepsilon_0 r^2)$, and a
shell of radius $r$ and thickness $dr$ holds $\rho\,4\pi r^2\,dr$ molecules. Then

$$\Delta G \approx -\frac{\rho\,\alpha_{\rm eff}}{2}\int_a^\infty
\left(\frac{q}{4\pi\varepsilon_0 r^2}\right)^2 4\pi r^2\,dr
= -\frac{q^2}{8\pi\varepsilon_0 a}\,\chi, \qquad \chi = \frac{\rho\,\alpha_{\rm eff}}{\varepsilon_0} = \varepsilon_r - 1.$$

Each shell adds $\propto r^{-2}\,dr$, so the integral converges, but slowly: half the energy
comes from beyond $r = 2a$ (the convergence explorer).

**Why this fails in a liquid.** For water $\chi \approx 77$, and the formula would win back 77
times the self-energy. That is impossible: the solvent can at most cancel the field. The flaw is
that each molecule was assumed to feel the bare field. In a dense liquid the molecules already
there have screened it to $E/\varepsilon_r$.

**Building the solvent up.** Grow the permittivity from $\varepsilon'$ to $\varepsilon' + d\varepsilon'$.
The new material has susceptibility $d\varepsilon'$ and feels the screened field, whose energy
density is smaller by $1/\varepsilon'^2$:

$$d\Delta G = -\frac{q^2}{8\pi\varepsilon_0 a}\,\frac{d\varepsilon'}{\varepsilon'^2}
\quad\Rightarrow\quad
\Delta G_{\rm solv} = -\frac{q^2}{8\pi\varepsilon_0 a}\int_1^{\varepsilon_r}\frac{d\varepsilon'}{\varepsilon'^2}
= \frac{q^2}{8\pi\varepsilon_0 a}\left(\frac1{\varepsilon_r}-1\right),$$

the same result as route 1. Integrating from $\varepsilon_1$ to $\varepsilon_2$ instead gives the
Born transfer energy.

## Numbers

In units of $k_BT$, $\Delta G_{\rm Born}/k_BT = (z^2\ell_B^{\rm vacuum}/2a)(1/\varepsilon_2 - 1/\varepsilon_1)$.
For a monovalent ion with $a = 2$ Å, from vacuum into water this is $-140 \times 0.99 = -138\,k_BT$,
about −340 kJ/mol; into oil ($\varepsilon_r = 2$) only $-70\,k_BT$.

**Assumptions.** The solvent is a uniform continuum right up to the ion's surface; it responds
linearly (no saturation, although the field next to a small ion is enormous); only electrostatics
counts. The radius $a$ is therefore an effective, fitted cavity radius.

**Notation.** Dill writes the dielectric constant as $D$ and $1/(4\pi\varepsilon_0)$ as $C$; here
$\varepsilon_r$ is the dielectric constant, as on days 2–3, and $\varepsilon_1$, $\varepsilon_2$,
$\varepsilon_{\rm w}$, $\varepsilon_{\rm oil}$ are its values in particular media. At 25 °C,
$k_BT$ = 2.48 kJ/mol = 0.593 kcal/mol.

## Self-test

1. Which changes the Born energy more, doubling $z$ or doubling $a$?
   *Answer: doubling $z$ (×4); doubling $a$ only halves it.*
2. What is the solvation free energy for $\varepsilon_r \to 1$ and for $\varepsilon_r \to \infty$?
   *Answer: 0, and $-z^2\ell_B^{\rm vacuum}/2a$ (the whole self-energy).*
3. Why does the dilute formula $-(q^2/8\pi\varepsilon_0 a)\chi$ fail for water?
   *Answer: it assumes every molecule feels the bare field; in a dense liquid the field is
   already screened to $E/\varepsilon_r$.*
4. Route 1 and route 2 give the same answer. What does route 2 tell you that route 1 does not?
   *Answer: where the energy comes from (the polarized solvent), and how far out it reaches.*
