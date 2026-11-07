# Foundation II: The Chiral Universe 🌌
### Geometric Dark Sector, Baryogenesis & Cosmic Alignment in Einstein-Cartan Cosmology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20629237.svg)](https://doi.org/10.5281/zenodo.20629237)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Pascal Fichant** — Independent Researcher, Montpellier, Occitanie, France  
**PREPRINT v5** (internal revision 20) · October 2026 · 173 pages
> **Zenodo PREPRINT v5 (rev. 20)**: concept doi:[10.5281/zenodo.20629237](https://doi.org/10.5281/zenodo.20629237) (always resolves to the latest version)  
> **Deposited file**: `fichant_ecf_F2_Extended_v20.pdf` (173 pages since the corrections of 23/10/2026, see the version register; a PDF with a different page count is not the deposited file)  
> **Supersedes**: PREPRINT v4 (rev. 17, 15 September 2026)  
> **GitHub**: https://github.com/pfichant/spin-torsion-cosmology  
> **Companion document of this deposit**: *Version register and erratum* (October 2026) — the authoritative list of what changed since the online versions, and why. See "What changed in this version" below.
---

## Corrections made after the first drafting of this README (22–24 October 2026)

- **Pages: 173** (172 before the Macro-Knot paragraph of 23/10/2026).
- **Macro-Knot (23/10/2026).** The Hubble-sphere mass 1.4×10⁵ M☉ at T = 1.02 MeV is almost entirely radiation (ρ_m/ρ_r ≃ 7×10⁻⁷; ≃ 0.08 M☉ of dark matter and ≃ 0.015 M☉ of baryons per Hubble volume). A collapse of a knot fluid at the present dark-matter density would gather ~0.1 M☉; reaching 10⁵ M☉ would require the collapse of the radiation itself (δρ/ρ ≳ 0.45). The benchmark 10⁵ M☉ stays an adopted value; **composition and formation channel are open** (`PO-F2-MACRO-COMP`). The 4.6–5.6 orders of magnitude by which a spin term would lower M_K come from extrapolating the calibrated Foundation I branch to T ~ 1 MeV, which BBN excludes; the radiation-only values correspond to a spin term negligible there, which is not shown for the calibrated branch.
- **Limit of the calibrated spin branch (23/10/2026).** The calibrated sound horizon r_s = 135.65 Mpc (hence H₀ = 73.04 km/s/Mpc) requires the spin term (∝ a⁻⁶, ρ_spin = 0.093 ρ_r at z_ref = 5600) to hold up to z ~ 10⁵ (if it stops at 2×10⁴: r_s = 139.4 Mpc). Extended unchanged to T ~ 1 MeV it gives ρ_spin/ρ_r ~ 10⁹–10¹¹ and is excluded by BBN; it also lies ~22 orders of magnitude above a primordial stiff fluid ending at t ~ 10⁻¹¹ s (Foundation II). Neither a rise-and-fall profile nor a distinct component is derived: **PO-ECF-BBN-SPIN stays open**. No numerical result changes.
- **Lithium 7 (23/10/2026).** The earlier suggestion of an O(10 %) reduction through Ω_τ ≈ 0.093 « at freeze-out » is withdrawn: that value is the normalisation at z_ref = 5600, not a value at T ~ 0.1–1 MeV. **The work retains no mechanism that resolves the lithium problem**; the g*s correction and the late decay of topological defects are listed as unevaluated.
- **Little Red Dots (23/10/2026).** The ECF fixes no redshift, redshift window or number-density evolution for LRDs; the range z = 5–15 is removed (observed LRDs lie mostly at z ~ 4–9, confirmed up to z = 9.29). The LRD/seed figure is redrawn (measured black holes UHZ1, J1342+0928; MoM-z14 marked); at f_Edd = 1 the LRD mass range does not discriminate between a Macro-Knot seed and a stellar seed; the schematic Macro-Knot → LRD → SMBH figure is withdrawn.
- **References and external values (20–22/10/2026).** Fifty-six references corrected and some forty passages rewritten where a source did not say what was attributed to it (anisotropy bounds, DESI significance, Bullet Cluster 8σ, AGC 114905, Dragonfly 44, FRB periods, ...). The agreement of the condensate trajectory with DESI is a consistency check of a calibrated trajectory, not a prediction (w_a is set through ξ = 1.645, calibrated on the DESI preference). Torsion condensate and Lorentz violation: laboratory SME bounds give s₀ ≲ 3×10⁻²⁷ GeV, hence m_T ≳ 4×10³ GeV (`check_torsion_sme_bound.py`); the former illustrative s₀ is excluded by ~10¹⁵; the weak-equivalence relation b_e ≡ s₀/M_Pl is withdrawn. Circular polarisation Π_circ ~ 3×10⁻⁶ (an unreviewed order-of-magnitude estimate; the earlier value was ~4×10⁴ too large). Two figures corrected (GRB 221009A E_iso ≈ 1.2×10⁵⁵ erg; intergalactic magnetic-field range).

The version register (§5, dated entries 20–24/10/2026) is the authority for each change; where this README and the register differ, the register and the PDF prevail.

---

## Overview

**Foundation II** identifies and develops the three observable fossil signatures
of the primordial spin-torsion bounce, and investigates geometric explanations for the
cosmological dark sector — no new particles, no ad-hoc scalar fields. The background
it builds on (Foundation I) uses H₀ = 73.04 km/s/Mpc with Ω_m = ω_m/h² ≃ 0.267;
on that background t₀ ≃ 13.33 Gyr is compatible with the globular-cluster age
(13.32 Gyr, Valcin et al. 2020), and the active tension lies in the BAO distances
and in the DESI (w₀, wₐ) plane (open problem PO-F2-5).

### The Three Fossils

| Fossil | Epoch | Key result |
|---|---|---|
| **1. Chiral Baryogenesis** | t ~ 10⁻¹¹ s | η ≃ **5.9×10⁻¹⁰** *(semi-derived; pre-dilution asymmetry normalised on the observed value, so the 3.5% agreement with 6.1×10⁻¹⁰ is not an independent test)* · 5:1 ratio from 20:4 torsion DoF *(consistency result within the Weyssenhoff approximation)* |
| **2. Geometric Dark Matter** | t ~ 1 s | SPARC: χ̃²_med = 0.80 for the adopted pseudo-isothermal halo vs 1.29 for NFW refitted under the same protocol (171/175 gal., ν≥3 cut, 2 parameters per galaxy for both; profile not yet derived from torsion, PO-ECF-HALO) |
| **3. Cosmic Alignment** | t ~ 368,000 yr | Torsion Vortex Ring R = 322 Mpc (Big Ring + Giant Arc, exploratory consistency check) |

### Topological Zoology — Unified Dark Sector

| Dim | Defect | Homotopy | Role | Kill-switch |
|---|---|---|---|---|
| **0D** | Micro-Knot | π₂ | Granular DM, M = (3.74 ± 0.05)×10²⁴ kg, hedgehog | Roman τ ~ 5×10⁻⁸ (posited benchmark), t_E ≈ 1.05 h (individual) / ≈ 6.3 h (aggregate at λ = 36) |
| **0D** | Macro-Knot | π₂ | Hubble-sphere mass at the Great Annihilation, benchmark M ~ 10⁵ M☉ (**structural hypothesis**), LRD seeds | JWST LRD |
| **1D** | Torsion String | π₁ | ⚠️ **Status open (PO-F2-8)** — see note below | *no kill-switch claimed* |
| **2D** | Chiral Wall | π₀ | Void boundaries, β ≠ 0 achromatic (\|β\| ≈ 0.35° *calibrated*), Israel repulsion | LiteBIRD |
| **3D** | Torsion Fluid | none | DE condensate, f_fluid ~ 0.73, w(z) | DESI DR3 |

> ⚠️ **On the Micro-Knot → Macro-Knot chain (withdrawn, applied in this version).**
> Earlier versions posited a coagulation chain from Micro-Knots to Macro-Knots.
> That chain is **withdrawn**: Macro-Knots come from a distinct channel (the
> Hubble-sphere mass at the Great Annihilation), and their formation is a
> **structural hypothesis**. The value M_typ ≃ 6.8×10⁻⁵ M☉ (≈ 23 M⊕) is a
> **minimal benchmark** at the Subaru/HSC compatibility threshold λ = 36, not a
> dynamical ceiling. No quantitative chain links the two scales.

> ⚠️ **On the 1D sector (withdrawn 30/08/2026).** Torsion Strings **do not
> have an established Lagrangian foundation** in the present field content:
> S^μ is a *real* axial vector — it has an amplitude but no internal phase,
> whereas a genuine cosmic string (quantised winding, π₁ = ℤ) requires a
> *complex* order parameter.
>
> **The helical J₅ mechanism is withdrawn.** The LISA f ~ 50 mHz merger
> signature is *not* retracted but **reattributed** to Macro-Knot mergers,
> which need no quantised string. The 1D sector is carried as an open, named
> problem (**PO-F2-8**), not as an established prediction.
>
> The *observations* it was meant to explain — filament rotation
> (Wang+2021, Jung+2025) — are unaffected. Only the ECF's proposed
> explanation changed.

---

## New Observational Context (June 2026)

| Observation | Source | ECF interpretation |
|---|---|---|
| BH ≈ 2/3 of system mass at z ≃ 7.04 | Abell2744-QSO1, JWST (STScI release 2026-110, 27 May 2026) | Compatible with the Macro-Knot benchmark mass; formation not derived |
| Candidate Dark Galaxy-2, 4 GCs, L~10⁶ L☉ | Euclid+Hubble+Subaru 2026 | Sterile galaxy (4 ECF conditions) |
| Evolving DE 3.1σ (BAO+CMB), 2.8–4.2σ with SNe | DESI DR2, arXiv:2503.14738 | ECF (w₀,wₐ) is **calibrated** on the DESI preference (via ξ = 1.645): not an independent test |
| LPT ASKAP J1424, ~36 min period, highly polarised, no optical/NIR counterpart | Pritchard+2026 | Micro-Knot erosion candidate (exploratory) |
| QCD topological dark energy | Lee+2026 arXiv:2606.20036 | Parallel; ECF differs at EW scale |
| Filament rotation (vortical motion, stacked) | Wang+2021 (SDSS) | H1 observation stands ⚠️ *mechanism revised 30/08 — see note* |
| Halo spin ⊥ filament 2σ | Rong+2025 | H2: open, no ECF mechanism proposed; TTT provisional |
| 15 Mpc rotating filament z=0.032 | Jung+2025 | H1 observation, second case |

---

## The Einstein-Cartan Corpus

| Paper | DOI | Role |
|---|---|---|
| **PIT Letter** | [10.5281/zenodo.19798923](https://doi.org/10.5281/zenodo.19798923) | TIP flatness postulate (Ω_K ≡ 0); does **not** derive (w₀, wₐ), which are calibrated |
| **Foundation I** | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | Background calibration (F_ion, Ω_spin^peak, (w₀, wₐ)); identifies the H₀–Age–BAO problem without resolving it |
| **Foundation II** *(this)* | [10.5281/zenodo.20629237](https://doi.org/10.5281/zenodo.20629237) | Baryogenesis, geometric dark sector, cosmic alignment |
| **Foundation III — Cosmological Physics** | [10.5281/zenodo.22359982](https://doi.org/10.5281/zenodo.22359982) | Bounce signatures, void statistics, primordial spectrum status, DESI full-covariance comparison, falsifiable predictions |
| **Foundation III — Strong Gravity** *(companion)* | In preparation, not yet publicly deposited | Wormhole mechanism, Cartan core, vacuum thermodynamics |
| **Foundation III — Chiral Bounce** *(companion)* | In preparation, not yet publicly deposited | Bounce as a chiral phase transition — Landau-Ginzburg + Cartan core |
| **Foundation IV** *(exploratory)* | In preparation, not yet publicly deposited | Molecular-scale chirality |
| **Corpus Architecture (French)** | [10.5281/zenodo.22778507](https://doi.org/10.5281/zenodo.22778507) | Map of the corpus; the English version will be updated and deposited separately |

---

## Key Results (v20)

| Observable | ΛCDM | ECF | Free params |
|---|---|---|---|
| DM/baryon ratio | free | **5:1** (20/4 torsion DoF; consistency result, Weyssenhoff approximation) | 0 fitted |
| SPARC χ̃²_med (same protocol v1) | 1.29 (NFW refit) | **0.80** (171/175 gal., ν≥3 cut, median) | 2/galaxy |
| SPARC χ̃²_wt (weighted) | 6.74 (NFW refit) | 4.82 *(dominated by 14 outliers; the median is the quoted statistic)* | — |
| Baryon asymmetry η | free (observed 6.1×10⁻¹⁰, Planck-inferred) | **5.9×10⁻¹⁰** ⚠️ *semi-derived; not an independent test (see note)* | — |
| Micro-Knot mass | free | **(3.74 ± 0.05)×10²⁴ kg** (≈ 1.9×10⁻⁶ M☉ ≈ 0.6 M⊕), horizon mass c³/(2GH) at the EW crossing | 0 |
| β birefringence | 0° | **β ≠ 0, achromatic** — \|β\| ≈ 0.35° ⚠️ *calibrated on Planck PR4, not predicted* | 1 (g_CS) |
| w₀ / wₐ | −1 / 0 | **−0.904 / −0.153**, `CALIBRATED` (optimisation point, no error bar; wₐ via ξ = 1.645 calibrated on the DESI preference) | — |
| DESI DR1 (full covariance, 12 observables; Foundation III) | — | Mahalanobis distance **2.03σ** (Planck prior) / **6.98σ** (SH0ES prior); Δχ²(ECF − ΛCDM) = **+6.21 / +38.59** — the ECF is **not** favoured | — |
| BAO, 4 bins (BOSS DR12 + eBOSS DR16) | χ²_BAO = 1.79 | χ²_BAO = **12.11** (Δ ≃ +10.3), `CALCULATED-CONDITIONAL` on PO-ECF-BAO-RDRAG | — |
| WIMP-like flux at Earth | — | **~2.9×10⁻⁴¹ m⁻²s⁻¹** (sparse, aperiodic) | — |
| \|V/I\| annihilation | — | **~0.8** (Chern-Simons, POLAR-2) | — |

> ⚠️ **On predictions H1/H2 (corrected 15/09/2026).** Earlier versions listed
> **"filament rotation 3.3σ — ECF prediction H1 confirmed"**. Two problems:
>
> - the **3.3σ figure is sourced** (corrected 14/10/2026): it is given in the body
>   of Wang et al. 2021 (Fig. 3), for dynamically cold filaments nearly perpendicular
>   to the line of sight (4.2σ for the 10 % with the most massive end-point groups),
>   not in the abstract; the earlier note calling it untraceable was wrong. It measures
>   rotation, not the ECF mechanism;
> - **"confirmed" overstates the status**: the mechanism H1 rested on
>   (a helical J₅ carried by a 1D Torsion String) was **withdrawn on
>   30/08/2026**. H1 is now "revised — magnetic torque candidate, not yet
>   quantified"; H3 and H4 are **withdrawn** with no replacement.

> ⚠️ **On the baryon asymmetry.** Earlier versions of this README gave
> **η = 6.1×10⁻¹⁰ with "0 free parameters"**. That number is the **observed**
> value, inferred from Planck 2018 (Ω_b h² = 0.0224 via η ≃ 273.9 Ω_b h²).
>
> The ECF result is **η ≃ 5.9×10⁻¹⁰** (`derive_f_dilution_baryogenesis.py`).
> The paper calls it **semi-derived**: stage (i) follows from first principles,
> stage (iii) is semi-analytic, and the pre-dilution asymmetry (stage ii) is
> **normalised on the observed value** (η_raw = η_obs/0.50). The 3.5% offset
> therefore only reflects the ratio of the resolved to the historical dilution
> factor; it is **not an independent test**.

> ⚠️ **On birefringence (corrected 15/09/2026).** The paper states throughout:
> **β_ECF ≠ 0** (achromatic), *with the magnitude |β| ≈ 0.35° **calibrated***
> on the Planck 2018 value of Minami & Komatsu 2020 (0.35° ± 0.14°) through the Chern-Simons coupling g_CS *(corrected 15/10/2026: formerly “Planck PR4 (0.32° ± 0.12°)”; PR4 gives 0.30° ± 0.11°)*
> (`script_05_birefringence_calibration.py`, Foundation I).
> **The prediction is the sign and the achromaticity, not the number.**
> The LiteBIRD kill-switch (β < 0.1°) tests β ≠ 0, not the value 0.35°.

> **Statistics note:** χ̃²_med (median) and χ̃²_wt (weighted mean) describe the same distribution; the weighted mean is dominated by a handful of outliers (14 galaxies at χ̃² > 10 carry 64% of the weighted sum). The external values of Li et al. 2020 (NFW 1.55) were obtained under a different convention and are not directly comparable.

---

## Falsifiable Kill-Switches

*Scope (from the paper):* none of these thresholds refutes the framework as a whole; each row tests the sector or pre-specified template it depends on, through at least one link that is currently calibrated, phenomenological, conditional or open.

| Observable | ECF expectation | Kill-switch | Instrument & date |
|---|---|---|---|
| Void excess R>60 Mpc | 1+α_KZ ≃ 2.1 at the peak of the adopted template (ξ_KZ = 60 Mpc adopted, PO-F3-XI) | No excess at 2σ | **Euclid DR1 (complete) · mid-2027** ⚠️ *no significance quotable before a survey mock* |
| Sterile galaxy V/σ | < 0.1 | V/σ > 0.3 | **JWST · 2026** |
| S₈ | 0.766 is the KiDS-1000 **calibration target**, not an ECF prediction; CAMB ΛCDM reference on the closure background 0.780; ECF growth prediction **OPEN** | S₈ > 0.80 at 3σ (would refute the calibration) | **Euclid DR1 (complete) · mid-2027** |
| (w₀, wₐ) | (−0.904, −0.153), `CALIBRATED`, not independent of DESI | w = −1 at 5σ | DESI DR3 · 2027 |
| τ_micro | ~5×10⁻⁸ (posited benchmark), t_E ~ 1–10 h | No excess in the t_E 1–10 h window | Roman (launched 30/08/2026) · 2027–28 |
| EMF mass function | Poisson λ ≥ 36, M_typ ~ 6.8×10⁻⁵ M☉ | Monochromatic peak at M_MK | Roman · 2027–28 |
| Birefringence β | **β ≠ 0**, achromatic (magnitude calibrated) | β < 0.1° at 3σ | LiteBIRD · JFY2036 (to be confirmed) |
| Π_GW chiral | 0.20 ± 0.05, `CALIBRATED TEMPLATE` | Π_GW < 0.02 at 95% CL | LISA (launch ~2035) |
| Macro-Knot merger burst | f ~ 50 mHz stiff tail *(reattributed from the 1D sector to Macro-Knot mergers)* | QNM ring-down only, no tail | LISA (launch ~2035) |
| \|V/I\| annihilation | ~0.8 | \|V/I\| < 0.1 at 3σ | POLAR-2 · 2027 |
| ~~Filament spin sign~~ | ⚠️ **withdrawn as a test** — mechanism open (PO-F2-8); no ECF prediction attached | — | — |
| ~~No dangling filaments (H4)~~ | ⚠️ **withdrawn 30/08/2026** — required the unfounded 1D sector | — | — |

> ⚠️ **On Euclid dates.** ESA split Euclid DR1 in June 2026: DR1-Foundation
> (images and catalogues) in November 2026, and the complete DR1 — with the
> level-3 products on which clustering, weak lensing and void catalogues
> depend — in mid-2027. Both Euclid kill-switches are keyed to the later date.

### Detection Windows

| Window | Period | Instruments | Channels | Action |
|---|---|---|---|---|
| **I** | 2026–2027 | Fermi-LAT + Euclid DR1 (complete) | 2 | Archive cross-match + void catalogue ≤500 CPU-h |
| **II** | 2027–2032 | POLAR-2 + Roman + CTA | 3 | γ-flash + \|V/I\|≃0.8 + galactic quenching |
| **III** | late 2030s, subject to mission schedules | LISA + CTA + POLAR-2 successor + JWST/HWO | 4 | LISA alert → ToO <6 h → 4-channel coincidence |

---

## Open Problems (explicitly documented)

| # | Problem | Type | Next step |
|---|---|---|---|
| PO-F2-1 | Origin of ΔN topological surplus (link ΔN/η not established) | O | open |
| PO-F2-2 | Torsion String pitch λ_hel | O | requires cylindrical ECF field equations |
| PO-F2-3 | Chiral Wall network dilution (↔ PO-F3-XI) | O | wall network evolution not simulated |
| PO-F2-4 | f_fluid partition; ⟨δS²⟩(z) calibrated, not derived (fixes w₀, wₐ); CC reformulated, not solved | O | perturbative treatment |
| PO-F2-5 | H₀–Age–BAO(–θ*) problem (open, not resolved by the calibrated w₀, wₐ); after A-7 the tension lies in BAO/DESI, not in the age | O | open |
| **PO-F2-6** | Axial-sector spectrum (sub-problem of PO-ECF-ACTION) | O | open |
| **PO-F2-7** | Micro-Knot maximal angular momentum and formation dynamics (hedgehog → ring) | O | open |
| **PO-F2-8** | ⚠️ **1D Torsion Strings: no complex order parameter in the present Lagrangian** — the helical J₅ mechanism is withdrawn | O | phase field not identified |
| **PO-F2-9** | Non-collisional (deflection) detection channels for the Micro-Knot mesh | O | open |
| **PO-F2-SEED-CMB** | CMB bound on early accretion onto Macro-Knot seeds (Table 8, Fig. 35; added 17/10/2026): under Eddington-limited accretion from recombination the adopted abundance (a working assumption, 𝒪(1) per galactic volume) exceeds the Planck bound by ≈ 1.5–70; no constraint under less efficient early accretion (disk and spherical recipes) | O | conditional on the accretion regime before z ~ 100 |
| PO-ECF-HALO | Pseudo-isothermal halo profile adopted, not derived from torsion; no link between M_MK and (ρ₀, R_s) | O | open |
| PO-ECF-BAO-RDRAG | r_drag not identified with r_s; all BAO comparisons `CALCULATED-CONDITIONAL` | O | open |
| PO-ECF-ACTION-BOUNCE | In the stiff phase (w = 1) the spin term alone does not produce a bounce | O | open |
| — | Einstein–Cartan perturbation (Boltzmann) solver: G_eff(k), S₈, C_ℓ, w_a | D | not yet available |
| — | DESI full covariance | D | done in Foundation III — Cosmological Physics (12 observables) |

> D = deliberate scope decision · O = open physical problem

---

## Installation & Reproducibility

```bash
git clone https://github.com/pfichant/spin-torsion-cosmology.git
cd spin-torsion-cosmology/Foundation_2
# Python dependencies used by the scripts: numpy, scipy, matplotlib, pandas, sympy, emcee
# (plotly + kaleido optional: needs Chrome; the pipeline continues without it)

# Full pipeline, run from the package root: 111 scripts = 54 calculations + 57 figures
python run_all_simulations_F2.py

# NGC 6503 and SPARC protocol (new in v20; run separately)
python 02_Scientific_Code/mcmc_ngc6503_sparc.py            # deterministic emcee chain, 31 SPARC points
python 02_Scientific_Code/sparc_protocole_v1.py            # ECF vs NFW, protocol v1 (Table tab:sparc_global)
python 02_Scientific_Code/B_Paper_Plots/plot_MCMC_NGC6503.py   # Fig. 32, drawn from the chain above
(cd 02_Scientific_Code/data/sparc && md5sum -c MANIFESTE_SPARC.md5)   # SPARC data integrity

# Pedagogical animations (~3 min)
python 02_Scientific_Code/D_Simulations/plot_F2_animations_ECF.py

# CMB bound on Macro-Knot seeds (PO-F2-SEED-CMB, Table 8, Fig. 35; added 17/10/2026; run separately)
# needs CLASS 3.3.2 patched and planck-lite-py at a fixed commit: see 02_Scientific_Code/CMB_Seeds_REPRO/README.md
cd 02_Scientific_Code/CMB_Seeds_REPRO && ZREIO_MIN=6 python ecf_cmb_seeds_planck_data.py && python fig_planck_data_bounds.py
```

---

## Figures and scripts changed or added in v20

| Script | Output | Change |
|---|---|---|
| `CMB_Seeds_REPRO/ecf_cmb_seeds_planck_data.py`, `CMB_Seeds_REPRO/fig_planck_data_bounds.py` | `Fig_CMB_Seeds_PlanckData.png` (Fig. 35), Table 8 | New (17/10/2026): bounds on accreting 10⁵ M☉ seeds from the Planck 2018 data (PO-F2-SEED-CMB); reproduction package with its own README and SHA256SUMS |
| `mcmc_ngc6503_sparc.py` | `sorties/mcmc_ngc6503.json` | Real emcee chain on the SPARC NGC 6503 file (32 walkers, 6000 steps, 2000 burn-in, seed fixed before the sampler) |
| `sparc_protocole_v1.py` | `sorties/` | Single producer of the homogeneous ECF/NFW SPARC comparison (0.80 vs 1.29); reads `data/sparc/` (MD5 manifest) |
| `plot_MCMC_NGC6503.py` | `Fig_MCMC_NGC6503.png` (Fig. 32) | Now drawn from the real chain (previously a synthetic normal distribution) |
| `plot_rotation_ngc6503_ecf.py` | `Fig1_NGC6503_ECF_Rotation.png` (Fig. 26) | Redone on SPARC data (31 points), χ²_ν = 1.68 |
| `plot_void_statistics.py` | `Fig_Void_Statistics.png` (Fig. 15) | Now an illustrative mock slice only; no simulated points labelled as observations, no fit statistic |
| `plot_ecf_ratio.py` | `Fig_ECF_Ratio_Evolution.png` (Fig. 8) | Ratio ρ_τ/ρ_m on the A-7 background: crossing at z = 0.40 ± 0.02, 2.75 ± 0.11 at z = 0 |

## Figures added in PREPRINT v3 (June 2026)

| Script | Output | Physics |
|---|---|---|
| `plot_F2_magnetic_fields.py` | `Fig_Magnetic_Fields_ECF.png` | B(r) profiles for all 4 defect levels (dipolar/solenoidal/tangential/SCMB) |
| `plot_F2_vsf_prediction.py` | `Fig_VSF_ECF_Prediction.png` | VSF ECF vs ΛCDM, semi-quantitative template (kill-switch at Euclid DR1 complete, mid-2027) |
| `plot_F2_sparc_model_comparison.py` | `Fig_SPARC_Model_Comparison.png` | χ² CDF: ECF vs NFW/DC14/MOND on SPARC-175 (external values: Li et al. 2020, McGaugh et al. 2016) |
| `plot_F2_topological_network.py` | `Fig_ECF_Topological_Network.png` | Cosmic web as 4-level topological network + H1–H4 (H3, H4 since withdrawn) |
| `plot_F2_Roman_EMF_prediction.py` | `Fig6_Roman_PBH_Prediction.png` | Roman microlensing: Poisson EMF λ≥36, mass spectrum vs HSC, t_E distribution, event forecast |
| `plot_F2_zoologie_topologique.py` | `Fig_MicroKnot_0D.png`, `Fig_MacroKnot_1D_Wake.png`, `Fig_DomainWall_2D.png`, `Fig_ChiralFluid_3D.png`, `Fig_ECF_Topological_Architecture.png` | Family of Knots |

## Pedagogical Animations

Script: `Foundation_2/02_Scientific_Code/D_Simulations/plot_F2_animations_ECF.py`. Blender scenes (Blender ≥ 4.2): `D_Simulations/blender/plot_ecf_blender_simulation_knot_constructive_v34fix.py` (V34-FIX) and `D_Simulations/blender/plot_ecf_blender_simulation_GRB2025-2_v40fix.py` (V40.1-FIX). Illustrative material, not producers of numerical results.

| File | Physics |
|---|---|
| `Anim_ECF_0D_MicroKnot.gif` | Lensing, hedgehog field, halo, Kerr toroidal geometry |
| `Anim_ECF_1D_TorsionString.gif` | Conical deficit, velocity kick δv, baryonic wake *(1D sector open, PO-F2-8)* |
| `Anim_ECF_2D_ChiralWall.gif` | Israel repulsion, void formation, β ≠ 0 birefringence |
| `Anim_ECF_3D_TorsionFluid.gif` | Back-reaction DM↔DE, w(z), DESI comparison |

80 frames · 18 FPS · white background · English labels

---

## Canonical Parameters

| Parameter | Value | Status / Origin |
|---|---|---|
| κ² | 2.0766×10⁻⁴³ m/J | CODATA 2018 |
| H₀ (ECF background) | 73.04 km/s/Mpc (h = 0.7304) | Foundation I calibration; H₀DN 73.50 ± 0.81 (arXiv:2510.23823) quoted as observational context |
| Ω_m | ω_m/h² ≃ 0.267 | closure of the A-7 background (0.315 = Planck value, historical reference only) |
| t₀ (w = −1) | 13.33 Gyr | compatibility check against t_GC = 13.32 ± 0.10 (stat) ± 0.5 (syst) Gyr (Valcin et al. 2020), not a 0.1σ test |
| (w₀, wₐ) | (−0.904, −0.153) | `CALIBRATED` (Foundation I), optimisation point without error bar; ξ = 1.645 calibrated on the DESI preference |
| F_ion | 1.2765 ± 0.015 | F1 MCMC |
| Ω_spin^peak | 0.093 ± 0.004 | `CALIBRATED` (Foundation I) |
| r_s (ECF) | 135.65 Mpc | Sound-horizon target of the Foundation I calibration |
| t_rec (ECF, z* = 1089.9) | 368.4 kyr (with spin term) vs 371.3 kyr ΛCDM | `script_09_cosmic_ages.py` (Foundation I), branch `with_spin`; not an observable |
| M_MK | (3.74 ± 0.05)×10²⁴ kg ≈ 1.9×10⁻⁶ M☉ | Horizon mass at the EW crossing (T_c ≃ 159 GeV) |
| ξ_KZ | 60 Mpc (adopted within 50–80 Mpc) | Adopted value, not derived ab initio (PO-F3-XI) |
| β_ECF | \|β\| ≈ 0.35° ⚠️ **calibrated**, not derived | Chern-Simons coupling g_CS calibrated on Minami & Komatsu 2020 (0.35° ± 0.14°) |
| η_baryon (ECF) | **5.9×10⁻¹⁰** | ⚠️ *semi-derived*, normalised on the observed 6.1×10⁻¹⁰ (Planck 2018, via η ≃ 273.9 Ω_b h²) |
| S₈ | 0.766 = KiDS-1000 target; 0.780 = conditional CAMB reference | ECF growth prediction `OPEN` (no perturbative chain) |

---

## Terminology Discipline

| ✗ Avoid | ✓ Use |
|---|---|
| "fractal" | "hierarchical" |
| "Domain Wall" | "Chiral Wall" |
| "Macro-Knot strings" | "Torsion String" |
| "3D chiral fluid" | "3D Torsion Fluid" |
| "predicts" for a calibrated quantity | "calibrated" |

---

## What changed in this version (PREPRINT v5, rev. 20, October 2026)

This version propagates the decisions of the second audit (September 2026)
and the October corrections. The complete list, with the reason for each
change, is in the **Version register and erratum** deposited with this lot
(October 2026); in case of discrepancy, the text of the paper prevails.
No open problem is closed by rewording.

### Corrections explicitly signalled (data and figures of v4)

1. **Void-statistics figure (`Fig_Void_Statistics`, Fig. 15).** In v4 the
   points labelled "Observations (SDSS BOSS Catalog)" were **simulated**
   (analytic curve plus noise, fixed seed), and the "Fit Statistics" box
   (χ²_ν = 1.14 / 4.82) was hard-coded in the script. The figure is replaced
   by an illustrative mock slice; no simulated data are presented as observations.
2. **NGC 6503 data.** v4 used a data file (`Data_S1_NGC6503_ECF.csv`, 24
   points) that does not match the SPARC file (31 points). The refit on the
   actual SPARC data gives χ²_ν = **1.68** (not 0.97). The rotation curve
   (Fig. 26) is redone on SPARC.
3. **NGC 6503 MCMC figure (Fig. 32).** The online figure was drawn from a
   **synthetic normal distribution** (hard-coded mean and covariance) and
   displayed ± 0.22 / ± 0.20 / V∞ = 114.0 ± 3.5. It is now drawn from the
   actual chain (`mcmc_ngc6503_sparc.py`, made deterministic):
   log₁₀ ρ₀ = −23.252 (+0.040/−0.039) g cm⁻³, R_s = 1.705 (+0.089/−0.087) kpc,
   V∞ = 113.96 (+0.80/−0.77) km/s, correlation −0.997, χ²_ν = 1.68. The
   values ± 0.22 / ± 0.20 / ± 3.5 did not come from sampling the likelihood.
4. **Mahalanobis distance ECF – DESI DR1.** 2.22σ / 7.32σ came from a
   13-observable block including two rows DESI DR1 does not publish. Now
   **2.03σ / 6.98σ**, full covariance, 12 observables.
5. **BOSS error at z = 0.61.** The statistical error alone had been used;
   now 0.166 / 0.206 / 0.251 (stat + syst, Alam et al. 2017).
6. **Annihilation energetics (14/10/2026).** For M₂ = 10⁴ M☉,
   2M₂c² = 3.6×10⁵⁸ erg, not 4×10⁵⁶ erg (a factor ≈ 100). The GRB/FRB
   "calibration" η_ann ∼ 0.1–0.5 rested on that error and is **withdrawn**:
   observed long-GRB energies (record E_iso ≈ 1.5×10⁵⁵ erg, GRB 221009A) require η_ann ≲ 4×10⁻⁴ for the reference pair
   (or a small prompt-photon fraction), and the FRB identification is not
   established. η_ann is `OPEN`. In the figure `Fig_ecf_Annihilation` the curves were correct, but the 10⁵/10⁶ M☉ markers (placed at 1 and 10 M☉) and the η = 0.1 energy markers were misplaced; corrected, with η = 0.1 now labelled illustrative; |V/I| ≃ 0.8 (POLAR-2) and the hostless signature are unchanged.

### Values and statuses changed (register § 3)

- **Background (decision A-7).** Ω_m = ω_m/h² ≃ **0.267** (0.315 kept only as the
  Planck reference); Ω_r = 7.8417×10⁻⁵. Age t₀ = **13.33 Gyr**, compatible with
  the globular-cluster age; the age-tension narrative is **abandoned** (5.7σ
  `HISTORICAL`). Globular-cluster reference corrected to Valcin et al. **2020**.
- **Recombination age**: **368.4 kyr** with the spin term (371.3 kyr ΛCDM).
- **Global Δχ² of Foundation I** (−39.5): `HISTORICAL`; not recomputed after
  A-7 (no ECF Boltzmann solver). No global preference is claimed.
- **BAO**: target at z = 1.48 is **30.21 ± 0.79** (eBOSS DR16 QSO consensus,
  Hou et al. 2021); χ²_BAO = **12.11** against 1.79 for ΛCDM (Δ ≃ +10.3);
  r_drag not identified with r_s (PO-ECF-BAO-RDRAG, `OPEN`); BAO comparisons
  `CALCULATED-CONDITIONAL`.
- **DESI DR1**: Δχ²(ECF − ΛCDM) = **+6.21 / +38.59** (the ECF is not
  favoured); χ² = 55.3 is over a ten-observable subset in the diagonal
  approximation, not the global DESI χ². DESI citations redirected to DR2
  *Results II*; "w₀ < −1" corrected (DR2: w₀ > −1).
- **(w₀, wₐ)**: `CALIBRATED`, optimisation point **without error bar**;
  ξ = 1.645 calibrated on the DESI preference, hence not independent of DESI.
- **S₈**: 0.766 is the KiDS-1000 target, not an ECF output; ECF growth `OPEN`.
- **γ_spin** = 0.3116: `HISTORICAL` calibration; physical value `OPEN`.
- **Π_GW** = 0.20 ± 0.05: `CALIBRATED TEMPLATE` (never "predicted", never "≥").
- **Void threshold**: ξ_KZ = 60 comoving Mpc is the physical threshold
  (40.4 Mpc/h is only its conversion at h_fid = 0.6732 for the DESIVAST
  catalogue); wording "threshold / would constrain", not "refuted".
- **n_s**: not predicted; inherited input (PO-F3-NS).
- **Micro-Knot → Macro-Knot chain**: `WITHDRAWN`; Macro-Knot formation is a
  structural hypothesis; 6.8×10⁻⁵ M☉ is a minimal benchmark, not a ceiling.
- **Reference masses**: ≈ 0.6 M⊕ (was "half the Earth mass") and ≈ 23 M⊕
  (was "≈ 26 M⊕").
- **Roman event duration**: two durations distinguished, ≈ 1.05 h (individual
  Micro-Knot) and ≈ 6.3 h (aggregate at λ = 36).
- **Instrument timeline**: LISA launch ~2035; LiteBIRD JFY2036 (ISAS/JAXA);
  Roman launched on 30/08/2026; DOE/NSF support for CMB-S4 ended (July 2025).
- **Bounce equations**: H² = (8πG/3) ρ (1 − ρ/ρc) is exact for fermionic dust
  in the spin-fluid description and schematic elsewhere; a per-regime form is
  added. In the stiff phase the spin term alone does not produce a bounce
  (PO-ECF-ACTION-BOUNCE, `OPEN`). The acceleration equation is corrected
  (it now changes sign; ρc/3 for radiation, 0.4 ρc for the stiff fluid within
  the single-density form). Popławski's Eq. (12) is qualified (Dirac description).

### Other changes in Foundation II (register § 5)

- Factor (1+z)^(−3wₐ) removed from the A_ECF equation.
- Ratio ρ_τ/ρ_m (Fig. 8) redone on the A-7 background: crossing at
  **z = 0.40 ± 0.02** (was "z ≈ 0.3") and **2.75 ± 0.11** at z = 0 (was
  saturation at "Ω_Λ^eff ≈ 0.69").
- Horizon mass written M_H = c³/(2GH) (Hubble convention).
- Baryogenesis: status "semi-derived", with the normalisation on the observed
  value stated.
- SPARC: homogeneous internal comparison 0.80 (ECF halo) vs 1.29 (NFW refit,
  same protocol); the external value 1.55 of Li et al. is no longer used as the comparison.
- Appendix lettering corrected.
- Actual paths and names of the pedagogical scripts (GIF, Blender V34-FIX /
  V40.1-FIX).
- Script suite: **111** (54 calculations + 57 figures).
- References to Foundation III: the bibliography points to *Cosmological
  Physics* (deposited); the Foundation III series is distinguished from
  Foundation IV; the complete derivation of the gravitational-wave background
  is presented as an open programme; molecular chirality is referred to
  Foundation IV (in preparation).
- Internal consistency: bounce time ~10⁻⁴⁴ s ("Torsion Gap"); Micro-Knot
  Schwarzschild radius 5.56 mm; the order-of-magnitude derivation of the
  Micro-Knots aligned on the canonical one (H(T_c) ≈ 5.4×10¹⁰ s⁻¹, size bounds
  coinciding at 5.6 mm); Macro-Knots formed through the Great-Annihilation
  channel, not by coagulation (four passages); the anti-parallel filament-spin
  correlation removed from the abstract and the prediction tables; S₈ = 0.766
  labelled as a target in the test table; Abell2744-QSO1 at z ≃ 7.04;
  a_bounce ~ 10⁻³² in the ellipticity bound (ε ≲ 1.1×10⁻⁷); the Cartan time
  ~10⁻⁴⁴ s in the two schematic figures (expansion velocity, scale factor).

---

## Version History

| Version | Date | Summary |
|---|---|---|
| v13 | 10 June 2026 | **PREPRINT v1** — Zenodo initial deposit (concept doi:10.5281/zenodo.20629237) |
| v14 | 18 June 2026 | "fractal"→"hierarchical" · 5 Topological Zoology figures |
| v15 | 19–22 June 2026 | **PREPRINT v3** — Zenodo deposit. Full referee audit (+2400 lines since v13): all section intros; `tab:sparc_comparison/limitations/roadmap`; VSF equations; GW benchmarks; WIMP flux; magnetic+electric fields (4 levels); Micro-Knot ISM transit T1–T6; planetary interactions P4/P5/P7; topological network H1–H4 (Wang+2021, Rong+2025 2σ ⚠️ *H1 mechanism revised, H3/H4 withdrawn 30/08*); kinematic decoupling + hierarchical coalescence; 4 referee figures |
| v16 | 1–3 July 2026 | **PREPRINT v3**. Cross-check with Foundation III — 10 corrections (Micro/Macro spacing; flux Φ_MK ×10¹¹ error; Macro-Knot local-density method; R_E; t_E reconciled; EMF section added; N_ev arithmetic; "Euclid Q2" → DR1; Roman captions; header). New: FFP discrimination, TTT vs ECF table, `plot_F2_Roman_EMF_prediction.py`. *(Several of these values were corrected again later: see v17 and v20.)* |
| v17 *(initial)* | 17–24 July 2026 | Cross-check with Foundation I/III — QCD-epoch mislabel relabelled "Great Annihilation" (numbers unchanged); trilemma over-claim withdrawn (PO-F2-5 open); Chiral Wall dilution sign corrected; PO-F2-3 ↔ PO-F3-XI cross-reference; concept DOIs throughout. |
| v17 | 15 September 2026 | **PREPRINT v4, corrected.** Eleven corrections, three touching a published value: DESI DR2 4.9σ → 3.1σ (the figure does not appear in arXiv:2503.14738); N_macro 10³ → O(1) per galactic volume; Israel repulsion dimensionally corrected, z̈ = (8πG/3)(σ_2D/ct)·z (eight occurrences). Also: dynamical friction ≲1 Gyr → ≃ 5.9×10³ Gyr at 10 kpc; recombination age updated (since superseded by the v20 value 368.4 kyr); bimodal Micro/Macro-Knot spectrum explained as two distinct mechanisms; Great-Annihilation temperatures distinguished (2m_ec² / m_ec² / ~16 keV freeze-out); `_{μK}` → `_{MK}` (54 places); three figures regenerated; Micro-Knot number density corrected (n_MK ≃ 1.34×10⁻⁵² cm⁻³, spacing ≃ 0.063 pc, flux 2.9×10⁻⁴¹ m⁻²s⁻¹). 156 pages. |
| **v20** | **October 2026** | **PREPRINT v5** (current). Propagation of audit v2 (decision A-7) and October corrections; three data/figure corrections explicitly signalled (void statistics, NGC 6503 data, NGC 6503 MCMC); DESI, BAO, age, recombination, (w₀,wₐ), S₈, Π_GW, VSF, Micro→Macro-Knot chain and instrument dates updated — see "What changed in this version" and the Version register and erratum. 173 pages. |

---

## Citation

```bibtex
@misc{FichantFoundationII2026,
  author    = {Fichant, Pascal},
  title     = {Foundation II: The Chiral Universe and the Three Fossils
               of the Bounce --- Baryogenesis, the Geometric Dark Sector,
               and Cosmic Alignment within an Einstein-Cartan Framework,
               Extended Version},
  year      = {2026},
  publisher = {Zenodo},
  version   = {v5},
  doi       = {10.5281/zenodo.20629237},
  url       = {https://doi.org/10.5281/zenodo.20629237},
  note      = {PREPRINT v5 (internal revision 20) on Zenodo (October 2026);
               concept DOI resolves to the latest version.
               Code: https://github.com/pfichant/spin-torsion-cosmology.
               Companion to PIT Letter (doi:10.5281/zenodo.19798923),
               Foundation I (doi:10.5281/zenodo.19577447) and
               Foundation III -- Cosmological Physics (doi:10.5281/zenodo.22359982).}
}
```

---

**Contact**: p.fichant.research@gmail.com  
**GitHub**: https://github.com/pfichant/spin-torsion-cosmology  
**Zenodo**: https://doi.org/10.5281/zenodo.20629237  
**CC-BY-4.0** | Montpellier, Occitanie | October 2026
