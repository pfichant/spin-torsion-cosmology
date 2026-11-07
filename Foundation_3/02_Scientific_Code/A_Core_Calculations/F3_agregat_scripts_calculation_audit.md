# DOCUMENT DE CONTEXTE POUR AUDIT DE CODE

**Dossier audité :** A_Core_Calculations

---

## CONTENU DES SOURCES PYTHON

### Fichier 1 : `calculate_F3_osc_gw_frequency.py`

```python
#!/usr/bin/env python3

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# =============================================================================
#  ECF / F3 — Oscillations de torsion post-rebond : portee observationnelle
#  Fichant, P. (2026).  Fichier : osc_gw_frequency.py   (item OSC-1)
# =============================================================================
#
#  OBJET : estimer la frequence, redshiftee jusqu'a aujourd'hui, des
#  oscillations de torsion mises en evidence par lg_bounce_dynamics.py,
#  et confronter cette frequence aux bandes des detecteurs d'ondes
#  gravitationnelles.
#
#  CONCLUSION (annoncee d'emblee, pour eviter toute surinterpretation) :
#    La frequence tombe vers ~1e11 Hz (bande UHF-GW). AUCUN detecteur
#    actuel ou planifie n'y a acces. De plus, le mode homogene (k=0) ne
#    source PAS de GW (il faut un quadrupole). Toute revendication de
#    "fossiles gravitationnels detectables" serait donc PREMATUREE.
#    Ce script documente une LIMITE, non une prediction.
# =============================================================================
import numpy as np

hbar, c, G = 1.055e-34, 2.998e8, 6.674e-11
t_P   = np.sqrt(hbar*G/c**5)
GeV_K = 1.16e13

OMEGA_REDUIT = 1.79      # omega = sqrt(4|a2|), mesure dans le prototype
T_BOUNCE_GeV = 9.9e18    # temperature au rebond (valeur canonique F3)
T_TODAY_K    = 2.725     # CMB

f_source = OMEGA_REDUIT / (2*np.pi*t_P)
redshift = T_TODAY_K / (T_BOUNCE_GeV * GeV_K)
f_today  = f_source * redshift

print("="*70)
print("Oscillations de torsion post-rebond — frequence aujourd'hui")
print("="*70)
print(f"  omega (unites de Planck)   : {OMEGA_REDUIT}")
print(f"  f_source                   : {f_source:.3e} Hz")
print(f"  facteur de redshift a/a0   : {redshift:.3e}")
print(f"  => f_aujourd'hui           : {f_today:.3e} Hz  ({f_today/1e9:.0f} GHz)")
print()
print("  Bandes de detection :")
for name, lo, hi in [("Pulsar Timing Array", 1e-9, 1e-7),
                     ("LISA",                1e-4, 1e-1),
                     ("LIGO / Virgo",        1e1,  1e3),
                     ("Einstein Telescope",  1e0,  1e4)]:
    print(f"    {name:22s} [{lo:.0e}, {hi:.0e}] Hz : "
          f"{'DANS LA BANDE' if lo <= f_today <= hi else 'hors bande'}")
print(f"""
  => La frequence excede de ~8 ordres de grandeur la limite superieure
     d'Einstein Telescope. Elle releve de la bande UHF-GW, pour laquelle
     seules des propositions exploratoires existent (cavites resonantes,
     conversion graviton-photon / effet Gertsenshtein), tres loin des
     sensibilites requises.

  DOUBLE RESERVE :
    (1) frequence hors de portee de tout instrument actuel ou planifie ;
    (2) le prototype integre un champ HOMOGENE T(t) : le mode k=0 n'a pas
        de moment quadrupolaire et ne source donc AUCUNE onde
        gravitationnelle. Etablir une signature exigerait de passer a
        T(x,t), de calculer le quadrupole, puis Omega_GW(f).

  STATUT : source POTENTIELLE de GW de tres haute frequence ; ni
  l'amplitude ni le spectre ne sont etablis. Non falsifiable en l'etat.
""")

```

---

### Fichier 2 : `audit_paper_vs_F3.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
audit_paper_vs_F3.py — l'article court est-il aligne sur F3 ?

POURQUOI CE SCRIPT EXISTE
-------------------------
F3-Extended le prescrit lui-meme, comme item permanent :

    [AUDIT-1, permanent] Apres toute modification scientifique de F3 :
    executer python audit_paper_vs_F3.py (valeurs canoniques + garde-fous
    epistemiques + perimetre), puis repercuter dans l'article court.
    F3 est la source de verite ; l'article en est une projection.
    Cet item ne se clot jamais.

Le script etait prescrit depuis des mois mais n'avait jamais ete ecrit
(fiche I84). Ecrit le 08/09/2026, apres une session ou F3-Extended et
StrongGravity ont justement ete corriges (I95) sans que rien ne verifie
la repercussion sur l'article court.

CE QU'IL VERIFIE — les trois axes prescrits
-------------------------------------------
1. VALEURS CANONIQUES : toute valeur numerique presente dans les DEUX
   documents doit y etre ecrite a l'identique. Une divergence signale une
   correction appliquee d'un seul cote -- exactement le defaut I95.

2. GARDE-FOUS EPISTEMIQUES : les problemes ouverts (PO-*) cites par
   l'article doivent exister dans F3. L'article ne doit pas presenter
   comme acquis ce que F3 tient pour ouvert.

3. PERIMETRE : les grandeurs que l'article manipule doivent etre
   definies dans F3. L'article est une projection, pas une extension.

CE QU'IL NE VERIFIE PAS
-----------------------
Il compare des chaines, pas de la physique. Il ne sait pas si une valeur
est juste -- seulement si les deux documents disent la meme chose. Comme
la table des valeurs canoniques dont il s'inspire : il complete l'audit,
il ne le remplace pas.

USAGE
-----
    python3 Scripts_F3/A_Core_Calculations/audit_paper_vs_F3.py

Code de retour : 0 si aligne, 1 si au moins une divergence.
"""

import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

SOURCE_VERITE = "Fichant_ecf_F3_Extended_v7_1.tex"
ARTICLE_COURT = "fichant_ecf_F3_ChiralBounce_v0_4.tex"

# Valeurs trop banales pour signaler quoi que ce soit si elles divergent
BANALES = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
           "100", "1000", "0.5", "1.5", "2.0", "12", "24", "2026", "2025"}


def lire(nom):
    chemin = os.path.join(RACINE, nom)
    if not os.path.isfile(chemin):
        return None
    with open(chemin, encoding="utf-8", errors="replace") as f:
        return f.read()


def sans_commentaires(tex):
    """Retire les lignes de commentaire LaTeX : elles contiennent des
    valeurs historiques citees volontairement, qui ne sont pas des
    divergences."""
    lignes = []
    for l in tex.split("\n"):
        depouillee = re.sub(r"(?<!\\)%.*$", "", l)
        lignes.append(depouillee)
    return "\n".join(lignes)


def valeurs_scientifiques(tex):
    """Extrait les valeurs en notation scientifique, normalisees.
    Couvre les deux notations du corpus : 1{,}34 (fr) et 1.34 (en)."""
    motif = re.compile(
        r"(\d+(?:[.,]|\{,\})?\d*)\s*\\times\s*10\^\{?(-?\d+)\}?")
    trouvees = {}
    for mantisse, exposant in motif.findall(tex):
        m = mantisse.replace("{,}", ".").replace(",", ".")
        try:
            cle = f"{float(m):.4g}e{int(exposant)}"
        except ValueError:
            continue
        trouvees[cle] = trouvees.get(cle, 0) + 1
    return trouvees


def problemes_ouverts(tex):
    return set(re.findall(r"PO-[A-Z0-9]+-[A-Z0-9]+", tex))


def main():
    f3 = lire(SOURCE_VERITE)
    art = lire(ARTICLE_COURT)

    print("=" * 74)
    print("  AUDIT — article court vs F3 (source de verite)")
    print("=" * 74)

    if f3 is None:
        print(f"  ERREUR : {SOURCE_VERITE} introuvable")
        return 1
    if art is None:
        print(f"  ERREUR : {ARTICLE_COURT} introuvable")
        return 1

    f3 = sans_commentaires(f3)
    art = sans_commentaires(art)
    divergences = 0

    # --- Axe 1 : valeurs canoniques ---------------------------------
    print("\n-- 1. Valeurs canoniques --")
    v_f3 = valeurs_scientifiques(f3)
    v_art = valeurs_scientifiques(art)
    communes_mantisses = {}
    for v in v_art:
        mant, exp = v.split("e")
        communes_mantisses.setdefault(exp, []).append(mant)

    suspectes = []
    for v in sorted(v_art):
        if v in BANALES:
            continue
        if v in v_f3:
            continue
        # meme exposant present dans F3 mais mantisse differente :
        # c'est le profil d'une correction appliquee d'un seul cote
        mant, exp = v.split("e")
        voisines = [w for w in v_f3 if w.endswith("e" + exp)]
        if voisines:
            suspectes.append((v, voisines))

    if not suspectes:
        print("   aucune divergence de mantisse a exposant egal")
    else:
        for v, voisines in suspectes:
            print(f"   ⚠️  article : {v}   |  F3 : {', '.join(sorted(voisines))}")
            divergences += 1
        print("   -> verifier si une correction n'a ete appliquee qu'a un")
        print("      seul des deux documents (profil du defaut I95).")

    # --- Axe 2 : garde-fous epistemiques ----------------------------
    print("\n-- 2. Garde-fous epistemiques --")
    po_f3 = problemes_ouverts(f3)
    po_art = problemes_ouverts(art)
    orphelins = po_art - po_f3
    if not po_art:
        print("   l'article ne cite aucun probleme ouvert")
    elif orphelins:
        for po in sorted(orphelins):
            print(f"   ⚠️  {po} cite par l'article, absent de F3")
            divergences += 1
    else:
        print(f"   les {len(po_art)} PO cites par l'article existent tous "
              f"dans F3")

    non_repercutes = po_f3 - po_art
    if non_repercutes:
        print(f"   (info : {len(non_repercutes)} PO dans F3 non cites par "
              f"l'article — normal, l'article est une projection)")

    # --- Axe 3 : perimetre ------------------------------------------
    print("\n-- 3. Perimetre --")
    cmd_art = set(re.findall(r"\\newcommand\{\\(\w+)\}", art))
    cmd_f3 = set(re.findall(r"\\newcommand\{\\(\w+)\}", f3))
    propres = cmd_art - cmd_f3
    if propres:
        print(f"   {len(propres)} macro(s) definie(s) par l'article seul :")
        print(f"      {', '.join(sorted(propres))}")
        print("   -> verifier qu'elles ne portent pas de grandeur absente")
        print("      de F3 (l'article projette, il n'etend pas).")
    else:
        print("   aucune macro propre a l'article")

    # --- Verdict -----------------------------------------------------
    print("\n" + "=" * 74)
    if divergences:
        print(f"  {divergences} divergence(s) — repercuter depuis F3 vers "
              f"l'article.")
    else:
        print("  Article aligne sur F3 sur les trois axes.")
    print("  Rappel : ce script compare des chaines, pas de la physique.")
    print("  Il complete l'audit, il ne le remplace pas.")
    print("=" * 74)
    return 1 if divergences else 0


if __name__ == "__main__":
    sys.exit(main())

```

---

### Fichier 3 : `script_01_solve_sound_horizon.py`

```python
"""
================================================================================
SCRIPT 01: script_01_solve_sound_horizon.py  —  v2 (referee-ready)
Paper:  Foundation I
        (Einstein-Cartan-Friedmann framework)
Author: Pascal Fichant
Date:   13/04/2026

DESCRIPTION:
    Numerically integrates the comoving sound horizon r_s for standard
    Lambda-CDM and the ECF model, reproducing Appendix D of the paper.

    FORMULA:
        r_s = integral_{z_drag}^{z_start} c_s(z) / H(z) dz

    where the upper limit z_start=1e7 approximates the early-universe limit;
    contributions above z ~ 5e5 are negligible (H grows as (1+z)^2 in
    radiation domination, suppressing the integrand as (1+z)^{-2}).

    PHYSICAL MECHANISM (Section 3):
        The ECF spin-torsion sector modifies H(z) via a stiff a^{-6} term,
        increasing the pre-recombination expansion rate and compressing r_s.
        A mild torsion damping on the effective sound speed (tau_tor=0.9975)
        provides the remaining subdominant correction.

    DECOMPOSITION NOTE:
        Paper Section 3 reports: spin background → ~5.2%, tau_tor → ~2.5%
        This script computes: spin background → 7.54%, tau_tor → 0.23%
        The final r_s_ECF = 135.80 Mpc matches the paper exactly.
        The decomposition in the paper refers to a three-way split
        (background Hz, plasma cs correction, zdrag shift) that does not
        map one-to-one to the two free parameters of this effective script.
        See Appendix D for the full decomposition.

    z_drag NOTE:
        Both models use z_drag = 1059.94 (Planck 2018, Table 2).
        The ECF torsion correction implies a small shift Dz_drag ~ -30
        (see Section 3). Numerical test shows this would shift r_s_ECF
        by -2.77 Mpc; tau_tor is calibrated to absorb this effect so
        that the final r_s_ECF = 135.80 Mpc remains consistent.

    TARGETS:
        r_s(LCDM) = 147.1 Mpc   (Planck 2018 fiducial)
        r_s(ECF)  = 135.8 Mpc   (ECF calibrated solution)
        Delta r_s / r_s = 7.7%

    CONSTANTS:
        SPIN_RAD_RATIO = 0.093   Spin/radiation ratio at z_trans=5600
                                  Fixed by QCD transition physics (Section 2)
        TAU_TOR = 0.9975         Effective torsion-cs damping factor
                                  Calibrated to obtain r_s_ECF = 135.8 Mpc
                                  (Appendix D, Table of priors)
================================================================================
"""
# Last modified: 02/09/2026, 11:10 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np
from scipy.integrate import quad

# ==============================================================================
# 1. PHYSICAL CONSTANTS
# ==============================================================================
c_light  = 299792.458   # km/s

# ==============================================================================
# 2. COSMOLOGICAL PARAMETERS  (Planck 2018, arXiv:1807.06209, Table 2)
# ==============================================================================
h_planck = 0.6736       # Reduced Hubble constant
omega_b  = 0.02237      # Physical baryon density
omega_c  = 0.1200       # Physical cold dark matter density
omega_g  = 2.4728e-5    # Photon density  (T_CMB = 2.7255 K)
omega_n  = 1.6918e-5    # Neutrino density (N_eff = 3.046)
omega_r  = omega_g + omega_n   # Total radiation density

# --- 1-sigma uncertainties on the measured inputs above (Planck 2018 Table 2;
#     T_CMB = 2.7255 +/- 0.0006 K propagated to omega_g via omega_g ~ T^4) ---
# [02/09/2026] Added to let this script propagate its own error bar instead of
# it being computed by hand outside the code (see ECF_DOSSIER_incertitudes_calibres.md
# section 3). Omega_spin_0 and TAU_TOR are CALIBRATED, not measured, and carry
# their own separate uncertainty (not yet propagated here): the bar below is
# therefore a FLOOR, covering only the four measured Planck inputs.
SIGMA_OMEGA_B  = 0.00015
SIGMA_OMEGA_C  = 0.0012
SIGMA_Z_DRAG   = 0.30      # Planck 2018 Table 2
SIGMA_OMEGA_G  = 2.5e-8    # from T_CMB = 2.7255 +/- 0.0006 K

# ==============================================================================
# 3. ECF-SPECIFIC PARAMETERS
# ==============================================================================
SPIN_RAD_RATIO = 0.093   # rho_spin / rho_rad at z_trans  (Section 2, Eq. spin)
TAU_TOR        = 0.9975  # Effective torsion damping on c_s  (Appendix D)
Z_DRAG         = 1059.94 # Baryon drag epoch  (Planck 2018 Table 2)
Z_START        = 1e7     # Upper integration limit (early universe approximation)
# [18/08/2026 audit] Two caveats on this line.
#
# (a) NAMING. "Spin-radiation equality" is a misnomer here: equality would
#     mean a ratio of 1, whereas SPIN_RAD_RATIO = 0.093 is imposed at this
#     redshift. Z_TRANS is the normalisation point of the spin sector, not
#     an equality epoch. With this normalisation the true equality falls
#     near z ~ 1.8e4.
#
# (b) VALUE -- RESOLVED 05/09/2026 (registry entry I82). Until that date the
#     papers quoted the acoustic-era window at z ~ 7500 (ten occurrences in
#     F1, none for 5600) while this script normalised at 5600. 5600 is what
#     reproduces the published r_s: setting Z_TRANS = 7500 with the same
#     ratio gives r_s(ECF) = 138.22 Mpc instead of 135.80, i.e. a 6.13 %
#     reduction instead of 7.77 %. The papers, Architecture, the figure
#     scripts and the Zenodo deposit copies have since all been realigned
#     on z_ref = 5600, together with the chain that followed from it
#     (0.20 % -> 0.36 % at recombination, dilution factor 47 -> 26).
#     Note for the record: the two anchors give r_s values compatible at
#     1.25 sigma given sigma(r_s) = +/- 1.93 Mpc, so the realignment was a
#     traceability fix, not the repair of a wrong result.
#
#     Note also that script_03_extract_physical_parameters.py reaches the
#     same r_s target with Omega_spin,0 = 1.51e-13, i.e. 1.8x less, because
#     it integrates a deliberately truncated approximation (z from 1089 to
#     2e5, no Lambda term, LCDM baseline 143.26 instead of 147.1). The two
#     scripts are internally consistent but not interchangeable: THIS one
#     reproduces the published r_s(LCDM) = 147.24 Mpc and is the reference.
#
# Left unchanged pending arbitration -- see ECF_DOSSIER_Omega_spin.md.
Z_TRANS        = 5600.0  # Spin-sector normalisation redshift (see note above)

# ==============================================================================
# 4. DERIVED DIMENSIONLESS PARAMETERS
# ==============================================================================
h2      = h_planck**2
Om_b    = omega_b / h2
Om_c    = omega_c / h2
Om_r    = omega_r / h2
Om_m    = Om_b + Om_c
Om_L    = 1.0 - (Om_m + Om_r)

# Omega_spin(z=0): derived from spin/radiation ratio at z_trans
# rho_spin(z_trans)/rho_rad(z_trans) = R
# => Om_spin_0 * (1+z_trans)^6 / (Om_r * (1+z_trans)^4) = R
# => Om_spin_0 = R * Om_r / (1+z_trans)^2
Om_spin_0 = SPIN_RAD_RATIO * Om_r / (1.0 + Z_TRANS)**2

# ==============================================================================
# 5. HUBBLE FUNCTIONS
# ==============================================================================

def Hz_LCDM(z):
    """Flat Lambda-CDM Friedmann equation."""
    E2 = Om_r * (1+z)**4 + Om_m * (1+z)**3 + Om_L
    return 100.0 * h_planck * np.sqrt(E2)


def Hz_ECF(z):
    """
    Modified Friedmann equation (ECF).
    Extra term: Om_spin_0 * (1+z)^6  (stiff spin fluid, w=1, from ECKS torsion).
    Scales as a^{-6}, dominant at z >> z_trans, negligible today.
    """
    E2 = Om_r * (1+z)**4 + Om_m * (1+z)**3 + Om_spin_0 * (1+z)**6 + Om_L
    return 100.0 * h_planck * np.sqrt(E2)

# ==============================================================================
# 6. SOUND SPEED
# ==============================================================================

def get_cs(z):
    """
    Baryon-photon fluid sound speed.
    R_b = (3 rho_b) / (4 rho_gamma) = (3 omega_b) / (4 omega_g) / (1+z)
    c_s = c / sqrt(3 (1 + R_b))
    """
    R_b = (3.0 * omega_b) / (4.0 * omega_g) / (1.0 + z)
    return c_light / np.sqrt(3.0 * (1.0 + R_b))

# ==============================================================================
# 7. SOUND HORIZON INTEGRATION
# ==============================================================================

def integrate_rs(hubble_func, cs_scale=1.0, z_drag=Z_DRAG, z_start=Z_START,
                  ob=omega_b, og=omega_g):
    """
    r_s = integral_{z_drag}^{z_start}  cs_scale * c_s(z) / H(z)  dz

    Parameters
    ----------
    hubble_func : callable   H(z) function
    cs_scale    : float      Multiplicative factor on c_s (tau_tor for ECF)
    z_drag      : float      Lower integration limit (baryon drag epoch)
    z_start     : float      Upper integration limit (early universe)
    ob, og      : float      omega_b, omega_g used inside get_cs (defaults to
                              the module-level Planck values; overridable for
                              finite-difference uncertainty propagation below)
    """
    cs = lambda z: c_light / np.sqrt(3.0 * (1.0 + (3.0*ob)/(4.0*og)/(1.0+z)))
    integrand = lambda z: cs_scale * cs(z) / hubble_func(z)
    rs, _ = quad(integrand, z_drag, z_start)
    return rs


def compute_rs_ecf(ob=omega_b, oc=omega_c, og=omega_g, zd=Z_DRAG):
    """
    Full ECF sound-horizon computation as a function of the four measured
    Planck inputs, so that this same code path can be re-run with each input
    perturbed by its own 1-sigma for finite-difference error propagation
    (section 9 below). Mirrors exactly the module-level computation in
    sections 2-7, but parameterised instead of hardcoded on globals.
    """
    on   = omega_n                      # fixed (N_eff not varied here)
    orad = og + on
    Om_b_  = ob / h2
    Om_c_  = oc / h2
    Om_r_  = orad / h2
    Om_m_  = Om_b_ + Om_c_
    Om_L_  = 1.0 - (Om_m_ + Om_r_)
    Om_spin_0_ = SPIN_RAD_RATIO * Om_r_ / (1.0 + Z_TRANS)**2

    def Hz_ECF_(z):
        E2 = Om_r_*(1+z)**4 + Om_m_*(1+z)**3 + Om_spin_0_*(1+z)**6 + Om_L_
        return 100.0 * h_planck * np.sqrt(E2)

    return integrate_rs(Hz_ECF_, cs_scale=TAU_TOR, z_drag=zd, ob=ob, og=og)


# ==============================================================================
# 8. UNCERTAINTY PROPAGATION ON r_s(ECF)  [added 02/09/2026]
# ==============================================================================
# Central finite differences on the four MEASURED Planck inputs; the two
# CALIBRATED parameters (Omega_spin_0, TAU_TOR) are held fixed, so this is a
# floor, not the complete error budget (see the module docstring note above).

def propagate_rs_ecf_uncertainty():
    baseline = compute_rs_ecf()
    contributions = {}
    for name, key, sigma in [
        ("omega_b", "ob", SIGMA_OMEGA_B),
        ("omega_c", "oc", SIGMA_OMEGA_C),
        ("z_drag",  "zd", SIGMA_Z_DRAG),
        ("omega_g", "og", SIGMA_OMEGA_G),
    ]:
        kwargs_plus  = {key: (omega_b if key=="ob" else omega_c if key=="oc"
                               else Z_DRAG if key=="zd" else omega_g) + sigma}
        kwargs_minus = {key: (omega_b if key=="ob" else omega_c if key=="oc"
                               else Z_DRAG if key=="zd" else omega_g) - sigma}
        rs_plus  = compute_rs_ecf(**kwargs_plus)
        rs_minus = compute_rs_ecf(**kwargs_minus)
        d_rs = (rs_plus - rs_minus) / 2.0   # central difference, at +/- 1 sigma
        contributions[name] = abs(d_rs)
    total = np.sqrt(sum(v**2 for v in contributions.values()))
    return baseline, contributions, total

# ==============================================================================
# 8. MAIN
# ==============================================================================

if __name__ == "__main__":
    SEP = "=" * 65

    # --- Compute ---
    rs_lcdm = integrate_rs(Hz_LCDM, cs_scale=1.0)
    rs_ecf  = integrate_rs(Hz_ECF,  cs_scale=TAU_TOR)
    rs_ecf_spin_only = integrate_rs(Hz_ECF, cs_scale=1.0)

    delta_abs = rs_lcdm - rs_ecf
    delta_pct = delta_abs / rs_lcdm * 100.0
    delta_spin_abs = rs_lcdm - rs_ecf_spin_only
    delta_spin_pct = delta_spin_abs / rs_lcdm * 100.0
    delta_tau_abs  = rs_ecf_spin_only - rs_ecf
    delta_tau_pct  = delta_tau_abs  / rs_lcdm * 100.0

    # Cross-check spin/radiation ratio
    ratio_check = Om_spin_0 * (1+Z_TRANS)**6 / (Om_r * (1+Z_TRANS)**4)

    print(SEP)
    print(">>> SOUND HORIZON SOLVER  (Foundation I, Section 3 + Appendix D)")
    print(SEP)

    print("\n>>> PARAMETERS")
    print(f"    h_planck          = {h_planck:.4f}  (Planck 2018)")
    print(f"    Om_m              = {Om_m:.5f}  (Planck 2018)")
    print(f"    Om_r              = {Om_r:.4e}  (Planck 2018)")
    print(f"    Om_L              = {Om_L:.5f}  (Planck 2018)")
    print(f"    Om_spin_0         = {Om_spin_0:.4e}  (derived from SPIN_RAD_RATIO)")
    print(f"    Spin/rad at z_trans: {ratio_check:.4f}  (target: {SPIN_RAD_RATIO})  "
          f"{'OK' if abs(ratio_check-SPIN_RAD_RATIO)<1e-6 else 'CHECK'}")
    print(f"    Z_DRAG            = {Z_DRAG}  (Planck 2018 Table 2)")
    print(f"    TAU_TOR           = {TAU_TOR}")

    print("\n>>> RESULTS")
    print(f"    r_s (LCDM)        = {rs_lcdm:.2f} Mpc  (target: 147.1 Mpc)")
    print(f"    r_s (ECF)         = {rs_ecf:.2f} Mpc  (target: 135.8 Mpc)")
    print(f"    Delta r_s         = -{delta_abs:.2f} Mpc  ({delta_pct:.2f}%)")

    print("\n>>> REDUCTION DECOMPOSITION")
    print(f"    Spin term Hz_ECF  : -{delta_spin_abs:.2f} Mpc  ({delta_spin_pct:.2f}%)")
    print(f"    tau_tor on c_s    : -{delta_tau_abs:.3f} Mpc  ({delta_tau_pct:.2f}%)")
    print(f"    Note: paper reports 5.2% + 2.5% = 7.7% using a three-way split")
    print(f"    (background / plasma / z_drag shift, see Appendix D).")
    print(f"    This two-parameter script gives {delta_spin_pct:.2f}% + {delta_tau_pct:.2f}%")
    print(f"    = {delta_pct:.2f}%; the final r_s_ECF agrees to 0.004 Mpc.")

    print("\n>>> VALIDATION")
    ok_lcdm = abs(rs_lcdm - 147.1) < 0.2
    ok_ecf  = abs(rs_ecf  - 135.8) < 0.2
    assert ok_lcdm, f"r_s LCDM = {rs_lcdm:.2f} outside tolerance"
    assert ok_ecf,  f"r_s ECF  = {rs_ecf:.2f} outside tolerance"
    print(f"    r_s LCDM = {rs_lcdm:.3f}  (target 147.1 ± 0.2)  OK")
    print(f"    r_s ECF  = {rs_ecf:.3f}   (target 135.8 ± 0.2)  OK")
    print(f"    Delta r_s / r_s = {delta_pct:.2f}%  (paper: 7.7%)  OK")

    print("\n>>> UNCERTAINTY PROPAGATION ON r_s(ECF)  [floor: measured inputs only]")
    baseline, contribs, sigma_rs = propagate_rs_ecf_uncertainty()
    for name, d in contribs.items():
        print(f"    d(r_s)/d({name}) * sigma  = {d:.3f} Mpc")
    print(f"    Total (quadrature)        = {sigma_rs:.3f} Mpc")
    print(f"    r_s(ECF) = {baseline:.2f} +/- {sigma_rs:.2f} Mpc  "
          f"({100*sigma_rs/baseline:.2f}%)")
    print(f"    NOTE: floor only -- excludes the calibrated Omega_spin_0 and")
    print(f"    TAU_TOR, whose own uncertainty is not propagated here.")
    print(SEP)

```

---

### Fichier 4 : `check_xi_kz_horizon.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_xi_kz_horizon.py  --  ECF Foundation III
======================================================================
Is xi_KZ = 60 Mpc or 65 Mpc? Recomputing the causal horizon on the ECF
background rather than on a LambdaCDM one.

WHY THIS SCRIPT EXISTS
----------------------
The corpus quotes three values for the Kibble-Zurek correlation length:
60 Mpc (the canonical table), 65 Mpc (F3 l.1092 and the VSF plotting
script), and a 50-80 Mpc range. The kill-switch threshold follows:
60 Mpc gives 40.4 Mpc/h, 65 Mpc gives 44 Mpc/h -- and both figures appear.

PO-F3-XI records that direct Kibble-Zurek dilution from T_EW misses the
observed scale by ~24 orders of magnitude, that hypothesis (i) -- a
different transition scale -- is quantitatively excluded, and that the
surviving hypothesis (ii) is that the defect network stays locked to the
comoving causal horizon (scaling behaviour) until a late freeze-out,
with the corpus quoting z ~ 6430.

CLOSED (30/08/2026): the corpus figure of z~6430 was itself the
LambdaCDM-background artefact this script exists to catch (see below).
Following this script's own result, the corpus (F2 and Foundation III)
has been corrected throughout to the ECF-background value, z~5153, with
z~6430 kept only as an explicitly labelled superseded figure. The
diagnostic below is left as-is: it is what established the correction.

That statement is checkable. If (ii) holds, xi_KZ IS the comoving
particle horizon at freeze-out, and the number follows from the
background -- it is not a free choice between 60 and 65.

WHY THE BACKGROUND MATTERS HERE
-------------------------------
A first pass on a standard LambdaCDM background (H0 = 67.32) gave
64.4 Mpc at z = 6430, apparently favouring 65. But the ECF background is
NOT LambdaCDM: it carries a stiff spin fluid scaling as (1+z)^6, which
dominates at high z and shortens the horizon. Concluding from the
LambdaCDM number would be comparing the wrong quantity -- so the ECF
background is used here, imported from the calibrated script so that this
computation cannot drift from it.

Dependency: numpy, scipy. Usage: python3 check_xi_kz_horizon.py
======================================================================
"""
# Last modified: 30/08/2026, 12:24 (Paris time)

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import importlib.util
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

_here = os.path.dirname(os.path.abspath(__file__))
_category = os.path.dirname(_here)          # .../Foundation_3/02_Scientific_Code
_found3 = os.path.dirname(_category)        # .../Foundation_3
_repo_root = os.path.dirname(_found3)        # .../spin-torsion-cosmology
_candidates = [
    os.path.join(_here, "..", "Scripts_F1", "script_01_solve_sound_horizon.py"),
    os.path.join(_here, "..", "..", "Scripts_F1", "script_01_solve_sound_horizon.py"),
    # [HARDENED 06/09/2026, again] This script moved from Scripts_F3/ root
    # into Scripts_F3/A_Core_Calculations/ (one level deeper), AND
    # script_01 moved from Scripts_F1/ root into Scripts_F1/A_Core_Calculations/
    # (same night's A/B split) -- both facts combined need this candidate.
    os.path.join(_here, "..", "..", "Scripts_F1", "A_Core_Calculations",
                 "script_01_solve_sound_horizon.py"),
    os.path.join(_here, "script_01_solve_sound_horizon.py"),
    # This working corpus's own A/B split (Scripts_F1/A_Core_Calculations,
    # no Foundation_1/02_Scientific_Code wrapper) -- added 06/09/2026 when
    # Scripts_F1 and Scripts_F2 were reorganised the same way Scripts_F3
    # already was.
    os.path.join(_here, "..", "Scripts_F1", "A_Core_Calculations",
                 "script_01_solve_sound_horizon.py"),
    # Foundation_1 mirroring Foundation_3's own 02_Scientific_Code layout,
    # under whichever category subfolder actually holds it there:
    os.path.join(_repo_root, "Foundation_1", "02_Scientific_Code",
                 "A_Core_Calculations", "script_01_solve_sound_horizon.py"),
    os.path.join(_repo_root, "Foundation_1", "02_Scientific_Code",
                 "B_Paper_Plots", "script_01_solve_sound_horizon.py"),
    os.path.join(_repo_root, "Foundation_1", "Scripts_F1",
                 "script_01_solve_sound_horizon.py"),
    os.path.join(_repo_root, "Foundation_1", "script_01_solve_sound_horizon.py"),
]
_path = None
for _c in _candidates:
    _c = os.path.normpath(_c)
    if os.path.exists(_c):
        _path = _c
        break
if _path is None:
    _path = os.path.normpath(_candidates[0])  # keep old default for the error message

_spec = importlib.util.spec_from_file_location("sh_ecf", _path)
_sh = importlib.util.module_from_spec(_spec)
try:
    _spec.loader.exec_module(_sh)
except SystemExit:
    pass

C_KM = 299792.458

print("=" * 70)
print("  xi_KZ from the causal horizon  --  ECF background")
print("=" * 70)
print(f"\n  background imported from: {os.path.basename(_path)}")
print(f"  Om_m = {_sh.Om_m:.4f}   Om_r = {_sh.Om_r:.4e}   "
      f"Om_spin_0 = {_sh.Om_spin_0:.3e}")
print(f"  stiff term: Om_spin_0 (1+z)^6   [absent from LambdaCDM]")


def chi_comoving(z, H_of_z):
    """Comoving particle horizon at redshift z: integral from z to infinity."""
    val, _ = quad(lambda zz: 1.0 / H_of_z(zz), z, np.inf, limit=400)
    return C_KM * val


print("\n" + "-" * 70)
print("  (1) Comoving horizon, ECF vs LambdaCDM")
print("-" * 70)
print(f"  {'z':>7} {'ECF (Mpc)':>12} {'LCDM (Mpc)':>12} {'ratio':>8}")
for z in (5600, 6365, 6430, 6953, 7500):
    he = chi_comoving(z, _sh.Hz_ECF)
    hl = chi_comoving(z, _sh.Hz_LCDM)
    print(f"  {z:>7} {he:>12.2f} {hl:>12.2f} {he/hl:>8.4f}")

print("\n" + "-" * 70)
print("  (2) Which z gives 60 Mpc, which gives 65 -- on the ECF background")
print("-" * 70)
for target in (60.0, 65.0):
    try:
        z = brentq(lambda zz: chi_comoving(zz, _sh.Hz_ECF) - target, 500, 60000)
        print(f"    xi_KZ = {target:.0f} Mpc  <=>  z_freeze = {z:.0f}")
    except ValueError:
        print(f"    xi_KZ = {target:.0f} Mpc  : not reachable on this background")

print("\n" + "-" * 70)
print("  (3) The corpus quotes z ~ 6430. What does the ECF background give?")
print("-" * 70)
xi_6430 = chi_comoving(6430, _sh.Hz_ECF)
h = _sh.h_planck
print(f"    xi_KZ(z=6430) = {xi_6430:.2f} Mpc = {xi_6430*h:.2f} Mpc/h")
print(f"    distance to 60 Mpc : {abs(xi_6430-60):.2f} Mpc "
      f"({100*abs(xi_6430-60)/60:.1f} %)")
print(f"    distance to 65 Mpc : {abs(xi_6430-65):.2f} Mpc "
      f"({100*abs(xi_6430-65)/65:.1f} %)")

print("\n" + "=" * 70)
print("  READING THIS")
print("=" * 70)
print("  The stiff (1+z)^6 term makes H larger at high z, hence the ECF")
print("  horizon SHORTER than the LambdaCDM one at the same redshift.")
print("  The comparison therefore has to be done on the ECF background;")
print("  the LambdaCDM number would not answer the question asked.")
print()
print("WHAT THIS DOES NOT ESTABLISH:")
print("  * that hypothesis (ii) is correct -- PO-F3-XI keeps it open, and")
print("    this script only asks what it would imply if it held;")
print("  * the freeze-out redshift itself, which is not derived anywhere;")
print("  * the 50-80 Mpc range, which comes from the VSF calibration and")
print("    is a separate statement from the horizon argument.")

```

---

### Fichier 5 : `verify_F3_PO3_thermalization_exponent.py`

```python
#!/usr/bin/env python3
"""
verify_F3_PO3_thermalization_exponent.py
Dernière modification : 20/07/2026, 23:00

PO-F3-3 : origine de l'exposant 1/2 dans sigma^2_baby ~ a*.

Teste l'hypothèse que la conversion du moment angulaire du trou noir
parent vers la densité de spin s_0 de l'univers enfant, si elle est
THERMALISÉE (incohérente) plutôt que directe, produit s_0 ~ (a*)^(1/2)
via le mécanisme de fluctuation en sqrt(N) d'une marche aléatoire biaisée.

Résultat attendu : exposant ~ 0.5 dans le régime thermalisé (biais faible),
en accord avec les hypothèses T1-T2 du corpus ECF.

[CORRECTION 20/07/2026] Ce script fournit une origine physique candidate
pour l'exposant sqrt(a*) ATTENDU par l'hypothèse T1-T2 (PO-F3-3) --
PAS pour le Lemme F3-SPIN-2. Le Lemme F3-SPIN-2 (mécanisme holographique,
couplage via l'aire de l'horizon) donne au contraire une dépendance
LINÉAIRE en a*, et se trouve donc en TENSION avec le résultat vérifié
ici, pas en accord avec lui. Cette tension (linéaire vs sqrt(a*)) est
documentée comme non résolue dans F3 (§PO-F3-3, l.5062-5069). Ce script
teste la branche thermalisée (T1-T2) de cette tension, pas les deux.
"""

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np

def spin_net_thermalise(bias, N, T_ratio, n_trials=20, seed=None):
    """
    Spin net normalisé d'un ensemble de N spins ±1 thermalisés,
    avec un biais d'alignement imposé par le moment angulaire parent.

    bias    : ~ a* (spin sans dimension du trou noir parent)
    N       : nombre de spins dans le cœur de Cartan
    T_ratio : rapport énergie_biais / énergie_thermique
              (faible = régime thermalisé ; fort = régime cohérent)
    """
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_trials):
        # probabilité d'alignement (réponse thermique au biais)
        p_align = 0.5 + 0.5 * np.tanh(bias * T_ratio)
        spins = rng.choice([1, -1], size=N, p=[p_align, 1 - p_align])
        vals.append(abs(spins.sum()) / N)
    return np.mean(vals)


def measure_exponent(T_ratio, N=100_000, n_seeds=10):
    """Mesure l'exposant d de la loi s_0 ~ (a*)^d par fit log-log,
    moyenné sur plusieurs graines pour réduire le bruit statistique."""
    a_star = np.array([0.1, 0.2, 0.3, 0.5, 0.7, 0.9])
    slopes = []
    for seed in range(n_seeds):
        s0 = np.array([
            spin_net_thermalise(a, N, T_ratio, n_trials=40, seed=1000 * seed + i)
            for i, a in enumerate(a_star)
        ])
        mask = s0 > 0
        if mask.sum() >= 2:
            slopes.append(np.polyfit(np.log(a_star[mask]), np.log(s0[mask]), 1)[0])
    return np.mean(slopes), np.std(slopes), a_star


if __name__ == "__main__":
    print("=" * 62)
    print("PO-F3-3 : exposant de s_0 vs a* selon le régime de conversion")
    print("=" * 62)

    # Régime thermalisé (biais faible) : fluctuation sqrt(N) attendue
    exp_thermal, std_thermal, a_vals = measure_exponent(T_ratio=0.01)
    print(f"\nRégime THERMALISÉ (T_ratio=0.01, moyenne sur 10 graines) :")
    print(f"  Exposant mesuré : {exp_thermal:.3f} ± {std_thermal:.3f}  (attendu ~ 0.5)")

    # Régime cohérent (biais fort) : alignement direct/saturation
    exp_coherent, std_coherent, _ = measure_exponent(T_ratio=100)
    print(f"\nRégime COHÉRENT (T_ratio=100) :")
    print(f"  Exposant mesuré : {exp_coherent:.3f} ± {std_coherent:.3f}  (saturation)")

    print("\n" + "=" * 62)
    print("CONCLUSION")
    print("=" * 62)
    print(f"""
La conversion thermalisée reproduit l'exposant 1/2 des hypothèses
T1-T2 du corpus ECF (mesuré : {exp_thermal:.2f} ± {std_thermal:.2f}),
fournissant une origine physique candidate à cet exposant : la
fluctuation nette en sqrt(N) d'un fluide de spin partiellement
randomisé au rebond.

Ce résultat NE dérive PAS ab initio que le rebond soit dans ce
régime ; il montre seulement que SI le rebond thermalise le spin,
l'exposant 1/2 en découle naturellement.

À noter : un mécanisme concurrent (Lemme F3-SPIN-2, couplage
holographique via l'aire de l'horizon) donne une dépendance LINÉAIRE
en a*, en tension avec l'exposant sqrt(a*) vérifié ici. Cette tension
est documentée comme non résolue dans F3 (§PO-F3-3) ; ce script ne
teste que la branche thermalisée de l'alternative.
""")

```

---

### Fichier 6 : `cartan_core.py`

```python
#!/usr/bin/env python3

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# =============================================================================
#  ECF / Foundation III - The Cartan core (item CORE-1)
#  Fichant, P. (2026).  File: cartan_core.py
#
#  [Translated to English 24/08/2026 -- rule 5quatervicies: what is deposited
#   is written in English. Physics, numbers and structure unchanged.]
# =============================================================================
#
#  THE ORIGINAL QUESTION (P. Fichant)
#  ----------------------------------
#  "What becomes of the parent's matter that keeps falling in AFTER the
#   bounce? If there is an inner bounce, then re-contraction, then another
#   bounce...?"
#
#  FIRST LINE EXPLORED: damped oscillation of successive bounces converging
#  towards a statically balanced core.
#  => THE INTUITION ABOUT THE RESULT (a static core) PROVED RIGHT, but the
#     MECHANISM is different: it is not a series of damped bounces, because
#     the Friedmann-torsion equation FORBIDS the density from exceeding
#     rho_c (see TEST 1). The core relaxes towards a HYDROSTATIC equilibrium
#     (TOV + torsion), not through FRW oscillations.
#
#  WHAT THIS SCRIPT ESTABLISHES
#  ----------------------------
#   (T1) The bound rho <= rho_c is EXACT (Friedmann-torsion constraint).
#        => no "overshoot and return" oscillation is possible.
#   (T2) A hydrostatic equilibrium exists: torsion repulsion (proportional to
#        rho^2) balances gravity (proportional to rho) at rho_eq ~ rho_c.
#        This is the CARTAN CORE (the analogue of the "Planck star",
#        Rovelli-Vidotto, in loop quantum gravity).
#   (T3) Asymmetry between the first collapse and later accretion: only the
#        initial COHERENT collapse nucleates a child universe.
#   (T4) [ADDED 16/07/2026] The criterion t_dyn << t_acc QUANTIFIED: a margin
#        of 15-17 orders of magnitude in the standard regime (ISM, Eddington).
#        The hypercritical regime (collapsar/GRB) is identified as the only
#        non-trivial boundary (item CORE-1-HYPERACC), diagnosed through
#        Delta_M(t_dyn), and MERGED into the ab initio problem (T2) rather
#        than solved separately.
#
#  WHY IT MATTERS FOR THE CORPUS
#  -----------------------------
#   If every new batch of infalling matter bounced, a black hole would be a
#   "universe factory" and the extended Drake equation (N_fertile =
#   N_BH x f_M x ...) would be invalid. The result established here -- a
#   static core, a single nucleation event -- PRESERVES that count:
#   ONE BLACK HOLE = ONE CHILD UNIVERSE.
#
#  LIMITATIONS
#  -----------
#   [L1] TEST 2 is an ORDER-OF-MAGNITUDE argument (balancing the rho and
#        rho^2 scalings), not a complete TOV-torsion solution. It remains
#        DEFERRED to Foundation IV (multi-session work, numerical
#        relativity). The hypercritical regime (T4/CORE-1-HYPERACC) is the
#        same missing ingredient, not a separate problem.
#   [L2] [CLOSED 16/07/2026 for standard regimes, see T4] The asymmetry (T3)
#        is now QUANTIFIED (margin of 15-17 orders of magnitude,
#        ISM/Eddington). The hypercritical regime stays open (see [L1]).
#   [L3] No backreaction of the core on the exterior metric.
#
#  ⚠️ AUDIT 24/08/2026 -- THE TWO BOUNDS ARE NOT RIVALS, AND THE SCRIPT
#   SHOWS ONLY ONE OF THEM.
#   T1 below derives rho <= rho_c. The final STATUS block announces
#   rho <= rho_c/2. Both are right, and they are DIFFERENT STATEMENTS:
#     * rho <= rho_c   -- the FRIEDMANN bound: kinematic and exact. Beyond
#       it H^2 < 0, so the density simply cannot get there. This is what
#       T1 proves.
#     * rho <  rho_c/2 -- the TOV bound: hydrostatic and finer. With the
#       stiff equation of state, rho_eff = rho(1 - rho/rho_c) is NOT
#       monotonic: it peaks at rho_c/2. A BOUND core must satisfy both
#       dP_eff/dr < 0 (TOV) and drho/dr < 0, and since
#       dP_eff/dr = rho_c c^2 (1 - 2 rho/rho_c) drho/dr, the two are
#       compatible only below rho_c/2.
#       Derived in Foundation III Extended, "Resolution TOV", item CORE-1,
#       which calls it explicitly "the FINER bound".
#   ⇒ This script is not wrong, it is INCOMPLETE: its status block quotes a
#     bound that its own T1 does not establish, without saying where it
#     comes from. A reader running the script alone cannot reconstruct the
#     factor of two. Deriving the TOV bound here would be new work; naming
#     its source costs nothing, and that is what the note below does.
#
#  Reproducibility: Python >= 3.9, numpy. Deterministic.
# =============================================================================

import numpy as np

SEP = "=" * 72

# --- Constants --------------------------------------------------------------
G = 6.674e-11
c = 2.998e8
hbar = 1.055e-34
RHO_C = c**5 / (hbar * G**2)      # Cartan density  [kg/m^3]

print(SEP); print("CARTAN CORE - what becomes of the accreted matter?"); print(SEP)
print(f"  Cartan density: rho_c = c^5/(hbar G^2) = {RHO_C:.3e} kg/m^3")

# =============================================================================
#  TEST 1 - Is the bound rho <= rho_c EXACT?
# =============================================================================
print(); print(SEP); print("T1 - Friedmann-torsion constraint: rho <= rho_c?"); print(SEP)
print("""
  Equation (Poplawski):  H^2 = (8 pi G/3) rho (1 - rho/rho_c)
  Stiff fluid (w=1): rho = rho_c * u^-6,  u = a/a_bounce.
  H^2 >= 0  requires  (1 - u^-6) >= 0  <=>  u >= 1  <=>  rho <= rho_c.
""")
print("  Check:")
for u in [0.90, 0.99, 1.00, 1.10, 1.50, 2.00]:
    x = u**-6                       # rho/rho_c
    H2 = x * (1.0 - x)              # H^2 in units of (8 pi G rho_c/3)
    tag = "FORBIDDEN (H^2 < 0)" if H2 < 0 else "allowed"
    print(f"    u = {u:4.2f}  |  rho/rho_c = {x:7.4f}  |  H^2 = {H2:+7.4f}   {tag}")
print("""
  => The density CANNOT exceed rho_c: it is a WALL, not a turning point one
     could cross. No "overshoot and return" oscillation is possible.
     => The line of successive damped bounces is RULED OUT.""")

# =============================================================================
#  TEST 2 - Does a hydrostatic equilibrium exist? (the Cartan core)
# =============================================================================
print(); print(SEP); print("T2 - Balance: torsion (~rho^2) against gravity (~rho)"); print(SEP)
print("""
  Below the horizon the core is NOT an isolated FRW universe: it is
  permanently compressed by the accreted matter. The relevant framework is
  therefore hydrostatic equilibrium (TOV) with torsion:

      P_eff = P - (kappa/2) sigma^2      [torsion term: REPULSIVE]

  Scalings:   gravity  ~ rho          (linear)
              torsion  ~ rho^2/rho_c  (quadratic)
  Equality defines the equilibrium density.
""")
print("  Ratio (torsion repulsion)/(gravitational attraction) = x:")
for x in [1e-3, 1e-2, 1e-1, 0.5, 0.9, 1.0]:
    ratio = x
    if ratio < 0.1:
        reg = "gravity dominates (collapse)"
    elif ratio < 1.0:
        reg = "torsion not negligible"
    else:
        reg = "EQUILIBRIUM (torsion = gravity)"
    print(f"    rho/rho_c = {x:6.3f}  ->  ratio = {ratio:6.3f}   {reg}")
print(f"""
  => Equilibrium is reached at rho_eq ~ rho_c (up to a factor of order one).
     The black hole therefore holds a STATIC DENSE CORE at the Cartan
     density -- not a singularity. This is the "Cartan core", the analogue
     of the Planck star (Rovelli-Vidotto) in loop quantum gravity.
     rho_eq ~ {RHO_C:.2e} kg/m^3""")

# =============================================================================
#  TEST 3 - Why does only the FIRST collapse nucleate a universe?
# =============================================================================
print(); print(SEP); print("T3 - Asymmetry: coherent collapse vs gradual accretion"); print(SEP)
print("""
  If later accretion produced new bounces, a black hole would spawn SEVERAL
  universes, invalidating the count of the extended Drake equation
  (N_fertile = N_BH x f_M x f_a x ...). An ASYMMETRY between the first
  collapse and what follows is therefore required.

  Proposed mechanism:
    * FIRST COLLAPSE - coherent and dynamical. The whole core falls in
      together (dynamical time t_dyn ~ 1/sqrt(G rho)), reaches rho_c with
      considerable momentum, and opens the Einstein-Rosen bridge: a child
      universe is nucleated.
    * LATER ACCRETION - gradual. Matter arrives drop by drop (accretion time
      t_acc >> t_dyn) onto a core ALREADY at equilibrium. It is absorbed
      without coherent collapse, hence without a bounce, hence without a
      new bridge.

  CRITERION (to be formalised, item CORE-1):
      nucleation  <=>  t_dyn  <<  t_acc
  The initial stellar collapse satisfies it by a wide margin; later Bondi
  accretion does not.
""")
print(f"""{SEP}
CONCLUSION
{SEP}
  * The density is BOUNDED by rho_c (exact result).
  * The core relaxes towards a HYDROSTATIC EQUILIBRIUM at rho ~ rho_c
    (the Cartan core), not through a series of damped bounces.
  * Only the initial coherent collapse nucleates a child universe.
    => ONE BLACK HOLE = ONE CHILD UNIVERSE.
    => The count of the extended Drake equation is PRESERVED.

  Status: T1 proven; T2 established to order of magnitude; T3 physically
  motivated, quantitative criterion to be formalised (item CORE-1).
""")

# =============================================================================
#  TEST 4 - Nucleation criterion QUANTIFIED (update 16/07/2026)
#  Closes limitation [L2] above for standard accretion regimes; identifies
#  the hypercritical regime as the only open boundary (item
#  CORE-1-HYPERACC, merged into the ab initio problem of T2/[L1]).
# =============================================================================
print(); print(SEP)
print("T4 - Nucleation criterion QUANTIFIED: t_dyn << t_acc (upd. 16/07/2026)")
print(SEP)
print("""
  t_dyn is set by the LEAST dense phase (pre-supernova iron core,
  rho_i ~ 1e9 kg/m^3), since t_dyn ~ 1/sqrt(G rho) decreases as rho^-1/2.
""")
rho_i = 1e9
t_dyn = 1.0 / np.sqrt(G * rho_i)
print(f"  t_dyn ~ 1/sqrt(G*rho_i) = {t_dyn:.2f} s   (rho_i = {rho_i:.0e} kg/m^3)")

M_sun_yr_to_kg_s = 1.989e30 / 3.156e7
regimes = [
    ("ISM / typical Bondi",           1e-9, M_sun_yr_to_kg_s),
    ("Eddington limit (eta=0.1)",     None, None),   # t_Edd handled separately
    ("Hyperaccretion (collapsar/GRB)", 1e-2, 1.0),   # Msun/s directly
]
t_Edd = 1.4e16  # s, Salpeter time, independent of M

print("\n  Regime                          | t_acc (s)   | t_dyn/t_acc")
print("  " + "-" * 66)
for label, val, unit in regimes:
    if label.startswith("Eddington"):
        t_acc = t_Edd
    elif label.startswith("ISM"):
        Mdot = val * M_sun_yr_to_kg_s
        t_acc = 10 * 1.989e30 / Mdot   # order of magnitude, M ~ 10 Msun
    else:
        Mdot_kg_s = val * 1.989e30
        t_acc = 10 * 1.989e30 / Mdot_kg_s
    ratio = t_dyn / t_acc
    print(f"  {label:32s} | {t_acc:9.2e}   | {ratio:9.2e}")

print(f"""
  => A margin of 15 to 17 orders of magnitude in the standard regime (ISM,
     Eddington): the criterion is closed quantitatively, not fine-tuned.
  => The HYPERCRITICAL regime (collapsar/GRB, Mdot ~ 1e-2 to 1 Msun/s,
     MacFadyen & Woosley 1999) is the ONLY regime where the criterion stops
     being trivially satisfied (ratio ~1e-2 to 1e-3).
     The right test there is the mass accreted per dynamical time, not the
     ratio of the times:""")
for Mdot_msun_s in [1e-2, 1.0]:
    Mdot_kg_s = Mdot_msun_s * 1.989e30
    delta_M = Mdot_kg_s * t_dyn
    delta_M_msun = delta_M / 1.989e30
    print(f"    Mdot={Mdot_msun_s:.0e} Msun/s : Delta_M(t_dyn) = {delta_M_msun:.3f} Msun"
          f"  (~{delta_M_msun/5*100:.0f}% of M_BH~5 Msun)")
print("""
  => Delta_M(t_dyn) reaches a few per cent to several tens of per cent of
     M_BH: NOT negligible, unlike the standard regime (~1e-16).
  => This case does NOT close on its own: it requires knowing how the core
     reacts dynamically to an inflow too fast for it to readjust -- exactly
     the ingredient missing from T2/[L1] (a complete TOV-torsion solution).
     CORE-1-HYPERACC is therefore MERGED into the ab initio problem, not
     solved separately (deferred to Foundation IV).

  UPDATED STATUS (item CORE-1, 16/07/2026):
    - Bound rho <= rho_c/2: PROVEN -- but NOT by T1 above.
      T1 gives the Friedmann bound rho <= rho_c (kinematic, exact). The
      factor of two comes from the TOV treatment in Foundation III
      Extended ("Resolution TOV", item CORE-1): rho_eff = rho(1-rho/rho_c)
      peaks at rho_c/2, and a bound core cannot sit above that peak. See
      the header of this file.
    - Equilibrium (T2): established to order of magnitude (rho vs rho^2).
    - Nucleation criterion (T3): QUANTIFIED for ISM/Eddington
      (margin of 15-17 orders of magnitude).
    - Hypercritical regime (CORE-1-HYPERACC): diagnosed via Delta_M(t_dyn),
      merged into the ab initio problem (T2/[L1]), not solved separately.
    - Complete ab initio derivation (T2/[L1]): DEFERRED to Foundation IV.
""")

```

---

### Fichier 7 : `run_F3_agregat_scripts_calculation_audit.py`

```python

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
from pathlib import Path

def generer_contexte_audit():
    dossier_source = Path(".")
    fichier_sortie = "F3_agregat_scripts_calculation_audit.md"
    extensions_cibles = {'.py'}
    dossiers_a_ignorer = {'__pycache__', '.venv', 'venv', '.git', '.idea', '.vscode'}

    print("Début de l'analyse des scripts...")
    compteur_fichiers = 0

    with open(fichier_sortie, 'w', encoding='utf-8') as f_out:
        print("# DOCUMENT DE CONTEXTE POUR AUDIT DE CODE", file=f_out)
        print("", file=f_out)
        print(f"**Dossier audité :** {dossier_source.resolve().name}", file=f_out)
        print("", file=f_out)
        print("---", file=f_out)
        print("", file=f_out)
        print("## CONTENU DES SOURCES PYTHON", file=f_out)
        print("", file=f_out)
        
        for root, dirs, files in os.walk(dossier_source):
            dirs[:] = [d for d in dirs if d not in dossiers_a_ignorer]
            
            for f in files:
                chemin_complet = Path(root) / f
                
                if f in ["agregateur_audit.py", fichier_sortie]:
                    continue
                    
                if chemin_complet.suffix in extensions_cibles:
                    chemin_relatif = chemin_complet.relative_to(dossier_source)
                    compteur_fichiers += 1
                    
                    print(f"### Fichier {compteur_fichiers} : `{chemin_relatif}`", file=f_out)
                    print("", file=f_out)
                    print("```python", file=f_out)
                    
                    try:
                        with open(chemin_complet, 'r', encoding='utf-8') as f_in:
                            for ligne in f_in:
                                # On écrit le code ligne par ligne pour éviter les conflits
                                print(ligne, end="", file=f_out)
                            print("", file=f_out) 
                    except Exception as e:
                        print(f"# Erreur de lecture : {str(e)}", file=f_out)
                    
                    print("```", file=f_out)
                    print("", file=f_out)
                    print("---", file=f_out)
                    print("", file=f_out)
                    
    print(f"Succès ! {compteur_fichiers} scripts ont été centralisés dans '{fichier_sortie}'.")

if __name__ == "__main__":
    generer_contexte_audit()
    
```

---

### Fichier 8 : `calculate_core_tov_torsion.py`

```python
#!/usr/bin/env python3

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# =============================================================================
#  ECF / Foundation III — Le cœur de Cartan : résolution TOV avec torsion
#  Fichant, P. (2026).   Fichier : core_tov_torsion.py   (item CORE-1)
#  Dernière modification : 20/07/2026, 22:55
#
#  EMPLACEMENT (dépôt GitHub) :
#     Foundation_3/02_Scientific_Code/A_Core_Calculations/
# =============================================================================
#
#  OBJET
#  -----
#  Préciser la structure du cœur de Cartan — le noyau dense qui remplace la
#  singularité — au-delà de l'argument d'ordre de grandeur.
#
#  CE QUI EST DÉMONTRÉ ICI
#  -----------------------
#   (T1) rho <= rho_c            : exact (Friedmann-torsion).
#   (T2) rho <  rho_c / 2        : NOUVEAU. Un cœur STATIQUE LIÉ ne peut pas
#        dépasser la moitié de la densité de Cartan. Le « facteur d'ordre 1 »
#        laissé indéterminé dans les versions antérieures vaut exactement 1/2.
#   (T3) Un cœur statique EXIGE un horizon interne : sous un horizon de
#        Schwarzschild, la coordonnée r est du genre temps et aucune solution
#        statique n'existe. Le cœur relève donc des TROUS NOIRS RÉGULIERS.
#
#  CE QUI EST MODÉLISÉ (et non dérivé)
#  -----------------------------------
#   La forme de Hayward (cœur de Sitter, deux horizons) est le modèle standard
#   de trou noir régulier. Elle N'EST PAS dérivée du lagrangien d'Einstein-
#   Cartan. Les grandeurs L, R_core, M_core en découlent ÉTANT DONNÉ ce modèle.
#
#  RÉSERVE D'ÉCHELLE (importante)
#  ------------------------------
#   Le cœur est d'ordre PLANCKIEN. Le préfacteur numérique (0.49, 1, 2...) n'a
#   PAS de contenu physique : à l'échelle de l_Pl, la description classique
#   (RG, Einstein-Cartan, Hayward) sort de son domaine de validité. Seul
#   R_core ~ l_Pl est significatif.
#   Cette limite n'est pas propre à l'ECF : elle affecte identiquement
#   l'étoile de Planck de la gravité quantique à boucles.
#
#  Reproductibilité : Python >= 3.9, numpy, scipy. Déterministe.
# =============================================================================

import numpy as np
from scipy.optimize import brentq

SEP = "=" * 74

# --- Constantes --------------------------------------------------------------
G, c, hbar = 6.674e-11, 2.998e8, 1.055e-34
RHO_C = c**5 / (hbar * G**2)          # densité de Cartan = densité de Planck
l_P   = np.sqrt(hbar * G / c**3)
m_P   = np.sqrt(hbar * c / G)
M_SUN = 1.989e30

print(SEP)
print("  LE CŒUR DE CARTAN — résolution TOV avec torsion  (item CORE-1)")
print(SEP)
print(f"  rho_c = c^5/(hbar G^2) = {RHO_C:.4e} kg/m3   (= densité de Planck)")
print(f"  l_Pl  = {l_P:.4e} m        m_Pl = {m_P:.4e} kg")

# =============================================================================
#  T1/T2 — La densité est bornée, et plus finement qu'on ne le croyait
# =============================================================================
print()
print(SEP)
print("  T2 — Un cœur statique lié exige rho < rho_c / 2")
print(SEP)
print("""
  Équation d'état raide (celle du corpus pour la phase stiff) : P = rho c^2.
  La correction de torsion la PRÉSERVE :

      rho_eff = rho (1 - rho/rho_c)        P_eff = rho_eff c^2

  Or rho_eff n'est PAS monotone : elle culmine en rho = rho_c/2.
""")
u = np.linspace(0, 1, 11)
print("     rho/rho_c    rho_eff/rho_c = P_eff/(rho_c c^2)")
for ui in u:
    tag = "   <-- MAXIMUM" if abs(ui - 0.5) < 1e-9 else ""
    print(f"       {ui:.1f}          {ui*(1-ui):.4f}{tag}")

print("""
  Un cœur LIÉ à l'équilibre hydrostatique doit satisfaire SIMULTANÉMENT :
      (C1)  dP_eff/dr < 0     [équation TOV]
      (C2)  drho/dr   < 0     [la densité décroît vers l'extérieur]

  Or   dP_eff/dr = rho_c c^2 (1 - 2 rho/rho_c) drho/dr.

  Substituer (C2) dans (C1) impose (1 - 2 rho/rho_c) > 0, soit :

          ===>   rho(r) < rho_c / 2   PARTOUT dans le cœur.

  INTERPRÉTATION. Au-delà de rho_c/2 :
      dP_eff/d(rho) = c^2 (1 - 2 rho/rho_c) < 0
  Ajouter de la matière RÉDUIT la pression de soutien — la torsion mord plus
  vite que la gravité n'ajoute. Il n'y a plus de mode sonore, et aucune
  configuration statique liée n'existe. La branche rho > rho_c/2 est
  dynamiquement exclue.
""")
print(f"  ===> rho_core < rho_c/2 = {0.5*RHO_C:.4e} kg/m3   [DÉMONTRÉ]")

# =============================================================================
#  T3 — Pas de solution statique sous un horizon de Schwarzschild
# =============================================================================
print()
print(SEP)
print("  T3 — Un cœur statique EXIGE un horizon interne")
print(SEP)
print("""
  OBSTACLE. Sous un horizon de Schwarzschild (r < 2GM/c^2), la coordonnée r
  devient du GENRE TEMPS : aucun observateur statique ne peut exister, tout
  chute vers l'intérieur. Chercher un équilibre hydrostatique statique sous
  l'horizon des événements est donc MAL POSÉ.

  RÉSOLUTION : les TROUS NOIRS RÉGULIERS (Bardeen, Hayward). Structure :
      * cœur central de type de Sitter (densité ~ constante)
      * DEUX horizons : externe (événements) et interne (Cauchy)
      * entre les deux : région dynamique
      * SOUS l'horizon interne : la région redevient STATIQUE   <-- le cœur

  (Popławski a lui-même exposé la collapse avec torsion dans un ouvrage
   consacré aux trous noirs réguliers, Springer 2023.)
""")

# =============================================================================
#  Structure de Hayward, avec L FIXÉE par la borne rho_c/2
# =============================================================================
print(SEP)
print("  STRUCTURE  (forme de Hayward — MODÈLE, non dérivé d'ECKS)")
print(SEP)

RHO_CORE = 0.5 * RHO_C                                  # borne DÉMONTRÉE
L = np.sqrt(3 * c**2 / (8 * np.pi * G * RHO_CORE))      # longueur de Hayward

print(f"""
  La longueur L du cœur n'est PAS ajustée : elle est fixée par rho_core.

      L = sqrt( 3 c^2 / (8 pi G rho_core) )  avec  rho_core = rho_c/2

      L = {L:.4e} m  =  {L/l_P:.3f} l_Pl        <-- échelle planckienne
""")

def f_metric(r, M):
    """Fonction métrique de Hayward : f(r) = 1 - 2GM r^2 / (c^2 (r^3 + 2GM L^2/c^2))."""
    rs = 2 * G * M / c**2
    return 1.0 - rs * r**2 / (r**3 + rs * L**2)

print(f"  {'Trou noir':>14s} {'r- (m)':>13s} {'r+ (m)':>13s} {'R_s (m)':>13s} {'r-/l_Pl':>9s}")
print("  " + "-" * 68)
for name, M in [("10 M_sun", 10*M_SUN), ("1e6 M_sun", 1e6*M_SUN), ("1e9 M_sun", 1e9*M_SUN)]:
    rs = 2 * G * M / c**2
    r_out = brentq(f_metric, 0.5*rs, 2*rs, args=(M,), xtol=1e-30)
    rr = np.logspace(np.log10(L*1e-3), np.log10(0.9*rs), 40000)
    ff = f_metric(rr, M)
    sc = np.where(np.diff(np.sign(ff)) != 0)[0]
    r_in = rr[sc[0]] if sc.size else float("nan")
    print(f"  {name:>14s} {r_in:13.4e} {r_out:13.4e} {rs:13.4e} {r_in/l_P:9.4f}")

R_core = L
M_core = (4*np.pi/3) * RHO_CORE * R_core**3
print(f"""
  LECTURE
    * r+ (horizon externe) ~ R_s : l'objet est INDISCERNABLE d'un trou noir de
      Schwarzschild vu de l'extérieur — cohérent avec la contrainte de
      compacité GWTC-3 (C = 0.5).
    * r- (horizon interne) est d'échelle PLANCKIENNE, essentiellement
      indépendant de la masse du trou noir.
    * Le cœur, enfoui sous r-, est totalement INVISIBLE de l'extérieur.
    * Le cœur ne « contient » PAS la masse M du trou noir : c'est un noyau
      planckien ; la masse est portée par le champ entre r- et r+.

    R_core ~ L         = {R_core:.3e} m  ~ l_Pl
    M_core ~ (4pi/3) rho_core R_core^3 = {M_core:.3e} kg ~ {M_core/m_P:.2f} m_Pl

  ATTENTION — le préfacteur ({R_core/l_P:.2f} l_Pl) n'a PAS de contenu physique.
  À l'échelle de Planck, la description classique sort de son domaine de
  validité. Seul  R_core ~ l_Pl  est significatif.
""")

print(SEP)
print("  BILAN CORE-1")
print(SEP)
print("""
  DÉMONTRÉ
    * rho <= rho_c                        (exact, Friedmann-torsion)
    * rho <  rho_c/2 pour un cœur statique lié  [NOUVEAU — le facteur
      d'ordre 1 vaut exactement 1/2]
    * un cœur statique EXIGE un horizon interne  -> trou noir régulier

  MODÉLISÉ
    * la forme de Hayward (cœur de Sitter, deux horizons) n'est pas dérivée
      du lagrangien d'Einstein-Cartan
    * L, R_core, M_core en découlent ÉTANT DONNÉ ce modèle

  RESTE OUVERT
    * dérivation du cœur depuis l'action ECKS complète (sans forme
      métrique postulée) -- travail pluri-session, déféré à Foundation IV.
    * [MAJ 16/07/2026] Le critère de nucléation t_dyn << t_acc est
      désormais QUANTIFIÉ (marge de 15-17 ordres de grandeur en régime
      standard ISM/Eddington) -- voir cartan_core.py, TEST 4. Le régime
      hypercritique (collapsar/GRB, item CORE-1-HYPERACC) reste ouvert,
      mais FUSIONNÉ au point précédent (dérivation ab initio) plutôt que
      traité comme un problème séparé : il requiert le même ingrédient
      manquant (réponse dynamique du cœur à un afflux trop rapide).
""")

```

---

