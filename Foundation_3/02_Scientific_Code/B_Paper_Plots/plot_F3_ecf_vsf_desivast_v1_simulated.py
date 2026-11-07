#!/usr/bin/env python3
"""
ecf_vsf_desivast_v1.py
======================
Comparison of the ECF Void Size Function (VSF, Foundation II)
with the DESIVAST DR1 catalogue (Rincon et al. 2025, ApJ 982:38).

PURPOSE
-------
Test the VSF kill-switch: ECF predicts an excess of large voids at
R > xi_KZ = 60 Mpc physical (= 40.4 Mpc/h; adopted value, harmonisation
22/09/2026, not derived -- PO-F3-XI) relative to LambdaCDM.
This signal is ACCESSIBLE in DESIVAST DR1 (max R ~ 80 Mpc/h).

IMPORTANT CORRECTION
--------------------
xi_KZ = 50-80 Mpc PHYSICAL = 34-54 Mpc/h (h=0.6732).
Kill-switch R > 60 Mpc physical = R > 40 Mpc/h.

USAGE MODES
-----------
  DATA_MODE = 'simulated' (defaut) : distribution simulee depuis les
    statistiques SDSS publiees (Douglass+2023), scalee sur DESIVAST DR1.

  DATA_MODE = 'fits' : lecture du vrai catalogue DESIVAST DR1.
    URL : data.desi.lbl.gov/doc/releases/dr1/vac/desivast/
    Telecharger : desivast_dr1_voidfinder_NGC.fits + _SGC.fits
    Puis : DATA_MODE = 'fits', FITS_PATH = '/chemin/vers/catalogue'

PREDICTION ECF (Foundation II, VSF)
-------------------------------------
  VSF_ECF(R) = VSF_LCDM(R) * A_ECF(R)
  A_ECF(R)   = 1 + 1.1 * exp(-(R - xi_KZ)^2 / (2*sigma_KZ^2))
  A_ECF(xi_KZ) = 2.1  (VSF kill-switch, Foundation III)

REFERENCES
----------
  Rincon et al. 2025, ApJ 982:38  doi:10.3847/1538-4357/adb559
  Douglass et al. 2023, ApJS 265:7
  Fichant 2026, Foundation II  doi:10.5281/zenodo.20802690

Auteur  : Pascal Fichant (ECF programme)
Version : 1.0 (27 juin 2026)
Licence : CC-BY 4.0
GitHub  : github.com/pfichant/spin-torsion-cosmology
Output  : Fig_ECF_VSF_DESIVAST_DR1.png
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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

np.random.seed(42)

# ===========================================================================
# CONFIGURATION — modifier ici
# ===========================================================================

DATA_MODE  = 'fits'        # 'simulated' | 'fits' | 'download'
# [26/08/2026] Recherche automatique du catalogue plutot qu'un chemin fixe :
# le mode 'simulated' etait actif alors que les FITS etaient presents dans
# desivast_dr1/, si bien que la figure du papier montrait le SUBSTITUT
# (21 vides au-dessus de 40 Mpc/h) la ou le vrai catalogue en compte ZERO.
def _find_desivast():
    import os as _os
    _here = _os.path.dirname(_os.path.abspath(__file__))
    _parent = _os.path.dirname(_here)
    _repo_root = _os.path.dirname(_parent)   # .../Foundation_3, two levels up
    for _c in (_os.path.join(_repo_root, 'data', 'desivast_dr1'),
               'desivast_dr1', 'data/dr1/desivast_dr1', '.',
               _os.path.join(_here, 'desivast_dr1'),
               _os.path.join(_parent, 'A_Core_Calculations', 'desivast_dr1'),
               _os.path.join(_parent, 'B_Paper_Plots', 'desivast_dr1'),
               _here):
        if _os.path.exists(_os.path.join(
                _c, 'DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits')):
            return _c
    return _os.path.join(_repo_root, 'data', 'desivast_dr1')

FITS_PATH  = _find_desivast()   # dossier des fichiers FITS DESIVAST DR1
#
# URL PUBLIQUE (sans authentification) :
#   https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/
#
# Fichiers VoidFinder :
#   DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits
#   DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits
#
# Téléchargement (remplacer FITS_PATH par le dossier local) :
#   wget -P ./desivast/ \
#     https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits
#   wget -P ./desivast/ \
#     https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits
#
# NERSC (si accès NERSC disponible) :
#   /global/cfs/cdirs/desi/public/dr1/vac/dr1/desivast/
#
# Colonnes clés (documentation : vast.readthedocs.io) :
#   EFFECTIVE_RADIUS      — rayon effectif du vide [Mpc/h]  (ajouté par DESIVAST)
#   EFFECTIVE_RADIUS_UNCERT — incertitude [Mpc/h]
#   flag (ou hole_id)     — identifiant unique du vide
#   edge_flag             — 1 = vide de bord, 0 = vide intérieur
OUTPUT_PNG = 'Fig_ECF_VSF_DESIVAST_DR1.png'

# ===========================================================================
# COSMOLOGIE FIDUCIELLE DESIVAST DR1 (Planck 2020)
# ===========================================================================

H0  = 67.32    # km/s/Mpc
h   = H0/100.  # 0.6732
Om  = 0.315
OmL = 0.685

# ===========================================================================
# PARAMETRES ECF CANONIQUES (Foundation II)
# ===========================================================================

XI_KZ_MPC  = 60.0   # Mpc physique — valeur ADOPTEE xi_KZ (harmonisation 22/09/2026, PO-F3-XI)
XI_KZ_LO   = 50.0   # borne basse
XI_KZ_HI   = 80.0   # borne haute
SIG_KZ_MPC = 15.0   # Mpc — largeur du pic KZ, valeur ADOPTEE (harmonisation 22/09/2026)
A_ECF_PEAK = 1.1    # A_ECF(xi_KZ) = 1 + 1.1 = 2.1

# [22/09/2026, arbitrage A-8] Harmonisation conventionnelle : pic = seuil.
#   XI_KZ_MPC = 60 Mpc : PIC adopte de la longueur de correlation KZ.
#   R_KS_MPC  = 60 Mpc : SEUIL du kill-switch, confondu avec le pic.
# Valeurs ADOPTEES, ni derivees ni ajustees (PO-F3-XI reste OPEN).
# 60 Mpc -> 40.4 Mpc/h (seuil et pic). L'ancienne note (pic 65 Mpc ->
# 43.8 Mpc/h, sigma 12 Mpc, seuil en deca du pic) est historique.
R_KS_MPC   = 60.0         # Mpc physique — seuil kill-switch (Foundation III)
                          # [26/08/2026] disait « F2 » : vestige d'avant le
                          # SPLIT-1. Le test VSF appartient à Foundation III.
R_KS_H     = R_KS_MPC * h  # = 40.4 Mpc/h

# ===========================================================================
# CALIBRATION LCDM : SDSS VoidFinder (Douglass+2023, ApJS 265:7)
# Digitisee depuis Figure 6 — 1163 vides interieurs, z<0.114, R_min=10 Mpc/h
# ===========================================================================

SDSS_BINS_H = np.array([10,13,16,19,22,25,28,32,36,42,54], dtype=float)  # Mpc/h
SDSS_COUNTS = np.array([155,210,215,185,150,110,70,40,20,8],  dtype=float)
N_SDSS      = int(SDSS_COUNTS.sum())   # 1163

BINS_MPC    = SDSS_BINS_H / h
BIN_CENTERS = 0.5 * (BINS_MPC[:-1] + BINS_MPC[1:])
BIN_WIDTHS  = np.diff(BINS_MPC)

# Scale vers DESIVAST DR1 (1484 vides, z<0.24)
N_DR1        = 1484
DEPTH_F      = 1.4     # profondeur accrue z<0.24 vs z<0.114
DR1_COUNTS   = SDSS_COUNTS * (N_DR1/N_SDSS) * DEPTH_F
DR1_COUNTS[-1] *= 1.5  # bin 42-54 Mpc/h : plus grands vides avec z_max=0.24

N_DESI_FULL  = 15000
SCALE_FULL   = N_DESI_FULL / N_DR1

# ===========================================================================
# CHARGEMENT DONNEES
# ===========================================================================

def load_fits_catalog(fits_dir):
    """
    Load the real DESIVAST DR1 VoidFinder catalogue (exact column names).
    Returns R_eff in physical Mpc (converted from Mpc/h).

    FITS structure (2 HDUs per file):
      HDU[0]: PrimaryHDU (empty)
      HDU[1]: BinTableHDU "Maximal Spheres" — one row per maximal sphere
        - EFFECTIVE_RADIUS      : effective void radius [Mpc/h]
        - EFFECTIVE_RADIUS_UNCERT : uncertainty [Mpc/h]
        - flag (or hole_id)     : unique void identifier
        - edge_flag             : 0 = interior, 1 = edge

    For unique voids: filter edge_flag==0, then deduplicate by flag.
    """
    try:
        from astropy.io import fits as apfits
        from astropy.table import Table
    except ImportError:
        raise ImportError("pip install astropy")

    # Noms de fichiers exacts (confirmés : data.desi.lbl.gov/doc/releases/dr1/vac/desivast/)
    FNAMES = [
        'DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits',
        'DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits',
    ]

    R_all = []
    for fname in FNAMES:
        fpath = os.path.join(fits_dir, fname)
        if not os.path.exists(fpath):
            print(f"  Absent : {fpath}")
            continue

        hdu  = apfits.open(fpath)
        # HDU[1] = maximal spheres table
        data = Table(hdu[1].data)
        hdu.close()
        print(f"  {fname} : {len(data)} lignes (sphères maximales)")

        # Sélection vides intérieurs (edge_flag == 0)
        eflag_col = None
        # [26/08/2026] 'EDGE' AJOUTE : c'est le nom reel de la colonne dans
        # DESIVAST DR1 (Table 4 de Rincon+2025). Sans lui le filtre ne
        # s'appliquait pas et le script comptait 3 764 vides « interieurs »
        # au lieu de 1 489 -- les vides de bord etaient tous inclus.
        for cname in ['EDGE', 'edge_flag', 'EDGE_FLAG', 'EdgeFlag', 'edge']:
            if cname in data.colnames:
                eflag_col = cname; break
        if eflag_col:
            data = data[data[eflag_col] == 0]
        else:
            print(f"  Attention : colonne edge_flag absente, tous les vides inclus")

        # Déduplification : une ligne par vide unique (par identifiant void)
        id_col = None
        for cname in ['flag', 'FLAG', 'hole_id', 'HOLE_ID', 'VoidID']:
            if cname in data.colnames:
                id_col = cname; break
        if id_col:
            # Garder la première occurrence de chaque void
            seen = set()
            keep = []
            for i, row in enumerate(data):
                vid = int(row[id_col])
                if vid not in seen:
                    seen.add(vid)
                    keep.append(i)
            data = data[keep]
        print(f"  Vides intérieurs uniques : {len(data)}")

        # Colonne rayon effectif (en Mpc/h) — ajoutée par DESIVAST
        r_col = None
        for cname in ['EFFECTIVE_RADIUS', 'effective_radius', 'R_EFF', 'r_eff']:
            if cname in data.colnames:
                r_col = cname; break
        if r_col is None:
            raise KeyError(
                f"Colonne rayon introuvable dans {fname}.\n"
                f"Colonnes disponibles : {data.colnames}")

        R_mpc = np.array(data[r_col]) / h   # Mpc/h -> Mpc physique
        print(f"  R_eff [Mpc] : min={R_mpc.min():.1f}  "
              f"median={np.median(R_mpc):.1f}  max={R_mpc.max():.1f}")
        R_all.append(R_mpc)

    if not R_all:
        raise FileNotFoundError(
            "No DESIVAST DR1 VoidFinder file found in: " + fits_dir + "\n"
            "Download from:\n"
            "  https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/\n"
            "Commande wget :\n"
            "  wget -P " + fits_dir + "/ \\\n"
            "    https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/"
            "DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits\n"
            "  wget -P " + fits_dir + "/ \\\n"
            "    https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/"
            "DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits")
    return np.concatenate(R_all)


def download_desivast(target_dir='.'):
    """
    Download the DESIVAST DR1 VoidFinder catalogues (public URL).
    Requires urllib (Python stdlib).
    """
    import urllib.request, os
    BASE = "https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/"
    FILES = [
        "DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits",
        "DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits",
    ]
    os.makedirs(target_dir, exist_ok=True)
    for fname in FILES:
        dest = os.path.join(target_dir, fname)
        if os.path.exists(dest):
            print(f"  Déjà présent : {dest}"); continue
        url = BASE + fname
        print(f"  Téléchargement : {url}")
        try:
            urllib.request.urlretrieve(url, dest)
            size = os.path.getsize(dest) / 1e6
            print(f"  OK — {size:.1f} MB sauvegardé : {dest}")
        except Exception as e:
            print(f"  ERREUR : {e}")
            print(f"  Essayer manuellement : wget {url} -P {target_dir}/")

print("="*65)
print("ECF VSF vs DESIVAST DR1  v1.0 — 27/06/2026")
print("="*65)
print(f"Mode : {DATA_MODE}")
print(f"Kill-switch : R > {R_KS_MPC:.0f} Mpc = {R_KS_H:.1f} Mpc/h\n")

if DATA_MODE == 'download':
    print("\nDownloading DESIVAST DR1...")
    download_desivast(FITS_PATH)
    DATA_MODE = 'fits'   # continuer avec les fichiers téléchargés

if DATA_MODE == 'fits':
    R_obs      = load_fits_catalog(FITS_PATH)
    R_obs      = R_obs[R_obs >= BINS_MPC[0]]
    OBS_COUNTS, _ = np.histogram(R_obs, bins=BINS_MPC)
    OBS_COUNTS = OBS_COUNTS.astype(float)
    print(f"Total charges : {len(R_obs)} vides interieurs")
else:
    R_obs      = None
    OBS_COUNTS = DR1_COUNTS.copy()

# ===========================================================================
# MODELE ECF
# ===========================================================================

def A_ecf(R_mpc, xi=XI_KZ_MPC):
    """Facteur d'amplification ECF (vaut 2.1 au pic xi_KZ)."""
    return 1. + A_ECF_PEAK * np.exp(-(R_mpc - xi)**2 / (2.*SIG_KZ_MPC**2))

ECF_MID = DR1_COUNTS * np.array([A_ecf(R)           for R in BIN_CENTERS])
ECF_LO  = DR1_COUNTS * np.array([A_ecf(R, XI_KZ_LO) for R in BIN_CENTERS])
ECF_HI  = DR1_COUNTS * np.array([A_ecf(R, XI_KZ_HI) for R in BIN_CENTERS])

# ===========================================================================
# STATISTIQUES DE TEST
# ===========================================================================

def N_above(counts, R_cut_h):
    return counts[SDSS_BINS_H[:-1] >= R_cut_h].sum()

def sigma_detect(N_l, N_e, f_syst=0.0):
    if N_l < 0.1: return 0.
    return (N_e - N_l) / np.sqrt(N_l + (f_syst*N_l)**2)

R_CUTS_H = [28., 32., 36., 40., 42.]

for label, scale, fsyst in [
    ("DESIVAST DR1  (stat. seule)",   1.,          0.00),
    ("DESIVAST DR1  (+30% syst.)",    1.,          0.30),
    ("Survey complet DESI (~15k)",    SCALE_FULL,  0.10),
]:
    print(f"── {label} ──")
    print(f"  {'Coupure':>12}  {'N_LCDM':>7}  {'N_ECF':>7}  {'x':>5}  {'sigma':>8}")
    for Rc in R_CUTS_H:
        N_l = N_above(DR1_COUNTS, Rc) * scale
        N_e = N_above(ECF_MID,    Rc) * scale
        sig = sigma_detect(N_l, N_e, fsyst)
        ks  = " <-- KS" if abs(Rc - R_KS_H) < 2. else ""
        print(f"  R>{Rc:>4.0f} Mpc/h  {N_l:>7.0f}  {N_e:>7.0f}  "
              f"{N_e/max(N_l,.01):>4.2f}x  {sig:>7.1f}s{ks}")
    print()

# Comparaison donnees reelles si mode FITS
if DATA_MODE == 'fits' and R_obs is not None:
    print("── Donnees reelles vs LCDM ──")
    for Rc in R_CUTS_H:
        N_obs_v = int((R_obs >= Rc/h).sum())
        N_l     = N_above(DR1_COUNTS, Rc)
        sig     = (N_obs_v - N_l) / np.sqrt(max(N_l, .1))
        verdict = "EXCES" if sig>2 else ("DEFICIT" if sig<-2 else "OK")
        print(f"  R>{Rc:>4.0f} Mpc/h  N_obs={N_obs_v:>5}  N_LCDM={N_l:>6.0f}  "
              f"{sig:>+6.1f}s  [{verdict}]")
    print()

# ===========================================================================
# FIGURE
# ===========================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='white')
fig.suptitle(
    # [26/08/2026] Le titre disait « VSF ECF vs LCDM ». Il n'y a PAS de VSF
    # LCDM ici : la serie de reference est un substitut recale depuis SDSS,
    # ce que la legende admettait quatre lignes plus bas. Le titre affirmait
    # donc ce que la legende dementait -- et un lecteur retient le titre.
    r"ECF void size function — DESIVAST DR1 (Rincon+2025, ApJ 982:38)"
    "\n"
    # [26/08/2026] Le « 40 » etait code en dur alors que le seuil derive de
    # R_KS_MPC : le titre annoncait 40 Mpc/h (soit xi_KZ = 60) sous sa propre
    # mention « xi_KZ = 65 Mpc ». Les deux valeurs coexistaient dans la meme
    # figure. Le seuil est desormais calcule, donc necessairement coherent.
    rf"Foundation III prediction: $N_{{\rm ECF}}(R>{R_KS_H:.0f}\,h^{{-1}}{{\rm Mpc}})"
    r"\approx 2.1\times N_{\rm baseline}$ ($\xi_{\rm KZ}=60$ Mpc, adopted)",
    fontsize=11, fontweight='bold'
)

W = BIN_WIDTHS * 0.42

# -- Panel gauche : distribution -----------------------------------------
ax = axes[0]

ax.bar(BIN_CENTERS, DR1_COUNTS, W, align='center',
       color='#1C3F7A', alpha=0.70,
       label=r'placeholder (rescaled SDSS$\to$DR1), NOT $\Lambda$CDM')
ax.bar(BIN_CENTERS, ECF_MID, W, align='center',
       color='#CC2222', alpha=0.45,
       label=r'placeholder $\times\,A_{\rm ECF}$ ($\xi_{\rm KZ}=60$ Mpc)')
ax.bar(BIN_CENTERS, DR1_COUNTS, W, align='center',
       color='none', edgecolor='#1C3F7A', lw=1.2)
if DATA_MODE == 'download':
    print("\nDownloading DESIVAST DR1...")
    download_desivast(FITS_PATH)
    DATA_MODE = 'fits'   # continuer avec les fichiers téléchargés

if DATA_MODE == 'fits':
    ax.errorbar(BIN_CENTERS, OBS_COUNTS,
                yerr=np.sqrt(np.maximum(OBS_COUNTS,1.)),
                fmt='ko', ms=4, lw=1.2, capsize=3, zorder=6,
                label='DESIVAST DR1 (data)')
ax.axvline(R_KS_MPC,  c='orange', lw=2.0, ls='--',
           label=fr'Kill-switch {R_KS_H:.0f} Mpc/$h$')
ax.axvline(XI_KZ_MPC, c='red',    lw=1.2, ls=':',
           label=fr'$\xi_{{KZ}}={XI_KZ_MPC:.0f}$ Mpc')
ax.fill_betweenx([0,420], R_KS_MPC, 200., color='orange', alpha=0.07, zorder=0)
ax.set_xlabel(r'$R_{\rm eff}$ [Mpc]', fontsize=11)
ax.set_ylabel('Number of voids per bin', fontsize=10)
ax.set_title('DESIVAST DR1 void distribution', fontsize=10)
ax.set_xlim(BINS_MPC[0], BINS_MPC[-1]); ax.set_ylim(0.)
ax.legend(fontsize=7.5); ax.grid(True, alpha=0.22)
ax_t = ax.twiny()
ax_t.set_xlim(ax.get_xlim()[0]*h, ax.get_xlim()[1]*h)
ax_t.set_xlabel(r'$R_{\rm eff}$ [Mpc/$h$]', fontsize=10)

# -- Panel droit : amplification + detectabilite -------------------------
ax2 = axes[1]
R_plt = np.linspace(BINS_MPC[0], BINS_MPC[-1], 400)
A_m = np.array([A_ecf(R)           for R in R_plt])
A_l = np.array([A_ecf(R, XI_KZ_LO) for R in R_plt])
A_h = np.array([A_ecf(R, XI_KZ_HI) for R in R_plt])

ax2.plot(R_plt, A_m, 'r-', lw=2.5,
         label=fr'$A_{{\rm ECF}}(R)$, $\xi_{{KZ}}={XI_KZ_MPC:.0f}$ Mpc')
ax2.fill_between(R_plt, A_l, A_h, color='red', alpha=0.18,
                 label=fr'$\xi_{{KZ}}={XI_KZ_LO:.0f}$-{XI_KZ_HI:.0f} Mpc')
ax2.axhline(1.0, c='k',      lw=1.0, ls='-',  label=r'$\Lambda$CDM')
ax2.axhline(2.1, c='orange', lw=1.5, ls='--', label=r'Kill-switch $\times 2.1$')
ax2.axvline(R_KS_MPC,  c='orange', lw=2.0, ls='--', alpha=0.8)
ax2.axvline(XI_KZ_MPC, c='red',    lw=1.2, ls=':',  alpha=0.7)

# [26/08/2026] LES SIGMA NE SONT PLUS TRACES SUR LA FIGURE.
# Ils etaient calcules contre DR1_COUNTS, qui n'est PAS une VSF LCDM mais un
# substitut recale a la main depuis un ancien catalogue SDSS. L'en-tete de
# plot_F3_ecf_vsf_desivast_fits.py dit que ces significativites sont « tres
# probablement un artefact » et « ne doivent pas etre citees, dans les papiers
# ni ailleurs » -- or une figure qui les affiche les rend citables.
# Les valeurs restent CALCULEES et imprimees en console : elles gardent leur
# valeur de diagnostic interne, elles n'ont pas leur place dans un papier.
# L'annotation indique desormais l'amplification predite, qui est ce que la
# figure peut legitimement affirmer.
for Rc_mpc, dx in [(32., -3.), (R_KS_MPC, +5.)]:
    Rc_h_ = Rc_mpc * h
    ax2.annotate(
        fr'$R>{Rc_h_:.0f}$ Mpc/$h$:' '\n'
        fr'$A_{{\rm ECF}}={A_ecf(Rc_mpc):.2f}$',
        xy=(Rc_mpc, A_ecf(Rc_mpc)),
        xytext=(Rc_mpc+dx, A_ecf(Rc_mpc)+0.18),
        fontsize=7.5, color='#222',
        ha='right' if dx < 0 else 'left',
        arrowprops=dict(arrowstyle='->', color='gray', lw=0.8)
    )
ax2.set_xlabel(r'$R_{\rm eff}$ [Mpc]', fontsize=11)
ax2.set_ylabel(r'$A_{\rm ECF}(R)$  (predicted amplification)', fontsize=10)
ax2.set_title('ECF amplification and detectability', fontsize=10)
ax2.set_xlim(BINS_MPC[0], BINS_MPC[-1]); ax2.set_ylim(0.75, 2.65)
ax2.legend(fontsize=8.5); ax2.grid(True, alpha=0.22)
ax_t2 = ax2.twiny()
ax_t2.set_xlim(ax2.get_xlim()[0]*h, ax2.get_xlim()[1]*h)
ax_t2.set_xlabel(r'[Mpc/$h$]', fontsize=10)

plt.tight_layout()
plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# ===========================================================================
# RAPPORT
# ===========================================================================
N_l_ks  = N_above(DR1_COUNTS, R_KS_H)
N_e_ks  = N_above(ECF_MID,    R_KS_H)

print(f"""
{'='*65}
RAPPORT FINAL
{'='*65}
Source     : {DATA_MODE}  (Rincon+2025, N_DR1={N_DR1})
Kill-switch: R > {R_KS_MPC:.0f} Mpc = {R_KS_H:.1f} Mpc/h
N_LCDM(ks) = {N_l_ks:.0f}   N_ECF(ks) = {N_e_ks:.0f}  (x{N_e_ks/max(N_l_ks,.01):.2f})

Detectabilite au kill-switch :
  DR1 stat seule : {sigma_detect(N_l_ks, N_e_ks, 0.00):.1f}s
  DR1 + 30% syst : {sigma_detect(N_l_ks, N_e_ks, 0.30):.1f}s  <- estimation realiste
  Survey complet : {sigma_detect(N_l_ks*SCALE_FULL, N_e_ks*SCALE_FULL, 0.10):.1f}s

Pour le vrai catalogue FITS :
  DATA_MODE = 'fits'
  FITS_PATH = '/chemin/vers/desivast_dr1/'
  URL       : data.desi.lbl.gov/doc/releases/dr1/vac/desivast/

Figure : {OUTPUT_PNG}
{'='*65}
""")
