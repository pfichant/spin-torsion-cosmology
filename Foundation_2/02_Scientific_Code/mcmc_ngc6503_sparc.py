#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mcmc_ngc6503_sparc.py — vraie chaîne MCMC pour NGC 6503 sur le fichier SPARC (audit v2, 22/09/2026)
Remplace, pour la prochaine version de F2, plot_MCMC_NGC6503.py, qui tirait 60 000 échantillons d'une loi normale
de moyenne et covariance écrites en dur, sur des données (Data_S1) qui ne sont pas celles de SPARC.

Données : Scripts_F2/data/sparc/NGC6503_rotmod.dat (31 points). Υd = 0,5 fixé (NGC 6503 n'a pas de bulbe).
Modèle  : halo ECF V² = V∞² (1 − arctan(x)/x), V∞² = 4πGρ₀R_s² (sphère pseudo-isotherme).
Paramètres échantillonnés : log10 ρ₀ [g cm⁻³] ∈ [−26, −20], R_s [kpc] ∈ [0,05, 50], a priori plats.
emcee, 32 marcheurs, 6000 pas, 2000 de chauffe ; graine fixée.
"""
import math, json, os
import numpy as np
import emcee

ICI = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(ICI, "data", "sparc", "NGC6503_rotmod.dat")   # Scripts_F2/data/sparc (versé au corpus le 05/10/2026, REPRO-01)
G_SI, KPC = 6.674e-11, 3.0857e19
d = np.loadtxt(F, comments="#")
r, v, e, vg, vd, vb = (d[:, i] for i in range(6))
vbar2 = vg * np.abs(vg) + 0.5 * vd * np.abs(vd) + 0.7 * vb * np.abs(vb)


def vinf_kms(lrho, rs):
    rho = 10 ** lrho * 1e3                       # kg/m^3
    return math.sqrt(4 * math.pi * G_SI * rho * (rs * KPC) ** 2) / 1e3


def lnp(p):
    lrho, rs = p
    if not (-26 < lrho < -20 and 0.05 < rs < 50):
        return -np.inf
    vi = vinf_kms(lrho, rs)
    x = r / rs
    m = np.sqrt(np.abs(vbar2 + vi ** 2 * (1 - np.arctan(x) / x)))
    return -0.5 * np.sum(((v - m) / e) ** 2)


rng = np.random.default_rng(20260922)
nw, nd = 32, 2
p0 = np.column_stack([-23.25 + 0.05 * rng.standard_normal(nw), 1.7 + 0.05 * rng.standard_normal(nw)])
np.random.seed(20260922)   # [REPRO-01b, 06/10/2026] seeded BEFORE the sampler: emcee draws its RandomState at construction
s = emcee.EnsembleSampler(nw, nd, lnp)
s.run_mcmc(p0, 6000, progress=False)
ch = s.get_chain(discard=2000, flat=True)
lp = s.get_log_prob(discard=2000, flat=True)
vi = np.array([vinf_kms(a, b) for a, b in ch])
best = ch[np.argmax(lp)]
q = lambda a: (float(np.percentile(a, 50)), float(np.percentile(a, 84) - np.percentile(a, 50)),
               float(np.percentile(a, 50) - np.percentile(a, 16)))
out = dict(
    n_points=int(r.size), chi2_min=float(-2 * lp.max()), chi2_red_min=float(-2 * lp.max() / (r.size - 2)),
    best=dict(log10_rho0=float(best[0]), Rs=float(best[1]), Vinf=vinf_kms(*best)),
    log10_rho0=q(ch[:, 0]), Rs=q(ch[:, 1]), Vinf=q(vi),
    corr_lrho_Rs=float(np.corrcoef(ch[:, 0], ch[:, 1])[0, 1]),
    acceptance=float(np.mean(s.acceptance_fraction)),
    tau=[float(t) for t in s.get_autocorr_time(quiet=True)],
)
os.makedirs(os.path.join(ICI, "sorties"), exist_ok=True)
json.dump(out, open(os.path.join(ICI, "sorties", "mcmc_ngc6503.json"), "w"), indent=2)
print(json.dumps(out, indent=2))
