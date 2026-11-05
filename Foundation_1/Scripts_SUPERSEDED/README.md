# Scripts et figures dépassés — conservés pour traçabilité

Ce dossier contient des versions **antérieures** de scripts et de figures qui ne
correspondent plus à l'état courant du corpus. Ils sont conservés — et non supprimés —
pour que l'historique des corrections reste vérifiable.

⚠️ **Ne pas utiliser ces scripts pour reproduire les valeurs publiées.** Les versions
actives se trouvent dans `../02_Scientific_Code/`.

## Écarts connus par rapport aux versions actives

- **Normalisation du secteur de spin** : ces scripts utilisent l'ancienne ancre
  $z=7500$. Les versions actives utilisent $z_{\rm ref}=5600$, la valeur de
  `script_01_solve_sound_horizon.py` qui reproduit $r_s = 135{,}8$ Mpc
  (correction du 05/09/2026 — voir I82 du registre des impasses).
  L'écart entre les deux ancres n'est pas statistiquement significatif
  (compatibles à 1,25σ compte tenu de $\sigma(r_s)=\pm1{,}93$ Mpc) ; l'alignement
  a été fait pour la traçabilité, non parce qu'un résultat était faux.

- **`run_F1_non_regression.py`** : cette copie code en dur sa propre chaîne de
  dilution. La version active importe l'ancre depuis le solveur, de sorte qu'une
  divergence entre papier et code ne peut plus y passer inaperçue.

- **`plot_h0_s8_contours.py` et `plot_Optimization_Intersection.py`** (retirés le
  09/10/2026) : anciennes Fig. 3 et 4 de Foundation I, tracées avec la calibration
  historique ($\gamma_{\rm spin}=0{,}3116$, $\Omega_m=0{,}315$). Remplacées par
  `plot_h0_s8_active.py` (plan $H_0$–$S_8$ sur le fond actif, $S_8$ ECF OPEN) et,
  pour le paysage en $F_{\rm ion}$, par `scan_F_ion_H0_BAO.py` (sans figure).
  `verify_calibration()` reproduit toujours le $\Delta\chi^2=-39{,}5$ HISTORICAL.

## Convention

Le corpus archive plutôt qu'il ne supprime. Un fichier ici signifie « remplacé »,
jamais « faux à l'époque » : la plupart de ces scripts étaient corrects au regard de
l'état du corpus au moment où ils ont été écrits.
