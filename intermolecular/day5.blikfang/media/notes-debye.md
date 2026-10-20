### Ionic strength, number density and Debye length

For species $i$, let $c_i$ be the molar concentration and $z_i$ its signed valence. Define $I=\tfrac12\sum_i c_i z_i^2$. NaCl at analytical concentration $c$ gives $I=c$. CaCl$_2$ and Na$_2$SO$_4$ give $I=3c$, while fully dissociated MgSO$_4$ gives $I=4c$. The formula counts ions and their squared valences; it does not model specific binding or ion pairing.

Use the definition $\ell_B=e^2/(4\pi\varepsilon_0\varepsilon_r k_BT)$ in $\kappa^2=2e^2n_\infty/(\varepsilon_0\varepsilon_r k_BT)$ to obtain $\kappa^2=8\pi\ell_Bn_\infty$ for 1:1 salt. More generally, $\kappa^2=4\pi\ell_B\sum_i n_i z_i^2$. Number density must match the length unit: 1 mol/L is $6.022\times10^{26}$ m$^{-3}$, or $6.022\times10^{-4}$ Å$^{-3}$. This is the conversion needed for Dill 23.12.

The shortcut uses ionic strength, not analytical salt concentration. It applies to different valences within the same ideal screening approximation; only replacing $I$ by $c$ requires $I=c$ (1:1 salt). The rounded water-at-25-°C shortcut is $\ell_D/\mathrm{\AA}=3.04/\sqrt{I/(1\,\mathrm M)}$. At 1, 10 and 100 mM, it gives 96.1, 30.4 and 9.61 Å. At 25 mM, it gives $3.04/\sqrt{0.025}=19.2$ Å. Therefore quadrupling ionic strength halves the range, and multiplying it by 100 divides the range by 10. The limit $I\to0$ makes the ideal added-salt screening length diverge; actual samples can still contain counterions, buffer and water ions.

The shortcut and $\ell_B=7.1$ Å are rounded independently. They differ slightly from a calculation retaining all physical constants, as does the supplied exam's specified 7.2 Å. Keep the displayed shortcut and the scene code identical; use problem-specific constants in assigned calculations. Dill's Table 23.1 uses slightly different rounding (e.g. 96.2 rather than 96.1 Å).

Sources: Dill & Bromberg, Chapter 23, Eqs. 23.8–23.10, Example 23.2 and Table 23.1, p. 459. Exercises 23.1–23.4 require the resulting $\kappa$; 23.12 requires the link to $\ell_B$ and the number-density conversion.

The former separate Debye and salt-composition slides are combined in main slide 8. The useful identity for a 1:1 salt remains $\kappa^2=8\pi\ell_Bn_\infty$; this is already derived above and is needed for Dill 23.12.
