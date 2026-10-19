# Transfer between media, partition and drugs

**The cycle.** A single ion cannot be moved from water to oil in a calorimeter, but its
free energy change can be computed by a detour. Discharge the ion in water (gaining back
$q^2/8\pi\varepsilon_0\varepsilon_{\rm w} a$), move the neutral sphere into oil (no electrostatic cost,
since there is no field to screen), and charge it again in oil (paying
$q^2/8\pi\varepsilon_0\varepsilon_{\rm oil} a$). Free energy is a state function, so the direct path
costs the same as the detour (Dill Fig. 22.14, Eq. 22.61):

$$\Delta G_{w\to o} = \frac{z^2\ell_B^{\rm vacuum}}{2a}\left(\frac1{\varepsilon_{\rm oil}}-\frac1{\varepsilon_{\rm w}}\right)kT
= \Delta G_{\rm solv}(o) - \Delta G_{\rm solv}(w).$$

**Partition coefficient.** At equilibrium the concentrations in the two phases satisfy
$c_o/c_w = K = e^{-\Delta G_{w\to o}/kT}$. For a monovalent ion with $a = 2$ Å, from water
($\varepsilon_r = 78$) to oil ($\varepsilon_r = 2$), $\Delta G = 140\times(0.5 - 0.013) \approx 68\,kT$
(Dill Ex. 22.13 takes $\varepsilon_r = 80$ for water and rounds to 70), so $K \approx 10^{-30}$. A litre of 1 M salt water holds
$6\times10^{23}$ ions; next to a litre of oil, on average fewer than one of them is in the oil.

**logP.** Chemists report $\log P = \log_{10}(c_{\rm octanol}/c_{\rm water})$. Natural logarithms
turn into decimal ones by dividing by $\ln 10 = 2.303$:
$\log P = -\Delta G_{w\to o}/(2.303\,kT)$. Ionizing a drug adds the Born transfer cost to the
neutral molecule's $\Delta G$. With dry oil the estimate (about 30 log units) is far too large.
Octanol, however, holds a lot of water and has $\varepsilon_r \approx 10$, and a drug's charge is spread
over a group with an effective radius of about 3 Å. Then
$\Delta G \approx (560/6)(1/10 - 1/78) \approx 8\,kT$, a drop of $8/2.3 \approx 3.5$ in $\log P$, close to
the 3–4 units usually measured between the neutral and ionized forms of a drug.

**pH.** Only the neutral form crosses a membrane easily. An acid is neutral where the pH is
below its $\mathrm{p}K_a$, a base where the pH is above it. This is why the pH along the gut, from
about 1.5 in the stomach to 7–8 in the small intestine, matters for which drugs are absorbed where.

**Near the surface.** An ion close to the water–air surface loses part of its solvation
shell. For a sharp surface this can be described with an image charge: in water the ion feels
a repulsion from its mirror image of about $(\ell_B/4d)(\varepsilon_{\rm w} - \varepsilon_{\rm air})/(\varepsilon_{\rm w} + \varepsilon_{\rm air})\,kT$
at distance $d$ (about $1\,kT$ at contact for a monovalent ion). The surface layer is therefore
depleted of small ions, which raises the surface tension of salt solutions (Onsager and
Samaras, 1934). Large polarizable anions are an exception, as simulations and surface-sensitive
spectroscopy have shown.

**Source.** Dill & Bromberg, *Molecular Driving Forces*, 2nd ed., ch. 22, pp. 444–451.

## Self-test

1. Is the transfer of an ion from oil into water positive or negative?
   *Answer: negative; $1/\varepsilon_r$ is 0.013 in water and 0.5 in oil.*
2. Water → octanol costs $+8.1\,kT$ for $a = 3$ Å. What does octanol → water cost?
   *Answer: $-8.1\,kT$; the same two states, opposite direction.*
3. Where is a weak base with $\mathrm{p}K_a = 9$ absorbed best, stomach or small intestine?
   *Answer: the small intestine, where more of it is neutral.*
4. Why are small ions depleted at the water surface?
   *Answer: they lose part of their solvation there; their image charge repels them.*
