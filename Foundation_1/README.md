# Foundation I — reproducibility material

Numerical material for **Foundation I: The Metric Universe** (Einstein–Cartan Framework, ECF).
Every figure and every published number can be regenerated from this directory.

Licence CC BY 4.0 · Pascal Fichant, independent researcher, Montpellier
· `p.fichant.research@gmail.com`

---

## Quick start

```bash
python run_all_simulations_F1.py
```

`run_all_simulations_F1.py` is the master orchestrator: it executes every script in the
two directories below, logs each run to `logs/`, and reports how many succeeded.

The orchestrator runs the calculations first, then the plotting scripts, and centralises
every image into `figures_output/`. Runtime ≈ 2 minutes.

Requirements: Python ≥ 3.8, `numpy`, `scipy`, `matplotlib`.

⚠️ **The directory layout matters.** The orchestrator resolves paths relative to its own
location and will abort with `[FATAL] Directory '02_Scientific_Code' not found` if the tree
is changed:

```
run_all_simulations_F1.py
02_Scientific_Code/
    A_Core_Calculations/     calculations, no figure output
    B_Paper_Plots/           figure generation (plot_* prefix)
figures_output/              all images end up here
```

⚠️ **The orchestrator first clears old images.** At start-up it deletes every image file
(`.png`, `.gif`, `.mp4`, …) left in the script folders by a previous run, so that whatever
`figures_output/` receives demonstrably comes from *this* run; data files (`.csv`, `.json`) are
never touched. Each new image is then copied into `figures_output/` (the copy in the script
folder is kept). Worth knowing before running it on a working folder.

---

## A_Core_Calculations — published quantities

Each of these reproduces a number that appears in the paper. The unnumbered section
*Code and Data Availability* cites `script_01` to `script_06`, `chi_carre.py` and four of the
verification scripts below; `calibrate_w0wa.py` is cited in Appendix B. The values quoted
here are those the scripts print (run of 09/10/2026).

| Script | Reproduces | Paper |
|---|---|---|
| `script_01_solve_sound_horizon.py` | r_s(ECF) = 135.65 ± 0.32 Mpc (floor, measured inputs only) · r_s(ΛCDM) = 147.07 Mpc · 7.77 % reduction | Sec. 3, App. D |
| `script_04_halo_abundance.py` | halo density at z = 15 (M = 10¹⁰ h⁻¹ M⊙, Ω_m ≃ 0.267): n ≈ 2.6 × 10⁻⁴ Mpc⁻³ with topological seeding (f_NL,eff = 0.295), compared in earlier versions with a JWST target 2–4 × 10⁻⁴ that has no traceable source; no longer used by the paper (17/10/2026) | App. E (withdrawn) |
| `script_05_birefringence_calibration.py` | I_torsion = 3.3320 · S_ref = 4.0456 · g_CS = 0.02596 deg/unit · β = 0.3500° (CALIBRATED: equal to β_obs by construction); independent check of I_torsion and S_ref against their canonical values (MATCH) | Sec. 7.1, Table 6 |
| `script_06_S8_resolution.py` | S₈ = 0.766 by construction from γ_spin = 0.3116 (HISTORICAL, Ω_m = 0.315); A-7 diagnostic: CAMB ΛCDM reference 0.780, conditional γ = 0.066 (+0.069/−0.094), compatible with zero (CALCULATED-CONDITIONAL); physical γ_spin OPEN | Sec. 4–5 |
| `chi_carre.py` | tension-sector χ² (H₀ + S₈ + 4 BAO bins): ΛCDM 43.26, ECF 12.11; BAO alone 1.79 (ΛCDM) vs 12.11 (ECF) · eBOSS DR16 D_M/r_s(z = 1.48) = 30.21 ± 0.79 (Hou et al. 2021) | Sec. 5, Table 4 |
| `calibrate_w0wa.py` | w₀ = −1 + Ω_spin,peak = −0.907 ± 0.004 · wₐ = −ξ Ω_spin,peak = −0.153 with ξ = 1.645 (not derived) — CALIBRATED | App. B, PO-F1-B |

### Independent verification scripts

These produce no figure. They recompute published quantities by a separate route, so
that each number can be checked without re-running the main pipeline.

| Script | Verifies |
|---|---|
| `script_02_statistical_validation.py` | two-observable {H₀, S₈} χ² proxy, independent of `chi_carre.py` (HISTORICAL: the S₈ term is zero by calibration) |
| `script_03_extract_physical_parameters.py` | r_s = 135.65 Mpc by inversion and the ρ_spin/ρ_r evolution table (9.29 % at z_ref = 5600; 0.36 % at z = 1100) |
| `check_S8_effective.py` | back-verification of γ_spin from S₈ = 0.766 (HISTORICAL; identical by construction) |
| `check_beta_birefringence.py` | the 1.6 % agreement between k = β_obs/F_ion and k_ECKS |
| `check_trilemma_optimizer.py` | best fit t₀ = 13.20 Gyr at 2.45 % BAO tension, χ²_res = 4.03 > 0 (H₀ = 73.04 fixed, Ω_m = 0.267, target D_M/r_s = 30.21) |
| `joint_fit_trilemma.py` | joint (Ω_m, w₀, wₐ) rescan against age, BAO and θ* |
| `table_echelles_bounce.py` | characteristic scales of the bounce (a_min ∼ 10⁻³²) |
| `target_reference_budget.py` | reconstruction of the Table 4 budget and of ΔAIC / ΔBIC (HISTORICAL, Ω_m = 0.315; not recomputed) |
| `scan_F_ion_H0_BAO.py` | F_ion scan on the active background (H₀ + 4 BAO bins): joint compromise F_ion ≃ 1.22, calibrated point Δχ² ≃ 1.6 above it (CALCULATED-CONDITIONAL; Sec. 5) |

*(Two internal audit aggregators, `run_F1_agregat_scripts_calculation_audit.py` and
`run_F1_agregat_scripts_plots_audit.py`, concatenate the whole script set into a single
Markdown file for review. They play no role in the published results and are kept in
`Scripts_SUPERSEDED/`, not run by the orchestrator.)*

---

## B_Paper_Plots — one script per figure

| Script | Figure |
|---|---|
| `plot_torsion_geometry_schema.py` | 1 — Riemannian vs Riemann–Cartan geometry |
| `plot_primordial_boost.py` | 2 — transient pre-recombination boost |
| `plot_h0_s8_active.py` | 3 — H₀–S₈ plane on the active background (Ω_m = 0.267; ECF S₈ OPEN) |
| `plot_BAO_HighVisibility.py` | 4 — BAO Hubble diagram |
| `plot_cosmic_age_cpl.py` | 5 — cosmic age and dynamical dark energy |
| `plot_jwst_comparison.py` | figure withdrawn (17/10/2026) |
| `plot_euclid_pk_S8.py` | 6 — matter power spectrum, Euclid forecast |
| `plot_desi_prediction.py` | 7 — effective dark-energy trajectory |
| `plot_ecf_desi_mcmc_v3_0.py` | 8 and 22 — DESI DR1 MCMC, full covariance |
| `plot_predict_birefringence.py` | 9 — birefringence signal |
| `plot_21cm_prediction.py` | 10 — 21 cm acoustic scale |
| `plot_ecf_gw_spectrum.py` | 11 — primordial gravitational-wave spectrum |
| `plot_trilemma_irreducibility.py` | 12 — H₀–Age–BAO irreducibility |
| `plot_spin_ratio_evolution.py` | 13 — spin/radiation density ratio |
| `plot_deceleration_transition.py` | 15 — deceleration–acceleration transition |
| `plot_singularity_Resolution.py` | 16 — regularized high-density behaviour |
| `plot_friedmann_evolution.py` | 17 — torsion dominance in the early universe |
| `plot_density_bounce_comparison.py` | 18 — density saturation at the bounce |
| `plot_Cosmic_History_Omegas.py` | 19 — global consistency and effective flatness |
| `plot_Figure_K1_Global_Consistency.py` | 20 — geometric consistency with Planck 2018 |
| `plot_Fig_k3_Residuals_Angles.py` | 21 — high-ℓ damping-tail residuals |
| `plot_global_history.py` | 23 — global cosmic history |
| `plot_structure_zoom.py` | 24 — cosmic dawn and structure formation |
| `plot_planck_tt_residuals_ecf.py` | F1 Short — CMB temperature residuals |

### Scripts producing no figure of the paper

One script generates an image that no `.tex` currently includes:

| Script | What it shows |
|---|---|
| `plot_quadrilemma_omega_m.py` | Ω_m scan against age, BAO and θ* simultaneously — complements Fig. 13, which scans (w₀, z_t) |

It is kept in the deposit because it cross-checks a published statement by an independent
route. The corresponding analysis (a 2500-point scan) is developed in Foundation II; the
script is left here rather than duplicated, and cited from there.

*Three further scripts (`plot_spectre_puissance.py`, `plot_S8_resolution.py`,
`plot_hubble_boost_ratio.py`) were diagnostic: they revealed the σ₈/S₈ inversion and a
caption mismatch, both fixed on 18/08/2026. Having served their purpose, they were moved
to `Scripts_SUPERSEDED/` and are not run by the orchestrator.*

---

## Conventions

- **UTF-8 is enforced** in every script (`sys.stdout.reconfigure`), so output is readable
  on Windows `cp1252` terminals.
- **All output paths are relative.** No script writes outside its own directory.
- Several scripts embed a `verify_calibration()` routine that re-derives their own numbers
  from closed-form expressions and raises on any discrepancy — `plot_predict_birefringence.py`
  in particular (`plot_Optimization_Intersection.py`, now in `Scripts_SUPERSEDED/`, still
  reproduces the historical Δχ² = −39.5).

## Reference

P. Fichant, *Foundation I: The Metric Universe — Extended Version*,
doi:10.5281/zenodo.19577447

Companion papers: *Foundation II* (doi:10.5281/zenodo.20629237) and the Letter
*Exact Spatial Flatness and the Spin–Torsion Link* (doi:10.5281/zenodo.19798923).

---

## Note sur `Scripts_SUPERSEDED/`

Ce dossier contient des versions antérieures de scripts et figures, conservées pour
traçabilité et **à ne pas utiliser pour reproduire les valeurs publiées**. Voir le
`README.md` qu'il contient pour la liste des écarts connus.
