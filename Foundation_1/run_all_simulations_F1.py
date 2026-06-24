#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation I: The Metric Universe
Script      : run_all_simulations_F1.py (v2)
Author      : Pascal Fichant
Date        : April 2026
Description :
    Master orchestrator for the ECF framework reproducibility pipeline.
    This script navigates through:
    1. 02_Scientific_Code/A_Core_Calculations (Physics & ODEs)
    2. 02_Scientific_Code/B_Paper_Plots (Visualization)

Usage (Windows):
    python run_all_simulations_F1.py

Note:
    UTF-8 is enforced for all subprocesses — no UnicodeEncodeError on
    Windows cp1252 terminals. All figures are centralized in figures_output/.
=============================================================================
"""
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

# Execution order: physics calculations first, then paper plots
STRUCTURE = [
    "A_Core_Calculations",
    "B_Paper_Plots",
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
        print("\n>>> CENTRALIZING FIGURES → figures_output/ ...")
        log_file.write("\n>>> FIGURE CENTRALIZATION\n")
        moved_count = 0

        for root, dirs, files in os.walk(CODE_BASE):
            for file in files:
                if file.lower().endswith((".png", ".pdf", ".jpg", ".jpeg")):
                    src = os.path.join(root, file)
                    dst = os.path.join(FIG_DIR, file)
                    try:
                        shutil.copy2(src, dst)
                        os.remove(src)
                        moved_count += 1
                        log_file.write(f"  [MOVED] {file}\n")
                    except Exception as exc:
                        log_file.write(f"  [COPY ERROR] {file}: {exc}\n")

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
