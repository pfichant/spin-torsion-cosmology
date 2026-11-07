#!/usr/bin/env bash
# Regenerate feff_disk_1e5_planckbg.dat and feff_sph_1e5_planckbg.dat with DarkAges 1.2.0
# (Stocker, Kramer, Lesgourgues & Poulin 2018), commit 1994ea49 of github.com/pstoecker/DarkAges.
# darkages_py311.diff: compatibility only (scipy >= 1.14 'trapz' -> 'trapezoid'; dill class identity
# under Python 3.11 in four isinstance checks). No change to the physics.
# Usage: bash make_feff.sh [work_dir]     (requires numpy scipy dill future pyyaml)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${1:-$(mktemp -d)}"; mkdir -p "$WORK" && cd "$WORK"
[ -d DarkAges ] || git clone https://github.com/pstoecker/DarkAges
cd DarkAges && git checkout -q 1994ea499562190b78cb11650ad0a8b3333adc07
git apply "$HERE/darkages_py311.diff" || true
python3 bin/DarkAges --hist=accreting_PBH -m 1e5 --accretion_recipe=disk_accretion >/dev/null 2>&1 || true   # first call builds transfer *.obj
for rec in disk sph; do
  r=$([ $rec = disk ] && echo disk_accretion || echo spherical_accretion)
  python3 bin/DarkAges --hist=accreting_PBH -m 1e5 --accretion_recipe=$r \
      --use-background 67.36 0.3153 0.0000920 --return_f_eff_table > raw_$rec.dat 2>/dev/null
  python3 - "$rec" "$HERE/.." <<'PY'
import sys, numpy as np
rec, out = sys.argv[1], sys.argv[2]
rows = [l.split() for l in open(f'raw_{rec}.dat') if l.strip() and not l.startswith('#')]
n = int(rows[0][0]); data = np.array(rows[1:], float); assert len(data) == n
data = np.vstack([data, [1e7, data[-1, 1]]])
with open(f'{out}/feff_{rec}_1e5_planckbg.dat', 'w') as f:
    f.write(f'# f_eff(z) from DarkAges 1.2.0 (accreting_PBH, {rec}_accretion, M = 1e5 Msun, H0 = 67.36, Om = 0.3153, Or = 9.2e-5); constant extension to z = 1e7 for CLASS\n{len(data)}\n')
    for z, v in data: f.write(f'{z:.4e}\t{v:.5e}\n')
print('written', rec)
PY
done
