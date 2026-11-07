#!/usr/bin/env bash
# Install CLASS 3.3.2 (classy) with the ECF patch to the exotic-injection module.
# The patch adds two environment switches read at run time by injection_rate_PBH_accretion():
#   PBH_LMODE = edd  -> L_acc = L_Edd (Eddington benchmark, Serpico et al. 2020, Eq. 25)
#   PBH_LMODE = cap  -> L_acc = min(L_acc, L_Edd) (the stock code has no Eddington cap)
#   PBH_ZCUT  = z    -> no injection below redshift z
# Unset variables leave CLASS behaviour unchanged.
# Usage: bash install_patched_class.sh [work_dir]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${1:-$(mktemp -d)}"
mkdir -p "$WORK" && cd "$WORK"
pip download classy==3.3.2.0 --no-deps -d . >/dev/null
echo "bad64cea3c3cd80e9b109fe33bbf34216a70037b56d981acb0484b7f09c5a291  classy-3.3.2.0.tar.gz" | sha256sum -c -
tar xzf classy-3.3.2.0.tar.gz
cd classy-3.3.2.0
patch -p1 < "$HERE/injection_ecf.diff"
grep -q "ECF patch 16/10/2026" external/heating/injection.c
pip install --force-reinstall --no-deps . ${PIP_EXTRA:-}
python3 -c "import classy; print('classy installed:', classy.__file__)"
