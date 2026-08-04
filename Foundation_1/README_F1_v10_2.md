# Foundation I: The Metric Universe 🌌
### A Geometric Einstein-Cartan-Kibble-Sciama Cosmology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19577447.svg)](https://doi.org/10.5281/zenodo.19577447)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**PREPRINT v4** (internal version 10.2) · 24 July 2026 · doi: [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447)

---

## Key Results

| Observable | Planck (ΛCDM) | ECF v10.2 |
|---|---|---|
| **H₀** | 67.4 km/s/Mpc | **73.04 km/s/Mpc** (SH0ES) |
| **S₈** | 0.832 | **0.766** (KiDS/DES) |
| **r_s** | 147.1 Mpc | **135.8 Mpc** |
| **Δχ²** | — | **−39.5** vs ΛCDM |
| **β** birefringence | 0° | **0.35°** (Planck PR4: 0.32° · ACT DR6: 0.215°) |
| **w₀ / w_a** | −1 / 0 | **−0.904 / −0.153** (a priori, see below) |
| **ρ_c** (Cartan/Planck density) | — | **5.15×10⁹⁶ kg m⁻³** (harmonised, v10.1) |

### Non-singular bounce (v10 — explicit in paper body)

```
H² = (8πG/3)(ρ_r + ρ_m + ρ_Λ − ρ_spin)
H = 0  ⟺  ρ_spin(a_min) = ρ_r + ρ_m + ρ_Λ
```

- `ρ_spin ∝ a⁻⁶` dominates `ρ_r ∝ a⁻⁴` as `a→0` → bounce **guaranteed**
- Robust against inhomogeneities: Poplawski (2010, 2012)
- Weak-field decoupling: `ρ_spin(z=0)/ρ_Λ ~ 10⁻²²` (Solar System intact)
- Physical origin: fermion spin density at the QCD confinement transition
  (T ~ 200 MeV); **observationally calibrated separately** at the
  acoustic-era reference redshift z≈7500 (T ~ 1.8 eV) — these are two
  different epochs and must not be conflated (v10.1 clarification, see
  Changelog).

### CMB peaks (v10 clarification)

- **Angular positions** (D_A/r_s): unchanged by construction
- **Peak heights** (Ω_b h²): not directly modified — CLASS-EC required for full check

### Status of (w₀, w_a) vs DESI

> **(w₀, w_a) = (−0.904, −0.153) is an a priori prediction** from the PIT
> calibration on SH0ES + Planck + BOSS DR12, not a fit to DESI data.

**Full covariance matrix (v3.0, current):**

| Prior H₀ | DESI DR1 best-fit (w₀, w_a) | Mahalanobis distance |
|---|---|---|
| Planck (h=0.674) | (−0.44, −2.43) | **2.22σ — compatible at 2σ** |
| SH0ES (h=0.730) | (−1.02, −0.78) | **7.32σ — severe tension** |

> **Update (20/07/2026):** an earlier diagonal-errors check reported 0.78σ
> (SH0ES) and 0.77σ (H₀DN), with a caveat that full covariance "may shift
> these values by 10-30%". That estimate is superseded: the full covariance
> matrix (Adame et al. 2024, intra-bin D_M-D_H correlations) shifts the SH0ES
> distance to **7.32σ** — an order of magnitude beyond the earlier estimate.
> H₀DN has not yet been re-run with full covariance and is not reported.
> The two priors give radically different CPL best-fits, reflecting the
> unresolved H₀ tension; the full covariance also reveals a near-perfect
> degeneracy ρ(w₀,w_a)≈−0.99, along which the ECF point sits perpendicular —
> explaining the strong prior-sensitivity. The SH0ES prior is itself in
> ~5σ tension with DESI+CMB, so the SH0ES+DESI combination is not
> internally consistent to begin with; the 7.32σ figure should be read
> in that light, not as an isolated failure of the ECF prediction.

> The 2.22σ distance under the Planck prior and the severe SH0ES tension both
> reflect the unresolved H₀ tension, not independently a failure of the ECF
> dark-energy prediction — see full discussion in the paper.

> **Scope note (v10.1):** this a priori consistency with DESI is a **BAO-sector**
> result only. It does **not** by itself resolve the separate $H_0$–Age–BAO
> trilemma discussed below — a systematic scan (`plot_trilemma_irreducibility.py`)
> finds **zero viable points out of 2500** in the scalar $w(z)$ family jointly
> satisfying the BAO and stellar-age constraints. Full resolution of the
> trilemma is an open problem, tracked as **PO-F2-5** in Foundation II.

> **Refinement (20/07/2026):** the 2500-point scan above fixed Ω_m=0.315
> (the Planck-h value) throughout, without recomputing it for H0=73.04. The
> physically consistent value is Ω_m≈0.268. Re-scanning (Ω_m, w₀, w_a) jointly
> shows the best compromise reaches t₀≈13.0-13.2 Gyr at Ω_m≈0.28-0.29 — closer
> to the 13.32 Gyr target than the original 12.74 Gyr, though not fully
> reaching it. Adding the CMB acoustic scale θ* reveals the trilemma is part
> of a **quadrilemma**: age, BAO, and θ* pull Ω_m in mutually incompatible
> directions. Precise quantification awaits a CLASS-EC calculation.

Independent MCMC script (full covariance matrix): `plot_ecf_desi_mcmc_v3_0.py`.

---

## Installation

```bash
git clone https://github.com/pfichant/spin-torsion-cosmology.git
cd spin-torsion-cosmology
pip install -r Foundation_1/requirements.txt
```

## Reproducibility

```bash
# All figures
python Foundation_1/run_all_simulations_F1.py

# Tension χ² (6 aggregated points: H₀ + S₈ + 4 BAO)
python Foundation_1/02_Scientific_Code/A_Core_Calculations/chi_carre.py

# Independent DESI DR1 MCMC, full covariance matrix (two H₀ priors: Planck, SH0ES)
python Foundation_1/02_Scientific_Code/B_Paper_Plots/plot_ecf_desi_mcmc_v3_0.py
# → Fig_ECF_DESI_Contours.png                (F1 Extended, main text)
# → Fig_ECF_DESI_Residuals.png               (Appendix K)

# Joint (Ω_m, w0, wa) fit vs BAO+Age+theta_* (quadrilemma diagnostic)
python Foundation_1/02_Scientific_Code/A_Core_Calculations/joint_fit_trilemma.py
python Foundation_1/02_Scientific_Code/B_Paper_Plots/plot_quadrilemma_omega_m.py

# H0-Age-BAO trilemma irreducibility scan (2500-point grid, Appendix L)
python Foundation_1/02_Scientific_Code/B_Paper_Plots/plot_trilemma_irreducibility.py
```

> **Script scope**: `chi_carre.py` covers 6 tension-sector points only.
> Full Δχ² = −39.5 requires the complete Planck likelihood pipeline.
> (w₀, w_a) are derived from the PIT — not fitted to DESI, and their
> DESI-consistency is independent of the (still open) H0-Age-BAO trilemma.

---

## Repository Structure

```text
Foundation_1/
├── 01_Paper_Publication/
│   ├── fichant_ecf_F1_Extended_v10_2.pdf   ← PDF only (source not distributed)
│   └── fichant_ecf_F1_PRD_Short_v6.pdf     ← NEW v6 (companion short PRD submission)
├── 02_Scientific_Code/
│   ├── A_Core_Calculations/
│   │   ├── check_S8_effective.py
│   │   ├── check_beta_birefringence.py
│   │   ├── check_trilemma_optimizer.py
│   │   ├── chi_carre.py                     ← 6 tension-sector points
│   │   ├── joint_fit_trilemma.py            ← NEW v10.2 (quadrilemma diagnostic)
│   │   ├── script_01_solve_sound_horizon.py
│   │   ├── script_02_statistical_validation.py
│   │   ├── script_03_extract_physical_parameters.py
│   │   ├── script_04_halo_abundance.py
│   │   ├── script_05_birefringence_calibration.py
│   │   ├── script_06_S8_resolution.py
│   │   ├── table_echelles_bounce.py
│   │   └── target_reference_budget.py
│   └── B_Paper_Plots/
│       ├── plot_21cm_prediction.py
│       ├── plot_appendix_K1K2_spectrum.py
│       ├── plot_BAO_HighVisibility.py
│       ├── plot_birefringence_future.py
│       ├── plot_Cosmic_History_Omegas.py
│       ├── plot_cosmic_age_cpl.py
│       ├── plot_deceleration_transition.py
│       ├── plot_density_bounce_comparison.py
│       ├── plot_desi_prediction.py
│       ├── plot_ecf_desi_mcmc_v3_0.py       ← v10.2 (full covariance, 2.22σ/7.32σ)
│       ├── plot_ecf_gw_spectrum.py
│       ├── plot_euclid_pk_S8.py
│       ├── plot_Fig_k3_Residuals_Angles.py
│       ├── plot_Figure_K1_Global_Consistency.py
│       ├── plot_friedmann_evolution.py
│       ├── plot_global_history.py
│       ├── plot_h0_s8_contours.py
│       ├── plot_hubble_boost_ratio.py
│       ├── plot_jwst_comparison.py
│       ├── plot_Optimization_Intersection.py
│       ├── plot_planck_tt_residuals_ecf.py
│       ├── plot_predict_birefringence.py
│       ├── plot_primordial_boost.py
│       ├── plot_quadrilemma_omega_m.py      ← NEW v10.2 (English labels)
│       ├── plot_S8_resolution.py
│       ├── plot_singularity_Resolution.py
│       ├── plot_spectre_puissance.py
│       ├── plot_spin_ratio_evolution.py
│       ├── plot_structure_zoom.py
│       ├── plot_torsion_geometry_schema.py
│       └── plot_trilemma_irreducibility.py  ← 2500-point scan (Appendix L)
├── figures_output/
├── run_all_simulations_F1.py
└── requirements.txt
```

---

## Falsifiable Predictions

| Observable | ECF | Falsified if | Instrument |
|---|---|---|---|
| Birefringence β | 0.35° | < 0.1° | LiteBIRD (2032) |
| r_s | 135.8 Mpc | > 145 Mpc | HERA/SKA |
| S₈ | 0.766 | > 0.82 | Euclid WL |
| t₀ (w=−1 ansatz) | 12.74 Gyr | GC age > 13.3 Gyr at H₀≈73 | JWST |
| GW chiral Π_GW | ≥ 0.20 | < 0.02 | LISA (2037) |

> **Note (v10.1):** $t_0=12.74$ Gyr is the strict prediction of this paper's
> $w=-1$ ansatz, and remains the best-supported value. No scalar $w(z)$
> extension found in this corpus reaches $t_0\geq13.32$ Gyr without an
> unacceptable BAO cost (see trilemma scope note above) — the age tension is
> an open problem, not one resolved by a dynamical dark-energy extension.

---

## Companion Papers

| Paper | DOI | Role |
|---|---|---|
| **PIT Letter** | [10.5281/zenodo.19798923](https://doi.org/10.5281/zenodo.19798923) | TIP gauge postulate |
| **Foundation I** *(this)* | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | H₀–S₈–BAO |
| **Foundation II** | [10.5281/zenodo.20629237](https://doi.org/10.5281/zenodo.20629237) | Geometric dark sector |
| **Foundation III (extended)** | In preparation (translation) | Strong gravity, wormhole, vacuum thermodynamics |
| **Chiral-bounce paper** | Zenodo (deposit pending) | Bounce as a chiral phase transition — LG mechanism + Cartan core |

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| v1 (PREPRINT v1) | Mar 2026 | Initial: Δχ²=−39.5, H₀/S₈ |
| v2 (PREPRINT v2) | Apr 2026 | H₀–Age–BAO trilemma, DESI DR1 |
| v3 (PREPRINT v2) | May 2026 | H₀DN 6σ, Pantos S₈, eBOSS fix |
| v3.1 (PREPRINT v2) | May 2026 | G_eff unification, AIC/BIC |
| v8 (PREPRINT v2) | May 2026 | Bounce explicit, DESI scope note |
| v9 (PREPRINT v2) | May 2026 | Poplawski robustness |
| v10 (PREPRINT v3) | June 2026 | ρ_spin(z=0)/ρ_Λ ~ 10⁻²²; CMB peak positions vs heights; birefringence Planck PR4 vs ACT DR6; DESI a priori scope note; MCMC consistency check (3 priors: Planck/SH0ES/H₀DN); 5 new figures; 6 new references |
| v10.1 (PREPRINT v4) | July 2026 | Editorial and correctness revision; headline numerical results unchanged (Δχ²=−39.5, H₀=73.04, r_s=135.8 Mpc). (1)~ρ_c harmonised to $5.15\times10^{96}\,{\rm kg\,m^{-3}}$ throughout (three occurrences previously rounded to 5.2, ~1% error), aligning with Foundation III and the chiral-bounce paper. (2)~Nine inherited LaTeX defects repaired (duplicate `\documentclass`, corrupted control character, undefined citation macros, malformed equation, missing TikZ library, unbalanced brace, misused list environment) — document now compiles with 0 errors (previously 16). (3)~"definitively rules out" softened to "strongly disfavours". (4)~**QCD-epoch mislabel corrected**: a passage paired the acoustic-era calibration redshift $z\approx7500$ with the QCD confinement temperature ($T\sim200$~MeV) as if they were the same epoch — they differ by ~8 orders of magnitude in redshift. Corrected to distinguish the spin fluid's physical origin (QCD transition) from its separate observational calibration point ($z\approx7500$). (5)~**Trilemma footnote corrected**: a footnote stated that the Foundation~II dynamical solution "removes th[e] BAO penalty entirely" and resolves the $H_0$–Age–BAO trilemma. A systematic 2500-point scan (`plot_trilemma_irreducibility.py`, Appendix~L) finds **zero viable points** satisfying both constraints simultaneously; the calibrated $(w_0,w_a)$ trajectory does not by itself resolve the trilemma. Reworded to state this honestly as an open problem (tracked as PO-F2-5 in Foundation~II), rather than as a result established by the present calibration. (6)~**Companion short PRD paper** (`fichant_ecf_F1_PRD_Short_v6.tex`) corrected in parallel, same day: one instance of Macro-Knot seed formation mislabelled "QCD transition scale," relabelled "Great Annihilation freeze-out" ($T\sim1$~MeV) — the short paper's own trilemma framing (§ High-Redshift Structure discussion) already stated the age tension as an open motivation rather than a resolved result, and needed no further change. |
| **v10.2** | **20 July 2026** | **Two further corrections, headline results still unchanged.** (7)~**Quadrilemma refinement**: the trilemma scan (item 5) fixed $\Omega_m=0.315$ (Planck-$h$) throughout without recomputing it for $H_0=73.04$; the physically consistent value from the fixed CMB density $\omega_m=0.1429$ is $\Omega_m\approx0.268$. Re-scanning $(\Omega_m,w_0,w_a)$ jointly reaches $t_0\approx13.0$–$13.2$~Gyr at $\Omega_m\approx0.28$–$0.29$ (closer to target, not fully there); adding the CMB acoustic scale $\theta_*$ reveals the trilemma is part of a **quadrilemma** (age, BAO, $\theta_*$ pull $\Omega_m$ in incompatible directions), precise quantification deferred to a CLASS-EC calculation. (8)~**DESI MCMC section rebuilt with the full covariance matrix**: the independent MCMC check previously used diagonal errors only ($d=0.78\sigma$ SH0ES, $0.77\sigma$ H$_0$DN), with a stated caveat that full covariance "may shift these values by 10–30\%." That estimate is superseded: the full published covariance matrix (Adame~et al.~2024, intra-bin $D_M$–$D_H$ correlations) shifts the SH0ES distance to $\mathbf{7.32\sigma}$ (Mahalanobis), an order of magnitude beyond the earlier estimate; Planck gives $2.22\sigma$. H$_0$DN has not yet been re-run with full covariance and is no longer reported as current. Text, both DESI figures, and Appendix~K rebuilt accordingly (script `plot_ecf_desi_mcmc_v3_0.py`, superseding `plot_ecf_desi_mcmc.py`); one unrelated pre-existing broken self-citation fixed in passing. |

---

## Citation

```bibtex
@misc{fichant2026foundation1,
  author    = {Fichant, Pascal},
  title     = {Foundation I: The Metric Universe --- Extended Version},
  year      = {2026},
  publisher = {Zenodo},
  version   = {PREPRINT v4},
  doi       = {10.5281/zenodo.19577447},
  note      = {(w0,wa)=(-0.904,-0.153) derived prior to DESI from PIT;
               full-covariance MCMC gives 2.22 sigma (Planck prior) and
               7.32 sigma (SH0ES prior) Mahalanobis distance to DESI DR1;
               does not by itself resolve the H0-Age-BAO(-theta*)
               quadrilemma (open, see PO-F2-5 in Foundation II).
               Bounce generic: rho_spin ~ a^-6 dominates a^-4.
               rho_spin(z=0)/rho_Lambda ~ 1e-22 (Solar System intact).}
}
```

**Contact**: p.fichant.research@gmail.com · CC-BY-4.0 · Montpellier, 20 July 2026
