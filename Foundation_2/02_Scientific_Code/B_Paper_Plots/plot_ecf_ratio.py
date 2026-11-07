"""
(02/10/2026, Corpus) -- replaces the former plot_ecf_ratio.py (promoted 07/10/2026).
Fig_ECF_Ratio_Evolution: ratio rho_tau / rho_m as a function of redshift z, ECF background w = -1.
Convention A-7: h_ECF = 0.7304, omega_m = 0.02237 + 0.12 -> Omega_m = omega_m/h^2.
With w = -1 the torsion (dark-energy) density is constant: rho_tau/rho_m = (Omega_tau/Omega_m)(1+z)^-3.
Omega_tau = 1 - Omega_m - Omega_r - Omega_spin,0 (flat closure). Radiation/spin are negligible at z <= 3.
Second curve: dynamical dark energy, CPL w(a)=w0+wa(1-a) with the calibrated (w0,wa)=(-0.904,-0.153) (F1, DESI-calibrated),
rho_DE(z)/rho_DE,0 = (1+z)^(3(1+w0+wa)) exp(-3 wa z/(1+z)). SAME Omega_m and flat closure at z=0: NOT refitted
(a self-consistent dynamical background would re-derive Omega_m; open point PO-F2-5 / PO-F3-9). Indicative.
"""
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

h = 0.7304
Om = (0.02237 + 0.12) / h**2
omega_g, Neff = 2.4728e-5, 3.046
Or = omega_g * (1 + 7/8 * (4/11)**(4/3) * Neff) / h**2
Os = 0.093 * Or / (1 + 5600)**2
Ot = 1 - Om - Or - Os

from scipy.optimize import brentq
w0, wa = -0.904, -0.153
z = np.linspace(0, 3, 600)
R = (Ot / Om) * (1 + z)**-3
fde = lambda z: (1 + z)**(3*(1 + w0 + wa)) * np.exp(-3*wa*z/(1 + z))
Rd = lambda z: (Ot / Om) * fde(z) * (1 + z)**-3
z_cross = (Ot / Om)**(1/3) - 1
z_cross_d = brentq(lambda x: Rd(x) - 1, 0, 2)
print(f"CPL: R(0)={Rd(0):.3f}  z(R=1)={z_cross_d:.3f}  R_cpl/R_w-1 at z=0.5,1,2,3: {[round(Rd(x)/((Ot/Om)*(1+x)**-3),3) for x in (0.5,1,2,3)]}")
print(f"Omega_m={Om:.4f} Omega_r={Or:.4e} Omega_spin0={Os:.3e} Omega_tau={Ot:.4f}")
print(f"R(0)={Ot/Om:.3f}  z(R=1)={z_cross:.3f}")

# --- 1-sigma band: propagation of the inputs of Omega_m = (omega_b+omega_c)/h^2 (independent Gaussians, Monte-Carlo) ---
# omega_b = 0.02237 +/- 0.00015, omega_c = 0.1200 +/- 0.0012 (Planck 2018); H0 = 73.04 +/- 1.04 (SH0ES 2021, F1).
# (w0, wa) are the optimisation minimum of F1: no posterior uncertainty is attached to them (F1 l.1083), so none is propagated.
rng = np.random.default_rng(20261002)
N = 200000
hh = rng.normal(0.7304, 0.0104, N); wb = rng.normal(0.02237, 0.00015, N); wc = rng.normal(0.1200, 0.0012, N)
Om_s = (wb + wc) / hh**2
Ot_s = 1 - Om_s - Or - Os
def band(zz, dyn):
    out = []
    for x in zz:
        r = (Ot_s / Om_s) * (1 + x)**-3 * (fde(x) if dyn else 1.0)
        out.append(np.percentile(r, [15.865, 84.135]))
    return np.array(out)
zb = np.linspace(0, 3, 61)
B0 = band(zb, False); B1 = band(zb, True)
print(f"Omega_m = {Om:.4f} +/- {Om_s.std():.4f} (MC);  R(0) = {Ot/Om:.3f}  [{B0[0,0]:.3f}, {B0[0,1]:.3f}]  (-{100*(1-B0[0,0]/(Ot/Om)):.1f}% / +{100*(B0[0,1]/(Ot/Om)-1):.1f}%)")
zc_s = (Ot_s / Om_s)**(1/3) - 1
print(f"z(R=1), w=-1: {z_cross:.3f}  68% interval [{np.percentile(zc_s,15.865):.3f}, {np.percentile(zc_s,84.135):.3f}]")
lin = (Om_s.std()/Om)/(1-Om)
print(f"linear check on R(0): {100*lin:.2f}%")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(z, R, lw=2.5, color="#2ca02c", label=r"$\rho_\tau/\rho_m$ (ECF, $w=-1$)")
ax.plot(z, Rd(z), lw=2.2, ls="--", color="#d62728", label=rf"$\rho_\tau/\rho_m$ (dynamical DE, CPL $w_0={w0}$, $w_a={wa}$; indicative)")
ax.scatter([z_cross_d], [1], color="#d62728", zorder=5)
ax.fill_between(zb, B0[:,0], B0[:,1], color="#2ca02c", alpha=0.20, lw=0, label=r"$1\sigma$ from $\omega_b,\omega_c,H_0$ (inputs of $\Omega_m$)")
ax.fill_between(zb, B1[:,0], B1[:,1], color="#d62728", alpha=0.15, lw=0)
ax.axhline(1, ls="--", color="k", lw=1)
ax.axvline(z_cross, ls=":", color="gray")
ax.scatter([z_cross], [1], color="k", zorder=5)
ax.annotate(rf"$w=-1$ : $\rho_\tau=\rho_m$ at $z={z_cross:.2f}$", (z_cross, 1), (0.75, 1.9))
ax.annotate(rf"CPL : $\rho_\tau=\rho_m$ at $z={z_cross_d:.2f}$", (z_cross_d, 1), (0.75, 1.35), color="#d62728")
ax.scatter([0], [Ot/Om], color="#2ca02c", zorder=5)
ax.annotate(rf"$z=0$ : {Ot/Om:.2f}", (0, Ot/Om), (0.12, Ot/Om*0.72))
ax.set_ylim(0.04, 5); ax.set_yscale("log"); ax.set_xlabel("Redshift $z$"); ax.set_ylabel(r"$\rho_\tau/\rho_m$")
ax.set_title(r"ECF dark-sector to matter density ratio ($\Omega_m=\omega_m/h^2$, A-7)")
ax.legend(loc="lower left", fontsize=8); ax.grid(alpha=.3, which="both")
plt.savefig("Fig_ECF_Ratio_Evolution.png", dpi=300, bbox_inches="tight")
