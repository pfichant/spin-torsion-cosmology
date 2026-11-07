#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sparc_protocole_v1.py — protocole figé de comparaison ECF / NFW sur SPARC (audit v2, 22/09/2026)
=====================================================================================================
Producteur unique de TOUS les nombres du tableau SPARC proposé pour la prochaine version de F2.
Ne modifie aucun fichier du dépôt ; écrit dans ./sorties/.

PROTOCOLE (gelé, v1)
--------------------
Données   : les 175 fichiers *_rotmod.dat de SPARC (Lelli, McGaugh & Schombert 2016, Rotmod_LTG), lus dans
            Scripts_F2/data/sparc/ (empreintes : data/sparc/MANIFESTE_SPARC.md5 ; versé au corpus le 05/10/2026, REPRO-01) ; lecture et sélection IDENTIQUES à fit_sparc175.py (errV > 0, R > 0, >= 5 points).
Baryons   : V_bar^2 = Vgas|Vgas| + Υd Vdisk|Vdisk| + Υb Vbul|Vbul|.
Modèles   : ECF   V_h^2 = V∞^2 (1 − arctan(x)/x), x = r/R_s      (identique à la sphère pseudo-isotherme)
            NFW   V_h^2 = V200^2 [ln(1+cx) − cx/(1+cx)] / (x [ln(1+c) − c/(1+c)]), x = r/R200,
                  R200 = V200 / (10 H0), H0 = 73,04 km/s/Mpc
Conventions :
  A  Υd = 0,5 et Υb = 0,7 FIXÉS (convention de fit_sparc175.py) ; k = 2 paramètres par galaxie et par modèle.
  B  Υd (et Υb si bulbe) LIBRES avec a priori log-normal centré sur 0,5 / 0,7, largeur 0,1 dex — inspiré de
     Li et al. 2020, SANS leurs a priori sur distance et inclinaison ; k = 2 + nombre de Υ libres.
Ajustement : moindres carrés pondérés (scipy least_squares, méthode trf), 4 points de départ par modèle, meilleur
            retenu. Bornes « standard » : ECF V∞ ∈ [1, 1000] km/s, R_s ∈ [0,05, 200] kpc ; NFW V200 ∈ [1, 1000] km/s,
            c ∈ [1, 100]. Bornes « élargies » (test) : V ∈ [1, 5000], R_s ∈ [0,01, 2000], c ∈ [0,1, 1000].
Statistiques : χ²_red = χ²_données / (n − k) ; médiane, moyenne, pondérée Σχ²/Σ(n−k), χ² total ;
            AIC = χ² + 2k (+ prior en B) sommé sur les galaxies ; ΔAIC = AIC(NFW) − AIC(ECF) ; nombre de galaxies
            où chaque modèle a le plus petit χ² ; nombre d'ajustements sur une borne.
Référence de non-régression : ECF, convention A, départ unique de fit_sparc175.py → médiane 0,802 sur 171 galaxies.
"""
import glob, json, math, os, sys
import numpy as np
from scipy.optimize import least_squares

ICI = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.environ.get("ECF_SPARC_DIR", os.path.join(ICI, "data", "sparc"))   # Scripts_F2/data/sparc (corpus ; manifeste data/sparc/MANIFESTE_SPARC.md5)
SORTIES = os.path.join(ICI, "sorties")
H0 = 73.04 / 1000.0            # km/s/kpc
UD0, UB0, SIG_DEX = 0.5, 0.7, 0.1
G_SI, KPC = 6.674e-11, 3.0857e19

BORNES = {
    "standard": {"ECF": ([1.0, 0.05], [1000.0, 200.0]), "NFW": ([1.0, 1.0], [1000.0, 100.0])},
    "elargies": {"ECF": ([1.0, 0.01], [5000.0, 2000.0]), "NFW": ([1.0, 0.1], [5000.0, 1000.0])},
}


def lire(chemin):
    d = np.loadtxt(chemin, comments="#")
    if d.ndim != 2 or d.shape[0] < 4 or d.shape[1] < 6:
        return None
    rad, vobs, errv, vgas, vdisk, vbul = (d[:, i] for i in range(6))
    ok = (errv > 0) & (rad > 0) & np.isfinite(vobs)
    if ok.sum() < 5:
        return None
    return dict(r=rad[ok], v=vobs[ok], e=errv[ok], g=vgas[ok], d=vdisk[ok], b=vbul[ok])


def vbar2(G, ud, ub):
    return G["g"] * np.abs(G["g"]) + ud * G["d"] * np.abs(G["d"]) + ub * G["b"] * np.abs(G["b"])


def halo_ecf(r, vinf, rs):
    x = r / rs
    return vinf ** 2 * (1.0 - np.arctan(x) / x)


def halo_nfw(r, v200, c):
    r200 = v200 / (10.0 * H0)
    x = r / r200
    m = lambda y: np.log1p(y) - y / (1.0 + y)
    return v200 ** 2 * m(c * x) / (x * m(c))


HALO = {"ECF": halo_ecf, "NFW": halo_nfw}


def ajuste(G, modele, convention, bornes, departs=None):
    a_bulbe = bool(np.any(G["b"] != 0))
    libres = [] if convention == "A" else (["ud", "ub"] if a_bulbe else ["ud"])
    lo, hi = BORNES[bornes][modele]
    lo = list(lo) + [-2.0] * len(libres)          # log10 Υ ∈ [−2, 1]
    hi = list(hi) + [1.0] * len(libres)

    def params(p):
        ud = 10 ** p[2] if "ud" in libres else UD0
        ub = 10 ** p[libres.index("ub") + 2] if "ub" in libres else UB0
        return p[0], p[1], ud, ub

    def resid(p):
        a, b, ud, ub = params(p)
        v = np.sqrt(np.abs(vbar2(G, ud, ub) + HALO[modele](G["r"], a, b)))
        res = (G["v"] - v) / G["e"]
        pri = []
        if "ud" in libres:
            pri.append((math.log10(ud) - math.log10(UD0)) / SIG_DEX)
        if "ub" in libres:
            pri.append((math.log10(ub) - math.log10(UB0)) / SIG_DEX)
        return np.concatenate([res, pri])

    vmax = max(float(G["v"].max()), 10.0)
    rmed = max(float(np.median(G["r"])), 0.5)
    if departs is None:
        departs = [[vmax, rmed], [vmax, 3 * rmed], [1.5 * vmax, 0.5 * rmed], [0.8 * vmax, 10.0]] if modele == "ECF" \
            else [[vmax, 10.0], [vmax, 3.0], [1.3 * vmax, 30.0], [0.8 * vmax, 1.5]]
    best = None
    for d0 in departs:
        p0 = [min(max(d0[0], lo[0] * 1.001), hi[0] * 0.999), min(max(d0[1], lo[1] * 1.001), hi[1] * 0.999)]
        p0 += [math.log10(UD0) if n == "ud" else math.log10(UB0) for n in libres]
        try:
            s = least_squares(resid, p0, bounds=(lo, hi), method="trf", max_nfev=20000)
        except Exception:
            continue
        if best is None or s.cost < best.cost:
            best = s
    p = best.x
    a, b, ud, ub = params(p)
    n = len(G["r"])
    k = 2 + len(libres)
    r_all = resid(p)
    chi2 = float(np.sum(r_all[:n] ** 2))
    prior = float(np.sum(r_all[n:] ** 2))
    borne = bool(np.any(np.isclose(p[:2], lo[:2], rtol=1e-3)) or np.any(np.isclose(p[:2], hi[:2], rtol=1e-3)))
    return dict(p1=float(a), p2=float(b), ud=float(ud), ub=float(ub), chi2=chi2, prior=prior, n=n, k=k,
                chi2_red=chi2 / max(n - k, 1), aic=chi2 + prior + 2 * k, borne=borne)


def fit_reference_fit_sparc175(G):
    """Départ unique de fit_sparc175.py (curve_fit) : sert de test de non-régression (médiane 0,802)."""
    from scipy.optimize import curve_fit
    vb = np.sqrt(np.abs(vbar2(G, UD0, UB0)))
    mod = lambda r, vi, rs: np.sqrt(vb ** 2 + np.abs(halo_ecf(r, vi, rs)))
    p, _ = curve_fit(mod, G["r"], G["v"], p0=[max(float(G["v"].max()), 10.0), max(float(np.median(G["r"])), 0.5)],
                     sigma=G["e"], absolute_sigma=True, maxfev=20000, bounds=([1.0, 0.05], [1000.0, 200.0]))
    return float(np.sum(((G["v"] - mod(G["r"], *p)) / G["e"]) ** 2) / (len(G["r"]) - 2))


def resume(rows, modele):
    c = np.array([r[modele]["chi2"] for r in rows]); red = np.array([r[modele]["chi2_red"] for r in rows])
    dof = np.array([r[modele]["n"] - r[modele]["k"] for r in rows])
    return dict(n_gal=len(rows), median=float(np.median(red)), mean=float(red.mean()),
                weighted=float(c.sum() / dof.sum()), chi2_total=float(c.sum()),
                aic_total=float(sum(r[modele]["aic"] for r in rows)),
                frac_lt1=float((red < 1).mean()), n_borne=int(sum(r[modele]["borne"] for r in rows)))


def main():
    os.makedirs(SORTIES, exist_ok=True)
    fichiers = sorted(glob.glob(os.path.join(DONNEES, "*_rotmod.dat")))
    assert len(fichiers) == 175, f"{len(fichiers)} fichiers rotmod (175 attendus)"
    gal = {}
    for f in fichiers:
        G = lire(f)
        if G is not None:
            gal[os.path.basename(f)[:-11]] = G
    out = {"protocole": "v1", "n_fichiers": len(fichiers), "n_retenues": len(gal)}

    ref = np.array([fit_reference_fit_sparc175(G) for G in gal.values()])
    out["reference_fit_sparc175"] = dict(median=float(np.median(ref)), n=len(ref))

    for conv in ("A", "B"):
        for bornes in ("standard", "elargies"):
            rows = []
            for nom, G in gal.items():
                rows.append(dict(nom=nom, ECF=ajuste(G, "ECF", conv, bornes), NFW=ajuste(G, "NFW", conv, bornes)))
            e, n_ = resume(rows, "ECF"), resume(rows, "NFW")
            wins = sum(r["ECF"]["chi2"] < r["NFW"]["chi2"] for r in rows)
            out[f"{conv}_{bornes}"] = dict(ECF=e, NFW=n_, delta_aic_nfw_moins_ecf=n_["aic_total"] - e["aic_total"],
                                           ecf_meilleur=int(wins), n=len(rows))
            with open(os.path.join(SORTIES, f"par_galaxie_{conv}_{bornes}.csv"), "w") as fh:
                fh.write("galaxie,n,ECF_Vinf,ECF_Rs,ECF_Ud,ECF_Ub,ECF_chi2red,ECF_borne,"
                         "NFW_V200,NFW_c,NFW_Ud,NFW_Ub,NFW_chi2red,NFW_borne\n")
                for r in rows:
                    E, N = r["ECF"], r["NFW"]
                    fh.write(f"{r['nom']},{E['n']},{E['p1']:.3f},{E['p2']:.4f},{E['ud']:.3f},{E['ub']:.3f},"
                             f"{E['chi2_red']:.4f},{int(E['borne'])},{N['p1']:.3f},{N['p2']:.3f},{N['ud']:.3f},"
                             f"{N['ub']:.3f},{N['chi2_red']:.4f},{int(N['borne'])}\n")
            if conv == "A" and bornes == "standard":
                ngc = next(r for r in rows if r["nom"] == "NGC6503")
                G = gal["NGC6503"]
                vb = np.sqrt(np.abs(vbar2(G, UD0, UB0)))
                chi_newton = float(np.sum(((G["v"] - vb) / G["e"]) ** 2) / len(G["r"]))
                vinf, rs = ngc["ECF"]["p1"], ngc["ECF"]["p2"]
                rho0 = (vinf * 1e3) ** 2 / (4 * math.pi * G_SI * (rs * KPC) ** 2)          # kg/m^3
                out["NGC6503"] = dict(n=int(G["r"].size), Vinf=vinf, Rs=rs, chi2_red=ngc["ECF"]["chi2_red"],
                                      chi2_red_newton=chi_newton, log10_rho0_gcm3=math.log10(rho0 * 1e-3),
                                      NFW_chi2_red=ngc["NFW"]["chi2_red"])

    # identité pseudo-isotherme (contrôle numérique ; la preuve analytique est dans le rapport)
    from scipy.integrate import quad
    ecarts = []
    for r in (0.1, 1.0, 3.0, 30.0):
        M = quad(lambda s: 4 * math.pi * s * s / (1 + s * s), 0, r)[0]
        ecarts.append(abs((M / r) / (4 * math.pi * (1 - math.atan(r) / r)) - 1))
    out["identite_pseudo_isotherme_ecart_max"] = max(ecarts)

    with open(os.path.join(SORTIES, "resultats.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
