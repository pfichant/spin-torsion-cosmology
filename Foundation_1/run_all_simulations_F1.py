#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation I: The Metric Universe
Script      : run_all_simulations_F1.py
Author      : Pascal Fichant
Date        : March 2026
Description :
    Master orchestrator for the ECF framework reproducibility pipeline.
    This script navigates through:
    1. 02_Scientific_Code/A_Core_Calculations (Physics & ODEs)
    2. 02_Scientific_Code/B_Paper_Plots (Visualization)
=============================================================================
"""

import os
import subprocess
import datetime
import sys
import shutil

# --- DIRECTORY CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_BASE = os.path.join(BASE_DIR, "02_Scientific_Code")
FIG_DIR = os.path.join(BASE_DIR, "figures_output")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Specific sub-directories in 02_Scientific_Code/
# We execute Calculations first, then Plots.
STRUCTURE = [
    "A_Core_Calculations",
    "B_Paper_Plots"
]

def setup_environment():
    """Initializes output directories."""
    for folder in [FIG_DIR, LOG_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"[INIT] Created directory: {folder}")

def run_script(script_path, log_file):
    """Executes a Python script and redirects output to log."""
    script_name = os.path.basename(script_path)
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] Executing: {script_name}")
    
    log_file.write(f"\n{'='*70}\n")
    log_file.write(f"SCRIPT: {script_name}\n")
    log_file.write(f"PATH: {script_path}\n")
    log_file.write(f"{'='*70}\n")
    
    try:
        # Crucial: run the script in its own directory for relative imports
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(script_path),
            capture_output=True,
            text=True,
            check=True
        )
        log_file.write(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  [!] ERROR in {script_name}")
        log_file.write(f"STDOUT: {e.stdout}\n")
        log_file.write(f"STDERR: {e.stderr}\n")
        return False

def main():
    setup_environment()
    
    start_time = datetime.datetime.now()
    log_path = os.path.join(LOG_DIR, f"pipeline_log_{start_time.strftime('%Y%m%d_%H%M')}.txt")
    
    if not os.path.exists(CODE_BASE):
        print(f"[FATAL] Directory '02_Scientific_Code' not found at {CODE_BASE}")
        return

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"ECF REPRODUCIBILITY PIPELINE - {start_time}\n")
        log_file.write("="*60 + "\n")

        total_scripts = 0
        success_count = 0

        for folder_name in STRUCTURE:
            folder_path = os.path.join(CODE_BASE, folder_name)
            
            if not os.path.exists(folder_path):
                print(f"[SKIP] Directory not found: {folder_name}")
                continue

            print(f"\n>>> CATEGORY: {folder_name.replace('_', ' ').upper()}")
            
            # Find all .py files in the sub-folder
            scripts = [f for f in os.listdir(folder_path) 
                       if f.endswith(".py") and not f.startswith("__")]
            
            for script in sorted(scripts):
                full_path = os.path.join(folder_path, script)
                total_scripts += 1
                if run_script(full_path, log_file):
                    success_count += 1

        # --- AUTOMATIC FIGURE AGGREGATION ---
        print("\n>>> CENTRALIZING FIGURES TO figures_output/...")
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
                    except Exception:
                        pass 

    duration = datetime.datetime.now() - start_time
    print("\n" + "="*60)
    print(f" PIPELINE COMPLETE: {success_count}/{total_scripts} successful.")
    print(f" Total Duration: {duration}")
    print(f" {moved_count} figures collected in: {FIG_DIR}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()