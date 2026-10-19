# Charging a sphere, step by step

**The model.** An ion is a sphere of radius $a$ with its charge $q = ze$ spread over the
surface. It sits in a uniform medium with dielectric constant $\varepsilon_r$. We ask how much
reversible work it takes to put the charge there, starting from a neutral sphere.

**Why charge it gradually.** We cannot place the whole charge at once and multiply by the
final potential: the first bits of charge arrived when the sphere was still neutral and cost
nothing, while the last bits had to be pushed against almost the full charge. So we add the
charge in small steps and add up the cost of each step.

**The steps.** Let $\lambda$ run from 0 (neutral) to 1 (fully charged). When the sphere carries
$\lambda q$, the potential at its surface is that of a point charge at its centre,

$$\psi(\lambda) = \frac{\lambda q}{4\pi\varepsilon_0\varepsilon_r a}.$$

Bringing the next bit $dq = q\,d\lambda$ from far away to the surface costs
$dG = \psi(\lambda)\,q\,d\lambda$. Adding all the steps,

$$\Delta G = \int_0^1 \frac{\lambda q}{4\pi\varepsilon_0\varepsilon_r a}\,q\,d\lambda
= \frac{q^2}{4\pi\varepsilon_0\varepsilon_r a}\int_0^1 \lambda\,d\lambda
= \frac{q^2}{8\pi\varepsilon_0\varepsilon_r a}.$$

The integral of $\lambda$ gives the factor ½. Dill reaches the same result a second way
(Ex. 22.10): half the surface charge times the final surface potential, integrated over the
surface. Both say the same thing: on average, each bit of charge feels half the final
potential.

**In units of $k_BT$.** With the Bjerrum length $\ell_B = e^2/(4\pi\varepsilon_0\varepsilon_r k_BT)$,

$$\frac{\Delta G}{k_BT} = \frac{z^2\,\ell_B}{2a}.$$

In vacuum $\ell_B^{\rm vacuum} = 560$ Å at 25 °C, so a monovalent ion with $a = 2$ Å costs
$560/4 = 140\,k_BT$, about 350 kJ/mol. In water $\ell_B = 7.1$ Å and the same ion costs only
$1.8\,k_BT$.

**What it means.** The self-energy is large for small ions ($1/a$) and grows with the square
of the charge ($z^2$): a divalent ion costs four times as much as a monovalent one of the same
size. A polarizable medium lowers the cost by $1/\varepsilon_r$. The next slides show where that
saving comes from.

**Notation.** Dill writes the dielectric constant as $D$ and $1/(4\pi\varepsilon_0)$ as $C$; here
$\varepsilon_r$ is the dielectric constant (relative permittivity), as on days 2–3;
$\varepsilon_1$, $\varepsilon_2$, $\varepsilon_{\rm w}$ and $\varepsilon_{\rm oil}$ are its values in particular media. At 25 °C, $k_BT$ = 2.48 kJ/mol = 0.593 kcal/mol.
