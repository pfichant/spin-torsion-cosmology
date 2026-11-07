# spin-torsion-cosmology

Official Open Science repository for the Einstein-Cartan Framework (ECF) in cosmology. Contains numerical simulation codes, datasets (SPARC validation), and preprints for the Foundation papers.

Licence CC BY 4.0 · Pascal Fichant, independent researcher, Montpellier · `p.fichant.research@gmail.com`

---

## Contents

| Folder | Document | Concept DOI (always resolves to the latest version) |
|---|---|---|
| [`Foundation_PIT/`](Foundation_PIT) | *Exact Spatial Flatness and the Spin-Torsion Link* (Topological Invariance Principle letter) | [10.5281/zenodo.19798923](https://doi.org/10.5281/zenodo.19798923) |
| [`Foundation_1/`](Foundation_1) | *Foundation I: The Metric Universe* (Extended and PRD Short versions) | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) |
| [`Foundation_2/`](Foundation_2) | *Foundation II: The Chiral Universe* | [10.5281/zenodo.20629237](https://doi.org/10.5281/zenodo.20629237) |
| [`Foundation_3/`](Foundation_3) | *Foundation III — Cosmological Physics* | [10.5281/zenodo.22359982](https://doi.org/10.5281/zenodo.22359982) |
| [`Architecture/`](Architecture) | *Architecture of the Corpus* (FR and EN PDFs, version registers) | [10.5281/zenodo.22778507](https://doi.org/10.5281/zenodo.22778507) |

### Working preprints (not deposited on Zenodo, no DOI)

| Folder | Document | Status |
|---|---|---|
| [`Foundation_4/`](Foundation_4) | *Fondation IV : L'Univers Fertile* (in French) | working preprint v0.3 — exploratory programme |
| [`Strong_Gravity/`](Strong_Gravity) | *Fondation III : Gravité Forte et Géométrie des Objets Compacts* (in French) | working preprint v2.1 |
| [`Chiral_Bounce/`](Chiral_Bounce) | *The Cosmological Bounce as a Chiral Phase Transition* | working preprint v0.4 |

These three are not part of the deposited corpus; their figures are produced by the scripts listed in their READMEs (Foundation IV has its own scripts; the other two share those of Foundation III).

Each paper folder holds the PDF of the paper (`01_Paper_Publication/`), the scripts (`02_Scientific_Code/`) and its own README, which lists every script and the figure or number it produces. The PDFs are also deposited on Zenodo with each paper; the LaTeX sources are not published in this repository.

---

## Reproducing the figures

```bash
pip install numpy scipy matplotlib pandas sympy astropy emcee camb requests pillow imageio-ffmpeg plotly kaleido

cd Foundation_1 && python run_all_simulations_F1.py   # about 2 min
cd Foundation_2 && python run_all_simulations_F2.py   # about 8 min
cd Foundation_3 && python run_all_simulations_F3.py   # about 2 min
cd Foundation_PIT && python run_all_simulations_PIT.py
```

Each orchestrator runs every script of its folder, logs each run to `logs/`, and copies the figures into `figures_output/`. At start-up it deletes the images left in the script folders by a previous run, so that `figures_output/` only holds figures from the current run; data files are never touched.

Notes:
- Two Foundation II figures are drawn with `plotly`, whose image export (`kaleido`) needs Chrome or Chromium.
- `Foundation_1/figures_output/figure_ecf_gw_spectrum_F2.png` is the figure Foundation I includes as `figure_ecf_gw_spectrum.png`.
- The two DESI figures of Foundation III are those produced in `Foundation_1/figures_output/`.

Data: the SPARC rotation curves used by Foundation II are in `Foundation_2/`; the DESIVAST DR1 void catalogue files used by Foundation III are in `Foundation_3/data/` (larger V2 catalogues are not redistributed; see the script headers for the download address).

---

## Scope and limits

The repository holds the scripts that **reproduce** the published values, not necessarily all those that **produced** them: some upstream parameter searches and calibrations are not included. Values are labelled in the papers as derived, calibrated, calculated-conditional, historical or open; the scripts print these labels where they apply. Superseded scripts are kept in `Scripts_SUPERSEDED/` folders for traceability and are not run by the orchestrators.
