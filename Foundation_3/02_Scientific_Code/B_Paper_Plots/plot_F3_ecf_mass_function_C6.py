#!/usr/bin/env python3
"""
plot_F3_ecf_mass_function_C6.py
===============================
ECF Foundation III — Strong Gravity — PO-F3-C6
Poisson coalescence mass function of the Micro-Knot network.
Author: Pascal Fichant
Date:   25 August 2026

PHYSICS  (all of it taken from F3 Strong Gravity, subsec. PO-F3-C6;
          nothing here is invented for the figure)
-----------------------------------------------------------------
The KZ network of Micro-Knots is already established as a 3D Poisson
point process of density n_KZ = xi_KZ^-3 (same process that yields
f_NL^KZ = +5/18 in F3 Cosmological Physics).

Coalescence is therefore a Poisson count. In a coalescence radius
R_coal(z):

    N ~ Poisson(lambda),   lambda = n_KZ * (4/3) pi R_coal(z)^3   [eq:lambda_coal]

and the resulting mass is M = N * M_micro, so the ECF mass function is
the Poisson law reparameterised in mass:

    n_ECF(M) dM  ∝  lambda^(M/M_micro) e^-lambda / (M/M_micro)!    [eq:n_ECF_poisson]

to be compared with the Gaussian form (Press-Schechter / Sheth-Tormen)
obtained for a continuous density field.

TESTABLE SIGNATURE
------------------
The Poisson law has exact skewness 1/sqrt(lambda), positive for every
finite lambda — the same statistical property that gives kappa_3 = sigma^2
and f_NL^KZ = +5/18 > 0. This is NOT a second ad hoc mechanism but the
same Poisson process seen at the scale of the mass function.

VALUES VERIFIED AGAINST THE PAPER (25/08/2026, before plotting)
---------------------------------------------------------------
    lambda    skewness 1/sqrt(lambda)    paper
    2         0.71                       0.71   OK
    5         0.45                       0.45   OK
    10        0.32                       0.32   OK
    100       0.10                       0.10   OK
    excess n_ECF/n_PS at M = 3<M>, lambda = 5 : 19.41  -> paper "x19"  OK

WHAT IS *NOT* CLOSED (stated in the paper, not to be overclaimed here)
----------------------------------------------------------------------
This lemma is a qualitative advance on PO-F3-C6, NOT its closure:
  (0) the n_KZ normalisation vs the real dark-matter density is unresolved;
  (a) R_coal(z) is a free, uncalibrated parameter, blocked by (0);
  (b) eq:n_ECF_poisson is not yet normalised to the observed baryon density;
  (c) no quantitative comparison to cluster mass functions yet.
=> lambda is therefore shown as an ILLUSTRATIVE range, never as a
   calibrated prediction. The figure carries that statement.

OUTPUT: Fig_ECF_MassFunction_C6.png (300 dpi, white background)
"""

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import poisson, norm

OUT = Path(__file__).with_name("Fig_ECF_MassFunction_C6.png")
DPI = 300

LAMBDAS = [2, 5, 10, 100]          # illustrative range, cf. paper table
LAM_TAIL = 5                       # panel C works at lambda = 5
COLORS = {2: "#4c72b0", 5: "#d62728", 10: "#2ca02c", 100: "#8c6d31"}

plt.rcParams.update({
    "font.size": 9,
    "axes.titlesize": 9.5,
    "axes.labelsize": 9,
    "legend.fontsize": 7.5,
    "figure.facecolor": "white",
})


# ---------------------------------------------------------------------
def check_against_paper():
    """Refuse to plot numbers that disagree with the paper."""
    print("Verification against F3 Strong Gravity, subsec. PO-F3-C6")
    ok = True
    for lam, ref in ((2, 0.71), (5, 0.45), (10, 0.32), (100, 0.10)):
        val = 1.0 / np.sqrt(lam)
        good = abs(val - ref) < 0.005
        ok &= good
        print(f"   lambda={lam:>3}  skewness={val:5.2f}  paper={ref:4.2f}"
              f"   {'OK' if good else 'MISMATCH'}")
    n_tail = 3 * LAM_TAIL                       # M = 3<M>
    ratio = (poisson.pmf(n_tail, LAM_TAIL)
             / norm.pdf(n_tail, loc=LAM_TAIL, scale=np.sqrt(LAM_TAIL)))
    good = 18.5 < ratio < 20.5                  # paper quotes "x19"
    ok &= good
    print(f"   excess at M=3<M>, lambda={LAM_TAIL}: x{ratio:.2f}"
          f"   paper=x19   {'OK' if good else 'MISMATCH'}")
    if not ok:
        raise SystemExit("Figure NOT produced: a value disagrees with the paper.")
    print("   -> all values reproduce the paper.\n")
    return ratio


# ---------------------------------------------------------------------
def panel_A(ax):
    """Coalescence distributions for several lambda, normalised to peak."""
    for lam in LAMBDAS:
        hi = int(lam + 6 * np.sqrt(lam)) + 5
        n = np.arange(0, hi)
        p = poisson.pmf(n, lam)
        ax.plot(n / lam, p / p.max(), "-o", ms=2.2, lw=1.2,
                color=COLORS[lam], label=rf"$\lambda={lam}$")
    ax.axvline(1.0, color="grey", ls=":", lw=0.8)
    ax.text(1.02, 0.05, r"$\langle M\rangle$", fontsize=7.5, color="grey")
    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel(r"$M/\langle M\rangle = N/\lambda$")
    ax.set_ylabel("distribution (normalised to peak)")
    ax.set_title("A — Coalescence distributions", loc="left")
    ax.legend(frameon=True, loc="upper right")
    ax.grid(alpha=0.25, ls=":")


def panel_B(ax):
    """Skewness 1/sqrt(lambda): same signature as f_NL^KZ = +5/18 > 0."""
    lam = np.logspace(np.log10(1.0), 2.3, 300)
    ax.plot(lam, 1.0 / np.sqrt(lam), "-", lw=1.8, color="#d62728")
    for l0 in LAMBDAS:
        ax.plot(l0, 1.0 / np.sqrt(l0), "o", ms=5, color=COLORS[l0], zorder=5)
        ax.annotate(f"{1/np.sqrt(l0):.2f}", (l0, 1 / np.sqrt(l0)),
                    textcoords="offset points", xytext=(6, 6), fontsize=7.5,
                    color=COLORS[l0])
    ax.axhline(0.0, color="black", lw=0.8)
    ax.set_xscale("log")
    ax.set_xlabel(r"$\lambda$")
    ax.set_ylabel(r"skewness $1/\sqrt{\lambda}$")
    ax.set_title("B — Skewness: positive for every finite $\\lambda$", loc="left")
    ax.set_ylim(-0.05, 0.85)
    ax.grid(alpha=0.25, ls=":", which="both")
    ax.text(0.04, 0.10,
            "same statistical signature as\n"
            r"$f_{\rm NL}^{\rm KZ}=+5/18>0$",
            transform=ax.transAxes, fontsize=7.5, va="bottom",
            bbox=dict(boxstyle="round,pad=0.35", fc="#fdf3f3",
                      ec="#d62728", lw=0.7))


def panel_C(ax, ratio):
    """Poisson vs Gaussian tail at lambda = 5."""
    lam = LAM_TAIL
    n = np.arange(0, 26)
    p = poisson.pmf(n, lam)
    g = norm.pdf(n, loc=lam, scale=np.sqrt(lam))
    ax.semilogy(n / lam, p, "-o", ms=3, lw=1.3, color="#d62728",
                label=rf"ECF Poisson ($\lambda={lam}$)")
    ax.semilogy(n / lam, g, "--", lw=1.3, color="#4c72b0",
                label="Gaussian (Press–Schechter)")
    ax.axvline(3.0, color="grey", ls=":", lw=0.9)
    ax.annotate(rf"$\times{ratio:.0f}$ at $M=3\langle M\rangle$",
                xy=(3.0, poisson.pmf(3 * lam, lam)),
                xytext=(0.35, 3e-6), fontsize=8.5, fontweight="bold",
                color="#d62728",
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.0))
    ax.set_xlim(0, 4.2)
    ax.set_ylim(1e-9, 0.4)
    ax.set_xlabel(r"$M/\langle M\rangle$")
    ax.set_ylabel("probability density")
    ax.set_title("C — Heavy tail: Poisson vs Gaussian", loc="left")
    ax.legend(frameon=True, loc="lower left")
    ax.grid(alpha=0.25, ls=":", which="both")


# ---------------------------------------------------------------------
def main():
    ratio = check_against_paper()

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.3), facecolor="white")
    panel_A(axes[0])
    panel_B(axes[1])
    panel_C(axes[2], ratio)

    fig.suptitle(
        "ECF mass function (Poisson coalescence) — PO-F3-C6\n"
        r"$N\sim\mathrm{Poisson}(\lambda)$, $\lambda=n_{\rm KZ}\,"
        r"\frac{4}{3}\pi R_{\rm coal}(z)^3$,  $M=N\,M_{\rm micro}$",
        fontsize=11, fontweight="bold", y=1.015)

    # The paper is explicit that C6 is NOT closed. The figure must say so,
    # otherwise an illustrative lambda reads as a calibrated prediction.
    fig.text(0.5, -0.055,
             "Open problem PO-F3-C6 — NOT closed: $R_{\\rm coal}(z)$ is a free, "
             "uncalibrated parameter and the $n_{\\rm KZ}$ normalisation against the "
             "observed dark-matter density is unresolved.\n"
             "$\\lambda$ is shown over an ILLUSTRATIVE range; the shape of the "
             "distribution is the prediction, not the value of $\\lambda$.",
             ha="center", va="top", fontsize=7.5, style="italic", color="#444")

    fig.tight_layout(rect=[0, 0.02, 1, 0.99])
    fig.savefig(OUT, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Figure: {OUT}")


if __name__ == "__main__":
    main()
