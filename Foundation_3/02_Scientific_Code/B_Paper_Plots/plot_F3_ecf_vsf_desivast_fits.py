#!/usr/bin/env python3
"""
ecf_vsf_desivast_fits.py
========================
ECF VSF (Foundation II) vs DESIVAST DR1 -- FITS MODE.
Public DESI catalogue: data.desi.lbl.gov/public/dr1/vac/dr1/desivast/

The script downloads the FITS files automatically if absent, then
compares N_obs(R > 40 Mpc/h) against the ECF kill-switch (x2.1).

USAGE
-----
  python ecf_vsf_desivast_fits.py            # download + analyse
  python ecf_vsf_desivast_fits.py --no-dl    # analyse without downloading

ECF PREDICTION (Foundation II, §VSF)
--------------------------------------
  VSF_ECF(R) = VSF_LCDM(R) × A_ECF(R)
  A_ECF(R)   = 1 + 1.1 × exp(-(R - 60)² / (2×15²))   [A-8: xi_KZ = 60, sigma_KZ = 15 Mpc, adopted]
  Kill-switch: N_ECF(R > 40 Mpc/h) ≈ 2.1 × N_LCDM

!! Read the LCDM BASELINE CAVEAT block further down before quoting any
   significance produced by this script: N_LCDM is a rescaled placeholder,
   not a theoretical prediction.

REFERENCES
----------
  Rincon et al. 2025, ApJ 982:38    arXiv:2411.00148
  Douglass et al. 2023, ApJS 265:7
  Fichant 2026, Foundation II       doi:10.5281/zenodo.20802690

Author  : Pascal Fichant (ECF programme)
Version : 1.2 (21/07/2026, 02:50). Changes vs v1.1:
          (1) Fixed a misleading kill-switch verdict: when the true
              threshold (60 Mpc = 40 Mpc/h) is out of catalogue range,
              the smaller fallback cut was displayed under the true
              threshold's label, in both the console output and the
              figure box. Both now state explicitly that the true
              kill-switch is out of reach (N=0) and that the value
              shown is a proxy at a reduced scale. The early
              diagnostic (N=0 at the true threshold) was already
              correct; only the final verdict was misleading if read
              in isolation.
          (2) Added an explicit caveat that N_LCDM is a rescaled
              placeholder, not a theoretical LCDM VSF, so the printed
              "DEFICIT" significances must not be read as cosmological
              tension.
          (3) All console and figure text translated to English
              (corpus language for Foundation I; Foundation III to be
              translated later).
Licence : CC-BY 4.0
GitHub  : github.com/pfichant/spin-torsion-cosmology
Output  : Fig_ECF_VSF_DESIVAST_DR1_fits.png
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
import os, sys, urllib.request

np.random.seed(42)

# ===========================================================================
# CHEMINS PUBLICS DESIVAST DR1 (confirmés 27/06/2026)
# ===========================================================================

# URLs candidates (la structure exacte peut varier selon la version du serveur)
# Essayées dans l'ordre jusqu'à succès
BASE_URLS = [
    "https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/v1/",    # avec version v1
    "https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/",        # doc officielle
    "https://data.desi.lbl.gov/public/dr1/vac/desivast/",            # sans /dr1/ double
    "https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/v1.0/",  # version v1.0
]
BASE_URL   = BASE_URLS[0]   # URL par défaut (sera tentée en premier)
NERSC_PATH = "/global/cfs/cdirs/desi/public/dr1/vac/dr1/desivast/"

FITS_FILES = [
    "DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits",
    "DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits",
]

# Dossier local ou stocker les fichiers telecharges.
# Canonique : Foundation_3/data/desivast_dr1/, un dossier de donnees
# unique et visible a la racine du depot, independant du sous-dossier de
# categorie (A_Core_Calculations, B_Paper_Plots, ...) ou vit ce script.
# Repli sur "./desivast_dr1" (a cote du script) si l'ancien dossier existe
# deja la et que le nouveau emplacement canonique n'a rien.
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_HERE))  # .../Foundation_3
_CANONICAL_DIR = os.path.join(_REPO_ROOT, "data", "desivast_dr1")
_LEGACY_DIR = os.path.join(_HERE, "desivast_dr1")
if os.path.exists(_LEGACY_DIR) and not os.path.exists(_CANONICAL_DIR):
    LOCAL_DIR = _LEGACY_DIR
else:
    LOCAL_DIR = _CANONICAL_DIR

# Fichier de sortie
OUTPUT_PNG = "Fig_ECF_VSF_DESIVAST_DR1_fits.png"

# ===========================================================================
# PARAMÈTRES ECF CANONIQUES (Foundation II)
# ===========================================================================

H0          = 67.32      # km/s/Mpc (DESIVAST fiduciel = Planck 2020)
h           = H0 / 100.  # 0.6732

XI_KZ_MPC   = 60.0       # Mpc physique — valeur ADOPTEE (harmonisation 22/09/2026, A-8 ; non derivee, PO-F3-XI)
XI_KZ_LO    = 50.0
XI_KZ_HI    = 80.0
SIG_KZ_MPC  = 15.0       # Mpc — largeur du pic, valeur ADOPTEE (harmonisation 22/09/2026, PO-F3-XI)
A_ECF_PEAK  = 1.1        # => A_ECF(xi_KZ) = 2.1

R_KS_MPC    = 60.0       # Mpc physique — seuil kill-switch (Foundation III)
                         # [26/08/2026] annotation corrigée : disait « F2 ».
                         # Le test VSF appartient à Foundation III depuis le
                         # SPLIT-1 ; F2 n'en porte aucune mention. L'ancienne
                         # note était un vestige d'avant la séparation.
R_KS_H      = R_KS_MPC * h   # = 40.4 Mpc/h

# ---------------------------------------------------------------------------
# LCDM BASELINE -- IMPORTANT CAVEAT (added 21/07/2026)
# ---------------------------------------------------------------------------
# DR1_COUNTS is NOT a theoretical LCDM void size function. It is a crude
# PLACEHOLDER: the *shape* is taken from an older SDSS VoidFinder catalogue
# (Douglass+2023), rescaled to an *expected* DESI DR1 total (N_DR1=1484) and
# multiplied by a hand-tuned depth factor (DEPTH_F=1.4), with an extra ad hoc
# x1.5 on the last bin. None of these numbers is derived from theory,
# simulation, or an excursion-set calculation.
#
# CONSEQUENCE: the per-cut "sigma_obs" values and the "DEFICIT" verdicts this
# script prints compare the real catalogue against THIS PLACEHOLDER, not
# against a genuine LCDM prediction. The large deficits reported at small,
# testable radii (roughly -6 sigma to -19 sigma) are therefore most plausibly
# an artefact of the rescaling not matching the true BGS volume/depth --
# NOT evidence of a real cosmological tension. They must not be quoted as
# such, in the papers or elsewhere.
#
# The ECF/LCDM *ratio* A_ecf(R) is unaffected by this normalisation (it is a
# multiplicative model), so the shape of the predicted ECF excess remains
# meaningful; only the absolute counts and their significances do not.
#
# TODO: replace with a proper LCDM VSF (simulation-calibrated or excursion-set)
# before any of these significances is used as a published result.
# ---------------------------------------------------------------------------
SDSS_BINS_H = np.array([10,13,16,19,22,25,28,32,36,42,54], dtype=float)
SDSS_COUNTS = np.array([155,210,215,185,150,110,70,40,20,8],  dtype=float)
N_DR1       = 1484       # expected DR1 total (assumed, not measured)
DEPTH_F     = 1.4        # ad hoc depth factor -- not derived
DR1_COUNTS  = SDSS_COUNTS * (N_DR1 / SDSS_COUNTS.sum()) * DEPTH_F
DR1_COUNTS[-1] *= 1.5    # ad hoc last-bin boost -- not derived
BINS_MPC    = SDSS_BINS_H / h
BIN_CENTERS = 0.5 * (BINS_MPC[:-1] + BINS_MPC[1:])

# ===========================================================================
# ÉTAPE 1 — TÉLÉCHARGEMENT
# ===========================================================================

def probe_url(base_url, fname):
    """Teste si une URL est accessible (HEAD request)."""
    import urllib.error
    url = base_url + fname
    req = urllib.request.Request(url, method='HEAD')
    try:
        urllib.request.urlopen(req, timeout=10)
        return url
    except Exception:
        return None

def find_working_url(fname):
    """Try every candidate URL; return the first one that responds."""
    print(f"  Probing URL for {fname} ...")
    for base in BASE_URLS:
        url = probe_url(base, fname)
        if url:
            print(f"  [OK] URL found: {base}")
            return url, base
    return None, None

def download_catalog(local_dir=LOCAL_DIR, force=False):
    """
    Download the 2 VoidFinder files from the public DESI URL.
    Tries several URL variants in case of 404.
    """
    os.makedirs(local_dir, exist_ok=True)
    print(f"\nDownloading DESIVAST DR1 -> {local_dir}/")

    working_base = None   # remember the base URL that works

    for fname in FITS_FILES:
        dest = os.path.join(local_dir, fname)
        if os.path.exists(dest) and not force:
            size = os.path.getsize(dest) / 1e6
            print(f"  [OK] Already present: {fname}  ({size:.1f} MB)")
            continue

        # Determine the URL
        if working_base:
            url = working_base + fname
        else:
            url, working_base = find_working_url(fname)

        if url is None:
            print(f"\n  [FAILED] No reachable URL for {fname}")
            print(f"  URLs tried:")
            for base in BASE_URLS:
                print(f"    {base}{fname}")
            print(f"\n  Workarounds:")
            print(f"  1. NERSC : cp {NERSC_PATH}{fname} {local_dir}/")
            print(f"  2. Contact: hrincon@ur.rochester.edu (DESIVAST author)")
            print(f"  3. Retry in a few minutes (the DESI server may be temporarily down)")
            continue

        print(f"  Downloading: {fname}", end=" ", flush=True)
        try:
            def progress(block, block_size, total):
                if total > 0:
                    pct = min(block * block_size / total * 100, 100)
                    print(f"\r  {fname} : {pct:.0f}%", end="", flush=True)
            urllib.request.urlretrieve(url, dest, reporthook=progress)
            size = os.path.getsize(dest) / 1e6
            print(f"\r  [OK] {fname}  ({size:.1f} MB) → {dest}")
        except Exception as e:
            print(f"\r  [ERROR] {e}")
            print(f"  wget '{url}' -P {local_dir}/")

# ===========================================================================
# ÉTAPE 2 — LECTURE DU CATALOGUE
# ===========================================================================

def load_catalog(local_dir=LOCAL_DIR):
    """
    Lit les fichiers FITS DESIVAST DR1 VoidFinder et retourne
    un tableau de rayons effectifs en Mpc physique.

    Structure FITS (par fichier) :
      HDU[0] : PrimaryHDU (vide)
      HDU[1] : BinTableHDU "Maximal Spheres"
        Colonnes clés :
          EFFECTIVE_RADIUS       [Mpc/h] — rayon effectif du vide (ajout DESIVAST)
          EFFECTIVE_RADIUS_UNCERT[Mpc/h] — incertitude
          flag / hole_id                 — identifiant unique du vide
          edge_flag                      — 0=intérieur, 1=bord
    """
    try:
        from astropy.io import fits as apfits
        from astropy.table import Table, vstack
    except ImportError:
        sys.exit("Please install astropy: pip install astropy")

    tables = []
    _missing_fits = []
    for fname in FITS_FILES:
        fpath = os.path.join(local_dir, fname)
        if not os.path.exists(fpath):
            print(f"  [MISSING] {fpath}")
            _missing_fits.append(fname)   # RÈGLE 23 -- voir contrôle plus bas
            continue

        hdu  = apfits.open(fpath)
        tbl  = Table(hdu[1].data)
        hdu.close()
        print(f"  {fname}: {len(tbl):,} rows (maximal spheres)")
        print(f"  Columns: {list(tbl.colnames)}")
        tables.append(tbl)

    if not tables:
        sys.exit(
            "\nNo FITS file found in: " + local_dir +
            "\nRe-run with --download, or check the URL:\n  " + BASE_URL
        )

    # RÈGLE 23 (25/08/2026) -- le cas "TOUT manque" était déjà traité, pas le
    # cas "UNE PARTIE manque". Un catalogue amputé ne donne pas une figure
    # vide mais une figure FAUSSE : le comptage de vides, donc le sigma du
    # kill-switch, seraient calculés sur un sous-ensemble sans que rien ne le
    # signale. Sortir à 0 mentirait à toute chaîne automatisée.
    if _missing_fits:
        sys.exit(
            f"\n[ERROR] {len(_missing_fits)}/{len(FITS_FILES)} FITS file(s) "
            f"missing: {', '.join(_missing_fits)}\n"
            "        The void counts -- and therefore the kill-switch sigma --\n"
            "        would be computed on a TRUNCATED catalogue.\n"
            "        Re-run with --download."
        )

    data = vstack(tables)
    print(f"\n  Raw total: {len(data):,} maximal spheres (NGC + SGC)")

    # -- Select interior voids (edge_flag == 0) --------------------------
    eflag_col = next(
        (c for c in ['edge_flag','EDGE_FLAG','EdgeFlag'] if c in data.colnames),
        None
    )
    if eflag_col:
        data = data[data[eflag_col] == 0]
        print(f"  After edge_flag==0 filter: {len(data):,} rows")
    else:
        print("  [WARN] edge_flag column absent -- all voids included")

    # -- Deduplication: one row per unique void --------------------------
    id_col = next(
        (c for c in ['flag','FLAG','hole_id','HOLE_ID','VoidID','void_id']
         if c in data.colnames),
        None
    )
    if id_col:
        _, idx = np.unique(data[id_col], return_index=True)
        data = data[np.sort(idx)]
        print(f"  Unique interior voids: {len(data):,}")
    else:
        print("  [WARN] void id column absent -- deduplication skipped")

    # -- Read the effective radius ---------------------------------------
    r_col = next(
        (c for c in ['EFFECTIVE_RADIUS','effective_radius','R_EFF','r_eff','radius']
         if c in data.colnames),
        None
    )
    if r_col is None:
        print("Available columns:", data.colnames)
        sys.exit("EFFECTIVE_RADIUS column not found.")

    R_h   = np.array(data[r_col], dtype=float)   # Mpc/h
    R_mpc = R_h / h                               # -> physical Mpc

    # Cut at R_min = 10 Mpc/h (VoidFinder standard)
    R_mpc = R_mpc[R_mpc >= BINS_MPC[0]]

    print(f"\n  Effective radius [Mpc]:")
    print(f"    min    = {R_mpc.min():.1f}")
    print(f"    median = {np.median(R_mpc):.1f}")
    print(f"    max    = {R_mpc.max():.1f}")
    print(f"    N(R > {R_KS_H:.0f} Mpc/h = {R_KS_MPC:.0f} Mpc) = "
          f"{(R_mpc >= R_KS_MPC).sum()}")
    R_max_h = R_mpc.max() * h
    if R_max_h < R_KS_H:
        print(f"\n  *** CRITICAL DIAGNOSTIC ***")
        print(f"  R_max = {R_mpc.max():.1f} Mpc = {R_max_h:.1f} Mpc/h")
        print(f"  Kill-switch at {R_KS_H:.0f} Mpc/h IS BEYOND THE CATALOGUE RANGE.")
        print(f"  -> BGS z<0.24 yields no voids larger than {R_KS_H:.0f} Mpc/h.")
        print(f"  -> ECF test not possible with DESIVAST DR1 BGS alone.")
        print(f"  -> Remedy: await DESI LRG/ELG or Euclid DR1 (Oct 2026).")
        print(f"  -> Fall back to R_CUTS_H = [18., 20., 22., 24., 28.] for current data.")

    return R_mpc

# ===========================================================================
# ÉTAPE 3 — ANALYSE ECF
# ===========================================================================

def A_ecf(R_mpc, xi=XI_KZ_MPC):
    return 1. + A_ECF_PEAK * np.exp(-(R_mpc - xi)**2 / (2.*SIG_KZ_MPC**2))

ECF_MID = DR1_COUNTS * np.array([A_ecf(R)            for R in BIN_CENTERS])
ECF_LO  = DR1_COUNTS * np.array([A_ecf(R, XI_KZ_LO)  for R in BIN_CENTERS])
ECF_HI  = DR1_COUNTS * np.array([A_ecf(R, XI_KZ_HI)  for R in BIN_CENTERS])

def N_above_model(counts, R_cut_h):
    return counts[SDSS_BINS_H[:-1] >= R_cut_h].sum()

def sigma_detect(N_l, N_e, f_syst=0.0):
    if N_l < 0.1: return 0.
    return (N_e - N_l) / np.sqrt(N_l + (f_syst * N_l)**2)

def verdict(N_obs, N_lcdm, N_ecf):
    sig_obs  = (N_obs - N_lcdm) / np.sqrt(max(N_lcdm, 0.1))
    sig_pred = sigma_detect(N_lcdm, N_ecf, f_syst=0.30)
    if   sig_obs >= sig_pred * 0.8: return "ECF SIGNAL", sig_obs
    elif sig_obs <= -2.0:            return "DEFICIT",    sig_obs
    elif sig_obs >=  2.0:            return "EXCESS",     sig_obs
    else:                            return "COMPATIBLE", sig_obs

# ===========================================================================
# MAIN
# ===========================================================================

def main():
    no_dl = '--no-dl' in sys.argv

    print("=" * 65)
    print("ECF VSF vs DESIVAST DR1  v1.2 -- 21/07/2026")
    print("=" * 65)
    print(f"VSF kill-switch : R > {R_KS_MPC:.0f} Mpc = {R_KS_H:.1f} Mpc/h")
    print(f"Local dir      : {LOCAL_DIR}")
    print(f"Public URL     : {BASE_URL}")

    # -- Download --------------------------------------------------------
    if not no_dl:
        download_catalog(LOCAL_DIR)
    else:
        print("\n[--no-dl] Download skipped")

    # -- Load ------------------------------------------------------------
    print("\n-- Reading FITS catalogue --")
    R_obs = load_catalog(LOCAL_DIR)
    N_obs_total = len(R_obs)
    if N_obs_total < 500:
        print(f"\n  WARNING: only {N_obs_total} voids loaded.")
        print(f"  The VoidFinder catalogue stores maximal spheres")
        print(f"  (several per void). Without a void_id column they are")
        print(f"  treated as distinct voids -- likely undercount.")
        print(f"  -> Look for a column: VOID_ID, VOID_INDEX, ZONEID, zone_id")

    # Observed histogram on the same bins
    OBS_COUNTS, _ = np.histogram(R_obs, bins=BINS_MPC)
    OBS_COUNTS    = OBS_COUNTS.astype(float)

    # -- Statistics table ------------------------------------------------
    print("\n" + "=" * 65)
    print("RESULTS -- Real data vs LCDM vs ECF")
    print("=" * 65)
    print("""
  !! CAVEAT -- READ BEFORE INTERPRETING THE COLUMNS BELOW !!
  N_LCDM is NOT a theoretical LCDM void size function. It is a crude
  placeholder: an older SDSS catalogue shape rescaled to an assumed DR1
  total with a hand-tuned depth factor (see the block comment at the top
  of this file). The sigma_obs values and any "DEFICIT" verdicts below
  therefore compare the data against that placeholder, not against a real
  LCDM prediction, and must NOT be quoted as evidence of cosmological
  tension. Only the ECF/LCDM ratio (shape of the predicted excess) is
  meaningful at this stage.""")
    print(f"\n{'Cut':>12}  {'N_obs':>6}  {'N_LCDM':>7}  "
          f"{'N_ECF':>7}  {'σ_obs':>8}  {'Verdict':>15}")
    print("-" * 65)

    # Adapter les coupures à la plage réelle du catalogue
    R_max_data_h = R_obs.max() * h if len(R_obs) > 0 else R_KS_H
    if R_max_data_h < R_KS_H:
        # Catalogue ne monte pas jusqu'au kill-switch → tester les plus petites échelles
        R_CUTS_H = [18., 20., 22., 24., 28.]
        print(f"\n  Cuts adapted to R_max={R_max_data_h:.1f} Mpc/h: {R_CUTS_H}")
    else:
        R_CUTS_H = [28., 32., 36., 40., 42.]
    results  = {}

    for Rc in R_CUTS_H:
        N_obs_c  = int((R_obs >= Rc / h).sum())
        N_lcdm_c = N_above_model(DR1_COUNTS, Rc)
        N_ecf_c  = N_above_model(ECF_MID,    Rc)
        verd, sig = verdict(N_obs_c, N_lcdm_c, N_ecf_c)
        ks        = " <-KS" if abs(Rc - R_KS_H) < 2. else ""
        print(f"  R>{Rc:>4.0f} Mpc/h  {N_obs_c:>6}  {N_lcdm_c:>7.0f}  "
              f"{N_ecf_c:>7.0f}  {sig:>+7.1f}σ  {verd}{ks}")
        results[Rc] = dict(N_obs=N_obs_c, N_lcdm=N_lcdm_c,
                           N_ecf=N_ecf_c, sigma=sig, verdict=verd)

    # Kill-switch summary
    # Robust lookup (float key never matches exactly)
    ks_key      = min(results.keys(), key=lambda x: abs(x - R_KS_H))
    ks_res      = results[ks_key]
    is_proxy    = abs(ks_key - R_KS_H) > 2.0   # true threshold could not be tested
    print(f"\n{'─'*65}")
    if is_proxy:
        print(f"VERDICT (PROXY -- true kill-switch R > {R_KS_H:.0f} Mpc/h = "
              f"{R_KS_MPC:.0f} Mpc IS OUT OF CATALOGUE RANGE):")
        print(f"  Cut actually tested here: R > {ks_key:.0f} Mpc/h "
              f"({ks_key/h:.1f} Mpc physical) -- NOT the official kill-switch.")
        print(f"  At the true threshold (R > {R_KS_MPC:.0f} Mpc physical) the BGS")
        print(f"  catalogue contains no void at all (N=0, see diagnostic above) --")
        print(f"  this is NOT a falsification, only an out-of-reach limitation.")
    else:
        print(f"KILL-SWITCH VERDICT (R > {R_KS_H:.0f} Mpc/h = {R_KS_MPC:.0f} Mpc):")
    print(f"  N_obs   = {ks_res['N_obs']}")
    print(f"  N_LCDM  = {ks_res['N_lcdm']:.0f}")
    print(f"  N_ECF   = {ks_res['N_ecf']:.0f}  (×{ks_res['N_ecf']/max(ks_res['N_lcdm'],.1):.2f})")
    print(f"  σ_obs   = {ks_res['sigma']:+.1f}σ")
    print(f"  Verdict : {ks_res['verdict']}"
          + ("  [proxy, reduced scale -- see warning above]" if is_proxy else ""))

    # -- Figure ----------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='white')
    fig.suptitle(
        r"ECF VSF vs $\Lambda$CDM -- REAL DESIVAST DR1 (Rincon+2025)"
        "\n"
        r"VSF kill-switch: $N_{\rm ECF}(R>40\,h^{-1}{\rm Mpc})"
        r"\approx 2.1\times N_{\Lambda{\rm CDM}}$ "
        fr"· $\xi_{{\rm KZ}}=60$ Mpc (adopted) · $N_{{\rm obs}}={N_obs_total}$ voids",
        fontsize=10.5, fontweight='bold'
    )

    W = np.diff(BINS_MPC) * 0.38

    # Left panel -- histograms
    ax = axes[0]
    ax.bar(BIN_CENTERS, DR1_COUNTS, W, align='center',
           color='#1C3F7A', alpha=0.45, label=r'$\Lambda$CDM toy model (rescaled, see caveat)')
    ax.bar(BIN_CENTERS, ECF_MID, W, align='center',
           color='#CC2222', alpha=0.35, label=r'ECF adopted template ($\xi_{\rm KZ}=60$ Mpc)')
    ax.errorbar(BIN_CENTERS, OBS_COUNTS,
                yerr=np.sqrt(np.maximum(OBS_COUNTS, 1.)),
                fmt='ko', ms=5, lw=1.5, capsize=4, zorder=7,
                label=f'DESIVAST DR1 real (N={N_obs_total})')
    ax.axvline(R_KS_MPC,   c='orange', lw=2.0, ls='--',
               label=fr'Kill-switch {R_KS_H:.0f} Mpc/$h$ (out of range)')
    ax.axvline(XI_KZ_MPC,  c='red',    lw=1.2, ls=':',
               label=fr'$\xi_{{\rm KZ}}={XI_KZ_MPC:.0f}$ Mpc')
    ax.fill_betweenx([0, max(OBS_COUNTS.max(), DR1_COUNTS.max())*1.1],
                     R_KS_MPC, 200., color='orange', alpha=0.07, zorder=0)

    # Annotate observed deviations
    for i, (Rc_h, Rc_mpc) in enumerate(zip(SDSS_BINS_H[:-1], BIN_CENTERS)):
        N_obs_b = OBS_COUNTS[i]
        N_l_b   = DR1_COUNTS[i]
        if N_l_b > 5 and Rc_h >= 28.:
            sig_b = (N_obs_b - N_l_b) / np.sqrt(max(N_l_b, 1.))
            color = '#CC0000' if abs(sig_b) > 2 else '#555555'
            ax.text(Rc_mpc, max(N_obs_b, N_l_b) + 4,
                    fr'{sig_b:+.1f}σ', ha='center', va='bottom',
                    fontsize=7, color=color)

    ax.set_xlabel(r'$R_{\rm eff}$ [Mpc]', fontsize=11)
    ax.set_ylabel('Number of voids per bin', fontsize=10)
    ax.set_title('Observed distribution vs models', fontsize=10)
    ax.set_xlim(BINS_MPC[0], BINS_MPC[-1])
    ax.set_ylim(0.)
    ax.legend(fontsize=7.5)
    ax.grid(True, alpha=0.22)
    ax_t = ax.twiny()
    ax_t.set_xlim(ax.get_xlim()[0]*h, ax.get_xlim()[1]*h)
    ax_t.set_xlabel(r'$R_{\rm eff}$ [Mpc/$h$]', fontsize=10)

    # Right panel -- per-cut statistical summary
    ax2 = axes[1]
    R_c_arr  = [r for r in R_CUTS_H]
    sig_obs  = [results[r]['sigma']  for r in R_c_arr]
    sig_pred = [sigma_detect(results[r]['N_lcdm'],
                             results[r]['N_ecf'], 0.30) for r in R_c_arr]
    colors   = ['#CC0000' if abs(s) > 2 else '#1C3F7A' for s in sig_obs]
    x_pos    = np.arange(len(R_c_arr))

    bars = ax2.bar(x_pos - 0.2, sig_obs,  0.38, color=colors, alpha=0.8,
                   label='observed σ (real data)')
    ax2.bar(x_pos + 0.2, sig_pred, 0.38, color='#CC2222', alpha=0.45,
            hatch='////', label='predicted σ if ECF true (+30% syst.)')

    ax2.axhline(0.,  c='k',      lw=0.8)
    ax2.axhline(2.,  c='gray',   lw=0.8, ls=':', label='2σ')
    ax2.axhline(-2., c='gray',   lw=0.8, ls=':')
    ax2.axhline(3.,  c='orange', lw=1.2, ls='--', label='3σ')

    # Value annotations
    for i, (so, sp) in enumerate(zip(sig_obs, sig_pred)):
        ax2.text(i-0.2, so + (0.15 if so >= 0 else -0.3),
                 f'{so:+.1f}σ', ha='center', fontsize=8,
                 color='#CC0000' if abs(so) > 2 else '#1C3F7A')

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([fr'R>${r:.0f}$' + '\nMpc/h' for r in R_c_arr], fontsize=9)
    ax2.set_ylabel(r'$(N_{\rm obs} - N_{\Lambda{\rm CDM}})/\sqrt{N_{\Lambda{\rm CDM}}}$ [$\sigma$]',
                   fontsize=9)
    ax2.set_title('Significance per cut', fontsize=10)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.22, axis='y')

    # Kill-switch verdict box
    # NOTE (v1.2): when the true kill-switch is out of catalogue range,
    # this box must say so explicitly rather than display a smaller
    # fallback cut under the kill-switch label.
    if is_proxy:
        verd_color = '#B36B00'
        box_txt = (f"True kill-switch R>{R_KS_H:.0f} Mpc/h:\n"
                   f"OUT OF CATALOGUE RANGE (N=0)\n"
                   f"— not a falsification —\n"
                   f"Proxy shown: R>{ks_key:.0f} Mpc/h, "
                   f"σ={ks_res['sigma']:+.1f}")
    else:
        verd_color = '#CC0000' if 'ECF' in ks_res['verdict'] else '#1C3F7A'
        box_txt = (f"Kill-switch R>{R_KS_H:.0f} Mpc/h:\n"
                   f"N_obs={ks_res['N_obs']}  N_LCDM={ks_res['N_lcdm']:.0f}\n"
                   f"σ = {ks_res['sigma']:+.1f}  -> {ks_res['verdict']}")
    ax2.text(0.97, 0.97, box_txt,
             transform=ax2.transAxes, va='top', ha='right', fontsize=8.5,
             bbox=dict(boxstyle='round', facecolor='#f8f8f8',
                       edgecolor=verd_color, lw=1.5),
             color=verd_color, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"\nFigure: {OUTPUT_PNG}")
    print("=" * 65)


if __name__ == "__main__":
    main()
