# Foundation I: The Metric Universe 🌌
### A Geometric Einstein-Cartan-Kibble-Sciama Cosmology

[![HAL](https://img.shields.io/badge/HAL-hal--xxxxxx-blueviolet.svg)](https://hal.science/hal-xxxxxx)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Repository for **"Foundation I: The Metric Universe"** (2026). Full reproducibility suite.

---

## 🔬 ECF Model

**Resolves $H_0$/$S_8$ tensions** via torsion-driven bounce + stiff phase ($\rho_{spin} \propto a^{-6}$).

**Key**: $\Delta \chi^2 = -39.5$ vs $\Lambda$CDM

---

## 🛠 Installation

```bash
git clone https://github.com/pfichant/spin-torsion-cosmology.git
cd spin-torsion-cosmology
pip install -r Foundation_1/requirements.txt
```

---

## 🚀 Reproducibility

```bash
cd Foundation_1
python run_all_simulations_F1.py
```

**Outputs** → `figures_output/` (paper figures HD)

---

## 📂 Structure
spin-torsion-cosmology/

└── Foundation_1/                    # F1 Root

    ├── 01_Paper_Publication/		 # Paper(s)
	├── 02_Scientific_Code/
    │   ├── A_Core_Calculations/     # ODE, torsion, χ²
    │   └── B_Paper_Plots/           # H0/S8, JWST, 21cm
    ├── figures_output/              # Paper figures HD
    ├── logs/                        # Audit trail
    ├── run_all_simulations_F1.py    # Master orchestrator
    ├── requirements.txt
    └── README.md
	
---

## 📊 Results

| Metric | Planck (ΛCDM) | ECF           |
|--------|---------------|---------------|
| **H₀** | 67.4 ± 0.5    | **73.04**     |
| **S₈** | 0.832 ± 0.013 | **0.766**     |
| **rₛ** | 147.1 Mpc     | **135.8 Mpc** |

---

## 📝 HAL Citation

```bibtex
@article{Fichant2026Foundation1,
  title={Foundation I: The Metric Universe -- Geometric ECF Cosmology},
  author={Fichant, Pascal},
  year={2026},
  note={HAL hal-05571311 | Code: Foundation_1/},
  url={https://hal.science/hal-05571311}
}
```

**Contact**: p.fichant.research@gmail.com

---
*CC-BY-4.0 | Montpellier | March 2026*
