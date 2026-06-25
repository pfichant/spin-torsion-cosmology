import bpy
import math

# =============================================================================
# ECF FRAMEWORK: 3D MACRO-KNOT SIMULATION (V34-FIX - FULLY COMMENTED IN ENGLISH)
# Theoretical basis: Einstein-Cartan-Fichant (ECF) Constructive Fusion (Regime I)
# Corrections 2026-05-08 :
#   [C1] IndentationError on module-level if/for blocks (CRLF artifacts)
#   [C2] min_dist / max_dist swapped in Proximity modifiers K1 & K2
#   [C3] mat_super_flash Emission node accessed by type, not by name
#   [C4] Camera keyframe pattern : set location THEN insert keyframe
# =============================================================================

# --- GLOBAL TIMELINE PARAMETERS ---
TOTAL_FRAMES    = 600   # Total duration of the animation
COLLISION_FRAME = 400   # Frame where Topological Fusion occurs
START_DANCE     = 50    # Frame where orbital inspiral begins

# --- 1. CLEANUP & SCENE PREPARATION ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# [C1] Fixed: module-level if block properly indented
if bpy.data.worlds:
    world = bpy.data.worlds[0]
    if world.use_nodes and "Background" in world.node_tree.nodes:
        world.node_tree.nodes["Background"].inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end   = TOTAL_FRAMES

# Robust EEVEE engine selection (Blender 4.2+ compatibility)
try:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
except Exception:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

if hasattr(bpy.context.scene.eevee, 'use_bloom'):
    bpy.context.scene.eevee.use_bloom        = True
    bpy.context.scene.eevee.bloom_intensity  = 0.05
    bpy.context.scene.eevee.bloom_radius     = 6.0

# --- 2. MATERIAL GENERATION FUNCTIONS ---
def create_emission_mat(name, color, strength):
    """Creates a basic glowing emission material using shader nodes."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)
    emission = mat.node_tree.nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value    = color
    emission.inputs['Strength'].default_value = strength
    output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    return mat

def create_plasma_mat(name, color, strength):
    """Creates a textured glowing plasma material using Voronoi noise."""
    mat   = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for node in nodes:
        nodes.remove(node)
    tex        = nodes.new(type='ShaderNodeTexVoronoi')
    tex.inputs['Scale'].default_value = 6.0
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    color_ramp.color_ramp.elements[1].color = color
    emission   = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Strength'].default_value = strength
    output     = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(tex.outputs['Distance'],       color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'],   emission.inputs['Color'])
    links.new(emission.outputs['Emission'],  output.inputs['Surface'])
    return mat

def create_grid_mat():
    """Creates the Spacetime Fabric material: semi-transparent wireframe."""
    mat   = bpy.data.materials.new(name="Mat_Spacetime_Grid")
    mat.use_nodes    = True
    mat.blend_method = 'BLEND'
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for node in nodes:
        nodes.remove(node)
    wireframe = nodes.new(type='ShaderNodeWireframe')
    wireframe.inputs['Size'].default_value = 0.003
    emission  = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value    = (0.05, 0.05, 0.2, 1.0)
    emission.inputs['Strength'].default_value = 1.0
    transparent = nodes.new(type='ShaderNodeBsdfTransparent')
    mix    = nodes.new(type='ShaderNodeMixShader')
    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(wireframe.outputs['Fac'],      mix.inputs['Fac'])
    links.new(transparent.outputs['BSDF'],   mix.inputs[1])
    links.new(emission.outputs['Emission'],  mix.inputs[2])
    links.new(mix.outputs['Shader'],         output.inputs['Surface'])
    return mat

# Instantiate materials
mat_knot1      = create_plasma_mat("Mat_Knot1",      (0.0, 0.8, 1.0, 1.0), 10.0)
mat_pole1      = create_emission_mat("Mat_Pole1",    (0.0, 1.0, 1.0, 1.0), 15.0)
mat_mag1       = create_emission_mat("Mat_Mag1",     (0.0, 0.8, 1.0, 1.0),  8.0)
mat_knot2      = create_plasma_mat("Mat_Knot2",      (1.0, 0.2, 0.0, 1.0), 10.0)
mat_pole2      = create_emission_mat("Mat_Pole2",    (1.0, 0.4, 0.0, 1.0), 15.0)
mat_mag2       = create_emission_mat("Mat_Mag2",     (1.0, 0.2, 0.0, 1.0),  8.0)
mat_grid       = create_grid_mat()
mat_text_white = create_emission_mat("Mat_Text_White", (1.0, 1.0, 1.0, 1.0),  8.0)
mat_text_cyan  = create_emission_mat("Mat_Text_Cyan",  (0.0, 1.0, 1.0, 1.0), 15.0)
mat_text_gold  = create_emission_mat("Mat_Text_Gold",  (1.0, 0.8, 0.2, 1.0),  8.0)

mat_super_flash              = create_emission_mat("Mat_SuperFlash", (1.0, 0.9, 1.0, 1.0), 100.0)
mat_super_flash.blend_method = 'BLEND'

# --- 3. CREATE SPACETIME FABRIC ---
bpy.ops.mesh.primitive_grid_add(size=40, x_subdivisions=300, y_subdivisions=300, location=(0, 0, -1))
grid      = bpy.context.active_object
grid.name = "Spacetime_Fabric"
grid.data.materials.append(mat_grid)

vg1 = grid.vertex_groups.new(name="Knot1_Influence")
vg2 = grid.vertex_groups.new(name="Knot2_Influence")
for v in grid.data.vertices:
    vg1.add([v.index], 0.0, 'REPLACE')
    vg2.add([v.index], 0.0, 'REPLACE')

# --- 4. TOPOLOGICAL DEFECTS GENERATION ---
def create_knot(name, mat_sphere, mat_pole, mat_mag, radius, mag_scale):
    """Builds a topological defect: central mass + spin pole + chiral magnetic loops."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=64, ring_count=32, location=(0, 0, 0))
    bpy.ops.object.shade_smooth()
    knot      = bpy.context.active_object
    knot.name = name
    knot.data.materials.append(mat_sphere)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=radius * 3.5, vertices=16, location=(0, 0, 0))
    bpy.ops.object.shade_smooth()
    pole        = bpy.context.active_object
    pole.name   = name + "_Pole"
    pole.data.materials.append(mat_pole)
    pole.parent = knot

    for i in range(12):
        angle = i * (math.pi / 12.0)
        bpy.ops.mesh.primitive_torus_add(
            major_radius=1.0, minor_radius=0.012,
            major_segments=64, minor_segments=8, location=(0, 0, 0))
        bpy.ops.object.shade_smooth()
        mag_loop               = bpy.context.active_object
        mag_loop.name          = f"{name}_MagLine_{i}"
        mag_loop.data.materials.append(mat_mag)
        mag_loop.scale         = mag_scale
        mag_loop.rotation_euler = (math.pi / 2.0, 0, angle)
        mag_loop.parent        = knot
    return knot

knot1 = create_knot("MacroKnot_1", mat_knot1, mat_pole1, mat_mag1, radius=0.6,  mag_scale=(1.8, 0.6, 1.0))
knot2 = create_knot("AntiKnot_2",  mat_knot2, mat_pole2, mat_mag2, radius=0.35, mag_scale=(1.0, 0.35, 0.6))

bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
flash_sphere      = bpy.context.active_object
flash_sphere.name = "Super_Flash_Bubble"
flash_sphere.data.materials.append(mat_super_flash)
flash_sphere.scale = (0, 0, 0)

# --- 5. SPACETIME DEFORMATION MODIFIERS ---
# [C2] FIXED: min_dist < max_dist (0.2 < 10.0 for K1, 0.2 < 6.0 for K2)
# KNOT 1
mod_prox1                 = grid.modifiers.new(name="Prox_K1", type='VERTEX_WEIGHT_PROXIMITY')
mod_prox1.vertex_group    = "Knot1_Influence"
mod_prox1.target          = knot1
mod_prox1.proximity_mode  = 'GEOMETRY'
mod_prox1.falloff_type    = 'SMOOTH'
mod_prox1.min_dist        = 0.2   # [C2] was 10.0 — corrected
mod_prox1.max_dist        = 10.0  # [C2] was 0.2  — corrected

mod_disp1                 = grid.modifiers.new(name="Curvature_K1", type='DISPLACE')
mod_disp1.direction       = 'Z'
mod_disp1.strength        = -12.0
mod_disp1.vertex_group    = "Knot1_Influence"

mod_twist1                = grid.modifiers.new(name="Torsion_K1", type='SIMPLE_DEFORM')
mod_twist1.deform_method  = 'TWIST'
mod_twist1.origin         = knot1
mod_twist1.angle          = math.radians(600)
mod_twist1.vertex_group   = "Knot1_Influence"

# KNOT 2
mod_prox2                 = grid.modifiers.new(name="Prox_K2", type='VERTEX_WEIGHT_PROXIMITY')
mod_prox2.vertex_group    = "Knot2_Influence"
mod_prox2.target          = knot2
mod_prox2.proximity_mode  = 'GEOMETRY'
mod_prox2.falloff_type    = 'SMOOTH'
mod_prox2.min_dist        = 0.2   # [C2] corrected
mod_prox2.max_dist        = 6.0   # [C2] corrected

mod_disp2                 = grid.modifiers.new(name="Curvature_K2", type='DISPLACE')
mod_disp2.direction       = 'Z'
mod_disp2.strength        = -4.0
mod_disp2.vertex_group    = "Knot2_Influence"

mod_twist2                = grid.modifiers.new(name="Torsion_K2", type='SIMPLE_DEFORM')
mod_twist2.deform_method  = 'TWIST'
mod_twist2.origin         = knot2
mod_twist2.angle          = math.radians(-600)
mod_twist2.vertex_group   = "Knot2_Influence"

# --- 6. LIGHTING, SOUND & CAMERA ---
gamma_light          = bpy.data.objects.new("Gamma_Flash_Source", bpy.data.lights.new(name="Gamma_Light", type='POINT'))
bpy.context.collection.objects.link(gamma_light)
gamma_light.location       = (0, 0, 3.0)
gamma_light.data.color     = (1.0, 0.9, 1.0)
gamma_light.data.energy    = 0.0

bpy.ops.object.speaker_add(location=(0, 0, 0))
speaker      = bpy.context.active_object
speaker.name = "Gamma_Sound_FX"
speaker.data.volume = 0.0

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
cam_target      = bpy.context.active_object
cam_target.name = "Camera_Target"

# [C4] FIXED: set location BEFORE inserting keyframe for frame=1
bpy.ops.object.camera_add(location=(0, -40, 20))
cam      = bpy.context.active_object
cam.name = "Cinematic_Camera"
bpy.context.scene.camera = cam

track_constraint            = cam.constraints.new(type='TRACK_TO')
track_constraint.target     = cam_target
track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
track_constraint.up_axis    = 'UP_Y'

# [C4] Pattern: location is already set by camera_add → insert frame 1 immediately
cam.keyframe_insert(data_path="location", frame=1)  # (0, -40, 20) locked at frame 1
cam.location = (25, -25, 12)
cam.keyframe_insert(data_path="location", frame=200)
cam.location = (15, -12, 8)
cam.keyframe_insert(data_path="location", frame=COLLISION_FRAME - 10)
cam.location = (6, -6, 3.5)
cam.keyframe_insert(data_path="location", frame=COLLISION_FRAME + 10)
cam.location = (-12, 9, 5)
cam.keyframe_insert(data_path="location", frame=TOTAL_FRAMES)

# --- 7. HUD & LABELS ---
def create_label(name, text, color):
    """Creates a 3D text object for UI elements."""
    bpy.ops.object.text_add(location=(0, 0, 0))
    lbl            = bpy.context.active_object
    lbl.name       = name
    lbl.data.body  = text
    lbl.data.align_x = 'CENTER'
    lbl.data.align_y = 'CENTER'
    lbl.data.extrude = 0.01
    lbl.scale        = (0.5, 0.5, 0.5)
    lbl.data.materials.append(color)
    return lbl

label_knot1 = create_label("Label_Knot1", "Macro-Noeud (H > 0)", mat_text_white)
label_knot2 = create_label("Label_Knot2", "Anti-Noeud  (H < 0)", mat_text_white)
for lbl in [label_knot1, label_knot2]:
    lbl.constraints.new(type='COPY_ROTATION').target = cam

legend_text = "Foundation II: Univers Chiral | Auteur : Fichant | 7 Mars 2026"
hud_legend        = create_label("HUD_Legend_Bottom", legend_text, mat_text_gold)
hud_legend.parent = cam
hud_legend.location = (0, -1.5, -10)
hud_legend.scale    = (0.12, 0.12, 0.12)

hud_intro        = create_label("HUD_Intro", "ECF: Frame-Dragging & Topological Annihilation", mat_text_white)
hud_intro.parent = cam
hud_intro.scale  = (0.15, 0.15, 0.15)

hud_flash        = create_label("HUD_Flash", ">> FUSION TOPOLOGIQUE : REDUCTION DE MASSE <<", mat_text_cyan)
hud_flash.parent = cam
hud_flash.scale  = (0.22, 0.22, 0.22)

def toggle_visibility(txt_obj, frame, make_visible, visible_loc):
    """Moves an object in/out of camera field of view at a specific frame."""
    hidden_loc = (0, 0, 20)
    loc        = visible_loc if make_visible else hidden_loc
    prev_loc   = hidden_loc  if make_visible else visible_loc
    txt_obj.location = prev_loc
    txt_obj.keyframe_insert(data_path="location", frame=max(1, frame - 1))
    txt_obj.location = loc
    txt_obj.keyframe_insert(data_path="location", frame=frame)

toggle_visibility(hud_intro, 1,              False, (0,  1.4, -10))
toggle_visibility(hud_flash, 1,              False, (0,  0.0,  -8))

# --- 8. REAL-TIME TELEMETRY GRAPH ---
def create_axis(name, loc, scale, rot):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.003, depth=1.0, location=(0, 0, 0))
    axis              = bpy.context.active_object
    axis.name         = name
    axis.parent       = cam
    axis.location     = loc
    axis.scale        = scale
    axis.rotation_euler = rot
    axis.data.materials.append(mat_text_white)

create_axis("Graph_AxisX", (0.1,  -1.0, -9), (1, 1, 2.0), (0, math.pi / 2, 0))
create_axis("Graph_AxisY", (-0.9, -0.65, -9), (1, 1, 0.7), (0, 0, 0))

label_t          = create_label("Label_Time", "Temps (ms)",       mat_text_white)
label_t.parent   = cam
label_t.scale    = (0.06, 0.06, 0.06)
label_t.location = (1.0, -1.15, -9)

label_i          = create_label("Label_Int", "Intensite (Gamma)", mat_text_white)
label_i.parent   = cam
label_i.scale    = (0.05, 0.05, 0.05)
label_i.location = (-0.95, -0.2, -9)

curve_data            = bpy.data.curves.new('GRB_Curve', type='CURVE')
curve_data.dimensions = '3D'
curve_data.fill_mode  = 'FULL'
curve_data.bevel_depth = 0.006
spline = curve_data.splines.new('POLY')
spline.points.add(TOTAL_FRAMES - 1)

for i, f in enumerate(range(1, TOTAL_FRAMES + 1)):
    x = -0.9 + (f / float(TOTAL_FRAMES)) * 2.0
    if   f < COLLISION_FRAME - 2:
        I = 0.0
    elif COLLISION_FRAME - 2 <= f <= COLLISION_FRAME:
        I = (f - (COLLISION_FRAME - 2)) / 2.0
    else:
        I = math.exp(-(f - COLLISION_FRAME) / 15.0)
    y = -1.0 + I * 0.7
    spline.points[i].co = (x, y, 0, 1)

graph_line        = bpy.data.objects.new('GRB_GraphLine', curve_data)
bpy.context.collection.objects.link(graph_line)
graph_line.parent   = cam
graph_line.location = (0, 0, -9)
graph_line.data.materials.append(mat_text_cyan)
graph_line.data.bevel_factor_end = 0.0
graph_line.data.keyframe_insert("bevel_factor_end", frame=1)
graph_line.data.bevel_factor_end = 1.0
graph_line.data.keyframe_insert("bevel_factor_end", frame=TOTAL_FRAMES)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.015, location=(0, 0, 0))
tracker_dot      = bpy.context.active_object
tracker_dot.name = "GraphTracker"
tracker_dot.data.materials.append(mat_text_white)
tracker_dot.parent = cam

for f in range(1, TOTAL_FRAMES + 1):
    x = -0.9 + (f / float(TOTAL_FRAMES)) * 2.0
    if   f < COLLISION_FRAME - 2:
        I = 0.0
    elif COLLISION_FRAME - 2 <= f <= COLLISION_FRAME:
        I = (f - (COLLISION_FRAME - 2)) / 2.0
    else:
        I = math.exp(-(f - COLLISION_FRAME) / 15.0)
    y = -1.0 + I * 0.7
    tracker_dot.location = (x, y, -9)
    tracker_dot.keyframe_insert("location", frame=f)

# --- 9. CORE ANIMATION LOOP ---
def insert_kf(obj, frame, loc, rot=None):
    obj.location = loc
    obj.keyframe_insert(data_path="location", frame=frame)
    if rot:
        obj.rotation_euler = rot
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)

mass_1, mass_2 = 10.0, 1.0
total_mass      = mass_1 + mass_2
r1_f, r2_f     = mass_2 / total_mass, mass_1 / total_mass

toggle_visibility(hud_intro, 2,              True,  (0, 1.4, -10))
toggle_visibility(hud_intro, START_DANCE - 1, False, (0, 1.4, -10))

# 9.A: Inspiral phase
for f in range(1, COLLISION_FRAME + 1):
    t     = 0 if f < START_DANCE else (f - START_DANCE) / (COLLISION_FRAME - START_DANCE)
    R     = 12.0 * (1.0 - t ** 2.5)
    theta = 18.0 * t
    spin  = 30.0 * t
    x1, y1 = R * r1_f * math.cos(theta), R * r1_f * math.sin(theta)
    x2, y2 = -R * r2_f * math.cos(theta), -R * r2_f * math.sin(theta)
    insert_kf(knot1, f, (x1, y1, 0), (0, 0,        spin))
    insert_kf(knot2, f, (x2, y2, 0), (math.pi, 0, -spin))
    insert_kf(label_knot1, f, (x1, y1, 2.5))
    insert_kf(label_knot2, f, (x2, y2, 2.5))

# 9.B: Topological Annihilation Event
insert_kf(knot2,       COLLISION_FRAME, (100, 100, 100))
insert_kf(label_knot2, COLLISION_FRAME, (100, 100, 100))

toggle_visibility(hud_flash, COLLISION_FRAME, True, (0, 0, -8))

gamma_light.data.energy = 0.0
gamma_light.data.keyframe_insert(data_path="energy", frame=COLLISION_FRAME - 1)
gamma_light.data.energy = 5000000.0
gamma_light.data.keyframe_insert(data_path="energy", frame=COLLISION_FRAME)
gamma_light.data.energy = 0.0
gamma_light.data.keyframe_insert(data_path="energy", frame=COLLISION_FRAME + 30)

flash_sphere.scale = (0, 0, 0)
flash_sphere.keyframe_insert("scale", frame=COLLISION_FRAME - 1)
flash_sphere.scale = (6, 6, 6)
flash_sphere.keyframe_insert("scale", frame=COLLISION_FRAME + 2)
flash_sphere.scale = (18, 18, 18)
flash_sphere.keyframe_insert("scale", frame=COLLISION_FRAME + 20)

# [C3] FIXED: access Emission node by type, not by name (avoids KeyError on 'Emission.001' etc.)
node_emission = next(n for n in mat_super_flash.node_tree.nodes if n.type == 'EMISSION')
node_emission.inputs['Strength'].default_value = 0.0
node_emission.inputs['Strength'].keyframe_insert("default_value", frame=COLLISION_FRAME - 1)
node_emission.inputs['Strength'].default_value = 100.0
node_emission.inputs['Strength'].keyframe_insert("default_value", frame=COLLISION_FRAME)
node_emission.inputs['Strength'].default_value = 0.0
node_emission.inputs['Strength'].keyframe_insert("default_value", frame=COLLISION_FRAME + 25)

speaker.data.volume = 0.0
speaker.data.keyframe_insert(data_path="volume", frame=COLLISION_FRAME - 1)
speaker.data.volume = 1.0
speaker.data.keyframe_insert(data_path="volume", frame=COLLISION_FRAME)
speaker.data.volume = 0.0
speaker.data.keyframe_insert(data_path="volume", frame=COLLISION_FRAME + 50)

# 9.C: Physical mass deficit — knot1 shrinks after absorbing knot2
knot1.scale = (1.0, 1.0, 1.0)
knot1.keyframe_insert(data_path="scale", frame=COLLISION_FRAME - 1)
knot1.scale = (0.6, 0.6, 0.6)
knot1.keyframe_insert(data_path="scale", frame=COLLISION_FRAME + 40)

toggle_visibility(hud_flash, COLLISION_FRAME + 70, False, (0, 0, -8))

# 9.D: Post-collision ringdown
for f in range(COLLISION_FRAME + 1, TOTAL_FRAMES + 1):
    t_spin = 30.0 + (f - COLLISION_FRAME) * 0.1
    insert_kf(knot1,       f, (0, 0, 0), (0, 0, t_spin))
    insert_kf(label_knot1, f, (0, 0, 1.5))

# Smooth fcurves for graph
if graph_line.data.animation_data and graph_line.data.animation_data.action:
    for fcu in graph_line.data.animation_data.action.fcurves:
        for kp in fcu.keyframe_points:
            kp.interpolation = 'LINEAR'

bpy.context.scene.frame_set(1)
bpy.context.view_layer.update()
print("ECF Simulation V34-FIX (Constructive Fusion, Regime I) — generated successfully!")
