# Foundation I: The Metric Universe 🌌
### A Geometric Einstein-Cartan-Kibble-Sciama Cosmology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19577447.svg)](https://doi.org/10.5281/zenodo.19577447)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**PREPRINT v3** (internal version 10) · June 2026 · doi: [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447)

---

## Key Results

| Observable | Planck (ΛCDM) | ECF v10 |
|---|---|---|
| **H₀** | 67.4 km/s/Mpc | **73.04 km/s/Mpc** (SH0ES) |
| **S₈** | 0.832 | **0.766** (KiDS/DES) |
| **r_s** | 147.1 Mpc | **135.8 Mpc** |
| **Δχ²** | — | **−39.5** vs ΛCDM |
| **β** birefringence | 0° | **0.35°** (Planck PR4: 0.32° · ACT DR6: 0.215°) |
| **w₀ / w_a** | −1 / 0 | **−0.904 / −0.153** (a priori, see below) |

### Non-singular bounce (v10 — explicit in paper body)

```
H² = (8πG/3)(ρ_r + ρ_m + ρ_Λ − ρ_spin)
H = 0  ⟺  ρ_spin(a_min) = ρ_r + ρ_m + ρ_Λ
```

- `ρ_spin ∝ a⁻⁶` dominates `ρ_r ∝ a⁻⁴` as `a→0` → bounce **guaranteed**
- Robust against inhomogeneities: Poplawski (2010, 2012)
- Weak-field decoupling: `ρ_spin(z=0)/ρ_Λ ~ 10⁻²²` (Solar System intact)

### CMB peaks (v10 clarification)

- **Angular positions** (D_A/r_s): unchanged by construction
- **Peak heights** (Ω_b h²): not directly modified — CLASS-EC required for full check

### Status of (w₀, w_a) vs DESI

> **(w₀, w_a) = (−0.904, −0.153) is an a priori prediction** from the PIT
> calibration on SH0ES + Planck + BOSS DR12, not a fit to DESI data.

| Prior H₀ | DESI DR1 best-fit (w₀, w_a) | ECF distance |
|---|---|---|
| Planck (h=0.674) | (−0.41, −2.57) | 3.9σ |
| **SH0ES (h=0.730)** | **(−0.98, −0.99)** | **0.78σ — inside 1σ** |
| **H₀DN (h=0.735)** | **(−1.05, −0.70)** | **0.77σ — inside 1σ** |

> The 3.9σ distance under the Planck prior reflects the H₀ tension, not a failure
> of the ECF dark-energy prediction. With local H₀ priors, ECF lies within 1σ.

Independent MCMC script (diagonal errors, consistency check only): `plot_ecf_desi_mcmc_v3.py`.

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

# Independent DESI DR1 MCMC (three H₀ priors: Planck, SH0ES, H₀DN — ~8 min)
python Foundation_1/02_Scientific_Code/B_Paper_Plots/plot_ecf_desi_mcmc_v3.py
# → Fig_ecf_desi_mcmc_contours_planck.png   (F1 Extended subfig a)
# → Fig_ecf_desi_mcmc_contours_shoes.png    (F1 Extended subfig b + F1 Short)
# → Fig_ecf_desi_mcmc_contours_h0dn.png     (F1 Extended subfig c)
# → Fig_ecf_desi_mcmc_contours.png          (combined — GitHub/README)
# → Fig_ecf_desi_mcmc_residuals.png         (Appendix K)
```

> **Script scope**: `chi_carre.py` covers 6 tension-sector points only.
> Full Δχ² = −39.5 requires the complete Planck likelihood pipeline.
> (w₀, w_a) are derived from the PIT — not fitted to DESI.

---

## Repository Structure

```text
Foundation_1/
├── 01_Paper_Publication/
│   └── fichant_ecf_F1_Extended_v10.pdf   ← PDF only (source not distributed)
├── 02_Scientific_Code/
│   ├── A_Core_Calculations/
│   │   ├── chi_carre.py
│   │   ├── script_01_solve_sound_horizon.py
│   │   └── ecf_ode_solver.py
│   └── B_Paper_Plots/
│       ├── plot_trilemma_irreducibility.py
│       ├── plot_Cosmic_History_Omegas.py
│       ├── plot_sound_horizon.py
│       └── plot_ecf_desi_mcmc.py     ← NEW v10 (figure script, consistency check)
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

---

## Companion Papers

| Paper | DOI | Role |
|---|---|---|
| **PIT Letter** | [10.5281/zenodo.19900557](https://doi.org/10.5281/zenodo.19900557) | TIP gauge postulate |
| **Foundation I** *(this)* | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | H₀–S₈–BAO |
| **Foundation II** | [10.5281/zenodo.20629238](https://doi.org/10.5281/zenodo.20629238) | Geometric dark sector |
| **Foundation III** | In preparation | Strong-gravity sector, CLASS-EC |

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
| **v10 (PREPRINT v3)** | **June 2026** | **ρ_spin(z=0)/ρ_Λ ~ 10⁻²²; CMB peak positions vs heights; birefringence Planck PR4 vs ACT DR6; DESI a priori scope note; MCMC consistency check (3 priors: Planck/SH0ES/H₀DN); 5 new figures; 6 new references** |

---

## Citation

```bibtex
@misc{fichant2026foundation1,
  author    = {Fichant, Pascal},
  title     = {Foundation I: The Metric Universe --- Extended Version},
  year      = {2026},
  publisher = {Zenodo},
  version   = {PREPRINT v3},
  doi       = {10.5281/zenodo.19577447},
  note      = {(w0,wa)=(-0.904,-0.153) derived prior to DESI from PIT.
               Bounce generic: rho_spin ~ a^-6 dominates a^-4.
               rho_spin(z=0)/rho_Lambda ~ 1e-22 (Solar System intact).}
}
```

**Contact**: p.fichant.research@gmail.com · CC-BY-4.0 · Montpellier, June 2026
