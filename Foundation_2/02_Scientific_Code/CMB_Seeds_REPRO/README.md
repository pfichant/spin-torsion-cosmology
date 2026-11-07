# CMB imprint of ECF Macro-Knot seeds — reproduction package

Status: computed 16/10/2026. Part 2 (real Planck 2018 data) is reported in Foundation II v20, open problem PO-F2-SEED-CMB (Table 8, Fig. 35; added 17/10/2026). Part 1 is a forecast. Orders of magnitude; not calibrated on ECF quantities.

In the Foundation II code tree this folder is `Scripts_F2/CMB_Seeds_REPRO/` (kit: `Foundation_2/02_Scientific_Code/CMB_Seeds_REPRO/`).

## What it computes

Compact Macro-Knot seeds of 10⁵ M☉ that accrete gas from recombination onward. The accreted gas heats and ionises the medium, which changes the CMB. The package computes:

1. the ionisation history x_e(z) and the change in the CMB spectra (TT, EE);
2. 95 % upper bounds on the seed density n, for a Planck-like and an S4-like experiment, and with large-scale EE polarisation near cosmic variance;
3. two validations against published bounds.

Only the product n·f_eff enters, where f_eff is the fraction of the accretion luminosity deposited in the gas.

## Requirements

- Python 3.11 with numpy, scipy, matplotlib.
- CLASS 3.3.2 (`classy`) with the ECF patch:

```bash
bash class_patch/install_patched_class.sh [build_dir]
```

The script downloads `classy-3.3.2.0.tar.gz` from PyPI and checks its SHA-256 (`bad64cea…c5a291`). It applies `class_patch/injection_ecf.diff` and installs the package.

The patch adds three run-time switches to `injection_rate_PBH_accretion()` (`external/heating/injection.c`):

| Variable | Effect |
|---|---|
| `PBH_LMODE=edd` | L = L_Edd at all redshifts (Eddington benchmark, Serpico et al. 2020, Eq. 25) |
| `PBH_LMODE=cap` | L = min(L_recipe, L_Edd); the stock code has no Eddington cap |
| `PBH_ZCUT=z` | no injection below redshift z |

With the variables unset, CLASS behaves as the stock version.

## Run

```bash
python3 ecf_cmb_seeds.py validate   # ~3 min on 8 cores
python3 ecf_cmb_seeds.py bounds     # ~10 min
python3 ecf_cmb_seeds.py figure     # ~1 min -> Fig_CMB_ECF_seeds.png
python3 ecf_cmb_seeds.py all
```

Then compare with the reference run:

```bash
python3 check_reproduction.py        # every f_95 within 2 % of reference/results_cmb_seeds_REFERENCE.json
```

The reference was produced on 16/10/2026 from scratch: fresh virtual environment, patched CLASS installed by the script above, no cache. That run gave 20/20 bounds identical to the working computation, and the same figure file (md5 `8ad3a626`). The figure checksum may differ with another matplotlib version; the numbers should not.

The number of processes is set by `NPROC` (default 8). Results go to `results_cmb_seeds.json`. Fiducial derivatives are cached in `deriv_<background>.npz`; delete them to recompute.

## Method

| Item | Choice |
|---|---|
| Background | h = 0.7304, ω_b = 0.02237, ω_cdm = 0.1200 (ECF closure values; spin term not included); validations on the Planck 2018 background |
| Accretion | `edd`: L = L_Edd (Ricotti, Ostriker & Mack 2008 with a dark-matter halo give Eddington from z ~ 1000 at 10⁵ M☉); `disk`: Poulin et al. 2017, λ = 0.01, δ_ADAF = 10⁻³, capped; `sph`: Ali-Haïmoud & Kamionkowski 2017, capped |
| Not included | dark-matter halo around the seed, mass growth, energy-deposition functions (on-the-spot, f_eff = 0.1–1) |
| Likelihood | Gaussian in C_ℓ (TT, TE, EE). Planck-like: 5′, 33/56 µK·arcmin, f_sky = 0.6, ℓ = 30–2500. S4-like: 1.4′, 1/1.4 µK·arcmin, f_sky = 0.4, ℓ = 30–3000 |
| Parameters | linear marginalisation over ω_b, ω_cdm, H0, ln10¹⁰A_s, n_s, z_reio |
| Optical depth | Gaussian prior σ = 0.007 on the total τ (Planck 2018 lowE), or large-scale EE (ℓ = 2–29) with white noise tuned to a target σ(τ) |
| Bound | direct scan in f (the response is not linear in f); 95 % at Δχ² = 3.84 |

## Numerical controls

- Each CLASS run is in a fresh process. Repeated runs in one process were found to carry state.
- The reference is a run with the injection module switched on at f = 10⁻¹⁴. Switching the module on produces a small threshold artefact (Δχ² ≈ 0.03 Planck-like, ≈ 0.55 S4-like). That size sets the numerical floor of the Δχ² values.
- Results scale exactly as 1/f_eff.
- A cut at z = 30 leaves the bounds unchanged: the signal comes from z > 30.
- A first linear-Fisher version (derivative in f) was abandoned. The artefact above biased it.

## Validation

| Benchmark | Published | This code |
|---|---|---|
| Serpico et al. 2020, Eq. 25 (L = L_Edd) | f_95 = 2.9×10⁻⁹ | ≈ 4×10⁻⁹ (f_eff = 0.1) |
| Poulin et al. 2017, 100 M☉, disk, λ = 0.01 (fit Eq. 23) | f_95 = 1.9×10⁻³ | ≈ 3×10⁻³ (f_eff = 1) |

The two benchmarks match at different f_eff. The energy deposition is the main systematic uncertainty, a factor of about 10.

## References

- Ricotti, Ostriker & Mack 2008, ApJ 680, 829, arXiv:0709.0524
- Ali-Haïmoud & Kamionkowski 2017, PRD 95, 043534, arXiv:1612.05644
- Poulin, Serpico, Calore, Clesse & Kohri 2017, PRD 96, 083524, arXiv:1707.04206
- Serpico, Poulin, Inman & Kohri 2020, PRR 2, 023204, arXiv:2002.10771
- Stöcker, Krämer, Lesgourgues & Poulin 2018, JCAP 03, 018, arXiv:1801.01871 (ExoCLASS, DarkAges)
- Planck Collaboration 2020, A&A 641, A6 (VI), arXiv:1807.06209; A&A 641, A5 (V, likelihoods), arXiv:1907.12875
- Prince & Dunkley 2019, PRD 100, 083502, arXiv:1909.05869 (planck-lite-py)
- Bosman et al. 2022, MNRAS 514, 55, arXiv:2108.03699
- Lesgourgues 2011, arXiv:1104.2932 (CLASS)

## Part 2 — bounds from the real Planck 2018 data (`ecf_cmb_seeds_planck_data.py`)

Part 1 above is a forecast with simplified noise. Part 2 replaces it with real data and a computed energy deposition.

### Inputs

| Item | Source |
|---|---|
| High-ℓ likelihood | Planck 2018 plik_lite TT,TE,EE (ℓ ≥ 30), data and covariance as distributed with planck-lite-py (github.com/heatherprince/planck-lite-py, commit `2c0d0f67`). The Python implementation reproduces the reference value −291.33481235418 to 10⁻¹³. Calibration A_planck with prior 1 ± 0.0025. |
| Optical depth | Gaussian prior on the total τ: 0.0506 ± 0.0086 (Planck 2018 VI, Eq. 4, lowE alone) |
| Reionisation floor (option) | `ZREIO_MIN=6`: reionisation is over by z = 5.3 (Bosman et al. 2022, MNRAS 514, 55, arXiv:2108.03699) |
| Energy deposition | f_eff(z) from DarkAges 1.2.0 (commit `1994ea49`) for the accreting-PBH spectra (disk: Poulin et al. 2017; spherical: Ali-Haïmoud & Kamionkowski 2017), M = 10⁵ M☉, Planck background: `feff_disk_1e5_planckbg.dat`, `feff_sph_1e5_planckbg.dat`. Regenerate with `darkages_patch/make_feff.sh`; the patch is compatibility only (scipy, dill). The soft-spectrum case uses on-the-spot f_eff = 1. |
| Background | Planck 2018 best fit. The ECF closure background is not fitted by these data without the spin term; the injection signal changes by < 2 % between the two backgrounds (Part 1). |

### Method

Profile likelihood. For each f, χ² is minimised over ω_b, ω_cdm, H0, ln10¹⁰A_s, n_s, z_reio and A_planck:
- Gauss–Newton steps use a Jacobian computed at the f = 0 best fit;
- each step is a line search over full, half and quarter steps, checked by exact CLASS evaluations;
- Δχ² is taken from the exact values, against a reference with the module switched on at f = 10⁻¹⁴;
- the bound is at Δχ² = 3.84.

### Run

```bash
git clone https://github.com/heatherprince/planck-lite-py && (cd planck-lite-py && git checkout 2c0d0f67e59ce781654cf62dd7fb10757b0e60be)
ZREIO_MIN=6 python3 ecf_cmb_seeds_planck_data.py      # ~17 min on 8 cores -> results_planck_data_zreio6.json
python3 ecf_cmb_seeds_planck_data.py                  # without the floor -> results_planck_data.json
```

### Results (reference, 16/10/2026; 95 % upper bounds, seeds of 10⁵ M☉)

| Accretion and spectrum | f_95 | n_95 (Mpc⁻³) | z_reio at the bound |
|---|---|---|---|
| Eddington from z ~ 1000, hard spectrum (DarkAges) | 3.9×10⁻⁹ | 1.3×10⁻³ | 6.0 (floor) |
| Eddington from z ~ 1000, soft spectrum (f_eff = 1) | 6.8×10⁻¹⁰ | 2.3×10⁻⁴ | 6.0 (floor) |
| Disk recipe (Poulin), capped, DarkAges | 1.6×10⁻⁷ | 5.3×10⁻² | 6.6 (corrected 17/10/2026; was 7.7) |
| Spherical recipe (AHK), capped, DarkAges | 2.7×10⁻⁶ | 0.89 | 7.7 |

**Without the floor**, the soft-spectrum case is allowed up to f ≈ 8×10⁻¹⁰ (Δχ² = 0.8), but only with z_reio ≈ 1.7, which the quasar data exclude.
- The no-floor runs at f = 9×10⁻¹⁰ and 10⁻⁹ stayed in a local minimum at z_reio = 0.8 (Δχ² ≈ 26–29). The floored run gives Δχ² = 14 at 10⁻⁹, so those values are not global minima.
- The no-floor value is therefore given as a range (`reference/diag_soft_free_zreio.*`).
- The physical result is the floored one.

**Reproduction test (16/10/2026).** Part 2 was rerun from scratch: fresh virtual environment, patched CLASS, fresh planck-lite-py clone at the pinned commit, no cache. All Δχ² values came out identical to the reference (maximum difference 0), and so did the f = 0 best fit (χ² = 582.6442). `darkages_patch/make_feff.sh` was also rerun on a fresh DarkAges clone and gives the two f(z) files byte for byte. `check_reproduction.py` covers both parts (24/24).

### Figure of Foundation II (`fig_planck_data_bounds.py`, added 17/10/2026)

```bash
python3 fig_planck_data_bounds.py            # reads results_planck_data.json if present,
                                             # otherwise reference/results_planck_data_zreio6_REFERENCE.json
```

Output: `Fig_CMB_Seeds_PlanckData.png` (Foundation II, Fig. 35): profile Δχ² versus seed density n for the four regimes, with the Little Red Dot abundance (10⁻⁵–10⁻⁴ Mpc⁻³; Matthee et al. 2024, ApJ 963, 129; Kocevski et al. 2025, ApJ 986, 126) and the Foundation II abundance, a working assumption (one seed per halo above 10¹² M☉ to one per halo above 10¹¹ M☉: n ≈ 2×10⁻³–1.6×10⁻² Mpc⁻³; corrected 17/10/2026, was ten per halo above 10¹¹ M☉, Tinker et al. 2008 mass function at z = 0, σ₈ = 0.81 assumed). Run on the reference json, it gives `reference/Fig_CMB_Seeds_PlanckData.png`. In the GitHub kit the reference PNG files are not versioned (kit `.gitignore`); they are deposited with the paper.

**Agreement with Part 1.** The forecast bracket (f_eff = 0.1–1) contains every real-data bound: Eddington 4.5×10⁻⁹ to 4.2×10⁻¹⁰; disk 2.5×10⁻⁷ to 2.5×10⁻⁸; spherical 3.1×10⁻⁶ to 3.1×10⁻⁷.
