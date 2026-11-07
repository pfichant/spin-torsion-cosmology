# Einstein-Cartan Framework — Architecture of the Corpus

### Genealogy of the building blocks, parameters and derivations

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Pascal Fichant** — Independent Researcher, Montpellier, Occitanie, France
**v2** (internal revision 1.5) · October 2026 · **72 pp. (FR) · 71 pp. (EN), including cover**
Concept doi: [10.5281/zenodo.22778507](https://doi.org/10.5281/zenodo.22778507) (always resolves to the latest version)

> **Both language versions are deposited together.** The French is the source;
> the English is a full translation of French version 2, checked for structural
> parity (headings, tables, equations and numerical values). In case of
> divergence, the French text prevails.
>
> **Deposited files**: `ECF_Architecture_v2_FR_AVEC_COUVERTURE.pdf` (72 pages
> including cover) and `ECF_Architecture_v2_EN_AVEC_COUVERTURE.pdf` (71 pages
> including cover). Supersedes v1 of 15 September 2026
> (version doi:[10.5281/zenodo.22778508](https://doi.org/10.5281/zenodo.22778508)).

---

## Corrections made after the first drafting of this README (22–24 October 2026)

- **Pages: 72 (FR) / 71 (EN), including cover** (73 / 72 in the 24/10/2026 files; see the register §5, entry of 30/10/2026).
- **Spin branch (23/10/2026).** The spin phase is no longer called « brief » without reserve: the calibration needs the a⁻⁶ law up to z ~ 10⁵ and the same branch is excluded by BBN at 1 MeV (PO-ECF-BBN-SPIN, open); the « Hubble tension » row is CONDITIONAL on this. See Foundation I, « Domain of validity of the calibrated branch ».
- **Aligned with the papers (22–23/10/2026).** The ECKS bounce is not said to « escape » the NEC critique (the spin–torsion term itself carries the violation); MICROSCOPE is a measurement compatible with zero; KiDS-1000 S₈ = 0.766 (+0.020/−0.014); ACT DR6 birefringence is published (PRD 113, L101302); Mars Sample Return cancelled (NASA budget, January 2026); the globular-cluster age is a lower bound on t₀; LISA alone is nearly blind to the net polarisation of an isotropic background; equivalence-principle rows state that no relation to s₀ is established; the LRD case states that the ECF fixes no redshift window (observed LRDs: z ~ 4–9).
- **Lithium 7.** Remains a deferred lead, not an established result of the corpus (Foundation II states that no mechanism is retained).

The version register (§5, dated entries 20–24/10/2026) is the authority for each change; where this README and the register differ, the register and the PDF prevail.

---

## What changed in v2 (this version)

v2 brings the Architecture in line with the post-audit v2 baseline of the
corpus (22/09/2026) and with the October 2026 versions of the deposited
papers. Every change of value or status is listed, with its reason, in the
**version register and erratum** deposited in the same October 2026 lot
(§3, rows listing "Architecture"; §5, "Architecture (French and English)"). In case of
discrepancy, the text of the papers prevails.

**Values and statuses propagated from the corpus** (register §3):

| Item | v2 value and status |
|---|---|
| Ω_m of the ECF background | **0.2669** (= ω_m/h², h = 0.7304); 0.315 kept only as Planck/historical reference |
| Ω_Λ | **0.733**, `CALCULATED-CONDITIONAL` (arithmetic closure of the budget) |
| Age t0 (w = −1 background) | **13.33 Gyr**, compatible with t_GC = 13.32 ± 0.10 (stat) ± 0.5 (syst) Gyr (Valcin et al. 2020); a compatibility check, not a 0.1σ test. The former age-tension narrative is abandoned (`HISTORICAL`) |
| Age at recombination (z* = 1089.9) | **368.4 kyr** with the spin term (`script_09_cosmic_ages.py`, branch `with_spin`), against 371.3 kyr in ΛCDM |
| Deceleration/acceleration transition | z_t(ECF) ≈ **0.76** on the A-7 background, against 0.63 for the Planck reference; `CALCULATED-CONDITIONAL` |
| BAO target at z = 1.48 (D_M/r_d) | **30.21 ± 0.79** (eBOSS DR16 QSO); the former 30.85 ± 0.80 is `WITHDRAWN` |
| BOSS DR12 errors (z = 0.38 / 0.51 / 0.61) | **0.166 / 0.206 / 0.251** (statistical and systematic combined) |
| χ²_BAO (4 bins, diagonal) | **12.11 (ECF) against 1.79 (ΛCDM)**, Δχ² ≃ +10.3, `CALCULATED-CONDITIONAL`; the active background tension now lies in the BAO/DESI sector |
| r_drag | no identification r_s = r_d is assumed; `PO-ECF-BAO-RDRAG` `OPEN` |
| Mahalanobis distance ECF – DESI DR1 | **2.03σ** (Planck prior) / **6.98σ** (SH0ES prior), full covariance, 12 observables |
| (w0, wa) | (−0.904, −0.153), `CALIBRATED`, calibration point **without error bar**; ξ = 1.645 is calibrated on the DESI preference used by the ECF |
| S8 | 0.766 is the **KiDS-1000 observational target**, not an ECF output; the ECF growth prediction is `OPEN` |
| Π_GW (chiral asymmetry of gravitational waves) | **0.20 ± 0.05, `CALIBRATED TEMPLATE`** |
| Large-void threshold (VSF) | ξ_KZ = **60 comoving Mpc**; 40.4 Mpc/h is the conversion at h_fid = 0.6732 of the DESIVAST catalogue |
| f_NL^KZ | **> 0, value open** (the former ≈ 0.09 projection is withdrawn) |
| Roman microlensing | two durations distinguished: ≈ 1.05 h (individual Micro-Knot) and ≈ 6.27 h (aggregate at the λ = 36 benchmark) |
| Instruments | LISA launch planned around 2035; DOE/NSF support for CMB-S4 ended (July 2025) |
| Bounce equation H² = (8πG/3) ρ (1 − ρ/ρc) | **exact** for fermionic dust in the spin-fluid description, **schematic** elsewhere; per-regime form added. In the stiff phase the spin term alone does not produce a bounce (`PO-ECF-ACTION-BOUNCE`, `OPEN`) |
| Acceleration equation | ä/a = −(4πG/3)[ρ(1 − 4ρ/ρc) + 3p(1 − 2ρ/ρc)], exact for p = 0 |
| Popławski 2012, Eq. (12) | qualified: Dirac description, in which dust does not bounce; the ECF uses the spin-fluid branch |
| Static-core bound ρ_core < ρc/2 | **conditional** on the form ρ(1 − ρ/ρc), exact for dust only |

**Changes specific to the Architecture** (register §5):

- **temporal** orientation of the axial-torsion expectation value, ⟨S_μ⟩ = s0 δ_μ⁰;
- truncated sentence of § 4.6 reconstructed;
- names of the producing scripts;
- density convention stated: ω_m = ω_b + ω_c does not count massive neutrinos
  (treated as massless radiation); with them, Ω_m = 0.2681 instead of 0.2669
  (t0 shorter by 0.016 Gyr, diagnostic only).

**Structure** (visible in the document itself):

- the narrative and navigation are reorganised (summary, "the corpus at a
  glance", quick start, three reading depths);
- a foreword inviting readers to comment on the Architecture or on any paper
  of the corpus, with the procedure in a new **Appendix G**;
- a new **Appendix H**: editorial traceability and the post-audit v2
  canonical baseline;
- Appendix D lists the October 2026 versions of the papers it uses;
- in the table of derived mechanisms, the bounce is no longer marked
  "demonstrated" (exact for dust, `OPEN` in the stiff phase,
  `PO-ECF-ACTION-BOUNCE`), and parity breaking at the bounce takes the status
  of the chiral crystallisation it derives from (`CALCULATED-CONDITIONAL`).

No open problem is closed by rewording. Quantities that depend on a
perturbation solver (Planck block, θ*, global Δχ², global AIC/BIC) are **not
recomputed**; their earlier values are `HISTORICAL`.

---

## What this document is

A **reference map of the Einstein-Cartan Framework corpus**. For each result,
it makes explicit which established theory is borrowed, from whom, and what
the framework adds.

⚠️ **It is not a paper.** It states no new result, derives nothing, and
proves nothing. Everything it reports is sourced to one of the four deposited
papers — which remain the authority whenever the two disagree.

---

## What it is for

Reading a 300-page corpus to answer *« is this quantity derived or
calibrated? »* costs hours. This document answers that class of question
directly, with the source.

| You want to know | Go to |
|---|---|
| What each paper covers, and what it does **not** | Appendix A |
| A symbol, its value, and **its status** | Appendix B |
| Which references are borrowed, and verified | Appendix C |
| Which version of each paper is used here | Appendix D |
| How to query the corpus in natural language | Appendix E |
| The method behind a given prediction | Appendix F |
| How to comment on the Architecture or on a paper | Appendix G |
| The editorial history and the post-audit v2 baseline | Appendix H |

---

## ⭐ The question this document is built to answer

> *« Which quantities are derived from the action, which are calibrated,
> which are predictions? »*

Every entry in Appendix B carries one of these labels. A few examples, to
show the document does not flatter the framework:

| Quantity | Status |
|---|---|
| $w = -1$ (static dark energy) | **derived** in the adopted effective action — static branch of the torsion condensate (Foundation II, Appendix J) |
| $F_{\rm ion} = 1.2765 \pm 0.0246$ | `CALIBRATED` — effective amplitude of the background; does not by itself predict $S_8$ |
| $(w_0, w_a) = (-0.904, -0.153)$ | `CALIBRATED` — calibration point without error bar, not a prediction independent of DESI |
| $S_8 = 0.766$ | KiDS-1000 **observational target**, not an ECF output; ECF growth prediction `OPEN` |
| $\beta \neq 0$ (birefringence) | **prediction** (non-zero rotation); the magnitude $\approx 0.35°$ is `CALIBRATED` on the Minami–Komatsu anchor; the sign is not claimed as derived |
| $\eta \simeq 5.9\times10^{-10}$ | **semi-derived** — coupling calibrated on Foundation I; complete kinetic chain `OPEN` |
| $n_s$ | **not predicted** — inherited, on the same footing as $\Omega_b$ (`PO-F3-NS`) |
| $\xi_{\rm KZ} \simeq 60$ Mpc | `CALIBRATED`, not derived *ab initio* (`PO-F3-XI`) |

⭐ **A withdrawn claim stays visible.** Earlier versions announced a
prediction $n_s \simeq 1$ and an $8.4\sigma$ tension with Planck; both rested
on a wrong identification of the Wands duality and are withdrawn. The
document says so (Appendix E). The 1D torsion-string sector is not retained
as an established component (open problem `PO-F2-8`); Corollary F3-1, which
relied on 1D strings connecting the walls, was withdrawn on 30/08/2026.

---

## The corpus it maps

| Paper | Concept DOI |
|---|---|
| **PIT Letter** | [10.5281/zenodo.19798923](https://doi.org/10.5281/zenodo.19798923) |
| **Foundation I** — cosmological background (Extended and PRD Short) | [10.5281/zenodo.19577447](https://doi.org/10.5281/zenodo.19577447) |
| **Foundation II** — geometric dark sector | [10.5281/zenodo.20629237](https://doi.org/10.5281/zenodo.20629237) |
| **Foundation III** — Cosmological Physics | [10.5281/zenodo.22359982](https://doi.org/10.5281/zenodo.22359982) |

> All four are **concept DOIs**: they resolve to the latest version of each
> deposit. ⚠️ The counterpart is worth knowing: a numerical value quoted here
> matches the version listed in Appendix D (PIT Letter v9, Foundation I v8,
> Foundation II v5, Foundation III — Cosmological Physics v3, all October
> 2026), which may not be the one a concept DOI resolves to at a later date.

Three companion documents — *Strong Gravity*, *Chiral Bounce*, *Foundation IV
— Fertile* — are outside this document's scope; they are **in preparation,
not yet publicly deposited**.

---

## Reproducibility

Every quantity cited points to the script that computes it:
[github.com/pfichant/spin-torsion-cosmology](https://github.com/pfichant/spin-torsion-cosmology)
(CC-BY-4.0).

⚠️ **A limitation stated plainly**, as in Foundation I: the repository holds
the scripts that **reproduce** the published values, not necessarily those
that **produced** them. Upstream parameter searches and MCMC calibrations are
not all included. Each value can be checked for internal consistency; the
calibration itself is not always re-runnable as it stands.

---

## Building the PDF

The PDFs are built from the Markdown sources
(`ECF_Architecture_v2_FR_SOURCE.md`, `ECF_Architecture_v2_EN_SOURCE.md`) with
pandoc and XeLaTeX; the build scripts are `build_pdf_0610.py` (French) and
`build_pdf_EN_0710.py` (English).

French/English parity was checked on the sources before deposit: same number
of headings (90), table rows (334), equation tags (24), anchors (29) and
internal links (77), and identical numerical values once French decimal commas
are converted. The English build script is `build_pdf_EN_0710.py`.

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **v2** (rev. 1.5) | October 2026 | French (72 pp.) and English (71 pp.) deposited together, including cover. Alignment on the post-audit v2 baseline and on the October 2026 versions of the papers (see "What changed in v2"); Appendices G and H added. English translated from French v2. |
| v1 (rev. 1.2) | 15 September 2026 | First deposit, French (62 pp.) and English (59 pp.) deposited together; the English was a full translation, checked for structural parity with the French by `build_architecture.py`, complemented by a hand check that found and fixed two asymmetries. |

---

## Citation

```bibtex
@misc{FichantArchitecture2026,
  author    = {Fichant, Pascal},
  title     = {Einstein-Cartan Framework: Architecture of the Corpus ---
               Genealogy of the Building Blocks, Parameters and Derivations},
  year      = {2026},
  publisher = {Zenodo},
  version   = {v2},
  doi       = {10.5281/zenodo.22778507},
  url       = {https://doi.org/10.5281/zenodo.22778507},
  note      = {PREPRINT v2 (revision 1.5), October 2026. French and English
               versions deposited together.
               Concept DOI, resolves to the latest version.
               Maps the corpus: PIT Letter doi:10.5281/zenodo.19798923;
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

> *"Which established theory is borrowed, from whom, and what does the
> framework add — stated for each result, including where the answer is
> 'nothing yet'."*
