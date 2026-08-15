# The Topological Invariance Principle (TIP) — PIT Letter v2

> **"The Topological Invariance Principle: Dark Energy as a Geometric
> Constraint of Spatial Flatness in Einstein-Cartan Cosmology"**
> Pascal Fichant — Independent Researcher, Montpellier, France
> Preprint (2026)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19900557.svg)](https://doi.org/10.5281/zenodo.19900557)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-v2-blue.svg)]()

---

## Overview

This repository contains the LaTeX source and figure-generation script
for the **PIT Letter**, the conceptual foundation of the Einstein-Cartan trilogy:

| Paper | Role | DOI |
|---|---|---|
| **PIT Letter** *(this repo)* | Formal statement of TIP as a gauge law | [10.5281/zenodo.19900557](https://doi.org/10.5281/zenodo.19900557) |
| **Foundation I** | Phenomenological calibration: H₀–S₈–BAO | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) |
| **Foundation II** | Geometric dark sector: baryogenesis, Macro-Knots, PGT condensate | In preparation |

The **Topological Invariance Principle (TIP)** postulates that global
spatial flatness (Ω_total ≡ 1) is a fundamental gauge law of spacetime,
not a coincidental initial condition. Any primordial spin density
injected prior to recombination generates a strictly compensatory
torsion debt, whose late-time residual is identified as Dark Energy.

---

## 🆕 What's new in v2

| Change | Impact |
|---|---|
| Foundation I DOI added in companion table | Full trilogy cross-referencing |
| `\bibitem{FichantPIT2026}` updated with `doi:10.5281/zenodo.19900557` | Self-citation corrected in F1 v2 |
| HAL references removed throughout | Zenodo-only deposition |

---

## The Core Equations

The TIP extends the Friedmann flatness constraint to include the
spin-torsion conjugate pair:

```text
Ω_m + Ω_r + (Ω_spin + Ω_τ) ≡ 1    [TIP global constraint]
Ω_τ^(initial) = − Ω_spin^(peak)    [Initial condition]
Ω_spin(a) + Ω_τ(a) = 0             [Continuous compensation]
```

With the ECF calibration from Foundation I:
- `Ω_spin^(peak) ≈ +0.093`  at  `z ≈ 7500`
- `Ω_τ^(initial) ≈ −0.093`  →  frozen at late times as Dark Energy
- Effective equation of state: `w₀ ≈ −0.904`, `w_a ≈ −0.153`

---

## Repository Structure

```text
spin-torsion-cosmology/
├── Fondation_PIT/
│   ├── 01_Paper_Publication/
│   │   ├── fichant_ecf_PIT_Letter_v1.pdf     # Paper PDF (archive)
│   │   └── fichant_ecf_PIT_Letter_v2.pdf     # Paper PDF (current)
│   └── 02_Scientific_Code/
│       └── B_Paper_Plots/
│           ├── Figure_CosmicHistory_Omegas_PIT.png  # Main figure
│           └── plot_Cosmic_History_Omegas.py        # Figure generation script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Reproducing the Figure

```bash
pip install -r requirements.txt
cd Fondation_PIT/02_Scientific_Code/B_Paper_Plots/
python plot_Cosmic_History_Omegas.py
```

Output: `Figure_CosmicHistory_Omegas_PIT.png` (ready for LaTeX inclusion).

> ⚠️ **Windows users**: run `set PYTHONIOENCODING=utf-8` before launching
> any script to avoid Unicode encoding errors on the console output.

---

## Compile the Letter

```bash
cd Fondation_PIT/01_Paper_Publication/
pdflatex fichant_ecf_PIT_Letter_v2.tex
bibtex   fichant_ecf_PIT_Letter_v2
pdflatex fichant_ecf_PIT_Letter_v2.tex
pdflatex fichant_ecf_PIT_Letter_v2.tex
```

Requires a standard LaTeX distribution with `revtex4-2` (APS journals).

---

## Companion Papers

- **Foundation I** — *The Metric Universe — Extended Version*
  ECF background solution, sound horizon, H₀–S₈–BAO trilemma, birefringence.
  DOI: [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | GitHub: `Foundation_1/`

- **Foundation II** — *The Chiral Universe and the Three Fossils of the Bounce*
  Baryogenesis, Macro-Knots dark matter, PGT condensate, cosmic alignment.
  GitHub: `Foundation_2/` *(in preparation)*

---

## Citation

```bibtex
@misc{FichantPIT2026,
  author       = {Fichant, Pascal},
  title        = {The Topological Invariance Principle: Dark Energy as
                  a Geometric Constraint of Spatial Flatness in
                  Einstein-Cartan Cosmology},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {v2},
  doi          = {10.5281/zenodo.19900557},
  url          = {https://doi.org/10.5281/zenodo.19900557},
  note         = {Companion papers: Foundation I doi:10.5281/zenodo.19577447;
                  Foundation II (in preparation).
                  Code: https://github.com/pfichant/spin-torsion-cosmology}
}
```

---

## Open Science

All source code, figure scripts, and datasets are publicly available
under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Contact**: p.fichant.research@gmail.com

---
*CC-BY-4.0 | Montpellier | April 2026*

> *"Spatial flatness is not a coincidence — it is a law."*
