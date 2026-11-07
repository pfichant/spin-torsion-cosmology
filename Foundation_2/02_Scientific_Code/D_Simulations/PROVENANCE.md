# Provenance — scripts pédagogiques de F2 (DOC-SCRIPTS-01)

- `plot_F2_animations_ECF.py` : téléchargé le 07/10/2026 à 13 h 38 depuis
  https://raw.githubusercontent.com/pfichant/spin-torsion-cosmology/main/Foundation_2/02_Scientific_Code/D_Simulations/plot_F2_animations_ECF.py
  (SHA-256 70739823b1d53885dd539f3c6d4bd3b9e37f666eae37c4fc8de816d725650263). Non exécuté (matériel pédagogique, pas un producteur de résultat chiffré).
  Contrôle de lecture : 4 GIF (0D/1D/2D/3D), 80 images, 18 images/s — conforme à F2 l.8160-8162.
  Remarque : l'en-tête du script date de « F2 PREPRINT v2 » et contient des formulations antérieures au corpus actuel (« Kill-switch: Roman (2028) », DOI de version 20629238 au lieu du DOI de concept 20629237) ; sans effet sur F2, à harmoniser dans le dépôt si Pascal le souhaite.
- `blender/plot_ecf_blender_simulation_knot_constructive_v34fix.py` (449 l., en-tête « V34-FIX », corrections du 08/05/2026 C1-C4) et `blender/plot_ecf_blender_simulation_GRB2025-2_v40fix.py` (447 l., en-tête « V40.1-FIX », corrections C1, C2, C4, C5) : fournis par Pascal le 07/10/2026 à 13 h 39 (archive `D_Simulations.zip` de son dépôt) ; `plot_F2_animations_ECF.py` de l'archive est identique au fichier téléchargé de GitHub. Non exécutés (Blender ≥ 4.2, `bpy`).
  **Écart avec F2** : F2 cite `ecf_blender_simulation_knot_constructive.py` (v34) et `ecf_blender_simulation_GRB2025-2.py` (v40.1), « corrected release v34.1 and v40.2 » ; les fichiers réels s'appellent `plot_ecf_blender_simulation_…_v34fix.py` / `…_v40fix.py` et portent « V34-FIX » / « V40.1-FIX ». Le contenu des corrections (modificateur Proximity min/max inversés ; nœud Emission accédé par type) correspond bien à la description de F2.
- L'archive contient aussi deux vidéos (`ecf_dual_genesis/ecf_dual_genesis.mp4`, `ecf_simulate_chiral_universe/ECF_Simulation_v1.4_EN.mp4`), non citées par nom dans les papiers ; non versées.
