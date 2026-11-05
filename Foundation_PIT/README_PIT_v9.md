# The Topological Invariance Principle (TIP) — PIT Letter 🌌
### Exact Spatial Flatness and the Spin-Torsion Link: an Open Problem in Einstein-Cartan Cosmology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19798923.svg)](https://doi.org/10.5281/zenodo.19798923)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-PREPRINT%20v9-blue.svg)]()

**Pascal Fichant** — Independent Researcher, Montpellier, Occitanie, France
**PREPRINT v9** · October 2026 · 6 pages · concept doi: `10.5281/zenodo.19798923` (always resolves to the latest version)

> **Zenodo version**: v9, published 26 October 2026, version doi:10.5281/zenodo.23674598 (this deposit, superseding v8 of 6 September 2026, version doi:10.5281/zenodo.22545411)
> **Deposited file**: `fichant_ecf_PIT_Letter_Preprint_v9_Deposit_Zenodo_261026.pdf` (6 pages; SHA256 `c07e3aa409a43d212b4ce071932a315aa096d06a57e2fd9af40ec6220c0d458f`)
> **arXiv**: not yet submitted (endorsement pending for gr-qc)

---

## Corrections made after the first drafting of this README (22–26 October 2026)

- **Pages: 6** (unchanged; two words shortened to keep six pages).
- **Limit of the calibrated spin branch (23/10/2026).** The PIT Letter quotes Ω_spin^peak = 0.093 only as an observational input of Foundation I. It now states that this calibration needs the a⁻⁶ law up to z ~ 10⁵ and that BBN excludes the same branch at 1 MeV (Foundation I; PO-ECF-BBN-SPIN, open). The sentence claiming that QCD physics fixes the value without a free parameter carries a dated correction (16/10/2026).
- **References checked at source (22/10/2026).** Nine references corrected. The paragraph formerly titled « Independent corroboration » no longer presents Ivanov & Wellenzohn and Yun & Lee as obtaining the same result independently (the first treats torsion as an external field; the second is a holographic dark-energy model whose Hubble-cutoff variant is excluded in Einstein–Cartan cosmology); « Planck+BAO » added for Ω_K; the vacuum-energy discrepancy reads ≈ 55 (electroweak scale) to ≈ 122 (cutoff) orders of magnitude, following Martin (2012).

- **Reproduction script (26/10/2026).** A single script, `run_all_simulations_PIT.py`, now runs the two scripts of the Letter (section « Reproducing the figure and the check »). The directory name in the structure and in the commands is `Foundation_PIT/`, the name in the repository; `pip install -r requirements.txt` is replaced by the explicit list (the repository has no `requirements.txt` for v9; `requirements_PIT.txt` dates from v8). The LaTeX source is not distributed in this repository: the Letter is the deposited PDF. No change to the paper or to its numbers.
- **Published (26/10/2026).** v9 was deposited on Zenodo as a new version of the concept record, version doi:10.5281/zenodo.23674598. The deposited PDF is the 26/10/2026 compilation; its text is identical to the 23/10/2026 compilation of the kit, except the « Dated: » line (`\today`).

The version register (§5, dated entries 20–24/10/2026) is the authority for each change; where this README and the register differ, the register and the PDF prevail.

---

## What changed in v9 (this version)

| Change | Detail |
|---|---|
| Mahalanobis distance corrected | The Mahalanobis distance of the calibrated point to the DESI DR1 central value is corrected from **2.22σ to 2.03σ** (full covariance, twelve observables). The earlier value came from a thirteen-observable DESI block, including two QSO rows that DESI DR1 does not publish; that block was withdrawn on 22/09/2026. The calibrated point is **not** favoured over ΛCDM on those data alone. |
| Calibrated point quoted without error bars | $(w_0, w_a) = (-0.904, -0.153)$ is a calibration point; the error bars ±0.004 / ±0.007 belong to the likelihood profile (−0.907 ± 0.004, −0.153 ± 0.007) and are now quoted as such. |

These are the only changes to the text of the Letter (see the paper's "Version note (v9)"). The withdrawal of the compensation mechanism (v8, below) is unchanged.

The correction is listed, with its reason, in the **version register and erratum** deposited in the same October 2026 lot (§3.2, "Mahalanobis distance ECF – DESI DR1"; §4, item 5; §5, "PIT Letter"). The same correction applies to five other documents of the corpus.

---

## ⚠️ v8 withdraws the compensation mechanism of v4–v7

Earlier versions of this Letter (v4 through v7) presented spatial flatness
as maintained by a **continuous compensation** between a spin-density
sector and a torsion sector, $\Omega_{\rm spin}(a)+\Omega_\tau(a)=0$, with
an initial condition $\Omega_\tau^{\rm initial}=-\Omega_{\rm spin}^{\rm
peak}$, drawn by analogy with charge conservation.

**Version 8 withdraws that mechanism.** On closer analysis, the closure
condition is an identity of the FLRW system once $\Omega_K\equiv0$ is
imposed — it holds automatically and therefore cannot be doing the work
of *enforcing* a compensating debt. The relation between $\Omega_{\rm
spin}$ and $\Omega_\tau$, previously assumed, is now stated as the
**central open question** the Letter leaves for the companion papers to
address. The analogy with charge conservation is withdrawn along with it.

**What survives, restricted in scope.** The Topological Invariance
Principle itself — that global spatial flatness ($\Omega_{\rm total}\equiv
1$) is a geometric gauge law rather than a tuned initial condition — is
**retained**, but its scope is now stated as exact spatial flatness only.
It is *not* claimed to derive the compensation mechanism, nor the specific
value of dark energy, nor the analogy that motivated earlier versions.
The static dark-energy term observed at late times is instead attributed
to the FLRW reduction of the action (Foundation II, Appendix J),
independently of the postulate.

If you are looking for the compensation-mechanism argument of v4–v7: it
is withdrawn, not merely revised. Please cite v8 or later (current: v9),
not the earlier description.

---

## Overview

The **Topological Invariance Principle (TIP)** postulates that global
spatial flatness ($\Omega_{\rm total}\equiv1$) is a fundamental geometric
gauge law of spacetime, not a coincidental initial condition. This is a
sharp, falsifiable claim in its own right: a measurement of $\Omega_K\neq0$
at any precision would exclude the framework, while leaving standard
inflation untouched (inflation predicts $\Omega_K\approx0$, not exactly
zero).

The TIP is a **geometric gauge postulate**, not a theorem derived from the
minimal ECKS Lagrangian. The numerical calibration ($\Omega_{\rm
spin}^{\rm peak}=0.093$) is an observational input from Foundation I, not
a logical prerequisite of the principle — and, as of v8, the relation
between that calibration and the postulate itself is an open question,
not an assumption.

---

## Einstein-Cartan Corpus

| Paper | DOI | Role |
|---|---|---|
| **PIT Letter** *(this)* | [10.5281/zenodo.19798923](https://doi.org/10.5281/zenodo.19798923) | TIP gauge postulate, spatial flatness |
| **Foundation I** | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | H₀–S₈–BAO calibration |
| **Foundation II** | [10.5281/zenodo.20629237](https://doi.org/10.5281/zenodo.20629237) | Baryogenesis, geometric dark sector, Micro-Knots |
| **Foundation III — Cosmological Physics** | [10.5281/zenodo.22359982](https://doi.org/10.5281/zenodo.22359982) | Bounce signatures, void statistics, falsifiable predictions |
| **Foundation III — Strong Gravity / Chiral Bounce** | In preparation, not yet publicly deposited | Strong gravity, wormhole, chiral phase transition |

> All cross-paper DOIs above are **concept DOIs**: they always resolve to
> the most recent version of each paper, never to a frozen one.

---

## The Core Claim (v8, unchanged in v9)

```
Ω_total ≡ 1                          [TIP: exact spatial flatness, a gauge law]
Ω_K ≠ 0 at any precision  ⟹  framework excluded
```

The relation between the calibrated spin sector and any compensating
torsion debt — the mechanism v4–v7 assumed — is **not** part of the
postulate as of v8. It is tracked as an open question for Foundation I/II.

| Parameter | Value | Status |
|---|---|---|
| $\Omega_{\rm spin}^{\rm peak}$ | 0.093 | F1 observational calibration (`CALIBRATED`), **not** a TIP prerequisite |
| $w_0$ | −0.904 | `CALIBRATED`, Foundation I calibration point (no error bar) |
| $w_a$ | −0.153 | `CALIBRATED`, Foundation I calibration point (no error bar) |
| $F_{\rm ion}$ | 1.2765 | F1 joint constraint |

$(w_0, w_a)$ are calibrated, not derived: $w_a$ is set through $\xi = 1.645$,
calibrated on the DESI preference used by the ECF, so their consistency with
DESI is not a prediction independent of DESI. A full-covariance comparison
places the calibrated point at 2.03σ from the DESI DR1 central value and does
not favour it over ΛCDM on those data alone (Foundation III).

### H₀ Tension Status

The H₀ Distance Network (H₀DN) Collaboration reports $H_0=73.50\pm0.81$
km/s/Mpc, a community-consensus result at 7.1σ tension with flat ΛCDM —
consistent with the ECF calibration at 73.04 km/s/Mpc (about 0.6σ difference;
this figure is not stated in the Letter, to be confirmed).
This is a background-level consistency check, not a prediction unique to
the TIP.

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **v9** | October 2026 | Mahalanobis distance to DESI DR1 corrected, 2.22σ → 2.03σ (twelve observables); calibrated point (w₀, w_a) quoted without the profile error bars. No other change. |
| v8 | 6 September 2026 | Compensation mechanism $\Omega_{\rm spin}(a)+\Omega_\tau(a)=0$, $\Omega_\tau^{\rm initial}=-\Omega_{\rm spin}^{\rm peak}$ (v4–v7) withdrawn: the closure condition is an identity, incapable of enforcing a compensating debt. Scope restricted to exact spatial flatness. Static dark-energy term attributed to the FLRW reduction of the action (Foundation II, Appendix J), independently of the postulate. Charge-conservation analogy withdrawn. The $\Omega_{\rm spin}$–$\Omega_\tau$ relation stated as the central open question. |
| v4–v7 | — | DESI qualification, epoch labels, concept-DOI migration (see the version history in the paper itself). |

---

## Repository Structure

```text
spin-torsion-cosmology/
├── Foundation_PIT/
│   ├── 01_Paper_Publication/
│   │   └── fichant_ecf_PIT_Letter_Preprint_v9.pdf   (deposited on Zenodo, 26/10/2026)
│   ├── 02_Scientific_Code/
│   │   ├── A_Core_Calculations/
│   │   │   └── verify_flrw_curvature_degeneracy.py
│   │   └── B_Paper_Plots/
│   │       ├── plot_Cosmic_History_Omegas.py
│   │       └── Figure_CosmicHistory_Omegas_PIT.png   (written here when the script is run)
│   ├── run_all_simulations_PIT.py     (runs the two scripts)
│   └── README_PIT_v9.md
```

The two scripts are deliberate copies of the Foundation I original
(`plot_Cosmic_History_Omegas.py`, here with `PAPER = "PIT"`) and of the
Foundation II original (`verify_flrw_curvature_degeneracy.py`, in
`Foundation_2/02_Scientific_Code/A_Core_Calculations/`), so that the Letter can
be reproduced from `Foundation_PIT/` alone.

---

## Reproducing the figure and the check

One command runs both scripts of the Letter, writes `logs/run_PIT.log` and copies the figure to `figures_output/`:

```bash
pip install numpy scipy matplotlib sympy
cd Foundation_PIT/
python run_all_simulations_PIT.py             # the two scripts
```

Expected: `2 script(s) OK, 0 failure(s)`. The script modifies nothing in `01_Paper_Publication/`. Exit code 0 if everything passes, 1 otherwise. The two scripts can also be run one by one, as below.

### Reproducing the Figure


```bash
pip install numpy scipy matplotlib sympy
cd Foundation_PIT/02_Scientific_Code/B_Paper_Plots/
python plot_Cosmic_History_Omegas.py
```

Output: `Figure_CosmicHistory_Omegas_PIT.png`

> ⚠️ **Windows**: run `set PYTHONIOENCODING=utf-8` before any script.

### Checking the curvature-degeneracy result (§"A degeneracy that does not arise here")

A separate objection is addressed directly in the text: van de Venn *et al.*
(*Eur. Phys. J. C* **83**, 288 (2023), arXiv:2211.11868) show that, in
Einstein–Cartan cosmology with totally antisymmetric torsion and *no* torsion
potential, conservation alone forces the axial amplitude to dilute as
$a^{-1}$, giving $w=-1/3$ — the equation of state of spatial curvature
itself. If that held here, the observed $\Omega_K$ would no longer test the
postulate, and the falsifiability claimed above would be blunted.

The ECF differs by carrying a torsion potential with a non-trivial vacuum
expectation value: it is the potential's minimum, not conservation, that
fixes the axial amplitude, pinning it to a constant. `verify_flrw_curvature_degeneracy.py`
reproduces this symbolically — it keeps spatial curvature $k$ throughout
(rather than imposing flatness from the outset, as the rest of Foundation II
does) and checks whether an $a^{-2}$ piece appears in the torsion sector. It
does not: the sector is degenerate with $\Lambda$, not with curvature, so
$\Omega_K$ remains a clean observable.

**Scope, stated in the paper and by the script itself**: this concerns the
homogeneous background only, and does not exclude a degeneracy arising from
perturbations or from non-minimal torsion–curvature couplings.

```bash
pip install sympy
cd Foundation_PIT/02_Scientific_Code/A_Core_Calculations/
python verify_flrw_curvature_degeneracy.py
```

---

## Citation

```bibtex
@misc{FichantPIT2026,
  author    = {Fichant, Pascal},
  title     = {Exact Spatial Flatness and the Spin-Torsion Link: an Open
               Problem in Einstein-Cartan Cosmology},
  year      = {2026},
  publisher = {Zenodo},
  version   = {v9},
  doi       = {10.5281/zenodo.19798923},
  url       = {https://doi.org/10.5281/zenodo.19798923},
  note      = {Concept DOI, resolves to the latest version. v9 corrects
               the Mahalanobis distance to DESI DR1 (2.03 sigma); v8
               withdrew the compensation mechanism of v4--v7; see the
               version notes in the paper. Companion papers:
               Foundation I doi:10.5281/zenodo.19577447;
               Foundation II doi:10.5281/zenodo.20629237;
               Foundation III doi:10.5281/zenodo.22359982.
               Code: https://github.com/pfichant/spin-torsion-cosmology}
}
```

---

**Contact**: p.fichant.research@gmail.com
**GitHub**: https://github.com/pfichant/spin-torsion-cosmology
**CC-BY-4.0** | Montpellier, Occitanie | October 2026

> *"Spatial flatness is exact."*
> — Pascal Fichant, *The Topological Invariance Principle* (2026)
