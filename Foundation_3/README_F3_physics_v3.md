# Foundation III — Cosmological Physics

### Bounce Signatures, Void Statistics, the Status of the Primordial Spectrum, and Falsifiable Predictions

[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Pascal Fichant** — Independent Researcher, Montpellier, Occitanie, France
**PREPRINT v3** (October 2026, 41 pages; internal revision 1.1 revised) · concept DOI: [10.5281/zenodo.22359982](https://doi.org/10.5281/zenodo.22359982)
Deposited file: `fichant_ecf_F3_physics_v1_1.pdf`

> **arXiv**: not yet submitted

---

## Corrections made after the first drafting of this README (22–24 October 2026)

- **Pages: 41** (unchanged).
- **Limit of the calibrated spin branch (23/10/2026).** The calibrated sound horizon r_s = 135.65 Mpc (hence H₀ = 73.04 km/s/Mpc) requires the spin term (∝ a⁻⁶, ρ_spin = 0.093 ρ_r at z_ref = 5600) to hold up to z ~ 10⁵ (if it stops at 2×10⁴: r_s = 139.4 Mpc). Extended unchanged to T ~ 1 MeV it gives ρ_spin/ρ_r ~ 10⁹–10¹¹ and is excluded by BBN; it also lies ~22 orders of magnitude above a primordial stiff fluid ending at t ~ 10⁻¹¹ s (Foundation II). Neither a rise-and-fall profile nor a distinct component is derived: **PO-ECF-BBN-SPIN stays open**. No numerical result changes.
- **BBN box.** Foundation III already states that BBN compatibility of the spin sector is **not demonstrated** (PO-ECF-SPIN-NORM, PO-ECF-BBN-SPIN) and that the |ρ_spin|/ρ_r ~ 10⁻⁵¹ estimate is withdrawn; a sentence now points to Foundation I for the quantitative statement above.
- **References and external values checked at source (22/10/2026).** Ten references corrected or completed; the gravitational-wave H₀ is 71.0 (+9.0/−7.1), the published value; the Nieh–Yan term is attributed to Nieh & Yan (1982); the « Gibbons–Turok problem » (six occurrences, including the WKB figure, regenerated) is renamed; Planck PR3 f_NL cites Planck 2018 IX.

The version register (§5, dated entries 20–24/10/2026) is the authority for each change; where this README and the register differ, the register and the PDF prevail.

---

## What changed in this version (PREPRINT v3, October 2026)

This version supersedes PREPRINT v2 (15 September 2026). The changes are
listed, with their reasons, in the **version register and erratum**
deposited in the same Zenodo lot (*Einstein–Cartan Framework — Version
register and erratum*, October 2026). In case of discrepancy, the text of
the paper prevails.

**A correction explicitly signalled (register § 4, item 4).** v2 contained,
in two illustrative places, a **dimensionally incorrect** form of the Israel
repulsion of the chiral-wall mechanism: the Friedmann coefficient was applied
to a *surface* density. The self-accelerating equation now reads
$\ddot z=(8\pi G/3)(\sigma_{2D}/ct)\,z$, using the effective volume density
of a wall of causal thickness $ct$ (§ 2, *KZ correlation length and
cosmological dilution*).

**DESI DR1 comparison rebuilt on 12 sourced observables (register § 3.2).**
The former block had 13 observables, including two QSO rows that DESI DR1
does not publish. With the 12-observable block and full covariance:

| Quantity | v2 | v3 |
|---|---|---|
| Mahalanobis distance ECF – DESI DR1 (Planck / SH0ES prior) | 2.22σ / 7.32σ | **2.03σ / 6.98σ** |
| Δχ²(ECF − ΛCDM), DESI DR1 (Planck / SH0ES prior) | +8.06 / +41.94 | **+6.21 / +38.59** |

The Δχ² is positive under both priors: the calibrated ECF point fits these
data less well than ΛCDM; the ECF is **not** favoured. The χ² = 55.3 quoted
in the PO-F3-DESI box is now qualified as the χ² over a **ten-observable
subset of DESI DR1 in the diagonal approximation** (`calibrate_w0wa.py`),
not the global DESI DR1 χ²; it is computed on the active background
Ω_m = ω_m/h² ≈ **0.267** (13.7 at the former Ω_m = 0.315, now a historical
value). The DESI figures and numbers are now produced by the Foundation I
script `Scripts_F1/B_Paper_Plots/plot_ecf_desi_mcmc_v3_0.py` (the F3 copy is
superseded; see the note at the end).

**Status of (w₀, w_a) (register § 3.3).** $(w_0,w_a)=(-0.904,-0.153)$ is a
**CALIBRATED** point, not a prediction made prior to DESI: $\xi=1.645$ is
calibrated on the DESI preference used by the ECF so as to reproduce the
target $w_a$, hence not independent of DESI. It is quoted without error bar.

**Growth discriminant recomputed on the Ω_m = 0.267 background.** The
ECF/ΛCDM ratio of $f\sigma_8$ rises from 0.870 to 0.959 across $0<z<0.8$
(a 9.8% variation; v2: "nearly redshift-independent, ≈2%"). Against six
published RSD measurements, Δχ² = −1.71 (N = 6; v2: −0.14), with
σ₈ = 0.812 obtained by converting the KiDS-1000 target S₈ = 0.766 at
Ω_m = 0.267 — a target, not a computed amplitude. With six heterogeneous
points, no covariance and no Alcock–Paczynski rescaling, this Δχ² carries
no evidential weight.

**Void Size Function threshold qualified (register § 3.3).** The physical
threshold is $\xi_{\rm KZ}=60$ comoving Mpc; 40.4 Mpc/h is its conversion at
$h_{\rm fid}=0.6732$, the fiducial of the DESIVAST catalogue; 43.8 Mpc/h is
not a universal threshold. $\xi_{\rm KZ}$ is described as an adopted value
whose calibration procedure is not documented; DESIVAST DR1 is a downstream
test, not its calibration. The absence of an excess would *constrain* the KZ
sector in this realisation (wording "threshold / would constrain", no longer
"refute").

**Instruments (register § 3.3).** DOE/NSF support for CMB-S4 **ended** in July 2025: its
forecast sensitivity σ(f_NL) ~ 0.3 is kept only as a forecast made before
that date, and the corresponding tests are reassigned to "future CMB surveys,
timescale not fixed". LISA: launch ~**2035** (was 2037). LiteBIRD: launch
**JFY2036**, Japanese fiscal year (ISAS/JAXA mission page; was 2032).

**Chiral asymmetry of gravitational waves (register § 3.3).**
$\Pi_{\rm GW}=0.20\pm0.05$ is a **CALIBRATED TEMPLATE** (formerly
"Π_GW ≥ 0.20, ECF confirmed"). A LISA detection consistent with it would
support the chiral tensor sector, not the framework as a whole.

**n_s (register § 3.3).** Unchanged in substance: $n_s$ is **not
predicted**; it is an inherited input (PO-F3-NS).

**Companion documents.** *Foundation III — Strong Gravity*, *Foundation
III — Chiral Bounce* and *Foundation IV* are now flagged in the paper as
**in preparation, not yet publicly deposited**.

**Also withdrawn or requalified in the paper text** (stated there as
corrections of earlier versions):

- **BBN.** The analytical estimate $|\rho_{\rm spin}|/\rho_r\sim10^{-51}$,
  presented in v2 as a confirmation with no free parameter, is withdrawn as
  a test: it relied on condensate-normalisation values without a producing
  calculation and on an $a^{-6}$ dilution inconsistent with Foundation II.
  BBN compatibility of the spin sector is **not demonstrated**
  (PO-ECF-SPIN-NORM, PO-ECF-BBN-SPIN, OPEN). The BBN figure is withdrawn.
- **$f_{\rm NL}^{\rm KZ}$.** $+5/18$ is the raw 3D statistic of a Poisson
  field; reading it as a primordial $f_{\rm NL}$ is conditional on the
  Poisson→ζ bridge, not demonstrated. The CMB-projected value ≈ +0.09
  (factor ×1/3) is withdrawn: no projection factor applies to $f_{\rm NL}$.
  The value to confront with CMB bounds is **OPEN**.
- **Isotropy.** The WKB / Vilenkin track *favours* isotropy within the
  mini-superspace model; it does not close PO-F3-ISO.
- **Internal consistency (register § 5).** The bounce is no longer placed at
  T_EW ~ 159 GeV: T_EW is the electroweak crystallisation that follows it.
  S251112cm (November 2025, O4c) is not part of GWTC-5.0, which covers O4b.

---

## Overview

This document collects the **testable, falsifiable cosmological-physics
content** of the Einstein–Cartan Framework (ECF) Foundation III programme —
the sector developed for peer review. The wormhole mechanism, the Cartan
core, the CPT cascade, the full Landau–Ginzburg formalisation of the bounce,
and the exploratory programme (baby universes, fertility curve, astrobiology,
holarchy) are developed in companion documents (*Foundation III — Strong
Gravity*, *Foundation III — Chiral Bounce*, and *Foundation IV*), which are
**in preparation, not yet publicly deposited**, and are not repeated here.

**Horizon without inflation.** The ECF proposes a structural, non-kinematic
alternative to inflation. We establish that the crystallised Kibble–Zurek
network forms a genuine chain complex on the ECKS manifold and prove
$\partial\circ\partial=0$ (Proposition F3-1) — a valid algebraic result in
its own right. Whether this delivers a globally coherent, causally-connected
horizon solution *a priori*, as an earlier version of this Corollary claimed,
is not established: that stronger claim required Chiral Walls to be stitched
into one object by a network of Torsion String loops, and was withdrawn on
30/08/2026 once Chiral Walls were shown to be independent closed bubbles
with no stable multi-way junction. The horizon problem therefore retains an
open status alongside the monopole problem, documented without occultation.

**Observational confrontation.** The calibrated ECF point
$(w_0,w_a)=(-0.904,-0.153)$ is compared to DESI DR1 with full covariance on
12 observables (Mahalanobis distance $2.03\sigma$ under a Planck prior,
$6.98\sigma$ under a SH0ES prior). The Void Size Function test is run
against the real DESIVAST DR1 catalogue: the observed maximum interior
radius is 31.7 Mpc/h, and the ECF threshold $\xi_{\rm KZ}=60$ comoving Mpc
(40.4 Mpc/h at $h_{\rm fid}=0.6732$) remains out of reach of the BGS sample
($z<0.24$); the method is validated and the definitive test deferred to
Euclid DR1-Complete (mid-2027).

**Primordial spectra, stated plainly.** The scalar spectral index $n_s$ is
**not predicted** by the framework: the large-scale spectrum is taken as
inherited, an input on the same footing as $\Omega_b$. An earlier claim of a
parameter-free prediction ($n_s\simeq1$) rested on an incorrect
identification of the Wands duality and has been withdrawn. The stiff era
does generate a blue tensor component whose amplitude bounds the stiff-phase
duration from below — a falsifiable *form*, not yet a calibrated threshold.

---

## What is asserted, derived, and left open

**Derived.** The chain-complex structure of the topological network and the
proof $\partial\circ\partial=0$ (Proposition F3-1) — a valid algebraic result
in its own right. Whether this delivers a globally coherent, causally-connected
horizon *a priori*, as an earlier version claimed, is **not** established: that
stronger claim was withdrawn on 30/08/2026 once Chiral Walls were shown to be
independent closed bubbles with no stable multi-way junction. The horizon
problem therefore retains an open status alongside the monopole problem.

**A degeneracy acknowledged, and the discriminant identified.** Petri, Marra &
von Marttens [Phys. Rev. D **113**, 023504 (2026)] show that an interacting
dark-sector model can be *exactly degenerate with CPL at the background level* —
so the DESI comparison reported here constrains the ECF trajectory without, by
itself, establishing that torsion rather than a dark-sector interaction is behind
it. This paper states that limitation rather than leaving it implicit, and points
to where the ECF is testable instead: late-time structure growth. Integrating the
Foundation I growth equation on the ECF background (Ω_m = 0.267) gives an
ECF/ΛCDM $f\sigma_8$ ratio that rises from 0.870 to 0.959 across $0<z<0.8$
(a 9.8% variation), rather than the sharp low-redshift drop that disfavours the
interacting model; against six published RSD measurements the two histories are
statistically indistinguishable ($\Delta\chi^2 = -1.71$, $N=6$, with
σ₈ = 0.812 converted from the KiDS-1000 target S₈ = 0.766, not a computed
amplitude). **This establishes that the ECF growth history is not excluded —
not that it is preferred**; the ECF growth prediction itself remains OPEN (no
perturbative chain). Reproduced by
`Scripts_F1/A_Core_Calculations/compute_fsigma8_ecf.py` and
`Scripts_F1/A_Core_Calculations/compare_fsigma8_data.py`.

**Confronted with real data.** The VSF method, validated against the actual
DESIVAST DR1 void catalogue (not a mock or a rescaled substitute) — the null
result so far is a limitation of survey reach, not a falsification: the
deeper V² catalogues reach the threshold only with boundary-truncated voids.
The decisive test is scheduled for Euclid DR1-Complete.

**Explicitly withdrawn.** The earlier claim of a parameter-free scalar
spectral index; the BBN "confirmation" $|\rho_{\rm spin}|/\rho_r\sim10^{-51}$;
the CMB-projected value $f_{\rm NL}^{\rm KZ}\approx+0.09$. The corpus names
these reversals rather than dropping them.

**Left open, and named.**

| Code | Problem |
|---|---|
| PO-F3-NS | Scalar spectral index $n_s$: not predicted, inherited |
| PO-F3-XI | $\xi_{\rm KZ}$ (void correlation scale): adopted value, calibration procedure not documented, not derived *ab initio* |
| PO-F3-ISO | Isotropy / BKL shear problem: not claimed resolved |
| PO-F3-DESI | Tension on the $w_a$ amplitude (DES 6yr + DESI DR2 + CMB) |
| PO-F3-VSF | VSF test currently out of reach of BGS survey depth |
| NEFOLD-1 | Numerical threshold for the blue tensor bound not yet calibrated |
| PO-ECF-SPIN-NORM, PO-ECF-BBN-SPIN | Condensate normalisation; BBN compatibility of the spin sector not demonstrated |

Strong-gravity and chiral-sector open problems (PO-F3-C6, PO-F3-B3, PO-F3-IC,
PO-F3-CHIRAL) are tracked in the companion *Foundation III — Strong Gravity*
document (in preparation, not yet publicly deposited), not repeated here.

---

## Einstein-Cartan Corpus

| Paper | Concept DOI | Role |
|---|---|---|
| **PIT Letter** | [10.5281/zenodo.19798923](https://doi.org/10.5281/zenodo.19798923) | Exact spatial flatness postulate; the spin–torsion link as an open problem |
| **Foundation I** | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | $H_0$–$r_s$ calibration, stiff-era expansion, regular bounce |
| **Foundation II** | [10.5281/zenodo.20629237](https://doi.org/10.5281/zenodo.20629237) | Baryogenesis, geometric dark sector, Micro-Knots; static dark energy |
| **Foundation III — Cosmological Physics** *(this deposit)* | `10.5281/zenodo.22359982` | Bounce signatures, void statistics, primordial-spectrum status, falsifiable predictions |
| Foundation III — Strong Gravity | *in preparation, not yet publicly deposited* | Cartan core, CPT cascade, strong-field sector |
| Foundation III — Chiral Bounce | *in preparation, not yet publicly deposited* | Landau–Ginzburg formalisation, parity breaking |

> All cross-paper DOIs are **concept DOIs**: they resolve to the latest
> version of each paper.

---

## Key quantities and their status

| Quantity | Value | Status |
|---|---|---|
| $\partial\circ\partial=0$ | — | **proved** (Proposition F3-1); global horizon coherence not established |
| $(w_0,w_a)$ | $(-0.904,-0.153)$, no error bar | **CALIBRATED** (Foundation I; $\xi=1.645$ calibrated on the DESI preference used by the ECF) |
| $(w_0,w_a)$ vs DESI DR1, 12 observables, full covariance | Mahalanobis $2.03\sigma$ (Planck) / $6.98\sigma$ (SH0ES); Δχ²(ECF − ΛCDM) = +6.21 / +38.59 | computed; the ECF is **not** favoured over ΛCDM on these data |
| VSF threshold | $\xi_{\rm KZ}=60$ comoving Mpc (40.4 Mpc/h at $h_{\rm fid}=0.6732$) | **out of reach** of DESIVAST DR1/BGS ($z<0.24$, observed maximum 31.7 Mpc/h); decisive test at Euclid DR1-Complete |
| $n_s$ (scalar spectral index) | — | **not predicted**, inherited (PO-F3-NS); earlier parameter-free claim withdrawn |
| Blue tensor bound | falsifiable *form*, $N_{\rm stiff}\gtrsim68$ (illustrative normalisation) | numerical threshold **not yet calibrated** (NEFOLD-1) |
| $\xi_{\rm KZ}$ | $\approx 60$ Mpc | adopted value, calibration procedure not documented; not derived *ab initio* (PO-F3-XI) |
| $\Pi_{\rm GW}$ (GW chirality) | $0.20\pm0.05$ | **CALIBRATED TEMPLATE**, chiral sector |
| $f_{\rm NL}^{\rm KZ}$ | $+5/18$ (raw 3D Poisson statistic) | conditional on the Poisson→ζ bridge; value at the CMB **OPEN** |
| BBN compatibility of the spin sector | — | **not demonstrated** (OPEN) |

---

## Falsifiable predictions and their instruments

None of these thresholds refutes the framework as a whole: each tests the
sector, realisation or calibrated template it depends on.

| Test | Constraining outcome | Instrument, date |
|---|---|---|
| Void Size Function | No excess of large voids beyond $\xi_{\rm KZ}=60$ comoving Mpc despite adequate survey reach would constrain the KZ sector in this realisation | Euclid DR1-Complete, mid-2027 |
| $(w_0,w_a)$ vs DESI | Full-covariance comparison excludes the calibrated point | DESI DR2/DR3, ongoing |
| Blue tensor tilt $n_T>0$ and GW chirality | $n_T\leq0$; or $\Pi_{\rm GW}<0.02$ (chiral sector) | LISA, launch ~2035 |
| Cosmic birefringence $\beta>0$ | Non-detection $\beta<0.1^\circ$ (CPT sector) | LiteBIRD, launch JFY2036 |
| Blue component bounding the stiff era | $N_{\rm stiff}$ independently fixed below 68, once the threshold is calibrated | CMB μ-distortions, PBH |

---

## Reproducibility

Every figure and every quantitative claim in this paper is reproducible from
the scripts on GitHub (not included in this Zenodo deposit — see below).

**Every script cited in this paper**, by category:

| Script | Category | Produces |
|---|---|---|
| `check_xi_kz_horizon.py` | A_Core_Calculations | test of whether $\xi_{\rm KZ}$ can result from a late KZ freeze-out (imports F1's solver) |
| `plot_F3_ecf_fNL_KZ.py` | B_Paper_Plots | Fig. 1 — $f_{\rm NL}^{\rm KZ}$ non-Gaussianity |
| `plot_F3_ecf_vsf_desivast_v1_simulated.py` | B_Paper_Plots | Fig. 2 — ECF void size function against DESIVAST DR1 |
| `build_vsf_observed_dr1.py` | B_Paper_Plots | VSF measurement on the real DESIVAST DR1 catalogue (1,489 interior voids, Fig. 2 points) |
| `check_vsf_v2_edge_voids.py` | B_Paper_Plots | edge-void diagnostic on the V² catalogues |
| `compute_vsf_lcdm_svdw.py` | B_Paper_Plots | $\Lambda$CDM Sheth–van de Weygaert reference void size function |
| `plot_F3_ecf_vsf_desivast_fits.py` | B_Paper_Plots | VSF pipeline on the DESIVAST DR1 FITS files (`Fig_ECF_VSF_DESIVAST_DR1_fits.png`, not reproduced in the paper) |
| `plot_F3_ecf_wkb_ecks.py` | B_Paper_Plots | Fig. 3 — WKB potential at the bounce |
| `plot_F3_ecf_Cell_suppression.py` | B_Paper_Plots | Fig. 4 — $C_\ell$ suppression |
| `plot_ecf_desi_mcmc_v3_0.py` | Foundation I (`Scripts_F1/B_Paper_Plots/`) | Figs. 5–6 — DESI DR1 MCMC contours and residuals (12 observables) |

**Imported from companion papers** (not duplicated, rule R13 — the script is
the reference):

| Script | Source | Role here |
|---|---|---|
| `script_01_solve_sound_horizon.py` | Foundation I | calibrated background ($r_s=135.65$ Mpc, $z_{\rm ref}=5600$); imported by `check_xi_kz_horizon.py` for consistency |
| `script_07_cartan_threshold.py` | Foundation I | Cartan threshold; settles the scope of the bounce-era tensor amplitude estimate (§ on the blue component and the stiff era) |
| `calibrate_w0wa.py` | Foundation I | ten-observable DESI DR1 subset, diagonal errors (χ² = 55.3, PO-F3-DESI box) |
| `compute_ecf_des_pivot.py` | Foundation II | decorrelated DES pivot, cited in the PO-F3-DESI discussion |
| `compute_fsigma8_ecf.py` | Foundation I | growth-rate solver behind the degeneracy discussion |
| `compare_fsigma8_data.py` | Foundation I | confronts $f\sigma_8(z)$ with published RSD data |

**Also in the F3 tree, not cited in the paper:** `plot_F3_ecf_bbn_constraint.py`
(produced the BBN figure, withdrawn in v3) and `anim_F3_bounce_well.py`
(pedagogical animation, see below).

```bash
python run_all_simulations_F3.py
```

The orchestrator runs every script in the three directories below in order,
logs each run, and centralises every static figure into `figures_output/`.
Requirements: Python ≥ 3.8, `numpy`, `scipy`, `matplotlib`.

```text
github.com/pfichant/spin-torsion-cosmology
    run_all_simulations_F3.py
    02_Scientific_Code/
        A_Core_Calculations/    quantitative checks, no figure output
        B_Paper_Plots/          figure generation for this paper
        C_Simulations/          pedagogical animation (bounce/chirality mechanism)
    data/
        desivast_dr1/           DESIVAST DR1 catalogues (see below)
    figures_output/             static figures (.png/.pdf) end up here
```

> **data/desivast_dr1/** holds the real DESIVAST DR1 void catalogues used by
> the VSF test: the VoidFinder FITS files (0.6–3.9 MB, mirrored
> here) and, when present, the four V² FITS files (62–612 MB, not
> redistributed — see `README_desivast.md` in that folder for provenance,
> licensing, and download instructions). This is a single, visible data
> folder at the repository root, independent of which `02_Scientific_Code`
> subfolder an analysis script lives in: `build_vsf_observed_dr1.py`,
> `check_vsf_v2_edge_voids.py` and `plot_F3_ecf_vsf_desivast_fits.py` all
> resolve it the same way, from their own location, and fall back to a few
> older conventions for anyone who has not moved their files here yet.

> **C_Simulations** contains `anim_F3_bounce_well.py`, a pedagogical animation
> of the Landau–Ginzburg bounce-and-chirality-selection mechanism (developed
> in full in the companion *Foundation III — Chiral Bounce*, in preparation,
> not yet publicly deposited). It solves the exact equation of motion
> numerically rather than illustrating a hand-drawn trajectory, and
> deliberately shows only what is established in that document — no child
> universes, no wormholes. Output (`.mp4`/`.gif`) is written to its own
> `output_simulations/` subfolder, not centralised with the static figures
> above.

> ⚠️ This Zenodo deposit contains **PDF and README only**. LaTeX source is
> withheld for authorship-protection reasons; all reproducibility code is
> maintained separately on GitHub under CC-BY-4.0.

---

> **On the MCMC script (settled 15/09/2026).** Two copies of this script
> existed, writing the same two files: `plot_F3_ecf_desi_mcmc_v3.py` here and
> `plot_ecf_desi_mcmc_v3_0.py` in Foundation I. A line-by-line comparison
> found **exactly one functional difference on 193 lines of diff**: `dpi=150`
> against `dpi=300`. All 90 numeric literals are identical, both seed with
> `np.random.seed(42)`, and the rest is a FR→EN translation. It was never a
> scientific divergence — two copies patched independently.
>
> The Foundation I copy is authoritative: it reproduces the figures carried by
> both papers, verified by hash after regeneration. In v3 the paper cites it
> directly (`Scripts_F1/B_Paper_Plots/plot_ecf_desi_mcmc_v3_0.py`). The F3
> copy is moved to `_SUPERSEDED/` rather than deleted — the two outputs
> differed for a fortnight, and erasing the file would erase the record of it.

---

## Version history

| Version | Date | Main content |
|---|---|---|
| PREPRINT v1 | 5 September 2026 | First public deposit (split from the Foundation III programme). |
| PREPRINT v2 | 15 September 2026 | DESI DR2 deviation corrected from "4.9σ" to the 3.1σ (BAO + CMB; 2.8–4.2σ with supernovae) reported in arXiv:2503.14738; heading on initial conditions changed to "partly derived, partly calibrated" (⟨S²⟩_vol⁽⁰⁾ tied to the calibrated amplitude s₀); δT/T quoted as ~10⁻⁵ with its definition dependence; DESI contour and residual figures realigned with Foundation I. |
| PREPRINT v3 | October 2026 | See "What changed in this version" above and the version register and erratum deposited with it. |

---

## Citation

```bibtex
@misc{FichantFoundationIII2026,
  author    = {Fichant, Pascal},
  title     = {Foundation III --- Cosmological Physics: Bounce Signatures,
               Void Statistics, the Status of the Primordial Spectrum,
               and Falsifiable Predictions},
  year      = {2026},
  publisher = {Zenodo},
  note      = {Preprint v3, October 2026.
               doi:10.5281/zenodo.22359982 (concept DOI, all versions).
               Companion papers:
               PIT Letter doi:10.5281/zenodo.19798923;
               Foundation I doi:10.5281/zenodo.19577447;
               Foundation II doi:10.5281/zenodo.20629237.
               Code: https://github.com/pfichant/spin-torsion-cosmology}
}
```

---

**Contact**: p.fichant.research@gmail.com
**GitHub**: https://github.com/pfichant/spin-torsion-cosmology
**CC-BY-4.0** | Montpellier, Occitanie

> *"The scalar spectral index is not predicted by this framework — stated
> plainly, and the earlier claim that it was is withdrawn, not revised."*
