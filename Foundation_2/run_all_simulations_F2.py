#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_simulations_F2.py — reproducibility pipeline for Foundation II

Run from the ROOT of the package:

    python3 run_all_simulations_F2.py

[REWRITTEN 11/09/2026] The previous version lived in
02_Scientific_Code/A_Core_Calculations/ and scanned only that folder --
the 57 scripts of B_Paper_Plots, which produce the figures of the paper,
were therefore NOT covered. A depositor following the instructions would
have regenerated the calculations only.

This version follows the Foundation I model exactly:
  - orchestrator at the root of the package (same level as run_all_simulations_F1.py);
  - scan of 02_Scientific_Code/{A_Core_Calculations, B_Paper_Plots}
    (+ since 28/10/2026 the plotting script fig_planck_data_bounds.py of
    CMB_Seeds_REPRO, for Fig. 35);
  - each script runs IN ITS OWN FOLDER (cwd=dirname), which
    preserves the relative paths to the data;
  - figures collected in figures_output/.

F2-SPECIFIC FEATURES kept:
  - PYTHONHASHSEED=0 for the reproducibility of seeded scripts;
  - SPARC pipeline order: fit_sparc175.py must precede
    merge_sparc_inclination.py (guaranteed by the alphabetical sort:
    f < m; now also declared in PRODUCERS_FIRST below);
  - the SPARC data are present at both required locations.

OPTIONAL DEPENDENCIES: plot_gamma_macro_z.py and plot_gamma_micro_z.py
export via plotly/kaleido, which requires a Chrome browser. Without it,
these two scripts fail cleanly and the pipeline continues.
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# DIRECTORY CONFIGURATION
# ---------------------------------------------------------------------------
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CODE_BASE = os.path.join(BASE_DIR, "02_Scientific_Code")
FIG_DIR   = os.path.join(BASE_DIR, "figures_output")
LOG_DIR   = os.path.join(BASE_DIR, "logs")

# Execution order: physics calculations first, then paper plots
STRUCTURE = [
    "A_Core_Calculations",
    "B_Paper_Plots",
]

# [ADDED 28/10/2026] Figure scripts outside A and B. CMB_Seeds_REPRO is a
# reproduction package with its own README, not scanned as a category; but
# Fig. 35 of the paper (Fig_CMB_Seeds_PlanckData.png) comes from it, and the
# run did not produce it. Only the PLOTTING script is run here: it redraws the
# figure from the reference json shipped in CMB_Seeds_REPRO/reference/ (or from
# results_planck_data.json if present). The CLASS fit itself
# (ecf_cmb_seeds_planck_data.py) is NOT run: it needs CLASS and the Planck
# likelihood. The script writes into its current directory (cwd), here its own
# folder, from which the collection step below picks the PNG up.
EXTRA_FIGURE_SCRIPTS = [
    ("CMB_Seeds_REPRO", "fig_planck_data_bounds.py",
     "Fig_CMB_Seeds_PlanckData.png"),
]

# ---------------------------------------------------------------------------
# DATA DEPENDENCIES -- ENFORCED order
# ---------------------------------------------------------------------------
# [ADDED 11/09/2026] Some scripts produce data files that others consume.
# The alphabetical sort ordered them correctly, but BY CHANCE: between
# plot_ECFLRDJeansMass.py and plot_ECF_LRD_Jeans_mass.py the gap is a single
# rank, and rests only on the fact that in ASCII 'L' (76) precedes '_' (95).
# Renaming either of them would reverse the order and break the pipeline
# with a file-not-found error.
#
# The producers are therefore declared explicitly: they run FIRST, in the
# order of this list, and the rest follows in alphabetical order.
#
# Each entry: (folder, script, what it produces and for whom)
PRODUCERS_FIRST = [
    ("A_Core_Calculations", "generate_data_files.py",
     "Data_S3_CMB_Multipoles.csv -> plot_ecf_axis_of_evil_cmb.py"),
    ("A_Core_Calculations", "fit_sparc175.py",
     "SPARC fits -> merge_sparc_inclination.py"),
    ("B_Paper_Plots", "plot_ECFLRDJeansMass.py",
     "data_jeans_mass_vs_zt.csv, data_lrd_jeans_mass.csv "
     "-> plot_ECF_LRD_Jeans_mass.py"),
    # [ADDED 12/09/2026, flagged by the test bench] Paths built by an
    # f-string on a variable (data/{name}.csv): invisible to any pattern-based
    # analysis, and the order held only by alphabetical chance.
    ("A_Core_Calculations", "fetch_sparc_data.py",
     "data/{galaxy}.csv -> verify_galaxies_from_csv.py (same category: "
     "the order held only through f < v)"),
    ("A_Core_Calculations", "prepare_fig10_csv.py",
     "data/{name}.csv -> plot_fig10_analysis.py (category B, already protected "
     "by the order of the categories)"),
    # merge_sparc_inclination.py reads AND writes output/sparc175_fit_results.csv
    # (--fits and --out point to the same default): it is a SECOND producer
    # of the file, not only a consumer. It must therefore run after
    # fit_sparc175.py, which the alphabetical order ensures today (f < m)
    # but without guarantee.
    ("A_Core_Calculations", "fit_sparc175.py",
     "output/sparc175_fit_results.csv -> merge_sparc_inclination.py, "
     "which then REWRITES it (--fits and --out identical)"),
]


def order_scripts(folder_name, scripts):
    """Put the declared producers first, the rest in alphabetical order."""
    # [FIXED 15/09/2026] fit_sparc175.py appears TWICE in PRODUCERS_FIRST,
    # with two distinct and equally valid justifications (producer for
    # merge_sparc_inclination, and second producer of the same CSV). Without
    # deduplication it was run twice -- visible in Pascal's log of 15/09.
    # Deduplication is done here rather than in the list, to keep both
    # comments, each of which documents a real dependency.
    firsts = list(dict.fromkeys(
        s for d, s, _ in PRODUCERS_FIRST
        if d == folder_name and s in scripts))
    rest = [s for s in scripts if s not in firsts]
    return firsts + rest

# Reproducibility: fixed hash seed for scripts using randomised containers
CHILD_ENV = dict(os.environ)
CHILD_ENV["PYTHONHASHSEED"] = "0"
CHILD_ENV["MPLBACKEND"] = "Agg"
# [ADDED 28/10/2026] Force UTF-8 on the standard streams of the child scripts.
# On a Windows console (cp1252) a script printing a character such as "≈" or an
# accented letter stopped with UnicodeEncodeError: chiffrage_OGLE_ECF.py failed
# on the depositor's PC on 28/10/2026, while the same script passes under a UTF-8
# locale. The orchestrator of Foundation I already forces it. No result changes.
CHILD_ENV["PYTHONIOENCODING"] = "utf-8"
CHILD_ENV["PYTHONUTF8"] = "1"


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def setup_environment():
    """Initializes output directories and clears stale image artefacts."""
    for folder in [FIG_DIR, LOG_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"[INIT] Created directory: {folder}")

    # [ADDED 15/09/2026, on Pascal's suggestion] Clear image artefacts left in
    # the script folders by the PREVIOUS run.
    #
    # Since centralisation was changed to copy-without-delete (a copy followed
    # by a remove gave two chances to fail, for no gain), the sources pile up.
    # Clearing them at the START rather than the end is the safer order:
    # nothing has been produced yet, so nothing can be lost -- and whatever
    # remains in these folders afterwards demonstrably came from THIS run.
    #
    # Data files are never touched: .csv, .json and the data/ and output/
    # subfolders are the chain's INPUTS. A CSV emptied this way is exactly
    # what caused the EmptyDataError on 15/09.
    IMAGE_EXT = (".png", ".mp4", ".gif", ".jpg", ".jpeg", ".svg",
                 ".mp3", ".webm", ".avi", ".mov", ".webp", ".bmp", ".tif", ".tiff")
    cleared = 0
    for folder_name in STRUCTURE:
        folder_path = os.path.join(CODE_BASE, folder_name)
        if not os.path.isdir(folder_path):
            continue
        # Walk the subfolders too: some scripts drop figures into output/ or
        # data/ alongside the CSVs. The criterion is the EXTENSION, not the
        # folder -- .csv and .json are never touched wherever they sit.
        # _generated/ is skipped: those frames are the scripts' own working
        # material, not stale artefacts.
        for root, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs if d != "_generated"]
            for f in files:
                if not f.lower().endswith(IMAGE_EXT):
                    continue
                try:
                    os.remove(os.path.join(root, f))
                    cleared += 1
                except Exception as exc:
                    print(f"  [CLEAN] could not remove {f}: {type(exc).__name__}")
    # [ADDED 28/10/2026] Same rule for the figures of EXTRA_FIGURE_SCRIPTS.
    for folder_name, _script, png in EXTRA_FIGURE_SCRIPTS:
        stale = os.path.join(CODE_BASE, folder_name, png)
        if os.path.isfile(stale):
            try:
                os.remove(stale)
                cleared += 1
            except Exception as exc:
                print(f"  [CLEAN] could not remove {png}: {type(exc).__name__}")
    if cleared:
        print(f"[INIT] Cleared {cleared} stale image(s) from the script folders"
              f" (data files untouched).")


def run_script(script_path, log_file):
    """
    Executes a Python script in its own directory and captures output.
    Returns True on success, False on any error.
    The pipeline continues regardless of individual script failures.
    """
    script_name = os.path.basename(script_path)
    timestamp   = datetime.now().strftime('%H:%M:%S')
    print(f"  [{timestamp}] Running: {script_name}")

    log_file.write(f"\n{'='*70}\n")
    log_file.write(f"SCRIPT: {script_name}\n")
    log_file.write(f"PATH:   {script_path}\n")
    log_file.write(f"{'='*70}\n")

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(script_path),   # run in script's own directory
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=CHILD_ENV,
            check=False,                        # do NOT raise — log and continue
        )

        log_file.write(result.stdout)

        if result.returncode != 0:
            print(f"  [!] ERROR in {script_name} (exit code {result.returncode})")
            log_file.write(f"STDERR: {result.stderr}\n")
            return False

        return True

    except Exception as exc:
        print(f"  [!] EXCEPTION in {script_name}: {exc}")
        log_file.write(f"EXCEPTION: {exc}\n")
        return False


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------


def propagate_data(code_base, log_file):
    """Propagate the data produced by A_Core_Calculations to B_Paper_Plots.

    [ADDED 11/09/2026] Since each script runs in ITS OWN folder
    (cwd=dirname, F1 model), a relative path such as output/xxx.csv no
    longer points to the same place depending on the category. Yet
    fit_sparc175.py writes A_Core_Calculations/output/sparc175_fit_results.csv,
    which plot_F2_sparc_model_comparison.py reads under B_Paper_Plots/output/.

    This file carries the central result of the dark-matter sector
    (chi2_med = 0.80 over 175 galaxies, quoted in the F2 abstract). An audit
    on 21/08/2026 had already found this chain broken the other way round:
    read by four scripts, written by none.

    Called BETWEEN the two categories, never after: B_Paper_Plots needs
    these data BEFORE it runs.
    """
    src_dir = os.path.join(code_base, "A_Core_Calculations")
    dst_dir = os.path.join(code_base, "B_Paper_Plots")
    n = 0
    if not os.path.isdir(src_dir):
        return 0

    # [FIXED 12/09/2026] The first version propagated output/ only.
    # Yet generate_data_files.py writes Data_S1/S2/S3_*.csv AT THE ROOT of
    # A_Core_Calculations, and export_cmb_data.py / plot_void_statistics.py
    # do the same. These files are read by scripts of B_Paper_Plots.
    # The pipeline passed only because they had been copied BY HAND
    # during testing: a depositor cloning the repository would have hit
    # failures. Both levels are therefore propagated.
    DATA_EXT = (".csv", ".txt", ".dat", ".npy", ".npz", ".json")

    for sous in ("", "output"):
        src = os.path.join(src_dir, sous) if sous else src_dir
        dst = os.path.join(dst_dir, sous) if sous else dst_dir
        if not os.path.isdir(src):
            continue
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(src):
            if not f.lower().endswith(DATA_EXT):
                continue
            s_path = os.path.join(src, f)
            if not os.path.isfile(s_path):
                continue
            d_path = os.path.join(dst, f)
            # never overwrite a larger file with a smaller one: a 1-byte
            # file is the symptom of a broken chain
            if (not os.path.exists(d_path)
                    or os.path.getsize(d_path) < os.path.getsize(s_path)):
                shutil.copy2(s_path, d_path)
                n += 1
                log_file.write(f"  [DATA] {os.path.join(sous, f)}\n")
    return n


def main():
    setup_environment()

    start_time = datetime.now()
    log_path   = os.path.join(
        LOG_DIR,
        f"pipeline_log_{start_time.strftime('%Y%m%d_%H%M')}.txt"
    )

    if not os.path.exists(CODE_BASE):
        print(f"[FATAL] Directory '02_Scientific_Code' not found at:\n  {CODE_BASE}")
        return

    with open(log_path, "w", encoding="utf-8") as log_file:

        header = f"ECF REPRODUCIBILITY PIPELINE (F2) — {start_time}\n" + "=" * 60
        print(header)
        log_file.write(header + "\n")

        total_scripts = 0
        success_count = 0

        # --- RUN SCRIPTS ---------------------------------------------------
        for folder_name in STRUCTURE:
            folder_path = os.path.join(CODE_BASE, folder_name)

            if not os.path.exists(folder_path):
                print(f"\n[SKIP] Directory not found: {folder_name}")
                log_file.write(f"\n[SKIP] {folder_name}\n")
                continue

            section_header = f"\n>>> CATEGORY: {folder_name.replace('_', ' ').upper()}"
            print(section_header)
            log_file.write(section_header + "\n")

            scripts = sorted([
                f for f in os.listdir(folder_path)
                if f.endswith(".py")
                and not f.startswith("__")
                and f != os.path.basename(__file__)
            ])

            scripts = order_scripts(folder_name, scripts)

            for script in scripts:
                full_path = os.path.join(folder_path, script)
                total_scripts += 1
                if run_script(full_path, log_file):
                    success_count += 1

            # The data produced by the calculations must be available to the
            # figure scripts BEFORE these run.
            if folder_name == "A_Core_Calculations":
                print("\n>>> PROPAGATING PRODUCED DATA -> B_Paper_Plots ...")
                log_file.write("\n>>> DATA PROPAGATION\n")
                nprop = propagate_data(CODE_BASE, log_file)
                # [CLARIFIED 15/09/2026] A zero counter is the NORMAL result of
                # any run following a successful one: the function only copies
                # when the destination is missing or smaller. A bare zero read
                # as a failure. It now says what it means, and points to the
                # only check that tells you anything: the SIZE of the file.
                if nprop:
                    print(f"    {nprop} file(s) propagated")
                else:
                    print("    0 file(s) propagated -- data already in place, "
                          "nothing to copy.")
                    print("      Expected after any successful run. The counter "
                          "reports what was copied,")
                    print("      not whether the data is sound. To check that, "
                          "look at the SIZE of")
                    print("      B_Paper_Plots/output/sparc175_fit_results.csv: "
                          "~8300 bytes is healthy,")
                    print("      1 byte means a broken chain.")
                log_file.write(f"  {nprop} file(s) propagated\n")

        # --- EXTRA FIGURE SCRIPTS (outside A and B) --------------------------
        extra_header = "\n>>> CATEGORY: EXTRA FIGURE SCRIPTS (CMB_SEEDS_REPRO)"
        print(extra_header)
        log_file.write(extra_header + "\n")
        for folder_name, script, png in EXTRA_FIGURE_SCRIPTS:
            full_path = os.path.join(CODE_BASE, folder_name, script)
            if not os.path.isfile(full_path):
                print(f"  [SKIP] {folder_name}/{script} not found")
                log_file.write(f"  [SKIP] {folder_name}/{script} not found\n")
                continue
            total_scripts += 1
            if run_script(full_path, log_file):
                if os.path.isfile(os.path.join(CODE_BASE, folder_name, png)):
                    success_count += 1
                else:
                    print(f"  [!] {script} ran but {png} was not written")
                    log_file.write(f"  [!] {png} not written\n")

        # --- CENTRALIZE FIGURES --------------------------------------------
        # CORRECTED 15/09/2026, same fix as run_all_simulations_F1.py and _F3.
        # The previous version copied then removed each file and swallowed any
        # exception into a silent counter. On F1 that produced "Figures
        # collected : 0" while all 27 had been generated.
        print("\n>>> CENTRALIZING FIGURES \u2192 figures_output/ ...")
        log_file.write("\n>>> FIGURE CENTRALIZATION\n")
        moved_count = 0
        failures = []

        dest_ok = True
        try:
            os.makedirs(FIG_DIR, exist_ok=True)
            probe = os.path.join(FIG_DIR, ".write_probe")
            with open(probe, "w") as fh:
                fh.write("ok")
            os.remove(probe)
        except Exception as exc:
            dest_ok = False
            msg = (f"  [FATAL] Cannot write into {FIG_DIR}\n"
                   f"          {type(exc).__name__}: {exc}\n"
                   f"          Figures stay under 02_Scientific_Code/. Nothing is lost.")
            print(msg)
            log_file.write(msg + "\n")

        if dest_ok:
            for root, dirs, files in os.walk(CODE_BASE):
                # [ADDED 15/09/2026, on Pascal's remark] Skip _generated/ :
                # animation frames are simulation intermediates, not figures of
                # the paper. Two scripts write hundreds of them there --
                # deliberately, in their own subfolder -- and the recursive walk
                # was hauling all of them into figures_output, where they
                # outnumbered the real figures three to one. None appears in any
                # PDF; they exist only to be assembled into a GIF or MP4.
                # [ADDED 28/10/2026] Also skip reference/ folders (reference
                # outputs of CMB_Seeds_REPRO): the walk visits a folder before
                # its subfolders, so a reference copy of a same-named figure
                # would overwrite the fresh one.
                dirs[:] = [d for d in dirs if d not in ("_generated", "reference")]
                for file in files:
                    if file.lower().endswith((".png", ".pdf", ".jpg", ".jpeg")):
                        src = os.path.join(root, file)
                        dst = os.path.join(FIG_DIR, file)
                        try:
                            shutil.copy2(src, dst)
                            moved_count += 1
                            log_file.write(f"  [COPIED] {file}\n")
                        except Exception as exc:
                            failures.append((file, type(exc).__name__, str(exc)[:70]))
                            log_file.write(f"  [COPY ERROR] {file}: {exc}\n")

            if failures:
                print(f"\n  {len(failures)} file(s) could not be copied:")
                for f, kind, m in failures[:8]:
                    print(f"    {f:44} {kind}: {m}")
                print("  Sources are intact under 02_Scientific_Code/.")

        # --- SUMMARY -------------------------------------------------------
        duration = datetime.now() - start_time
        summary = (
            f"\n{'='*60}\n"
            f" PIPELINE COMPLETE : {success_count}/{total_scripts} scripts OK\n"
            f" Failed scripts    : {total_scripts - success_count}\n"
            f" Figures collected : {moved_count}  →  {FIG_DIR}\n"
            f" Total duration    : {duration}\n"
            f" Log               : {log_path}\n"
            f"{'='*60}\n"
        )
        print(summary)
        log_file.write(summary)


if __name__ == "__main__":
    main()
