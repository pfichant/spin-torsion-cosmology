# Superseded scripts — kept for traceability

These scripts are **not run** by `run_all_simulations_F3.py` and must not be used to reproduce the published values.

- `plot_F3_ecf_desi_mcmc_v3.py` was withdrawn on 09/10/2026. It still carries two QSO rows (D_M/r_d and D_H/r_d) attributed to DESI DR1, but DESI DR1 does not publish them (MIXED-DATA / PROVENANCE INVALID, audit decision Q2 of 22/09/2026). The two DESI figures of *Cosmological Physics* (`Fig_ECF_DESI_Contours.png`, `Fig_ECF_DESI_Residuals.png`) are the ones produced by `Foundation_1/02_Scientific_Code/B_Paper_Plots/plot_ecf_desi_mcmc_v3_0.py`. That script uses the reconstructed 12-observable DESI DR1 block, and its figures are identical to those of the paper.

The corpus archives rather than deletes: a file here means "replaced", not "wrong at the time".
