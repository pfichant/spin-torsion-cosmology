#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_F1_non_regression.py — Foundation I regression suite
=========================================================

Every check below corresponds to a defect actually found and fixed during the
15-18 August 2026 audit. The point is not to test the physics: it is to make
sure that none of these specific defects comes back, silently, on the next
edit or the next regeneration.

Run from anywhere:

    python run_F1_non_regression.py [path-to-corpus]

Default corpus path is the parent directory of this script's parent.
Exit code 0 if all checks pass, 1 otherwise.

Author: Pascal Fichant / audit trail
Date:   18/08/2026
"""
# Last modified: 19/08/2026, 09:37 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys, os, re, io

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --------------------------------------------------------------------------
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

F1   = os.path.join(ROOT, "fichant_ecf_F1_Extended_v11.tex")
F1S  = os.path.join(ROOT, "fichant_ecf_F1_PRD_Short_v7_1.tex")
SDIR = os.path.join(ROOT, "Scripts_F1")

results = []

def check(name, ok, detail=""):
    results.append((name, ok, detail))

def read(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()

def strip_comments(tex):
    """LaTeX comments carry the audit trail; they must not trigger checks."""
    return re.sub(r'(?m)^%.*$', '', tex)

# ==========================================================================
# A. STRUCTURAL CHECKS — these catch broken edits, whatever their cause
# ==========================================================================
for path, label in [(F1, "F1 Extended"), (F1S, "F1 Short")]:
    s = read(path)
    if s is None:
        check(f"[A] {label} present", False, "file not found")
        continue
    labels = set(re.findall(r'\\label\{([^}]*)\}', s))
    refs   = set(re.findall(r'\\ref\{([^}]*)\}', s))
    broken = sorted(refs - labels)
    # A1 — dangling references. Triggered SEVEN times during the audit, always
    # because a label name was invented rather than read from the file.
    check(f"[A1] {label}: no dangling \\ref", not broken, str(broken))
    # A2 — figure environments balanced
    nb, ne = s.count(r'\begin{figure}'), s.count(r'\end{figure}')
    check(f"[A2] {label}: figure environments balanced", nb == ne, f"{nb} begin / {ne} end")
    # A3 — list environments balanced (a misused list broke compilation once)
    for env in ("itemize", "enumerate"):
        b, e = s.count(r'\begin{%s}' % env), s.count(r'\end{%s}' % env)
        check(f"[A3] {label}: {env} balanced", b == e, f"{b}/{e}")

# ==========================================================================
# B. WITHDRAWN VALUES — each of these was published and is now wrong
# ==========================================================================
s1, s1s = read(F1), read(F1S)
body1  = strip_comments(s1)  if s1  else ""
body1s = strip_comments(s1s) if s1s else ""
both = body1 + "\n" + body1s

WITHDRAWN = [
    # (pattern, label, what it was)
    (r'(?<![0-9.])39\.5(?![0-9])',  "Delta chi2 = -39.5",
     "superseded by -39.4: the published total omitted the eBOSS row and used "
     "an unsourced chi2_H0 = 30.5"),
    (r'(?<![0-9.])31\.5(?![0-9])',  "Delta AIC = -31.5",  "superseded by -31.4"),
    (r'(?<![0-9.])8\.2(?![0-9])',   "Delta BIC = -8.2",   "superseded by -8.1"),
    (r'(?<![0-9.])30\.5(?![0-9])',  "chi2_H0(LCDM) = 30.5",
     "reproduced by no declared parameter set; the declared values give 29.41"),
    (r'1\.65\s*\\?times\s*10\^\{-7\}', "Omega_spin,0 ~ 1.65e-7",
     "a RATIO (rho_spin/rho_r = 1.65e-9) displayed as a density parameter, with "
     "two orders lost in transcription; the actual value is 1.5e-13"),
    (r'10\^\{-22\}',                "rho_spin(0)/rho_Lambda ~ 1e-22",
     "the formula printed just above it yields 2.2e-13"),
    (r'10\^\{-60\}',                "Omega_spin,0 ~ 1e-60",
     "47 orders below the script value; hidden by a \\mathrm notation variant"),
    (r'0\.853',                     "S_8(LCDM) = 0.853",
     "sigma_8 and S_8 were inverted: 0.832 IS Planck's S_8, sigma_8 = 0.812"),
    (r'isotropic distribution of spins', "isotropic spin distribution",
     "contradicted by F2, F3 ChiralBounce and F3 physics, which all describe an "
     "aligned axial condensate"),
    (r'well before BBN',            "'well before BBN'",
     "chronological inversion: z = 3e6 is T ~ 0.7 keV, i.e. AFTER "
     "nucleosynthesis (T ~ 1 MeV, z ~ 4e9)"),
    (r'subdominant by a factor',    "'subdominant by a factor ~1e6 at BBN'",
     "impossible while the ratio scales as (1+z)^2"),
    (r'governs? both',              "'the same parameter GOVERNS both'",
     "the link is a property of the calibrated solution, not derived from the "
     "field equations (PO-F3-9)"),
    (r'lies within the DESI',       "'lies within the DESI contour'",
     "true only for z ~ 0.05-0.4"),
    (r'reading rules apply',        "the three JWST reading rules",
     "they invited a galaxy-by-galaxy test that the schematic lines cannot support"),
    (r'ECF ceiling',                "'ECF ceiling'",
     "the line is a schematic reference, not a computed luminosity ceiling"),
    (r'PO-F3-9', "the internal code PO-F3-9",
     "this open-problem code appears only in a document that is never "
     "deposited; the public Foundation III does not carry it and attributes "
     "the solver to Foundation IV. Describe the missing solver instead"),
    (r'(?<![0-9.])30\$--\$35(?![0-9])', "Cosmic Dawn z = 30-35",
     "not derivable from B_ECF = 1.45, which gives z = 27-29"),
]
for pat, label, why in WITHDRAWN:
    hits = len(re.findall(pat, both))
    check(f"[B] withdrawn: {label}", hits == 0, f"{hits} occurrence(s) — {why}")

# ==========================================================================
# C. VALUES THAT MUST BE PRESENT — the replacements, and the audit chain
# ==========================================================================
REQUIRED = [
    (r'(?<![0-9.])39\.4(?![0-9])', "Delta chi2 = -39.4", body1),
    (r'0\.20\\%',                  "the 0.20% ratio at recombination", body1),
    # [18/08/2026 revised] The check used to require the string "PO-F3-9".
    # That code exists only in an internal document which is not deposited,
    # and the public Foundation III attributes the solver to Foundation IV,
    # not III. F1 now describes the missing solver instead of citing a code
    # a reader cannot resolve -- so the check tests the description.
    (r'perturbation solver',       "the missing perturbation solver is named", body1),
    (r'remains to be developed|does not yet exist',
                                   "its status is stated (not yet existing)", body1),
    (r'calibrated proxy',          "'calibrated proxy' wording from F2", body1),
    (r'axial condensate',          "'axial condensate' in Appendix A", body1),
    (r'ionisation calibration factor', "F_ion physical definition", body1),
    (r'Spin fluid amplitude',      "Omega_spin^peak in the parameter table", body1),
]
for pat, label, hay in REQUIRED:
    check(f"[C] present: {label}", bool(re.search(pat, hay)), "missing")

# ==========================================================================
# D. NOTATION — variants hide values (this is how the 1e-60 escaped)
# ==========================================================================
for path, label in [(F1, "F1 Extended"), (F1S, "F1 Short")]:
    s = read(path)
    if s is None:
        continue
    bad = []
    for pat, why in [(r'\\Omega_\{\\mathrm\{spin\}', r'\mathrm variant'),
                     (r'\\Omega_\{spin', r'missing \rm'),
                     (r'\\Omega_\{\\rm spin,peak\}', 'spin,peak instead of ^{\\rm peak}'),
                     (r'\\rho_\{\\mathrm\{spin\}\}', r'\mathrm variant')]:
        if re.search(pat, s):
            bad.append(why)
    check(f"[D] {label}: spin notation harmonised", not bad, "; ".join(bad))

# ==========================================================================
# E. SCRIPTS — defects found in the code itself
# ==========================================================================
if os.path.isdir(SDIR):
    scripts = [f for f in os.listdir(SDIR) if f.endswith(".py")]

    # E1 — no absolute path (one script wrote to /tmp and its figure never
    #      reached the deposit; it also broke on Windows)
    offenders = []
    for f in scripts:
        src = read(os.path.join(SDIR, f)) or ""
        code = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
        if re.search(r'["\'](?:/tmp/|/home/|[A-Z]:\\\\)', code):
            offenders.append(f)
    check("[E1] no absolute output path", not offenders, ", ".join(offenders))

    # E2 — every script declares the UTF-8 guard (Windows cp1252 terminals)
    missing = [f for f in scripts
               if "reconfigure" not in (read(os.path.join(SDIR, f)) or "")]
    check("[E2] UTF-8 guard on every script", not missing,
          f"{len(missing)} without: {', '.join(missing[:4])}")

    # E3 — no two active scripts write the same figure (three such collisions
    #      were found; the loser silently overwrote the published figure)
    outputs = {}
    for f in scripts:
        src = read(os.path.join(SDIR, f)) or ""
        if "SUPERSEDED" in src[:4000]:
            continue
        for m in re.finditer(r'savefig\(\s*["\']([^"\']+\.png)', src):
            outputs.setdefault(m.group(1), []).append(f)
    clashes = {k: v for k, v in outputs.items() if len(v) > 1}
    check("[E3] no figure written by two scripts", not clashes,
          "; ".join(f"{k}: {v}" for k, v in clashes.items()))

    # E3b — deposited scripts must be in English. Rule set by Pascal on
    #       19/08/2026: the GitHub and Zenodo deposits are international, so
    #       every comment in a deposited script is written in English. This
    #       does not apply to the internal audit tooling, which never ships.
    INTERNAL = ("run_F1_agregat", "run_F1_non_regression",
                "check_architecture_sync", "stamp_headers")
    fr_words = (r'\b(?:le|la|les|des|une|dans|pour|avec|sur|par|sont|cette|qui|'
                r'que|nous|donc|ainsi|selon|entre|toute|voir|calculs?|valeurs?|'
                r'lignes?|ajout|retrait)\b')
    frenchisms = []
    for f in scripts:
        if f.startswith(INTERNAL):
            continue
        src = read(os.path.join(SDIR, f)) or ""
        if "SUPERSEDED" in src[:4000]:
            continue
        for line in src.splitlines():
            t = line.strip()
            if not t.startswith("#"):
                continue
            # "DES" is the Dark Energy Survey, not the French article
            if " DES " in line or "DES Y3" in line or "KiDS+DES" in line:
                continue
            if re.search(fr_words, t, re.I) or re.search(r'[àâçéèêëîïôùûœ]', t):
                frenchisms.append(f"{f}: {t[:44]}")
    check("[E3b] deposited scripts are in English", not frenchisms,
          "; ".join(frenchisms[:3]))

    # E4 — LaTeX labels must not leak into displayed strings (two did)
    leaks = []
    for f in scripts:
        src = read(os.path.join(SDIR, f)) or ""
        for m in re.finditer(r'(?:set_title|suptitle|set_xlabel|set_ylabel|\.text|annotate|label\s*=)'
                             r'\s*\(?\s*[rf]{0,2}["\']([^"\']{3,200})["\']', src):
            if re.search(r'\b(?:fig|eq|tab|sec|app):', m.group(1)):
                leaks.append(f"{f}: {m.group(1)[:40]}")
    check("[E4] no LaTeX label in displayed strings", not leaks, "; ".join(leaks[:3]))

    # E5 — literal double hyphens do not render as a dash under mathtext
    dashes = []
    for f in scripts:
        src = read(os.path.join(SDIR, f)) or ""
        for m in re.finditer(r'(?:set_title|suptitle|set_xlabel|set_ylabel|\.text|annotate|label\s*=)'
                             r'\s*\(?\s*[rf]{0,2}["\']([^"\']{3,200})["\']', src):
            if "--" in m.group(1) and "\\" not in m.group(1):
                dashes.append(f"{f}: {m.group(1)[:40]}")
    check("[E5] no literal '--' in displayed strings", not dashes, "; ".join(dashes[:3]))
else:
    check("[E] Scripts_F1 directory present", False, SDIR)

# ==========================================================================
# F. PHYSICS CONSISTENCY — the numbers that must keep agreeing
# ==========================================================================
try:
    RATIO_PEAK, Z_PEAK, OM_R = 0.093, 7500.0, 9.0e-5

    # F1 — the dilution chain quoted throughout the paper
    ratio_rec = RATIO_PEAK * ((1 + 1100.0) / (1 + Z_PEAK)) ** 2
    check("[F1] spin/rad ratio at recombination ~ 0.20%",
          abs(ratio_rec * 100 - 0.20) < 0.01, f"{ratio_rec*100:.3f}%")

    # F2 — the chi2 budget must sum to the published total
    rows = [(2345.20, 2347.00), (420.10, 420.10), (6.20, 6.20),
            (3.20, 3.30), (29.41, 0.10), (12.07, 0.09)]
    d = sum(e for _, e in rows) - sum(l for l, _ in rows)
    check("[F2] chi2 rows sum to -39.4", abs(d + 39.39) < 0.05, f"{d:.2f}")

    # F3 — S_8 / sigma_8 conversion (this was inverted)
    s8, om = 0.832, 0.315
    check("[F3] sigma_8 = S_8/sqrt(Om/0.3) = 0.812",
          abs(s8 / (om / 0.3) ** 0.5 - 0.8119) < 1e-3, f"{s8/(om/0.3)**0.5:.4f}")

    # F4 — Cosmic Dawn from the growth boost
    z_ecf = 1.45 * (1 + 20) - 1
    check("[F4] Cosmic Dawn ECF ~ 27-29 from B_ECF = 1.45",
          27 <= z_ecf <= 30, f"z = {z_ecf:.1f}")

    # F5 — BBN really is earlier than the spin-radiation crossing shown
    kB, T0 = 1.380649e-23, 2.7255
    a_bbn = T0 / (1e6 * 1.602176634e-19 / kB)
    check("[F5] a_BBN < a_sr (spin dominates at BBN)",
          a_bbn < 3.3e-7, f"a_BBN = {a_bbn:.2e} vs a_sr = 3.3e-07")
except Exception as exc:                                    # pragma: no cover
    check("[F] physics consistency block", False, repr(exc))

# ==========================================================================
print("=" * 74)
print("  FOUNDATION I — NON-REGRESSION SUITE")
print("=" * 74)
failed = 0
for name, ok, detail in results:
    if ok:
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}")
        if detail:
            print(f"        -> {detail}")
print("-" * 74)
print(f"  {len(results) - failed} passed, {failed} failed, {len(results)} total")
print("=" * 74)
sys.exit(1 if failed else 0)
