# [AJOUTE 15/09/2026] Garde UTF-8. Sans lui, un print contenant un caractere
# non-ASCII (fleche, etoile, accent) fait planter le script sur une console
# Windows en cp1252 : UnicodeEncodeError, code de sortie 1. Quatre scripts F2
# ont echoue ainsi chez Pascal le 15/09 alors qu'ils tournaient sous Linux.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
from pathlib import Path

def generer_contexte_audit():
    dossier_source = Path(".")
    fichier_sortie = "F2_agregat_scripts_calculation_audit.md"
    extensions_cibles = {'.py'}
    dossiers_a_ignorer = {'__pycache__', '.venv', 'venv', '.git', '.idea', '.vscode'}

    print("Début de l'analyse des scripts...")
    compteur_fichiers = 0

    with open(fichier_sortie, 'w', encoding='utf-8') as f_out:
        print("# DOCUMENT DE CONTEXTE POUR AUDIT DE CODE", file=f_out)
        print("", file=f_out)
        print(f"**Dossier audité :** {dossier_source.resolve().name}", file=f_out)
        print("", file=f_out)
        print("---", file=f_out)
        print("", file=f_out)
        print("## CONTENU DES SOURCES PYTHON", file=f_out)
        print("", file=f_out)
        
        for root, dirs, files in os.walk(dossier_source):
            dirs[:] = [d for d in dirs if d not in dossiers_a_ignorer]
            
            for f in files:
                chemin_complet = Path(root) / f
                
                if f in ["agregateur_audit.py", fichier_sortie]:
                    continue
                    
                if chemin_complet.suffix in extensions_cibles:
                    chemin_relatif = chemin_complet.relative_to(dossier_source)
                    compteur_fichiers += 1
                    
                    print(f"### Fichier {compteur_fichiers} : `{chemin_relatif}`", file=f_out)
                    print("", file=f_out)
                    print("```python", file=f_out)
                    
                    try:
                        with open(chemin_complet, 'r', encoding='utf-8') as f_in:
                            for ligne in f_in:
                                # Written line by line, to avoid conflicts
                                print(ligne, end="", file=f_out)
                            print("", file=f_out) 
                    except Exception as e:
                        print(f"# Erreur de lecture : {str(e)}", file=f_out)
                    
                    print("```", file=f_out)
                    print("", file=f_out)
                    print("---", file=f_out)
                    print("", file=f_out)
                    
    print(f"Succès ! {compteur_fichiers} scripts ont été centralisés dans '{fichier_sortie}'.")

if __name__ == "__main__":
    generer_contexte_audit()
    