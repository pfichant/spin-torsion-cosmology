# The Topological Invariance Principle (TIP) — Companion Letter

> **"The Topological Invariance Principle: Dark Energy as a Geometric  
> Constraint of Spatial Flatness in Einstein-Cartan Cosmology"**  
> Pascal Fichant — Independent Researcher, Montpellier, France  
> Preprint (2026) — Zenodo: `10.5281/zenodo.XXXXXXX` *(to be updated upon deposition)*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## Overview

This repository contains the LaTeX source and figure-generation script
for the **PIT Letter**, the conceptual foundation of the Einstein-Cartan trilogy:

| Paper | Role |
|---|---|
| **PIT Letter** *(this repo)* | Formal statement of the Topological Invariance Principle as a gauge law |
| **Foundation I** | Phenomenological calibration: H₀–S₈ joint resolution, sound horizon |
| **Foundation II** | Geometric dark sector: baryogenesis, Macro-Knots, cosmic alignment |

The **Topological Invariance Principle (TIP)** postulates that global
spatial flatness (Ω_total ≡ 1) is a fundamental gauge law of spacetime,
not a coincidental initial condition. Any primordial spin density
injected prior to recombination generates a strictly compensatory
torsion debt, whose late-time residual is identified as Dark Energy.

---

## Repository Structure

```text
Fondation_PIT/
├── 01_Paper_Publication/
│   └── fichant_ecf_PIT_Letter_v1.pdf     # Paper PDF
├── 02_Scientific_Code/
│   └── B_Paper_Plots/
│       ├── Figure_CosmicHistory_Omegas_PIT.png    # Main figure (TIP version)
│       └── plot_Cosmic_History_Omegas.py          # Figure generation script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## The Core Equations

The TIP extends the Friedmann flatness constraint to include the
spin-torsion conjugate pair:

```text
Ω_m + Ω_r + (Ω_spin + Ω_τ) ≡ 1    [TIP global constraint]
Ω_τ^(initial) = − Ω_spin^(peak)    [Initial condition]
Ω_spin(a) + Ω_τ(a) = 0             [Continuous compensation]
```

With the ECF calibration from Foundation I (DOI: 10.5281/zenodo.19577447):
- `Ω_spin^(peak) ≈ +0.093`  at  `z ≈ 7500`
- `Ω_τ^(initial) ≈ −0.093`  →  frozen at late times as Dark Energy
- Effective equation of state: `w₀ ≈ −0.904`, `w_a ≈ −0.153`

---

## Reproducing the Figure

The single figure (`Figure_CosmicHistory_Omegas_PIT.png`) shows the
temporal evolution of all fractional densities Ω_i(a) under the TIP.

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Generate the figure:**
```bash
cd Fondation_PIT/02_Scientific_Code/B_Paper_Plots/
python plot_Cosmic_History_Omegas.py
```

Output: `Figure_CosmicHistory_Omegas_PIT.png` (ready for LaTeX inclusion).

---

## Compile the Letter

```bash
cd Fondation_PIT/01_Paper_Publication/
pdflatex fichant_ecf_PIT_Letter_v1.tex
bibtex fichant_ecf_PIT_Letter_v1
pdflatex fichant_ecf_PIT_Letter_v1.tex
pdflatex fichant_ecf_PIT_Letter_v1.tex
```

Requires a standard LaTeX distribution with `revtex4-2` (APS journals).

---

## Companion Papers

| Paper | DOI | Role |
|---|---|---|
| **Foundation I** — *The Metric Universe* | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) | H₀–S₈–BAO trilemma, sound horizon, χ²=−39.5 |
| **Foundation II** — *The Chiral Universe* | In preparation | Baryogenesis, Macro-Knots dark matter, cosmic alignment |

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
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX},
  note         = {Companion Letter to Foundation I (doi:10.5281/zenodo.19577447)}
}
```

---

## Open Science

All source code, figure scripts, and paper source are publicly available
under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

> *"Spatial flatness is not a coincidence — it is a law."*
