# Foundation I: The Metric Universe 🌌
### A Geometric Einstein-Cartan-Kibble-Sciama Cosmology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19577447.svg)](https://doi.org/10.5281/zenodo.19577447)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**PREPRINT v8** (internal revision 13) · October 2026 · Extended version 86 pp. · PRD Short companion v8 (internal 7.1 revised) 8 pp. · concept doi: [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447)

Deposited files: `fichant_ecf_F1_Extended_v13.pdf` (86 pp.) and `fichant_ecf_F1_PRD_Short_v7_1.pdf` (8 pp.). A PDF whose page count differs is not the deposited file.

---

## Corrections made after the first drafting of this README (22–24 October 2026)

- **Foundation I, Extended (p. 14) and PRD Short (§ III.A).** New paragraph « Domain of validity of the calibrated branch » with the *work required* (derivation of ρ_spin(a) from the action; parametric rise-and-fall test; Einstein–Cartan perturbation solver validated against BBN, CMB, BAO), and the same limit in one sentence in the PRD Short. New script `check_rs_spin_domain.py` (see Scripts).
- **Limit of the calibrated spin branch (23/10/2026).** The calibrated sound horizon r_s = 135.65 Mpc (hence H₀ = 73.04 km/s/Mpc) requires the spin term (∝ a⁻⁶, ρ_spin = 0.093 ρ_r at z_ref = 5600) to hold up to z ~ 10⁵ (if it stops at 2×10⁴: r_s = 139.4 Mpc). Extended unchanged to T ~ 1 MeV it gives ρ_spin/ρ_r ~ 10⁹–10¹¹ and is excluded by BBN; it also lies ~22 orders of magnitude above a primordial stiff fluid ending at t ~ 10⁻¹¹ s (Foundation II). Neither a rise-and-fall profile nor a distinct component is derived: **PO-ECF-BBN-SPIN stays open**. No numerical result changes.
- **References and external values checked at source (22/10/2026).** Twenty-two references corrected in the Extended version and seven in the PRD Short (e.g. Riess et al. ApJ Lett. 934, L7; Ivanov et al. PRD 102, 103502; DESI 2024 VI is JCAP 02 (2025) 021). The ECKS bounce no longer « introduces no NEC-violating field » (the spin–torsion term itself violates the energy condition); MICROSCOPE is quoted as a measurement compatible with zero; « decisive » becomes « very strong »; the globular-cluster age 13.32 Gyr is a lower bound on t₀; UHZ1 redshift z = 10.1 (spectroscopic); equivalence-principle rows state that no relation to s₀ is established.
- **Pages:** Extended 86, PRD Short 8.

The version register (§5, dated entries 20–24/10/2026) is the authority for each change; where this README and the register differ, the register and the PDF prevail.

---

## Key Results

Status labels follow the paper: `CALIBRATED` (fitted to data, not a prediction), `CALCULATED-CONDITIONAL` (conditional on a stated assumption), `HISTORICAL` (earlier value kept for traceability, not active), `OPEN`.

| Observable | Planck (ΛCDM) reference | ECF v8 | Status |
|---|---|---|---|
| **H₀** | 67.4 km/s/Mpc | **73.04 km/s/Mpc** (SH0ES) | CALIBRATED (through F_ion = 1.2765) |
| **r_s** | 147.1 Mpc (r_drag) | **135.65 Mpc** | CALIBRATED (sound-horizon reduction) |
| **Ω_m** | 0.315 | **0.267** (= ω_m/h², h = 0.7304) | internal closure (decision A-7) |
| **t₀** (w = −1 background) | 13.8 Gyr | **13.33 Gyr** | compatibility check against t_GC = 13.32 ± 0.10 (stat) ± 0.5 (sys) Gyr (Valcin et al. 2020) |
| **S₈** | 0.832 (Planck background) | 0.766 = KiDS-1000 3×2pt **target**, not an ECF output; CAMB ΛCDM reference on the closure background 0.780 | ECF growth prediction OPEN |
| **χ²_BAO** (4 bins, diagonal) | 1.79 | **12.11** (Δχ²_BAO ≃ +10.3 against the ECF) | CALCULATED-CONDITIONAL (PO-ECF-BAO-RDRAG) |
| **Global Δχ²** | — | −39.5 | HISTORICAL (Ω_m = 0.315), not recomputed |
| **β** birefringence | 0° | β ≠ 0; magnitude **0.35°** | magnitude CALIBRATED on the Minami–Komatsu anchor (0.35° ± 0.14°) |
| **w₀ / w_a** | −1 / 0 | **−0.904 / −0.153** | CALIBRATED point, no error bar (see below) |
| **ρ_c** (Cartan/Planck density) | — | **5.15×10⁹⁶ kg m⁻³** | reference scale |

> **Where the tension now lies.** With Ω_m = ω_m/h² = 0.267 the age tension
> reported in earlier versions does not arise. The difficulty is displaced to
> the late-time distance sector: the four BOSS/eBOSS BAO bins give
> χ²_BAO = 12.11 against 1.79 for ΛCDM, and the calibrated (w₀, w_a)
> trajectory gives χ² = 55.3 on a ten-observable subset of DESI DR1 with
> diagonal errors (13.7 with the former Ω_m = 0.315). The 55.3 is **not** the
> global DESI DR1 χ².

### Non-singular bounce

```
H² = (8πG/3)(ρ_r + ρ_m + ρ_Λ − ρ_spin)
H = 0  ⟺  ρ_spin(a_min) = ρ_r + ρ_m + ρ_Λ
```

- `ρ_spin ∝ a⁻⁶` overtakes `ρ_r ∝ a⁻⁴` as `a→0`, so the bounce condition has a
  solution at finite `a_min` in this two-term equation.
- **Status of the single-density form.** The schematic equation
  `H² = (8πG/3) ρ (1 − ρ/ρ_c)` (Appendix H) is exact for non-relativistic
  fermionic matter in the spin-fluid description (n ∝ a⁻³); for other
  equations of state the spin term scales as ρ^(2/(1+w)) and the form is a
  schematic extrapolation, in particular in the stiff phase (w = 1). Popławski's
  Eq. (12) corresponds to the Dirac description, in which dust does not
  bounce; the ECF uses the spin-fluid branch. Whether the spin term alone
  produces a bounce in the stiff phase is **OPEN** (`PO-ECF-ACTION-BOUNCE`).
- **Inhomogeneities.** Popławski (2010, 2012) work in FLRW, where homogeneity
  is assumed. The locality argument for robustness against spin
  inhomogeneities is the author's; that the bounce is a generic attractor
  **remains to be demonstrated** in an inhomogeneous setting.
- Weak-field decoupling: the a⁻⁶ dilution brings the spin-to-radiation ratio
  from 9.3% at z_ref = 5600 to 0.36% at recombination; the residual
  torsion-induced Lense-Thirring rate today is ≲ 10⁻²⁰ of the GP-B value.
- Physical origin: fermion spin density at the QCD confinement transition
  (T ~ 200 MeV); **observationally calibrated separately** at the
  normalisation redshift **z_ref = 5600** — two different epochs, which must
  not be conflated. (Earlier versions quoted z ≈ 7500, a value used by no
  script; corrected in v6.)

### CMB peaks

- **Angular positions** (D_A/r_s): unchanged by construction
- **Peak heights** (Ω_b h²): not directly modified — an Einstein–Cartan
  perturbation (Boltzmann) solver is required for a full check; it does not
  yet exist. The Planck block, θ*, the global Δχ² and the global AIC/BIC have
  therefore **not been recomputed** on the Ω_m = 0.267 background.

### Status of (w₀, w_a) vs DESI

> **(w₀, w_a) = (−0.904, −0.153) is a CALIBRATED point.** It is the output of
> a χ² optimisation, a minimum rather than a posterior, and carries no error
> bar. w_a is set through ξ = 1.645, a parameter calibrated on the DESI
> preference used by the ECF; the pair is therefore neither independent of
> nor prior to DESI, and it is not an *ab initio* prediction (open problem
> PO-F1-B). A likelihood profile along the sound-horizon chain gives the
> frequentist intervals w₀ = −0.907 ± 0.004 and w_a = −0.153 ± 0.007
> (`profile_likelihood_calibrated.py`), quoted only so that comparisons can be
> read against a width.

**Full covariance matrix, 12 DESI DR1 observables (Adame et al. 2024):**

| Prior H₀ | DESI DR1 best-fit (w₀, w_a) | Mahalanobis distance |
|---|---|---|
| Planck (h=0.674) | ≈ (−0.45, −2.36) | **2.03σ — compatible at 2σ** |
| SH0ES (h=0.730) | ≈ (−1.02, −0.73) | **6.98σ — severe tension** |

The comparison is a consistency check of the calibrated point, not an
independent test. The SH0ES prior is itself in ~5σ tension with DESI+CMB, so
the SH0ES+DESI DR1 combination is not internally consistent to begin with.
The full covariance reveals a near-perfect degeneracy ρ(w₀,w_a) ≈ −0.99, to
which the ECF point lies perpendicular — hence the strong prior-sensitivity.
DESI DR2 (arXiv:2503.14738) reports w ≠ −1 at 3.1σ (BAO+CMB) and 2.8–4.2σ with
supernovae; a full-covariance DR2 re-analysis is deferred.

> **Open problem PO-F1-B.** A single-parameter torsion ansatz does not
> reproduce the pair: both CPL parameters depend on one coupling and no value
> gives (−0.904, −0.153). `calibrate_w0wa.py` provides a partial
> reconstruction: w₀ is numerically close to −1 + Ω_spin^peak = −0.907
> (0.3% on w₀), but since Ω_spin^peak is itself calibrated on r_s this is an
> **empirical identification**, not a derivation and not an independent test.
> w_a = −ξ·Ω_spin^peak with ξ ≈ 1.645, not derived from the ECKS action (it
> would follow only from the condensate dynamics ⟨δS²⟩(z), cf. Foundation II,
> PO-F2-4).

> **Phantom crossing.** The calibrated trajectory crosses the phantom divide at
> z = 1.684. A single canonical scalar cannot do so; modified-gravity sectors
> can; the mechanism licensing it here is not derived and is tracked as open.

> **Scope note — the H₀–Age–BAO problem.** Within the tanh family of
> late-time w(z) studied in the paper, no model satisfies the age and BAO
> constraints together (`plot_trilemma_irreducibility.py`, 2500-point scan).
> Once the CMB acoustic scale θ* is included, the problem becomes a
> **quadrilemma** (`joint_fit_trilemma.py`): age, BAO and θ* pull Ω_m in
> mutually incompatible directions. It remains open, tracked as **PO-F2-5** in
> Foundation II. A second problem is opened in this version: the BAO
> comparisons use r_s^ECF as the ruler of measurements published in units of
> r_drag without the relation having been established
> (**PO-ECF-BAO-RDRAG**, OPEN); every BAO result is CALCULATED-CONDITIONAL.

Independent MCMC script (full covariance matrix): `plot_ecf_desi_mcmc_v3_0.py`.

---

## What changed in this version (PREPRINT v8, October 2026)

This version propagates the decision to close the background on the physical
densities (Ω_i = ω_i/h², decision A-7 of the September 2026 audit) and the
October corrections. Every change is listed, with its reason, in the
**Version register and erratum** deposited in the same lot
(`VERSION_REGISTER_AND_ERRATUM_EN.md`, §3–§5); in case of discrepancy the text
of the paper prevails.

**Background and ages.**
- Ω_m of the ECF background: 0.315 → **0.267** (= ω_m/h², h = 0.7304); 0.315
  is kept only as the Planck reference. Radiation follows the same rule.
- t₀ (w = −1): 12.74 Gyr → **13.33 Gyr**, compatible with the globular-cluster
  age t_GC = 13.32 ± 0.10 (stat) ± 0.5 (sys) Gyr. This is a compatibility
  check, not a 0.1σ test. The age-tension narrative of earlier versions is
  **abandoned**; its significance is HISTORICAL. Citation corrected to
  Valcin et al. 2020 (JCAP 12 (2020) 002).
- Age at recombination (z* = 1089.9): **368.4 kyr** with the spin term (the
  background that yields r_s), against 371.3 kyr in ΛCDM. The former ECF value
  relied on Ω_m = 0.315; an intermediate 371.8 kyr omitted the spin term.
  `script_09_cosmic_ages.py` now has two branches, `with_spin` (the F1 value)
  and `without_spin`.
- Deceleration/acceleration transition recomputed on the Ω_m = 0.267
  background: z_t ≈ 0.76 (ECF) against ≈ 0.63 (ΛCDM/Planck)
  (`plot_deceleration_transition.py`).
- Global Δχ² = −39.5 and ΔAIC/ΔBIC: now **HISTORICAL** (Ω_m = 0.315 branch),
  not recomputed — they depend on a perturbation solver that does not exist.
  **No global preference is claimed.**

**BAO and DESI.**
- BAO target at z = 1.48: **30.21 ± 0.79** (eBOSS DR16 QSO consensus,
  Hou et al. 2021); the former target, for which no source was found, is
  WITHDRAWN. Hou et al. 2021 is added to the PRD Short.
- BOSS DR12 errors corrected to **0.166 / 0.206 / 0.251** (statistical and
  systematic combined, Alam et al. 2017); the z = 0.61 error previously used
  was the statistical error alone (register §4).
- χ²_BAO (4 bins, diagonal): **12.11 against 1.79** (Δ ≃ +10.3); per bin
  4.060 / 3.161 / 2.749 / 2.137. The BAO sector is no longer near-neutral.
- Mahalanobis distance to DESI DR1: **2.03σ (Planck prior) / 6.98σ (SH0ES
  prior)**, full covariance, 12 observables. The previously quoted
  2.22σ / 7.32σ came from a 13-observable block including two QSO rows that
  DESI DR1 does not publish; the figures already showed 2.03 / 6.98
  (register §3.2, §4).
- DESI χ² = 55.3 qualified as a ten-observable subset with diagonal errors,
  not the global DESI DR1 χ².
- New open problem `PO-ECF-BAO-RDRAG`: r_s is no longer identified with r_drag.

**Dark energy and growth.**
- (w₀, w_a) = (−0.904, −0.153): CALIBRATED, a point without error bar; the
  profile intervals are distinguished from it. ξ = 1.645 is calibrated on the
  DESI preference, hence not independent of DESI.
- "What is derivable" box rewritten: w₀ ≃ −1 + Ω_spin^peak is an empirical
  identification, not a derivation.
- S₈ = 0.766 is the KiDS-1000 target, not an ECF output; S₈^ref = 0.780 is a
  conditional CAMB ΛCDM reference on the closure background; the ECF growth
  prediction is OPEN.
- γ_spin = 0.3116 (+0.073 / −0.100) retained as a HISTORICAL calibration
  (`gamma_spin_calibration.py`); conditional reference 0.066 (+0.069 / −0.094);
  physical value OPEN.

**Bounce equations.** The single-density form H² = (8πG/3) ρ (1 − ρ/ρ_c) is
stated as exact for fermionic dust in the spin-fluid description and schematic
elsewhere; Popławski's Eq. (12) is qualified (Dirac description); the titles of
the Popławski 2012 references are corrected. Bounce in the stiff phase:
`PO-ECF-ACTION-BOUNCE`, OPEN. Symbolic check of the per-regime equations:
`check_regimes.py`.

**Instruments.** DOE/NSF support for CMB-S4 is stated as ended (July 2025); its forecasts are kept
only as lapsed forecasts.

**Internal consistency (register § 5).** The bounce time is ~10⁻⁴⁴ s (the
10⁻⁴¹ s of earlier versions, withdrawn in Foundation II, is corrected in the
global-history caption, the milestone table and `plot_global_history.py`).

---

## Installation

```bash
git clone https://github.com/pfichant/spin-torsion-cosmology.git
cd spin-torsion-cosmology
pip install numpy scipy matplotlib     # core dependencies stated in the paper
pip install sympy camb                 # only for check_regimes.py and calc_S8_reference_camb_A7.py
```

A `requirements.txt` is provided in `Foundation_1/`.

## Scope of this deposit

The scripts listed below produce or check the results of the paper:
22 calculations, 26 figure scripts and the orchestrator. Five superseded
figure scripts are kept in `Scripts_SUPERSEDED/` for traceability.

The working corpus also holds internal tools (LaTeX consistency checks,
caption auditing, cross-document value tracking, session bookkeeping). They
operate on the whole multi-paper corpus rather than on Foundation I alone,
would fail in isolation, and are not part of what this paper claims. They are
deliberately excluded.

**One limitation, as stated in the paper.** The repository contains the
scripts that *reproduce* the published values, not those that *produced*
them: the parameter search that yielded F_ion = 1.2765, the global χ²
optimisation, and the calibration of A_sup and k_cut are not part of the
deposit. Each published number can be checked for internal consistency, but
the calibration itself is not re-executable from the repository.

## Scripts — what each one produces

**22 calculations** (`02_Scientific_Code/A_Core_Calculations/`) plus the
orchestrator at the root, and **26 figure scripts**
(`02_Scientific_Code/B_Paper_Plots/`).

### Calculations

| Script | Produces |
|---|---|
| `script_01_solve_sound_horizon.py` | Sound horizon r_s = 135.65 Mpc, F_ion = 1.2765 (normalised at z_ref = 5600) |
| `script_02_statistical_validation.py` | Two-observable {H₀, S₈} χ² proxy, independent of `chi_carre.py` |
| `script_03_extract_physical_parameters.py` | r_s and the ρ_spin/ρ_r table (9.30% at z_ref = 5600; 0.36% at z = 1100) |
| `check_rs_spin_domain.py` | Domain of validity of the calibrated spin branch: r_s as a function of the redshift up to which the a⁻⁶ law holds (135.65 Mpc at 10⁶ … 144.6 Mpc at 6×10³), ρ_spin/ρ_r at T ~ 1 MeV, comparison with the primordial stiff fluid — **new, 23/10/2026** |
| `script_04_halo_abundance.py` | High-redshift halo abundance (Ω_m ≃ 0.267); no longer used by the paper, Appendix E withdrawn (17/10/2026) |
| `script_05_birefringence_calibration.py` | Calibrates β_ECF = 0.35° |
| `script_06_S8_resolution.py` | S₈^ECF = 0.766 by construction from the HISTORICAL γ_spin = 0.3116 (not active under the internal closure) |
| `script_07_cartan_threshold.py` | Cartan threshold: where spin density equals radiation density |
| `script_09_cosmic_ages.py` | Cosmic ages t(z), ΛCDM vs ECF, branches `with_spin` (F1 value, 368.4 kyr at z*) and `without_spin` (371.8 kyr) — **updated in v8** |
| `chi_carre.py` | Partial χ² over the 6 tension-sector points (H₀ + S₈ + 4 BAO); corrected BOSS DR12 errors and eBOSS target 30.21 ± 0.79 — **updated in v8** |
| `target_reference_budget.py` | Reconstruction of the χ² budget table and ΔAIC/ΔBIC (HISTORICAL, Ω_m = 0.315) |
| `calibrate_w0wa.py` | Partial reconstruction of (w₀, w_a); DESI DR1 ten-observable subset χ² |
| `joint_fit_trilemma.py` | Joint (Ω_m, w₀, w_a) rescan vs BAO + age + θ* |
| `check_trilemma_optimizer.py` | Numerical diagnostic of the H₀–age–BAO irreducibility |
| `profile_likelihood_calibrated.py` | Profile intervals on the calibrated values |
| `compute_fsigma8_ecf.py` | Linear growth equation, f·σ₈ |
| `compare_fsigma8_data.py` | The same against published RSD measurements |
| `check_S8_effective.py` | Back-verification of the HISTORICAL γ_spin calibration |
| `check_beta_birefringence.py` | The 1.6% agreement between k = β_obs/F_ion and k_ECKS (its Δχ² is NOT a fit quality) |
| `table_echelles_bounce.py` | Characteristic scales of the bounce (a_min ~ 10⁻³²) |
| `gamma_spin_calibration.py` | γ_spin and its interval by inversion of the S₈ target bounds — **new in v8** |
| `calc_S8_reference_camb_A7.py` | CAMB ΛCDM S₈ reference on the closure background and the conditional γ_spin (CALCULATED-CONDITIONAL) — **new in v8** |
| `check_regimes.py` | Symbolic check (sympy) of the per-regime Einstein–Cartan Friedmann/Raychaudhuri equations; stiff case has no H = 0 — **new in v8** |
| `scan_F_ion_H0_BAO.py` | F_ion scan on the active background, H₀ + 4 BAO bins: joint compromise F_ion ≃ 1.22 (H₀ ≃ 71.8, Ω_m ≃ 0.276), calibrated point Δχ² ≃ 1.6 above it (CALCULATED-CONDITIONAL: linear H₀(F_ion), no CMB block, r_drag = r_s); F_ion stays calibrated on H₀ — **new in v8** |

### Orchestrator

`run_all_simulations_F1.py` sits at the **root of the archive**, alongside
`02_Scientific_Code/` — not inside it. It walks both subfolders, runs every
script in its own directory, and collects the figures into `figures_output/`.

### Figures

| Script | Figure |
|---|---|
| `plot_21cm_prediction.py` | Figure_21cm_ECF_Prediction.png |
| `plot_BAO_HighVisibility.py` | Figure_BAO_HighVisibility.png |
| `plot_Cosmic_History_Omegas.py` | Figure_CosmicHistory_Omegas_F1.png, Figure_CosmicHistory_Omegas_PIT.png |
| `plot_Fig_k3_Residuals_Angles.py` | Figure_K3_Residuals_Angles.png |
| `plot_Figure_K1_Global_Consistency.py` | Figure_K1_Global_Consistency.png |
| `plot_cosmic_age_cpl.py` | Fig_ECF_Cosmic_Age.png |
| `plot_deceleration_transition.py` | figure_deceleration_transition.png — **recomputed in v8** (Ω_m = 0.267) |
| `plot_density_bounce_comparison.py` | figure_density_bounce_comparison.png |
| `plot_desi_prediction.py` | Figure_DESI_Prediction.png |
| `plot_ecf_desi_mcmc_v3_0.py` | Fig_ECF_DESI_Residuals.png, Fig_ECF_DESI_Contours.png |
| `plot_ecf_gw_spectrum.py` | figure_ecf_gw_spectrum.png |
| `plot_euclid_pk_S8.py` | Figure_Euclid_Pk_S8.png |
| `plot_friedmann_evolution.py` | Figure_Friedmann_Evolution.png |
| `plot_global_history.py` | Figure_global_history.png |
| `plot_h0_s8_active.py` | Figure_H0_S8_Active.png — **new in v8** (H₀–S₈ plane on the active background Ω_m = 0.267; ECF S₈ OPEN) |
| `plot_jwst_comparison.py` | Figure_JWST_ECF_comparison.png (figure withdrawn, 17/10/2026) |
| `plot_planck_tt_residuals_ecf.py` | planck_tt_residuals_ecf.png |
| `plot_predict_birefringence.py` | Figure_Birefringence_Prediction.png |
| `plot_primordial_boost.py` | figure_primordial_boost.png |
| `plot_quadrilemma_omega_m.py` | fig_quadrilemma_omega_m.png |
| `plot_singularity_Resolution.py` | Figure_Singularity_Resolution.png |
| `plot_spin_ratio_evolution.py` | Figure_spin_ratio_evolution.png |
| `plot_structure_zoom.py` | Figure_Structure_Zoom.png |
| `plot_torsion_geometry_schema.py` | figure_torsion_geometry_schema.png |
| `plot_trilemma_irreducibility.py` | fig_trilemma_irreducibility_contours.png |

⚠️ Five scripts that produce no figure used by the paper live in
`Scripts_SUPERSEDED/`, outside the pipeline. They are kept because two of
them document a real defect in their own header: they wrote files that
another script also wrote, so whichever ran last silently overwrote the
other. Removing them would erase that record.

---

## Reproducibility

```bash
# All figures (orchestrator). Full run last verified 14/09/2026 (46/46 scripts,
# 0 failures) on the previous version; not re-verified for v8.
python Foundation_1/run_all_simulations_F1.py

# Cosmic ages: reproduces every row of the "Comparison of timescales" table.
# Validates itself against Planck (371 kyr at z* = 1089.9, ~372 published),
# then prints both ECF branches: with_spin 368.4 kyr (the F1 value),
# without_spin 371.8 kyr; t0 = 13.33 Gyr.
python Foundation_1/02_Scientific_Code/A_Core_Calculations/script_09_cosmic_ages.py

# Partial χ² (6 tension-sector points: H₀ + S₈ + 4 BAO)
# At Ω_m = 0.267: ECF 12.11 vs ΛCDM 43.26; χ²_BAO 12.11 vs 1.79.
python Foundation_1/02_Scientific_Code/A_Core_Calculations/chi_carre.py

# γ_spin (HISTORICAL calibration) and its interval; CAMB S₈ reference
python Foundation_1/02_Scientific_Code/A_Core_Calculations/gamma_spin_calibration.py
python Foundation_1/02_Scientific_Code/A_Core_Calculations/calc_S8_reference_camb_A7.py

# Per-regime bounce equations (symbolic, requires sympy)
python Foundation_1/02_Scientific_Code/A_Core_Calculations/check_regimes.py

# Partial reconstruction of (w₀, w_a) — see PO-F1-B above
python Foundation_1/02_Scientific_Code/A_Core_Calculations/calibrate_w0wa.py

# Independent DESI DR1 MCMC, full covariance matrix (two H₀ priors)
python Foundation_1/02_Scientific_Code/B_Paper_Plots/plot_ecf_desi_mcmc_v3_0.py
# → Fig_ECF_DESI_Contours.png                (F1 Extended, main text)
# → Fig_ECF_DESI_Residuals.png               (Appendix K)

# Deceleration transition: z_t(ECF) ≈ 0.76, z_t(ΛCDM) ≈ 0.63
python Foundation_1/02_Scientific_Code/B_Paper_Plots/plot_deceleration_transition.py

# Joint (Ω_m, w0, wa) fit vs BAO+Age+theta_* (quadrilemma diagnostic)
python Foundation_1/02_Scientific_Code/A_Core_Calculations/joint_fit_trilemma.py
python Foundation_1/02_Scientific_Code/B_Paper_Plots/plot_quadrilemma_omega_m.py

# H0-Age-BAO irreducibility scan (2500-point grid, Sec. "Perspectives")
python Foundation_1/02_Scientific_Code/B_Paper_Plots/plot_trilemma_irreducibility.py
```

> **Script scope**: `chi_carre.py` covers the 6 tension-sector points only.
> The global Δχ² = −39.5 is HISTORICAL (Ω_m = 0.315); it required the
> complete Planck likelihood pipeline and has not been recomputed.

The LaTeX sources of the papers are not published in this repository; the PDFs in
`01_Paper_Publication/` are the files deposited on Zenodo.

---

## Repository Structure

```text
Foundation_1/
├── 01_Paper_Publication/
│   ├── fichant_ecf_F1_Extended_v13.pdf      ← 86 pp. (preprint v8)
│   └── fichant_ecf_F1_PRD_Short_v7_1.pdf    ← 8 pp. (companion PRD summary, preprint v8)
├── 02_Scientific_Code/
│   ├── A_Core_Calculations/                 ← 23 scripts
│   │   ├── calc_S8_reference_camb_A7.py     ← CAMB S₈ reference (new in v8)
│   │   ├── calibrate_w0wa.py                ← empirical identification of w₀; ξ calibrated (PO-F1-B)
│   │   ├── check_S8_effective.py
│   │   ├── check_beta_birefringence.py
│   │   ├── check_regimes.py                 ← per-regime bounce equations (new in v8)
│   │   ├── check_trilemma_optimizer.py
│   │   ├── chi_carre.py                     ← 6 tension-sector points, corrected BOSS errors
│   │   ├── compare_fsigma8_data.py          ← against published RSD
│   │   ├── compute_fsigma8_ecf.py           ← linear growth, f·σ₈
│   │   ├── gamma_spin_calibration.py        ← γ_spin, HISTORICAL (new in v8)
│   │   ├── joint_fit_trilemma.py            ← quadrilemma diagnostic
│   │   ├── profile_likelihood_calibrated.py ← profile intervals
│   │   ├── scan_F_ion_H0_BAO.py             ← H₀ + BAO compromise on F_ion (new in v8)
│   │   ├── script_01_solve_sound_horizon.py ← normalises at z_ref = 5600
│   │   ├── script_02_statistical_validation.py
│   │   ├── script_03_extract_physical_parameters.py
│   │   ├── script_04_halo_abundance.py
│   │   ├── script_05_birefringence_calibration.py
│   │   ├── script_06_S8_resolution.py
│   │   ├── script_07_cartan_threshold.py    ← spin density = radiation density
│   │   ├── script_09_cosmic_ages.py         ← with_spin / without_spin branches
│   │   ├── table_echelles_bounce.py
│   │   └── target_reference_budget.py
│   └── B_Paper_Plots/                       ← 25 scripts
│       ├── plot_21cm_prediction.py
│       ├── plot_BAO_HighVisibility.py
│       ├── plot_Cosmic_History_Omegas.py
│       ├── plot_cosmic_age_cpl.py
│       ├── plot_deceleration_transition.py  ← recomputed on Ω_m = 0.267
│       ├── plot_density_bounce_comparison.py
│       ├── plot_desi_prediction.py
│       ├── plot_ecf_desi_mcmc_v3_0.py       ← full covariance (2.03σ / 6.98σ)
│       ├── plot_ecf_gw_spectrum.py
│       ├── plot_euclid_pk_S8.py
│       ├── plot_Fig_k3_Residuals_Angles.py
│       ├── plot_Figure_K1_Global_Consistency.py
│       ├── plot_friedmann_evolution.py
│       ├── plot_global_history.py
│       ├── plot_h0_s8_active.py             ← active background (new in v8)
│       ├── plot_jwst_comparison.py
│       ├── plot_planck_tt_residuals_ecf.py
│       ├── plot_predict_birefringence.py
│       ├── plot_primordial_boost.py
│       ├── plot_quadrilemma_omega_m.py
│       ├── plot_singularity_Resolution.py
│       ├── plot_spin_ratio_evolution.py
│       ├── plot_structure_zoom.py
│       ├── plot_torsion_geometry_schema.py
│       └── plot_trilemma_irreducibility.py  ← 2500-point scan
├── Scripts_SUPERSEDED/                      ← withdrawn, kept for traceability
├── figures_output/
└── run_all_simulations_F1.py
```

> **On `Scripts_SUPERSEDED/`.** Seven scripts listed in earlier READMEs live
> here: `plot_S8_resolution.py`, `plot_appendix_K1K2_spectrum.py`,
> `plot_birefringence_future.py`, `plot_hubble_boost_ratio.py`,
> `plot_spectre_puissance.py`, and, since v8, `plot_h0_s8_contours.py` and
> `plot_Optimization_Intersection.py` (former Figs. 3 and 4, historical
> calibration γ_spin = 0.3116, Ω_m = 0.315; `verify_calibration()` still
> reproduces the historical Δχ² = −39.5). They are retained for traceability,
> **not run** by the orchestrator, and their physical interpretation is superseded.

---

## Falsifiable Predictions

| Observable | ECF | Falsified if | Instrument |
|---|---|---|---|
| Birefringence β | β ≠ 0 (magnitude 0.35° CALIBRATED) | β consistent with 0 at < 0.1° | LiteBIRD (launch JFY2036, to be confirmed) |
| r_s (21 cm acoustic scale) | 135.65 Mpc | > 145 Mpc | HERA/SKA |
| S₈ | 0.766 is a target, not an ECF prediction (CAMB ΛCDM reference on the closure background: 0.780); ECF growth prediction OPEN | > 0.82 | Euclid WL |
| t₀ (w = −1 ansatz) | 13.33 Gyr | a confirmed stellar age, or a ladder-independent t₀, significantly above 13.33 Gyr | JWST GC photometry |
| GW chiral asymmetry | Δχ_GW > 0 (sign non-zero; quantified in Foundation II) | Δχ_GW < 0.02 at 95% CL | LISA (2035) |
| GW spectral index | Ω_GW ∝ f¹ (PTA band) | Ω_GW ∝ f^(2/3) only ⇒ standard BBH | PTA |
| WEP violation η_ECF | ~10⁻¹⁵ | non-detection at η < 10⁻¹⁶ (falsifies at 3σ) | MICROSCOPE II |

> **Note:** t₀ = 13.33 Gyr is the age of this paper's w = −1 background at
> Ω_m = 0.267; it lies 0.01 Gyr above the globular-cluster chronometry. The
> comparison is a compatibility check, not a 0.1σ test. The exposed point is
> now the BAO/DESI distance sector, not the age. CMB-S4, once forecast for the
> damping-tail and birefringence tests, lost its DOE/NSF support in July 2025.

---

## Companion Papers

| Paper | DOI | Role |
|---|---|---|
| **PIT Letter** | [10.5281/zenodo.19798923](https://doi.org/10.5281/zenodo.19798923) | Topological Invariance Principle (exact spatial flatness) |
| **Foundation I** *(this)* | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | H₀–S₈–BAO |
| **Foundation II** | [10.5281/zenodo.20629237](https://doi.org/10.5281/zenodo.20629237) | Geometric dark sector |
| **Foundation III — Cosmological Physics** | [10.5281/zenodo.22359982](https://doi.org/10.5281/zenodo.22359982) | Electroweak, baryogenesis, Wheeler-DeWitt |
| **Corpus Architecture (French)** | [10.5281/zenodo.22778507](https://doi.org/10.5281/zenodo.22778507) | Map of the corpus; English version to be deposited separately |
| **Foundation III — Strong Gravity** | In preparation, not yet publicly deposited | Black holes, bounce cores, compact objects |
| **Chiral-bounce paper** | In preparation, not yet publicly deposited | Bounce as a chiral phase transition |

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| v1 (PREPRINT v1) | Mar 2026 | Initial: Δχ² = −39.5 (now HISTORICAL), H₀/S₈ |
| v2 (PREPRINT v2) | Apr 2026 | H₀–Age–BAO trilemma, DESI DR1 |
| v3 (PREPRINT v2) | May 2026 | H₀DN 6σ, Pantheon S₈, eBOSS fix |
| v3.1 (PREPRINT v2) | May 2026 | G_eff unification, AIC/BIC |
| v8 (PREPRINT v2) | May 2026 | Bounce explicit, DESI scope note |
| v9 (PREPRINT v2) | May 2026 | Popławski robustness |
| v10 (PREPRINT v3) | June 2026 | Weak-field decoupling quantified; CMB peak positions vs heights; birefringence; MCMC consistency check; 5 new figures |
| v10.1 (PREPRINT v4) | July 2026 | Editorial and correctness revision. ρ_c harmonised to 5.15×10⁹⁶ kg m⁻³. Nine inherited LaTeX defects repaired. QCD-epoch mislabel corrected. Trilemma footnote corrected: the 2500-point scan finds **zero viable points** (PO-F2-5). |
| v10.2 (PREPRINT v4) | 20 July 2026 | Quadrilemma refinement (θ* added). DESI MCMC rebuilt with the **full covariance matrix** (the distances then quoted were corrected in v8). |
| v10.2 (PREPRINT v5) | 7 Aug 2026 | **Appendix B correction (PO-F1-B).** (w₀,w_a) stated as **calibration outputs**, not an *ab initio* derivation. |
| v11 (PREPRINT v6) | September 2026 | Five corrections: spin-density sign calibrated, not derived (PO-F1-SIGMA0); anchor realigned to z_ref = 5600; appendix cross-references repaired; H_b clarified; Kopczyński attribution corrected. |
| v11 (PREPRINT v7) | 13–14 September 2026 | A DESI DR2 significance not present in the cited paper (which reports 3.1σ) removed; the recombination row recomputed at z* = 1089.9 with `script_09_cosmic_ages.py` (values since revised in v8); Popławski's FLRW analyses no longer credited with robustness against spin inhomogeneities; Kibble (1961) and Sciama (1964) cited separately; PO-F1-SSC opened on the spin supplementary condition; `Figure_H0_S8_Contours.png` legend realigned. |
| **v13 (PREPRINT v8)** | **October 2026** | **Internal closure Ω_m = ω_m/h² = 0.267 (A-7) propagated.** t₀ = 13.33 Gyr, compatible with globular clusters (age tension abandoned); t_rec = 368.4 kyr with the spin term; deceleration figure recomputed; global Δχ² HISTORICAL; BAO target 30.21 ± 0.79 and corrected BOSS errors, χ²_BAO 12.11 vs 1.79; Mahalanobis 2.03σ / 6.98σ (12 observables); (w₀,w_a) CALIBRATED without error bar; S₈ target, γ_spin HISTORICAL; bounce-equation status qualified; PO-ECF-BAO-RDRAG opened; H₀–S₈ figure redrawn on the active background (ECF S₈ OPEN); optimisation figure withdrawn and archived, replaced by the joint H₀ + BAO compromise (F_ion ≃ 1.22, CALCULATED-CONDITIONAL; F_ion unchanged). See the version register and erratum. |

---

## Citation

```bibtex
@misc{fichant2026foundation1,
  author    = {Fichant, Pascal},
  title     = {Foundation I: The Metric Universe --- Extended Version},
  year      = {2026},
  publisher = {Zenodo},
  version   = {PREPRINT v8},
  doi       = {10.5281/zenodo.19577447},
  note      = {Internal closure Omega_m = omega_m/h^2 = 0.267: t0 = 13.33 Gyr
               (w=-1), compatible with globular-cluster ages; the difficulty
               moves to the BAO/DESI distance sector (chi2_BAO 12.11 vs 1.79).
               (w0,wa)=(-0.904,-0.153) is a CALIBRATED point, not an ab initio
               derivation (open problem PO-F1-B); xi is calibrated on the
               DESI preference. Full-covariance MCMC on 12 DESI DR1
               observables: 2.03 sigma (Planck prior), 6.98 sigma (SH0ES
               prior). Global Delta chi2 = -39.5 is historical (Omega_m =
               0.315), not recomputed. S8 = 0.766 is a target, not an ECF
               output. H0-Age-BAO(-theta*) quadrilemma open (PO-F2-5);
               r_s/r_drag relation open (PO-ECF-BAO-RDRAG); stiff-phase bounce
               open (PO-ECF-ACTION-BOUNCE). Spin sector normalised at
               z_ref = 5600.}
}
```

**Contact**: p.fichant.research@gmail.com · CC-BY-4.0 · Montpellier, October 2026
