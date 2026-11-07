#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation III: Cosmological Physics
Script      : run_all_simulations_F3.py (v2)
Author      : Pascal Fichant
Date        : April 2026
Description :
    Master orchestrator for the ECF framework reproducibility pipeline.
    This script navigates through:
    1. 02_Scientific_Code/A_Core_Calculations (Physics & ODEs)
    2. 02_Scientific_Code/B_Paper_Plots (Visualization)
    3. 02_Scientific_Code/C_Simulations (Pedagogical animations)

Usage (Windows):
    python run_all_simulations_F3.py

Note:
    UTF-8 is enforced for all subprocesses — no UnicodeEncodeError on
    Windows cp1252 terminals. All figures are centralized in figures_output/.
=============================================================================
"""

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import sys
import io
import subprocess
import shutil
from datetime import datetime

# ---------------------------------------------------------------------------
# Force UTF-8 for this process (Windows cp1252 console)
# ---------------------------------------------------------------------------
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Force UTF-8 for all child subprocesses
os.environ["PYTHONIOENCODING"] = "utf-8"

# ---------------------------------------------------------------------------
# DIRECTORY CONFIGURATION
# ---------------------------------------------------------------------------
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CODE_BASE = os.path.join(BASE_DIR, "02_Scientific_Code")
FIG_DIR   = os.path.join(BASE_DIR, "figures_output")
LOG_DIR   = os.path.join(BASE_DIR, "logs")

# Execution order: physics calculations first, then paper plots, then animations
STRUCTURE = [
    "A_Core_Calculations",
    "B_Paper_Plots",
    "C_Simulations",
]


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def setup_environment():
    """Initializes output directories."""
    for folder in [FIG_DIR, LOG_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"[INIT] Created directory: {folder}")

    # [ADDED 15/09/2026, on Pascal's suggestion] Clear image artefacts left in
    # the script folders by the PREVIOUS run.
    #
    # Since centralisation was changed to copy-without-delete, the sources pile
    # up. Clearing them at the START rather than the end is the safer order:
    # nothing has been produced yet, so nothing can be lost -- and whatever
    # remains afterwards demonstrably came from THIS run.
    #
    # Data files are never touched: .csv, .json and the data/ and output/
    # subfolders are the chain's INPUTS.
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
            encoding='utf-8',                   # force UTF-8 capture
            errors='replace',                   # replace unmappable chars with '?'
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

        header = f"ECF REPRODUCIBILITY PIPELINE — {start_time}\n" + "=" * 60
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
                if f.endswith(".py") and not f.startswith("__")
            ])

            for script in scripts:
                full_path = os.path.join(folder_path, script)
                total_scripts += 1
                if run_script(full_path, log_file):
                    success_count += 1

        # --- CENTRALIZE FIGURES --------------------------------------------
        # CORRECTED 14/09/2026, same fix as run_all_simulations_F1.py. The
        # previous version copied then removed each file and swallowed any
        # exception into a silent counter. On F1 that produced "Figures
        # collected : 0" while all 27 had been generated -- a result
        # indistinguishable from having produced nothing.
        #
        # Destination proved writable first, sources never deleted, every
        # failure named.
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
                   f"          Figures stay where they were produced, under\n"
                   f"          02_Scientific_Code/. Nothing is lost.")
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
                dirs[:] = [d for d in dirs if d != "_generated"]
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
