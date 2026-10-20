### Plane, sphere and cylinder: forward and inverse calculations

For the one-sided planar electrolyte in Dill Example 23.3, solve $d^2\psi/dx^2=\kappa^2\psi$. The general solution is $A_1e^{\kappa x}+A_2e^{-\kappa x}$. The condition $\psi(\infty)=0$ removes the growing term. Setting $\psi(0)=\psi_0$ gives $\psi(x)=\psi_0e^{-\kappa x}$. The boundary condition $-d\psi/dx|_0=\sigma/(\varepsilon_0\varepsilon_r)$ then gives $\psi_0=\sigma/(\varepsilon_0\varepsilon_r\kappa)$.

At 10 mM salt, $\ell_D=30.4$ Å. A plane with $\psi_0=5$ mV has $\psi(30\,\mathrm{\AA})=5e^{-30/30.4}=1.86$ mV. Inverting gives $\psi_0=\psi(x)e^{\kappa x}$. To calculate charge density use SI units: $\kappa=1/(30.4\times10^{-10}\,\mathrm m)$, $\psi_0=0.005$ V and $\varepsilon_r=78.4$. Thus $\sigma\approx1.14\times10^{-3}$ C/m$^2$. Replacing mV by V and Å$^{-1}$ by m$^{-1}$ is essential. These steps prepare Dill 23.4 without supplying its answers.

For a sphere, $r\psi$ obeys the same decaying linear equation. With $\psi(\infty)=0$, write $\psi(r)=A e^{-\kappa r}/r$. The boundary field at $r=a$ is $Q/(4\pi\varepsilon_0\varepsilon_r a^2)$ for the textbook model. Differentiating the potential gives $\psi_a=Q/[4\pi\varepsilon_0\varepsilon_r a(1+\kappa a)]$. Therefore

$$\psi(r)=\frac{Q}{4\pi\varepsilon_0\varepsilon_r r}\frac{e^{-\kappa(r-a)}}{1+\kappa a},\qquad
\Phi(r)=\frac{Z\ell_B}{r}\frac{e^{-\kappa(r-a)}}{1+\kappa a}.$$

The domain is $r\ge a$. Use $r=a+x$ when the distance is measured from the surface. Dividing by the surface potential gives $\psi(r)/\psi_a=(a/r)e^{-\kappa(r-a)}$. The extra $a/r$ factor expresses spherical spreading. The planar limit is local: $a\gg x$ and $a\gg\ell_D$, so $a/(a+x)\approx1$. For fixed charge, changing salt also changes the surface amplitude through $(1+\kappa a)^{-1}$; it does not merely change the exponential.

For the lecture example, $a=25$ Å, $r=45$ Å, $I=0.010$ M and $\psi(r)=1.0$ mV. First obtain $\kappa=1/30.4$ Å$^{-1}$. Next recover $\psi_a=1.0(45/25)e^{20/30.4}=3.48$ mV. Then $\Phi_a=3.48/25.7=0.135$ and $Z=\Phi_a a(1+\kappa a)/\ell_B\approx0.87$. The inferred surface potential is small, so the linearization check is satisfactory. At the surface, use the Boltzmann rule to get $c_+=10e^{-0.135}=8.73$ mM and $c_-=10e^{0.135}=11.45$ mM. The calculation applies an approximate potential in the full concentration rule.

For an unscreened finite sphere, set $\kappa=0$ to recover $\Phi(r)=Z\ell_B/r$ outside it. To convert any dimensionless potential to volts, multiply by 0.0257 V. Always draw a radius and label whether the measurement is from the centre or surface; exercise 23.1's wording should be read with this distance convention made explicit.

Sources: Dill & Bromberg, Example 23.3, Eqs. 23.11–23.16, pp. 459–460; Example 23.4, Eqs. 23.17–23.25, pp. 461–462. Exercises 23.1–23.3 need the sphere formula; 23.2 also needs the Boltzmann rule. Exercise 23.3 requires the inverse steps and charge recovery. Exercise 23.4 requires the planar boundary condition and a validity check. Cylinder geometry is included in the comparison slide; evaluation of Bessel functions is not required by these assignments.

### Cylindrical comparison

For an infinitely long cylinder of radius $a$, outside its surface, the linear-PB solution at fixed surface potential is $\psi(r)/\psi_s=K_0(r/\ell_D)/K_0(a/\ell_D)$. Here $r=a+x$ is measured from the axis. $K_0$ is the order-zero modified Bessel function of the second kind, selected because it decays at infinity. Its large-argument form is $K_0(u)\sim\sqrt{\pi/(2u)}e^{-u}$. The far field is therefore an exponential times $r^{-1/2}$; the sphere has $r^{-1}$, and the plane no spreading factor. This does not make the cylindrical profile a pure exponential near the surface. See NIST DLMF §10.40.2: https://dlmf.nist.gov/10.40.E2. The common exponential factor may be written using $r$ or $x=r-a$; the shift is absorbed into an amplitude. All three formulas in the comparison solve linearized PB.
