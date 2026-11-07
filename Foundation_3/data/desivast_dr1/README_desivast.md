# DESIVAST DR1 void catalogues — mirror for the ECF VSF test

This directory mirrors the DESIVAST value-added catalogue used by the
Einstein–Cartan Framework void-size-function test, so that the analysis can be
reproduced without re-deriving where the data came from.

**These files are not ours.** They are redistributed unchanged for
reproducibility; the science, the algorithms and the credit belong to the
DESIVAST team.

## Provenance

| | |
|---|---|
| Source | `https://data.desi.lbl.gov/public/dr1/vac/dr1/desivast/v1.0/` |
| Documentation | `https://data.desi.lbl.gov/doc/releases/dr1/vac/desivast/` |
| VAC paper | Rincon *et al.*, *DESIVAST: Catalogs of Low-redshift Voids using Data from the DESI DR1 Bright Galaxy Survey*, ApJ (2025), [arXiv:2411.00148](https://arxiv.org/abs/2411.00148) |
| Generating code | `https://github.com/hbrincon/DESIVAST` |
| Fiducial cosmology | Planck 2018, `h = 0.6732` — radii are in Mpc/*h* |
| Sample | volume-limited DESI Y1 BGS Bright, `z < 0.24`, `M_r < −20` |

Please cite Rincon *et al.* if you use these catalogues, and prefer the DESI
server as the primary source.

## Files

| File | Size | Voids | max `RADIUS` (Mpc/*h*) |
|---|---|---|---|
| `DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits` | 3.9 MB | 3 765 maximal spheres | 31.69 (`R_EFF`) |
| `DESIVAST_BGS_VOLLIM_VoidFinder_SGC.fits` | 0.6 MB | — | — |
| `DESIVAST_BGS_VOLLIM_V2_VIDE_NGC.fits` | 459 MB | 1 258 | 55.88 |
| `DESIVAST_BGS_VOLLIM_V2_VIDE_SGC.fits` | 62 MB | 220 | 38.30 |
| `DESIVAST_BGS_VOLLIM_V2_REVOLVER_NGC.fits` | 612 MB | 1 692 | 43.50 |
| `DESIVAST_BGS_VOLLIM_V2_REVOLVER_SGC.fits` | 87 MB | 300 | 35.76 |

VoidFinder files hold `MAXIMALS` and `HOLES` HDUs, with both `RADIUS` (maximal
sphere) and `R_EFF` (effective radius of the void). The V² files hold `VOIDS`,
`ZONEVOID`, `GALZONE`, `TRIANGLE` and `GALVIZ`; the void radii are the `RADIUS`
column of `VOIDS`, which reproduces the published maxima exactly.

The V² files are large because they carry the galaxy–zone membership of the
watershed, not because the void catalogue itself is large: `VOIDS` has a few
hundred to a couple of thousand rows.

## ⚠️ The one thing to know before using the V² maxima

The V² catalogues reach further than VoidFinder — 55.9 against 31.7 Mpc/*h* —
but **the large V² voids are truncated by the survey boundary**. Each void
carries `TOT_AREA` and `EDGE_AREA`, so the boundary fraction
`f = EDGE_AREA / TOT_AREA` is directly available. In V²/VIDE NGC:

| cut on `f` | voids kept | max radius |
|---|---|---|
| `f ≤ 0.00` | 105 | 30.20 |
| `f ≤ 0.05` | 191 | 33.51 |
| `f ≤ 0.10` | 269 | 43.46 |
| `f ≤ 0.25` | 884 | 55.58 |
| no cut | 1 258 | 55.88 |

Of the eight voids above 43.8 Mpc/*h*, the cleanest still has **10.6 %** of its
surface on the boundary and the largest has **31.6 %**. A void cut by the survey
edge has an ill-constrained volume and therefore an overestimated effective
radius, which is why a void size function must exclude such objects — the
DESIVAST analysis is stricter still, reporting 297 interior voids for V²/VIDE
where `f ≤ 0.25` would retain 884.

Quoting a maximum radius from these catalogues without stating the boundary
criterion is misleading, in either direction.

## Layout and reproducing

The catalogues live under

```
Foundation_3/data/desivast_dr1/
```

a single visible data folder at the repository root, independent of which
`02_Scientific_Code` category subfolder (`A_Core_Calculations`,
`B_Paper_Plots`, `C_Simulations`) an analysis script happens to live in.
From `B_Paper_Plots/` (where `check_vsf_v2_edge_voids.py` and
`build_vsf_observed_dr1.py` currently live):

```
python3 check_vsf_v2_edge_voids.py
```

No argument is needed: the script computes the repository root from its own
location and looks in `data/desivast_dr1/` there first, then falls back to
a few older conventions (beside itself, the current directory) for anyone
who has not moved their files to the canonical location yet. Pass
`--dir PATH` to override.

It prints the maximum void radius as a function of the cut on the boundary
fraction `f`, and falls back to recorded values when the FITS files are absent —
so the numbers quoted in the papers stay inspectable whether or not a reader
downloads 1.2 GB.

Two companion scripts are included for inspection rather than for the result:
`extract_v2_radii.py` (radii and threshold counts, all catalogues) and
`inspect_edge_area.py` (the boundary-fraction distribution and the largest voids,
one by one).

## Licence

The catalogues are DESI public data and remain under DESI's terms; see the DESI
data release pages. This README and the analysis scripts are CC-BY 4.0.
