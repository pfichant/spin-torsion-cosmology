#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Topological Invariance Principle (PIT) Letter, v9
Script      : run_all_simulations_PIT.py
Author      : Pascal Fichant
Date        : October 2026
Description :
    Master script for the PIT Letter reproducibility pipeline, in the same
    form as run_all_simulations_F1.py and run_all_simulations_F2.py. It runs,
    in this order:
    1. 02_Scientific_Code/A_Core_Calculations/verify_flrw_curvature_degeneracy.py
    2. 02_Scientific_Code/B_Paper_Plots/plot_Cosmic_History_Omegas.py
    and, with --compile, recompiles the Letter (pdflatex x3; the bibliography
    is inside the .tex, no bibtex is needed) in a temporary folder.

Usage:
    python run_all_simulations_PIT.py              # the two scripts
    python run_all_simulations_PIT.py --compile    # + recompile the Letter

Outputs (nothing in 01_Paper_Publication is modified):
    logs/run_PIT.log                  full output of each script
    figures_output/Figure_CosmicHistory_Omegas_PIT.png   (copy of the figure)
    _build_PIT/fichant_ecf_PIT_Letter_v9.pdf             (with --compile)

Requirements: python >= 3.10 with numpy, scipy, matplotlib, sympy;
    pdflatex with revtex4-2 for --compile.
Note: UTF-8 is enforced for all subprocesses (Windows cp1252 terminals).
=============================================================================
"""
# Last modified: 26/10/2026 (Paris time)
# Corpus: PIT Letter — github.com/pfichant/spin-torsion-cosmology
import os
import sys
import shutil
import subprocess
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_BASE = os.path.join(BASE_DIR, "02_Scientific_Code")
PAPER_DIR = os.path.join(BASE_DIR, "01_Paper_Publication")
FIG_DIR = os.path.join(BASE_DIR, "figures_output")
LOG_DIR = os.path.join(BASE_DIR, "logs")
BUILD_DIR = os.path.join(BASE_DIR, "_build_PIT")
TEX = "fichant_ecf_PIT_Letter_v9.tex"

# (folder, script), physics first, then the figure
SCRIPTS = [
    ("A_Core_Calculations", "verify_flrw_curvature_degeneracy.py"),
    ("B_Paper_Plots", "plot_Cosmic_History_Omegas.py"),
]

ENV = dict(os.environ, PYTHONIOENCODING="utf-8", MPLBACKEND="Agg")


def run_script(folder, name, log):
    path = os.path.join(CODE_BASE, folder, name)
    print(f"  [{datetime.now():%H:%M:%S}] Running: {name}")
    log.write(f"\n{'=' * 70}\nSCRIPT: {name}\nPATH:   {path}\n{'=' * 70}\n")
    if not os.path.isfile(path):
        print(f"  [!] MISSING: {path}")
        log.write("MISSING\n")
        return False
    r = subprocess.run([sys.executable, path], cwd=os.path.dirname(path), env=ENV,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", check=False)
    log.write(r.stdout)
    if r.returncode != 0:
        print(f"  [!] ERROR in {name} (exit code {r.returncode})")
        log.write(f"STDERR: {r.stderr}\n")
        return False
    return True


def centralise_figure():
    src_dir = os.path.join(CODE_BASE, "B_Paper_Plots")
    pngs = [f for f in os.listdir(src_dir) if f.lower().endswith(".png")]
    os.makedirs(FIG_DIR, exist_ok=True)
    for f in pngs:
        shutil.copy2(os.path.join(src_dir, f), os.path.join(FIG_DIR, f))
    return pngs


def compile_letter():
    if shutil.which("pdflatex") is None:
        print("  pdflatex not found: compilation skipped")
        return None
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    os.makedirs(BUILD_DIR)
    for f in os.listdir(PAPER_DIR):
        shutil.copy2(os.path.join(PAPER_DIR, f), BUILD_DIR)
    for f in os.listdir(FIG_DIR):
        shutil.copy2(os.path.join(FIG_DIR, f), BUILD_DIR)
    for i in (1, 2, 3):
        with open(os.path.join(BUILD_DIR, f"build_{i}.log"), "w") as lg:
            subprocess.run(["pdflatex", "-interaction=nonstopmode", TEX],
                           cwd=BUILD_DIR, stdout=lg, stderr=subprocess.STDOUT, check=False)
    log3 = open(os.path.join(BUILD_DIR, "build_3.log"), encoding="utf-8", errors="replace").read()
    errors = sum(1 for line in log3.splitlines() if line.startswith("!"))
    pdf = os.path.join(BUILD_DIR, TEX.replace(".tex", ".pdf"))
    pages = None
    if shutil.which("pdfinfo") and os.path.isfile(pdf):
        out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if line.startswith("Pages"):
                pages = int(line.split()[1])
    print(f"  Pages: {pages if pages is not None else 'n/a'} (expected: 6)   LaTeX errors: {errors} (expected: 0)")
    print(f"  PDF: {pdf}   (the 'Dated:' line follows today's date, \\today)")
    return errors == 0


def main():
    do_compile = "--compile" in sys.argv[1:]
    os.makedirs(LOG_DIR, exist_ok=True)
    print("=" * 70)
    print(f" PIT Letter v9: reproducibility pipeline   {datetime.now():%Y-%m-%d %H:%M}")
    print("=" * 70)
    ok = ko = 0
    with open(os.path.join(LOG_DIR, "run_PIT.log"), "w", encoding="utf-8") as log:
        for folder, name in SCRIPTS:
            if run_script(folder, name, log):
                ok += 1
            else:
                ko += 1
    pngs = centralise_figure()
    print(f"\n  Figure(s) copied to figures_output/: {', '.join(pngs) if pngs else 'none'}")
    if do_compile:
        print("\n  Compilation of the Letter")
        if compile_letter() is False:
            ko += 1
    print(f"\n  Summary: {ok} script(s) OK, {ko} failure(s). Log: logs/run_PIT.log")
    sys.exit(0 if ko == 0 else 1)


if __name__ == "__main__":
    main()
