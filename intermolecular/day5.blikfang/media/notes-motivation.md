### Motivation and teaching target

This is a 45-minute presented lecture for experimentally oriented MSc chemistry students, following day 4. Students know Coulomb energy, electric field, Bjerrum length, dielectric response and thermal energy. Algebra is required; differential equations are interpreted physically and their derivations are optional. The projected route contains short class questions without gates. The first eight slides form a continuous opening sequence. Supporting notes follow the main lecture.

After the lecture, students should be able to explain counterion enrichment and co-ion depletion; calculate ionic strength and Debye length; calculate planar and spherical potentials and local ion concentrations; estimate a salt-dependent contact repulsion between spheres; and assess the assumptions and experimental interpretation of these calculations.

The opening food example is qualitative. Screening may reduce droplet repulsion while attraction remains, but steric stabilization, hydration, interfacial chemistry and kinetics also matter. A protein can carry both positive and negative patches. A gel combines electrostatics with ion partitioning and network elasticity. No aggregation probability is inferred from a screening factor.

At 25 °C, use $\ell_B=7.1$ Å, $k_BT/e=25.7$ mV and $N_Ak_BT=2.479$ kJ/mol. These are rounded teaching values. The supplied exam problem specifies $\ell_B=7.2$ Å; use its stated value when solving it. Earlier day 4 scenes use $560.4/78.4\simeq7.15$ Å; this lecture rounds to 7.1 Å consistently. Here $\varepsilon=\varepsilon_0\varepsilon_r$, and $\Phi=e\psi/k_BT$. Concentrations $c_i$ are in mol/L; number densities $n_i$ are particles per volume. Energy symbols are $U$ for the ideal point-pair energy and $w$ for the finite-sphere interaction free energy.

Sources: Dill & Bromberg (2011), Chapter 23, pp. 455–458, Fig. 23.1 and Example 23.1. The application artwork comes from the supplied salt-screening teaching ZIP and consists of original teaching schematics. Food context: McClements, Bai & Chung (2017), DOI 10.1146/annurev-food-030216-030154. Protein/PB context: Grochowski & Trylska (2008), DOI 10.1002/bip.20877. Detailed literature is a reading route, not a claim that the supplied schematics are measured results.

### Symbols and model names

The following notation is used throughout the slides and figures. These definitions also provide a short recap of day 4. We use $\varepsilon_r$ for relative permittivity and $k_BT$ or kJ/mol for energies.

| Symbol | Meaning and units |
|:--|:--|
| $e$, $k_B$, $T$ | Positive elementary charge (C), Boltzmann's constant (J/K), absolute temperature (K) |
| $k_BT$ | Thermal energy per particle; at 25 °C, the corresponding molar energy is $N_Ak_BT=2.479$ kJ/mol |
| $\psi$, $\Phi=e\psi/(k_BT)$ | Electric potential relative to bulk (V), dimensionless potential |
| $n_i(r)$, $n_i^\infty$ | Local and bulk number density of ion species $i$ (particles per volume) |
| $c_i$, $c$ | Molar concentration of ion species $i$, analytical salt concentration (mol/L) |
| $z_i$ | Signed valence of ion species $i$, dimensionless |
| $I=\tfrac12\sum_i c_i z_i^2$ | Ionic strength (mol/L) |
| $\ell_D$, $\kappa=1/\ell_D$ | Debye screening length (Å or m), inverse screening length (Å$^{-1}$ or m$^{-1}$) |
| $\ell_B=e^2/(4\pi\varepsilon_0\varepsilon_r k_BT)$ | Bjerrum length; elementary-charge Coulomb energy has magnitude $k_BT$ at this distance; use 7.1 Å in water at 25 °C |
| $\varepsilon_0$, $\varepsilon_r$, $\varepsilon=\varepsilon_0\varepsilon_r$ | Vacuum permittivity (F/m), relative permittivity (dimensionless), absolute permittivity (F/m) |
| $a$, $r$, $x=r-a$ | Sphere/cylinder radius, distance from the centre/axis, distance from the surface (Å); for a plane, $x$ starts at the plane |
| $R$, $h=R-2a$ | Centre–centre separation of two particles, surface–surface separation for identical spheres (Å) |
| $\psi_0=\psi(0)$, $\psi_a=\psi(a)$ | Surface potential of a plane, surface potential of a sphere (V) |
| $\Phi_a=e\psi_a/(k_BT)$ | Dimensionless surface potential of a sphere |
| $Q=Ze$, $Z=Q/e$ | Total sphere charge (C), charge in elementary-charge units |
| $\rho$, $\sigma$ | Ionic charge density (C/m$^3$), surface charge density (C/m$^2$) |
| $N_A$ | Avogadro's constant (mol$^{-1}$) |
| $K_0$ | Order-zero decaying modified Bessel function used in the cylindrical linear-PB solution |
| $\psi_s$ | Generic surface potential in the geometry comparison (V); $\psi_0$ for the plane and $\psi_a$ for the sphere/cylinder |
| $U_C$, $U_Y$ | Unscreened Coulomb energy, screened Coulomb (Yukawa) energy of ideal point charges (J or $k_BT$) |
| $w(R)$ | Finite-sphere interaction free energy; the worked contact target is $w(2a)=0.1k_BT$ |
| $Z_{\rm eff}$, $Q_{\rm eff}=Z_{\rm eff}e$ | Effective valence and effective charge used to express the sphere's far-field amplitude |

PB abbreviates Poisson–Boltzmann. Its mean-field approximation replaces discrete, fluctuating ion configurations by smooth average distributions. Linearized PB additionally assumes $|z_i\Phi|\ll1$. The Laplacian $\nabla^2$ measures spatial curvature. Hyperbolic sine is $\sinh\Phi=(e^\Phi-e^{-\Phi})/2$; in exponentials, $e^u$ is the exponential function, whereas $e$ multiplying a charge or potential denotes elementary charge.

The Coulomb and Yukawa point-charge energies are

$$\frac{U_C(R)}{k_BT}=z_1z_2\frac{\ell_B}{R},\qquad U_Y(R)=U_C(R)e^{-R/\ell_D}.$$

The symbols C and Y refer to Coulomb and Yukawa, respectively. Finite spheres use the additional radius-dependent amplitude in $w(R)$; the simple point-charge ratio is labelled explicitly on the slides.

Useful units: 1 M = 1 mol/L, 1 mM = $10^{-3}$ M, 1 Å = $10^{-10}$ m and 1 mV = $10^{-3}$ V. Counterions have the opposite sign to the fixed object and co-ions the same sign. Ion pairing associates opposite ions; bridging links two objects through a bound ion. An activity describes the effective concentration entering chemical potential. DLVO theory combines screened electrostatic repulsion and van der Waals attraction. Donnan partitioning is the unequal distribution of mobile ions across a boundary containing fixed charges; it contributes to gel osmotic pressure.
