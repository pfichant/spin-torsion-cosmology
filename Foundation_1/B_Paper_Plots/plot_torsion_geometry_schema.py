#plot_torsion_geometry_schema.py
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import matplotlib

# Configuration pour éviter les erreurs de backend
matplotlib.use('Agg') # Force la génération sans fenêtre (plus stable)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

# --- CLASSE ARROW3D MISE À JOUR (COMPATIBLE MATPLOTLIB RÉCENT) ---
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        """Méthode requise par les versions récentes de Matplotlib pour le tri Z."""
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)

def plot_surface_and_loop(ax, torsion=False):
    # 1. Générer une surface courbe simple (portion de cylindre)
    x = np.linspace(-1, 1, 20)
    y = np.linspace(-1, 1, 20)
    X, Y = np.meshgrid(x, y)
    Z = 0.3 * X**2 # Courbure

    # Couleurs différentes pour GR (bleu) et EC (rouge/orange)
    cmap = plt.cm.Blues if not torsion else plt.cm.Oranges
    ax.plot_surface(X, Y, Z, cmap=cmap, alpha=0.6, rstride=2, cstride=2, edgecolor='k', linewidth=0.2)

    # 2. Définir les points du "parallélogramme"
    A = np.array([-0.5, -0.5, 0.3*(-0.5)**2])
    B = np.array([-0.5,  0.5, 0.3*(-0.5)**2])
    C = np.array([ 0.5, -0.5, 0.3*( 0.5)**2])
    
    # Point D idéal (transport commutatif)
    vecAB = B - A
    vecAC = C - A
    D_ideal = A + vecAB + vecAC
    D_ideal[2] = 0.3 * D_ideal[0]**2 + 0.05 # Projection visuelle

    if not torsion:
        # --- Cas GR : Le parallélogramme se ferme ---
        ax.add_artist(Arrow3D([A[0], B[0]], [A[1], B[1]], [A[2], B[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color='k'))
        ax.add_artist(Arrow3D([B[0], D_ideal[0]], [B[1], D_ideal[1]], [B[2], D_ideal[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color='k'))
        ax.add_artist(Arrow3D([A[0], C[0]], [A[1], C[1]], [A[2], C[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color='k'))
        ax.add_artist(Arrow3D([C[0], D_ideal[0]], [C[1], D_ideal[1]], [C[2], D_ideal[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color='k'))
        
        # Annotations
        ax.text(A[0], A[1], A[2]-0.1, 'A', fontsize=12)
        ax.text(B[0]-0.1, B[1], B[2], 'B', fontsize=12)
        ax.text(C[0], C[1]-0.1, C[2], 'C', fontsize=12)
        ax.text(D_ideal[0]+0.05, D_ideal[1], D_ideal[2], 'D', fontsize=12)
        
        ax.set_title("Riemannian Geometry (GR)\nZero Torsion", fontsize=14, pad=20)
        # Notez le r"..." pour raw string
        ax.text2D(0.5, -0.1, r"Commutative Transport" + "\n" + r"($S^\lambda_{\mu\nu}=0$)", transform=ax.transAxes, ha='center', fontsize=12)

    else:
        # --- Cas EC : Défaut de fermeture ---
        D_path1 = D_ideal + np.array([0, -0.1, 0.05]) # Chemin A->B->D1
        D_path2 = D_ideal + np.array([0.15, 0.1, 0.1]) # Chemin A->C->D2
        
        # Chemin 1 (Bleuté)
        ax.add_artist(Arrow3D([A[0], B[0]], [A[1], B[1]], [A[2], B[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color='navy'))
        ax.add_artist(Arrow3D([B[0], D_path1[0]], [B[1], D_path1[1]], [B[2], D_path1[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color='navy'))
        # Chemin 2 (Rougeâtre)
        ax.add_artist(Arrow3D([A[0], C[0]], [A[1], C[1]], [A[2], C[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color='darkred'))
        ax.add_artist(Arrow3D([C[0], D_path2[0]], [C[1], D_path2[1]], [C[2], D_path2[2]], mutation_scale=15, lw=2, arrowstyle="-|>", color='darkred'))

        # Flèche du Défaut de Fermeture (Torsion)
        ax.add_artist(Arrow3D([D_path1[0], D_path2[0]], [D_path1[1], D_path2[1]], [D_path1[2], D_path2[2]], 
                              mutation_scale=20, lw=3, arrowstyle="-|>", color='red', linestyle='--'))

        # Annotations
        ax.text(A[0], A[1], A[2]-0.1, 'A', fontsize=12)
        ax.text(B[0]-0.1, B[1], B[2], 'B', fontsize=12)
        ax.text(C[0], C[1]-0.1, C[2], 'C', fontsize=12)
        ax.text(D_path2[0]+0.05, D_path2[1], D_path2[2], 'D', fontsize=12)

        # Annotation Torsion et Spin
        mid_D = (D_path1 + D_path2) / 2
        ax.text(mid_D[0]+0.2, mid_D[1], mid_D[2]+0.15, r"Closure Failure" + "\n" + r"($\propto S^\lambda_{\mu\nu}$)", color='red', fontsize=11)
        ax.text(C[0]+0.2, C[1], C[2]-0.1, "Spin\nDensity", color='darkred', ha='center', fontsize=10)

        ax.set_title("Riemann-Cartan Geometry (EC)\nNon-Zero Torsion", fontsize=14, pad=20)
        ax.text2D(0.5, -0.1, r"Torsion driven by Spin" + "\n" + r"($S^\lambda_{\mu\nu} \neq 0$)", transform=ax.transAxes, ha='center', fontsize=12)

    # Nettoyage
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(0, 1)
    ax.set_axis_off()
    ax.view_init(elev=30, azim=-60)

# --- Création de la figure ---
fig = plt.figure(figsize=(12, 6))

ax1 = fig.add_subplot(121, projection='3d')
plot_surface_and_loop(ax1, torsion=False)

ax2 = fig.add_subplot(122, projection='3d')
plot_surface_and_loop(ax2, torsion=True)

# Ligne de séparation
line = plt.Line2D([0.5, 0.5], [0.1, 0.9], transform=fig.transFigure, color='black', linewidth=1.5)
fig.add_artist(line)

plt.tight_layout()
output_filename = 'figure_torsion_geometry_schema.png'
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"Success : Image '{output_filename}' générée.")