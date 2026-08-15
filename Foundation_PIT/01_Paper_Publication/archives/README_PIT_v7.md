# The Topological Invariance Principle (TIP) — PIT Letter 🌌
### Dark Energy as a Geometric Constraint of Spatial Flatness in Einstein-Cartan Cosmology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19798923.svg)](https://doi.org/10.5281/zenodo.19798923)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-PREPRINT%20v4-blue.svg)]()

**Pascal Fichant** — Independent Researcher, Montpellier, Occitanie, France  
**PREPRINT v4** · concept doi: `10.5281/zenodo.19798923` (always resolves to the latest version)

> **Zenodo version**: v4 (current public deposit)  
> **Internal development version**: v7  
> **arXiv**: not yet submitted (endorsement pending for gr-qc)

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
| **PIT Letter** *(this)* | [10.5281/zenodo.19798923](https://doi.org/10.5281/zenodo.19798923) | TIP gauge postulate, geometric dark energy |
| **Foundation I** | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | H₀–S₈–BAO calibration, Δχ²=−39.5 |
| **Foundation II** | [10.5281/zenodo.20629237](https://doi.org/10.5281/zenodo.20629237) | Baryogenesis, geometric dark sector, Micro-Knots |
| **Foundation III (extended)** | In preparation (translation) | Strong gravity, wormhole, vacuum thermodynamics |
| **Chiral-bounce paper** | Zenodo (deposit pending) | Bounce as a chiral phase transition — LG mechanism + Cartan core |

> All cross-paper DOIs above are **concept DOIs**: they always resolve to
> the most recent version of each paper, never to a frozen one.

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

## What's New in PREPRINT v4 (internal v7)

| Change | Detail |
|---|---|
| TIP as geometric gauge postulate | Ω_spin = 0.093 is observational input from F1, not a logical prerequisite |
| DESI comparison qualified | Consistency check only, not a parameter-free prediction |
| H₀DN 73.50 added | arXiv:2510.23823, 7.1σ tension confirmed |
| Epoch labels clarified | The QCD transition (T~200 MeV) is stated as the *physical origin* of the spin fluid, kept distinct from its much later *observational calibration point*; no numerical value affected |
| Cross-paper DOIs → concept DOIs | Foundation II now cited as 10.5281/zenodo.20629237 and this Letter as 10.5281/zenodo.19798923; previous entries pointed to frozen version DOIs |
| Scope note strengthened | TIP is not calibrated to reproduce observed tensions |

---

## Repository Structure

```text
spin-torsion-cosmology/
├── Foundation_PIT/
│   ├── 01_Paper_Publication/
│   │   └── fichant_ecf_PIT_Letter_v7.pdf     ← internal v7 = PREPRINT v4
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
cd Foundation_PIT/02_Scientific_Code/B_Paper_Plots/
python plot_Cosmic_History_Omegas.py
```

Output: `Figure_CosmicHistory_Omegas_PIT.png`

> ⚠️ **Windows**: run `set PYTHONIOENCODING=utf-8` before any script.

---

## Compile

```bash
cd Foundation_PIT/01_Paper_Publication/
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
  version   = {v4},
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
**CC-BY-4.0** | Montpellier, Occitanie | July 2026

> *"Spatial flatness is not a coincidence — it is a law."*
