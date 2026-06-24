# The Topological Invariance Principle (TIP) — PIT Letter 🌌
### Dark Energy as a Geometric Constraint of Spatial Flatness in Einstein-Cartan Cosmology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19900557.svg)](https://doi.org/10.5281/zenodo.19900557)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-PREPRINT%20v3-blue.svg)]()

**Pascal Fichant** — Independent Researcher, Montpellier, Occitanie, France  
**PREPRINT v3** · doi: `10.5281/zenodo.19900557`

> **arXiv preprint version**: v3 (current public submission)  
> **Internal development version**: v7

---

## Overview

The **Topological Invariance Principle (TIP)** postulates that global
spatial flatness ($\Omega_{\rm total} \equiv 1$) is a fundamental
geometric gauge law of spacetime, not a coincidental initial condition.
Any primordial spin density injected prior to recombination generates a
strictly compensatory torsion debt, whose late-time residual is
identified as dark energy — without free parameters.

The TIP is a **geometric gauge postulate**, not a theorem derived from
the minimal ECKS Lagrangian. The numerical calibration ($\Omega_{\rm
spin}^{\rm peak} = 0.093$) is an observational input from Foundation I,
not a logical prerequisite of the principle.

---

## Einstein-Cartan Trilogy

| Paper | DOI | Role |
|---|---|---|
| **PIT Letter** *(this)* | [10.5281/zenodo.19900557](https://doi.org/10.5281/zenodo.19900557) | TIP gauge postulate, geometric dark energy |
| **Foundation I** | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | H₀–S₈–BAO calibration, Δχ²=−39.5 |
| **Foundation II** | [10.5281/zenodo.20629238](https://doi.org/10.5281/zenodo.20629238) | Baryogenesis, geometric dark sector, Micro-Knots |
| **Foundation III** | In preparation | Tensor spectrum, CLASS-EC, CMB peaks |

---

## The Core Equations

```
Ω_m + Ω_r + (Ω_spin + Ω_τ) ≡ 1    [TIP global constraint]
Ω_τ^(initial) = − Ω_spin^(peak)    [Initial condition]
Ω_spin(a) + Ω_τ(a) = 0             [Continuous compensation]
```

With the ECF calibration from Foundation I:

| Parameter | Value | Origin |
|---|---|---|
| Ω_spin^(peak) | +0.093 | F1 MCMC observational input |
| Ω_τ^(initial) | −0.093 | Frozen late-time as Dark Energy |
| w₀ | −0.904 | Geometric derivation |
| wₐ | −0.153 | Geometric derivation |
| F_ion | 1.2765 | F1 joint constraint |

### H₀ Tension Status

The H₀ Distance Network (H₀DN) Collaboration has confirmed
$H_0 = 73.50 \pm 0.81$ km/s/Mpc (arXiv:2510.23823), a community
consensus result at 7.1σ tension with flat ΛCDM — consistent with
the ECF calibration at 73.04 km/s/Mpc (0.6σ difference).

---

## What's New in PREPRINT v3 (internal v7)

| Change | Detail |
|---|---|
| TIP as geometric gauge postulate | Ω_spin = 0.093 is observational input from F1, not a logical prerequisite |
| DESI comparison qualified | Consistency check only, not a parameter-free prediction |
| H₀DN 73.50 added | arXiv:2510.23823, 7.1σ tension confirmed |
| Foundation II DOI | doi:10.5281/zenodo.20629238 (deposited June 2026) |
| Scope note strengthened | TIP is not calibrated to reproduce observed tensions |

---

## Repository Structure

```text
spin-torsion-cosmology/
├── Fondation_PIT/
│   ├── 01_Paper_Publication/
│   │   └── fichant_ecf_PIT_Letter_v7.pdf     ← internal v7 = PREPRINT v3
│   └── 02_Scientific_Code/
│       └── B_Paper_Plots/
│           ├── Figure_CosmicHistory_Omegas_PIT.png
│           └── plot_Cosmic_History_Omegas.py
├── requirements.txt
└── README_PIT_v7.md
```

---

## Reproducing the Figure

```bash
pip install -r requirements.txt
cd Fondation_PIT/02_Scientific_Code/B_Paper_Plots/
python plot_Cosmic_History_Omegas.py
```

Output: `Figure_CosmicHistory_Omegas_PIT.png`

> ⚠️ **Windows**: run `set PYTHONIOENCODING=utf-8` before any script.

---

## Compile

```bash
cd Fondation_PIT/01_Paper_Publication/
pdflatex fichant_ecf_PIT_Letter_v7.tex
bibtex   fichant_ecf_PIT_Letter_v7
pdflatex fichant_ecf_PIT_Letter_v7.tex
pdflatex fichant_ecf_PIT_Letter_v7.tex
```

Requires `revtex4-2` (standard APS distribution).

---

## Citation

```bibtex
@misc{FichantPIT2026,
  author    = {Fichant, Pascal},
  title     = {The Topological Invariance Principle: Dark Energy as
               a Geometric Constraint of Spatial Flatness in
               Einstein-Cartan Cosmology},
  year      = {2026},
  publisher = {Zenodo},
  version   = {v3},
  doi       = {10.5281/zenodo.19900557},
  url       = {https://doi.org/10.5281/zenodo.19900557},
  note      = {Companion papers:
               Foundation I doi:10.5281/zenodo.19577447;
               Foundation II doi:10.5281/zenodo.20629238.
               Code: https://github.com/pfichant/spin-torsion-cosmology}
}
```

---

**Contact**: p.fichant.research@gmail.com  
**GitHub**: https://github.com/pfichant/spin-torsion-cosmology  
**CC-BY-4.0** | Montpellier, Occitanie | June 2026

> *"Spatial flatness is not a coincidence — it is a law."*
