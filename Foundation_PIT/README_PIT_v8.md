# The Topological Invariance Principle (TIP) — PIT Letter

### Exact Spatial Flatness and the Spin–Torsion Link: an Open Problem in Einstein–Cartan Cosmology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19798923.svg)](https://doi.org/10.5281/zenodo.19798923)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Pascal Fichant** — Independent Researcher, Montpellier, Occitanie, France
**PREPRINT v5** · concept doi: `10.5281/zenodo.19798923` (always resolves to the latest version)

> **arXiv**: not yet submitted (endorsement pending for gr-qc)

---

## Overview

The **Topological Invariance Principle (TIP)** states spatial flatness as a
**postulate**: $\Omega_K \equiv 0$ exactly, as a topological property of
spacetime rather than a dynamical outcome of inflation. Unlike inflationary
flattening — which predicts only $\Omega_K \approx 0$ — this is a sharp,
falsifiable claim: a measurement of $\Omega_K \neq 0$ at **any** precision
would exclude the framework, while leaving inflation untouched. That
asymmetry is the entire empirical content of the postulate.

This version (v8) is deliberate about **what the postulate does not do**.
Once $k = 0$, the identity $\sum_i \Omega_i = 1$ holds for any matter content
whatsoever — adding a spin component changes $H$, and the critical density
$\rho_{\rm crit} = 3H^2/8\pi G$ is recomputed with it. The closure condition
is therefore an **identity, not a constraint**: it fixes neither $\rho_{\rm
DE}$ nor its equation of state, and cannot enforce any compensating
dark-energy component.

---

## What changed in v8 (this version)

This version **withdraws** the compensation mechanism presented in v4–v7 and
reformulates the Letter around the open problem it leaves.

| Change | Detail |
|---|---|
| **Compensation mechanism withdrawn** | Earlier versions stated that injected spin density algebraically enforces a compensating torsion debt, and that $\Omega_\tau$ rises mechanically to maintain equilibrium. Both are withdrawn: $\sum_i \Omega_i = 1$ is an identity once $k=0$. |
| **Scope of the postulate restricted** | The TIP now underwrites **exact spatial flatness only**, not the dark-energy sector. |
| **Static dark energy attributed to the action** | The $w=-1$ term is derived from the FLRW reduction of the axial torsion sector (Foundation II, Appendix J) — **independently** of the postulate, not from closure. |
| **$\Omega_{\rm spin}$–$\Omega_\tau$ relation stated as open** | A relation between the pre-recombination spin fluid and the late-time condensate is expected on physical grounds, but must be **derived from the action**, not imposed by $\Omega$-bookkeeping. This is the central open question. |
| **Charge-conservation analogy withdrawn** | In FRW, $k$ is a constant of the solution, not a Noether charge — there is nothing to conserve. |

---

## What the Letter asserts, withdraws, and leaves open

**Asserted.** Spatial flatness is exact, $\Omega_K \equiv 0$, by topological
necessity rather than dynamical relaxation. Falsifiable: any measured
$\Omega_K \neq 0$ excludes the framework.

**Derived (independently of the postulate).** A static dark-energy term,
$w=-1$, from the FLRW reduction of the axial torsion sector (Foundation II,
Appendix J). Its fluctuations behave as radiation ($w=+1/3$). This result has
been reached independently by different routes (Ivanov & Wellenzohn 2016; Yun
& Lee 2024).

**Left open.** Whether the Poincaré Gauge action implies a relation between
$\Omega_{\rm spin}$ (which governs the pre-recombination sound horizon) and
$\Omega_\tau$ (which sources late-time dark energy) — and with which sign. The
observed **evolution** of the equation of state does not follow from the
action here, and remains **calibrated**: $(w_0, w_a) = (-0.904, -0.153)$,
inherited from the Foundation I calibration.

---

## Einstein-Cartan Trilogy

| Paper | Concept DOI | Role |
|---|---|---|
| **PIT Letter** *(this)* | [10.5281/zenodo.19798923](https://doi.org/10.5281/zenodo.19798923) | Exact spatial flatness postulate; the spin–torsion link as an open problem |
| **Foundation I** | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | $H_0$–$S_8$–$r_s$ calibration, stiff-era expansion, regular bounce |
| **Foundation II** | [10.5281/zenodo.20629237](https://doi.org/10.5281/zenodo.20629237) | Baryogenesis, geometric dark sector, Micro-Knots; static dark energy (Appendix J) |
| **Foundation III** | In preparation | Strong gravity, Cartan core, vacuum thermodynamics |

> All cross-paper DOIs are **concept DOIs**: they resolve to the latest
> version of each paper.

---

## Key quantities

| Parameter | Value | Status |
|---|---|---|
| $\Omega_K$ | $\equiv 0$ | **postulated** (exact, falsifiable) |
| $\Omega_{\rm spin}^{\rm peak}$ | $0.093$ | observational input from Foundation I (broadly $[0.05, 0.15]$ from QCD thermodynamics) |
| $z_{\rm peak}$ | $7500$ | acoustic-era reference redshift |
| $F_{\rm ion}$ | $1.2765$ | Foundation I joint constraint |
| $w$ (static) | $-1$ | **derived** from the action (Foundation II, App. J) |
| $(w_0, w_a)$ | $(-0.904, -0.153)$ | **calibrated**, inherited from Foundation I — not derived here |

### H₀ tension context

The H₀ Distance Network (H₀DN) Collaboration reports $H_0 = 73.50 \pm 0.81$
km/s/Mpc (arXiv:2510.23823), a 7.1σ tension with flat ΛCDM. The ECF
calibration ($H_0 = 73.04$) sits 0.6σ from that value. This is context for the
Letter, not a result of the postulate.

### DESI note

The calibrated $w(z)$ departs from $-1$ in the direction DESI has since
measured, but a full-covariance comparison places the point at 2.22σ from the
DR1 central value and **does not favour it over ΛCDM** on those data alone. A
full likelihood comparison is deferred to Foundation III.

---

## Repository structure

```text
spin-torsion-cosmology/
├── Foundation_PIT/
│   ├── 01_Paper_Publication/
│   │   └── fichant_ecf_PIT_Letter_v8.pdf
│   └── 02_Scientific_Code/
│       └── B_Paper_Plots/
│           ├── Figure_CosmicHistory_Omegas_PIT.png
│           └── plot_Cosmic_History_Omegas.py
├── requirements.txt
└── README_PIT_v8.md
```

---

## Reproducing the figure

```bash
pip install -r requirements.txt
cd Foundation_PIT/02_Scientific_Code/B_Paper_Plots/
python plot_Cosmic_History_Omegas.py
```

Output: `Figure_CosmicHistory_Omegas_PIT.png`

The figure shows the evolution of the fractional densities $\Omega_i(a)$. The
bottom panel displays $\Omega_K$, which is **identically zero once $k=0$** —
this is the visual expression of the flatness postulate, i.e. an identity, not
a verified prediction. The late-time rise of $\Omega_\Lambda$ is an
arithmetical consequence of matter dilution (it occurs for a strict
cosmological constant too), **not** the signature of a new field.

> ⚠️ **Windows**: run `set PYTHONIOENCODING=utf-8` before any script.

---

## Compile the Letter

```bash
cd Foundation_PIT/01_Paper_Publication/
pdflatex fichant_ecf_PIT_Letter_v8.tex
bibtex   fichant_ecf_PIT_Letter_v8
pdflatex fichant_ecf_PIT_Letter_v8.tex
pdflatex fichant_ecf_PIT_Letter_v8.tex
```

Requires `revtex4-2` (standard APS distribution).

---

## Citation

```bibtex
@misc{FichantPIT2026,
  author    = {Fichant, Pascal},
  title     = {Exact Spatial Flatness and the Spin--Torsion Link:
               an Open Problem in Einstein--Cartan Cosmology},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.19798923},
  url       = {https://doi.org/10.5281/zenodo.19798923},
  note      = {Concept DOI, resolves to the latest version.
               Companion papers:
               Foundation I doi:10.5281/zenodo.19577447;
               Foundation II doi:10.5281/zenodo.20629237.
               Code: https://github.com/pfichant/spin-torsion-cosmology}
}
```

---

**Contact**: p.fichant.research@gmail.com
**GitHub**: https://github.com/pfichant/spin-torsion-cosmology
**CC-BY-4.0** | Montpellier, Occitanie

> *"Spatial flatness is exact — and what that does, and does not, imply is stated precisely."*
