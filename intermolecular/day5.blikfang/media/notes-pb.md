### From Boltzmann distributions to linearized PB

An ion with signed valence $z_i$ has energy $z_i e\psi$. Equilibrium weighting relative to the bulk gives $n_i(r)=n_i^\infty\exp[-z_i e\psi(r)/(k_BT)]$. The potential reference is zero in the bulk. A positive potential suppresses positive ions and enriches negative ions. The same concentration ratios hold in mol/L because the unit conversion cancels. For example, at $\Phi=-0.20$ in 20 mM NaCl, $c_+=20e^{0.20}=24.4$ mM and $c_-=20e^{-0.20}=16.4$ mM. This is a local equilibrium concentration, not a bulk change of salt composition.

For a symmetric 1:1 salt, $n_+=n_\infty e^{-\Phi}$ and $n_-=n_\infty e^{\Phi}$. Therefore $\rho=e(n_+-n_-)=-2en_\infty\sinh\Phi$. Substitute into Poisson's equation $\nabla^2\psi=-\rho/(\varepsilon_0\varepsilon_r)$, then multiply by $e/(k_BT)$:

$$\nabla^2\Phi=\frac{2e^2n_\infty}{\varepsilon_0\varepsilon_r k_BT}\sinh\Phi=\kappa^2\sinh\Phi.$$

This derivation applies in the mobile-ion region. Fixed surface charge is imposed by the boundary condition. The electrolyte is treated as fully dissociated, with a continuum solvent, uniform permittivity and a mean-field potential. A positive potential gives negative ionic charge density, so the sign of the curvature is positive, as the equation requires.

For $|z_i\Phi|\ll1$, expand $e^{\pm\Phi}\approx1\pm\Phi$ to obtain $\sinh\Phi\approx\Phi$ and $\nabla^2\psi=\kappa^2\psi$. At $\Phi=0.20$, $\sinh\Phi=0.2013$, close to 0.20. The limit is an approximation, not a sharp transition. Full Boltzmann factors are often evaluated using a linear-PB potential in textbook exercises; report that this combines an approximate field with the exponential concentration rule. Expanding the concentrations too would be a further approximation and can give unphysical negative concentrations at large potentials.

For Dill 23.4, reconstruct the surface potential from the specified off-surface value, then test $|\Phi_0|$. A value of 30 mV is already of order $k_BT/e$, so the small-potential condition is questionable even before extrapolating to the surface. To compare with nonlinear PB at fixed positive off-surface potential, use $\tanh(\Phi(x)/4)=\tanh(\Phi_0/4)e^{-\kappa x}$ for a planar 1:1 electrolyte. At positive $\Phi$, $\sinh\Phi>\Phi$; the nonlinear response changes the extrapolation. There is also a saturation bound on the off-surface potential for a finite surface potential. Check this bound before assuming that the specified data admit a finite nonlinear solution. Do not silently accept every linear extrapolation as a valid nonlinear boundary condition.

Source: Dill & Bromberg, Chapter 23, pp. 457–459, Eqs. 23.1–23.8. Use $\varepsilon_r$ for relative permittivity, $\varepsilon=\varepsilon_0\varepsilon_r$ for absolute permittivity, and $\Phi=e\psi/k_BT$. No vector-calculus derivation is required in the projected lecture.

### Profiles and iteration in the opening sequence

The density slide uses the exact nonlinear planar 1:1 solution at fixed $\psi_0=25.7$ mV and variable salt. Its graph shows $c_\pm/c_\infty$, while the surface readouts show absolute mM. The iteration animation uses a finite interval from a wall at 25.7 mV to a reservoir at 120 Å held at zero, at fixed 10 mM salt. Its finite endpoint is not the infinite-reservoir boundary used for the density slide. It alternates Boltzmann concentrations with a damped finite-difference Poisson solve; it is a numerical algorithm for equilibrium, not a model of ion trajectories. The following slide combines the relations into nonlinear PB, then the linearization slide introduces the weak-potential approximation. The three-geometry comparison and later worked examples use that approximation.
