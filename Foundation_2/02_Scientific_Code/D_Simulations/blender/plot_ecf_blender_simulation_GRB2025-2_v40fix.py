import bpy
import math

# =============================================================================
# ECF FRAMEWORK: 3D MACRO-KNOT SIMULATION (V40.1-FIX — EXCENTRIC ORBITS)
# Theoretical basis: Einstein-Cartan-Fichant (ECF) Topological Annihilation (Regime II)
# Corrections 2026-05-08 :
#   [C1] IndentationError on module-level if/for blocks (CRLF artifacts)
#   [C2] min_dist / max_dist swapped in add_mods() Proximity modifier
#   [C4] Camera keyframe frame=1: insert THEN change location
#   [C5] label_knot1 repositioned on survivor after COLLISION_FRAME
# =============================================================================

bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'

# --- GLOBAL TIMELINE PARAMETERS ---
TOTAL_FRAMES    = 600
COLLISION_FRAME = 400
START_DANCE     = 50

# --- 1. CLEANUP & SCENE PREPARATION ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# [C1] Fixed: module-level if properly indented
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

# [C1] Fixed: if properly indented
if hasattr(bpy.context.scene.eevee, 'use_bloom'):
    bpy.context.scene.eevee.use_bloom       = True
    bpy.context.scene.eevee.bloom_intensity = 0.05
    bpy.context.scene.eevee.bloom_radius    = 6.0

# --- 2. MATERIALS ---
def create_emission_mat(name, color, strength):
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
    links.new(tex.outputs['Distance'],      color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'],  emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    return mat

def create_grid_mat():
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
    links.new(wireframe.outputs['Fac'],     mix.inputs['Fac'])
    links.new(transparent.outputs['BSDF'],  mix.inputs[1])
    links.new(emission.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'],        output.inputs['Surface'])
    return mat

# Mat_SuperFlash with animatable transparency (MixShader FadeMix)
mat_super_flash              = bpy.data.materials.new(name="Mat_SuperFlash")
mat_super_flash.use_nodes    = True
mat_super_flash.blend_method = 'BLEND'
nodes = mat_super_flash.node_tree.nodes
links = mat_super_flash.node_tree.links
for n in nodes:
    nodes.remove(n)
emission = nodes.new(type='ShaderNodeEmission')
emission.inputs['Color'].default_value    = (1.0, 0.9, 1.0, 1.0)
emission.inputs['Strength'].default_value = 100.0
transparent = nodes.new(type='ShaderNodeBsdfTransparent')
mix      = nodes.new(type='ShaderNodeMixShader')
mix.name = "FadeMix"
output   = nodes.new(type='ShaderNodeOutputMaterial')
links.new(transparent.outputs['BSDF'],  mix.inputs[1])
links.new(emission.outputs['Emission'], mix.inputs[2])
links.new(mix.outputs['Shader'],        output.inputs['Surface'])

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

# --- 3. CREATE SPACETIME FABRIC ---
bpy.ops.mesh.primitive_grid_add(size=40, x_subdivisions=300, y_subdivisions=300, location=(0, 0, -1))
grid      = bpy.context.active_object
grid.name = "Spacetime_Fabric"
grid.data.materials.append(mat_grid)

vg1 = grid.vertex_groups.new(name="Knot1_Influence")
vg2 = grid.vertex_groups.new(name="Knot2_Influence")
# [C1] Fixed: for loop indented properly
for v in grid.data.vertices:
    vg1.add([v.index], 0.0, 'REPLACE')
    vg2.add([v.index], 0.0, 'REPLACE')

# --- 4. TOPOLOGICAL DEFECTS ---
def create_knot(name, mat_sphere, mat_pole, mat_mag, radius, mag_scale):
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
    # [C1] Fixed: for loop indented properly
    for i in range(12):
        angle = i * (math.pi / 12.0)
        bpy.ops.mesh.primitive_torus_add(
            major_radius=1.0, minor_radius=0.012,
            major_segments=64, minor_segments=8, location=(0, 0, 0))
        bpy.ops.object.shade_smooth()
        mag_loop                = bpy.context.active_object
        mag_loop.name           = f"{name}_MagLine_{i}"
        mag_loop.data.materials.append(mat_mag)
        mag_loop.scale          = mag_scale
        mag_loop.rotation_euler = (math.pi / 2.0, 0, angle)
        mag_loop.parent         = knot
    return knot

knot1 = create_knot("MacroKnot_1", mat_knot1, mat_pole1, mat_mag1, radius=0.6,  mag_scale=(1.8, 0.6, 1.0))
knot2 = create_knot("AntiKnot_2",  mat_knot2, mat_pole2, mat_mag2, radius=0.35, mag_scale=(1.0, 0.35, 0.6))

bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
flash_sphere      = bpy.context.active_object
flash_sphere.name = "Super_Flash_Bubble"
flash_sphere.data.materials.append(mat_super_flash)
flash_sphere.scale = (0, 0, 0)

# --- 5. DEFORMATION MODIFIERS ---
def add_mods(target, vg_name, twist_angle, disp_str):
    """[C2] FIXED: min_dist (0.2) < max_dist (10.0) — previously inverted."""
    mod_prox                = grid.modifiers.new(name=f"Prox_{target.name}", type='VERTEX_WEIGHT_PROXIMITY')
    mod_prox.vertex_group   = vg_name
    mod_prox.target         = target
    mod_prox.proximity_mode = 'GEOMETRY'
    mod_prox.falloff_type   = 'SMOOTH'
    mod_prox.min_dist       = 0.2   # [C2] was 10.0 — corrected
    mod_prox.max_dist       = 10.0  # [C2] was 0.2  — corrected

    mod_disp              = grid.modifiers.new(name=f"Disp_{target.name}", type='DISPLACE')
    mod_disp.direction    = 'Z'
    mod_disp.strength     = disp_str
    mod_disp.vertex_group = vg_name

    mod_twist                = grid.modifiers.new(name=f"Twist_{target.name}", type='SIMPLE_DEFORM')
    mod_twist.deform_method  = 'TWIST'
    mod_twist.origin         = target
    mod_twist.angle          = math.radians(twist_angle)
    mod_twist.vertex_group   = vg_name

add_mods(knot1, "Knot1_Influence",  600, -12.0)
add_mods(knot2, "Knot2_Influence", -600,  -4.0)

# --- 6. LIGHTING, SOUND & CAMERA ---
gamma_light       = bpy.data.objects.new("Gamma_Flash_Source", bpy.data.lights.new(name="Gamma_Light", type='POINT'))
bpy.context.collection.objects.link(gamma_light)
gamma_light.location    = (0, 0, 3.0)
gamma_light.data.color  = (1.0, 0.9, 1.0)
gamma_light.data.energy = 0.0

bpy.ops.object.speaker_add(location=(0, 0, 0))
speaker      = bpy.context.active_object
speaker.name = "Gamma_Sound_FX"
speaker.data.volume = 0.0

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
cam_target      = bpy.context.active_object
cam_target.name = "Camera_Target"

# [C4] FIXED: camera_add places camera at (0,-40,20) → insert frame=1 BEFORE moving
bpy.ops.object.camera_add(location=(0, -40, 20))
cam      = bpy.context.active_object
cam.name = "Cinematic_Camera"
bpy.context.scene.camera = cam

track_constraint            = cam.constraints.new(type='TRACK_TO')
track_constraint.target     = cam_target
track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
track_constraint.up_axis    = 'UP_Y'

cam.keyframe_insert(data_path="location", frame=1)   # (0,-40,20) locked
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
    bpy.ops.object.text_add(location=(0, 0, 0))
    lbl              = bpy.context.active_object
    lbl.name         = name
    lbl.data.body    = text
    lbl.data.align_x = 'CENTER'
    lbl.data.align_y = 'CENTER'
    lbl.data.extrude = 0.01
    lbl.scale        = (0.5, 0.5, 0.5)
    lbl.data.materials.append(color)
    return lbl

label_knot1 = create_label("Label_Knot1", "Macro-Noeud", mat_text_white)
label_knot2 = create_label("Label_Knot2", "Anti-Noeud",  mat_text_white)
for lbl in [label_knot1, label_knot2]:
    lbl.constraints.new(type='COPY_ROTATION').target = cam

hud_intro        = create_label("HUD_Intro", "ECF Topological Annihilation : Event GRB 2025", mat_text_white)
hud_intro.parent = cam
hud_intro.scale  = (0.15, 0.15, 0.15)

hud_flash        = create_label("HUD_Flash", ">> ANNIHILATION : PLATEAU GAMMA 8 HEURES <<", mat_text_cyan)
hud_flash.parent = cam
hud_flash.scale  = (0.2, 0.2, 0.2)

def toggle_visibility(txt_obj, frame, make_visible, visible_loc):
    hidden_loc = (0, 0, 20)
    loc      = visible_loc if make_visible else hidden_loc
    prev_loc = hidden_loc  if make_visible else visible_loc
    txt_obj.location = prev_loc
    txt_obj.keyframe_insert(data_path="location", frame=max(1, frame - 1))
    txt_obj.location = loc
    txt_obj.keyframe_insert(data_path="location", frame=frame)

toggle_visibility(hud_intro, 1, False, (0,  1.4, -10))
toggle_visibility(hud_flash, 1, False, (0,  0.0,  -8))

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

create_axis("Graph_AxisX", (0.1,  -1.0,  -9), (1, 1, 2.0), (0, math.pi / 2, 0))
create_axis("Graph_AxisY", (-0.9, -0.65, -9), (1, 1, 0.7), (0, 0, 0))

label_i          = create_label("Label_Int", "Courbe de Lumiere GRB 2025", mat_text_cyan)
label_i.parent   = cam
label_i.scale    = (0.05, 0.05, 0.05)
label_i.location = (-0.95, -0.2, -9)

def get_gamma_intensity(f):
    I = 0.0
    if 130 < f < 150: I += 0.20 * math.exp(-((f - 140) / 2.0) ** 2)
    if 230 < f < 250: I += 0.35 * math.exp(-((f - 240) / 2.0) ** 2)
    if 330 < f < 350: I += 0.50 * math.exp(-((f - 340) / 2.0) ** 2)
    if f >= COLLISION_FRAME:
        if f < COLLISION_FRAME + 5:
            I += math.exp(-((f - (COLLISION_FRAME + 5)) / 2.0) ** 2) * 1.0
        else:
            I += 1.0 * math.exp(-(f - (COLLISION_FRAME + 5)) / 2000.0)
    return I

curve_data             = bpy.data.curves.new('GRB_Curve', type='CURVE')
curve_data.dimensions  = '3D'
curve_data.fill_mode   = 'FULL'
curve_data.bevel_depth = 0.006
spline = curve_data.splines.new('POLY')
spline.points.add(TOTAL_FRAMES - 1)

for i, f in enumerate(range(1, TOTAL_FRAMES + 1)):
    x = -0.9 + (f / float(TOTAL_FRAMES)) * 2.0
    y = -1.0 + get_gamma_intensity(f) * 0.7
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
tracker_dot        = bpy.context.active_object
tracker_dot.name   = "GraphTracker"
tracker_dot.data.materials.append(mat_text_white)
tracker_dot.parent = cam

# --- 9. ANIMATION & EXCENTRIC ORBITS ---
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

for f in range(1, COLLISION_FRAME + 1):
    t     = 0 if f < START_DANCE else (f - START_DANCE) / (COLLISION_FRAME - START_DANCE)
    R_env = 12.0 * (1.0 - t ** 2.5)

    if f > START_DANCE and f < COLLISION_FRAME - 10:
        bounce_amp = 3.0 * (1.0 - t) ** 1.5
        bounce     = bounce_amp * (1.0 - math.cos(math.pi * 2.0 * (f - 140) / 100.0))
    else:
        bounce = 0.0

    R     = R_env + bounce
    theta = 18.0 * t
    spin  = 30.0 * t

    x1, y1 = R * r1_f * math.cos(theta),  R * r1_f * math.sin(theta)
    x2, y2 = -R * r2_f * math.cos(theta), -R * r2_f * math.sin(theta)

    insert_kf(knot1, f, (x1, y1, 0), (0, 0,        spin))
    insert_kf(knot2, f, (x2, y2, 0), (math.pi, 0, -spin))
    insert_kf(label_knot1, f, (x1, y1, 2.5))
    insert_kf(label_knot2, f, (x2, y2, 2.5))

    gx = -0.9 + (f / float(TOTAL_FRAMES)) * 2.0
    gy = -1.0 + get_gamma_intensity(f) * 0.7
    tracker_dot.location = (gx, gy, -9)
    tracker_dot.keyframe_insert("location", frame=f)

def add_flash(frame, energy):
    gamma_light.data.energy = 0.0
    gamma_light.data.keyframe_insert("energy", frame=frame - 2)
    gamma_light.data.energy = energy
    gamma_light.data.keyframe_insert("energy", frame=frame)
    gamma_light.data.energy = 0.0
    gamma_light.data.keyframe_insert("energy", frame=frame + 6)

add_flash(140, 1000000.0)
add_flash(240, 1800000.0)
add_flash(340, 3000000.0)

# --- COLLISION EVENT ---
insert_kf(knot2,       COLLISION_FRAME, (100, 100, 100))
insert_kf(label_knot2, COLLISION_FRAME, (100, 100, 100))

# [C5] FIXED: label_knot1 NOT teleported — stays visible on survivor
# label_knot1 continues to track knot1 position (stays at origin post-collision)
# No teleport to (100,100,100) — the label remains anchored to the surviving knot

toggle_visibility(hud_flash, COLLISION_FRAME, True, (0, 0, -8))

gamma_light.data.energy = 0.0
gamma_light.data.keyframe_insert("energy", frame=COLLISION_FRAME - 1)
gamma_light.data.energy = 15000000.0
gamma_light.data.keyframe_insert("energy", frame=COLLISION_FRAME + 5)
gamma_light.data.energy = 2000000.0
gamma_light.data.keyframe_insert("energy", frame=TOTAL_FRAMES)

flash_sphere.scale = (0, 0, 0)
flash_sphere.keyframe_insert("scale", frame=COLLISION_FRAME - 1)
flash_sphere.scale = (6, 6, 6)
flash_sphere.keyframe_insert("scale", frame=COLLISION_FRAME + 2)
flash_sphere.scale = (35, 35, 35)
flash_sphere.keyframe_insert("scale", frame=COLLISION_FRAME + 50)

mix_node = mat_super_flash.node_tree.nodes["FadeMix"]
mix_node.inputs['Fac'].default_value = 0.0
mix_node.inputs['Fac'].keyframe_insert("default_value", frame=COLLISION_FRAME - 1)
mix_node.inputs['Fac'].default_value = 1.0
mix_node.inputs['Fac'].keyframe_insert("default_value", frame=COLLISION_FRAME + 2)
mix_node.inputs['Fac'].default_value = 0.0
mix_node.inputs['Fac'].keyframe_insert("default_value", frame=COLLISION_FRAME + 40)

knot1.scale = (1.0, 1.0, 1.0)
knot1.keyframe_insert(data_path="scale", frame=COLLISION_FRAME - 1)
knot1.scale = (0.7, 0.7, 0.7)
knot1.keyframe_insert(data_path="scale", frame=COLLISION_FRAME + 40)

toggle_visibility(hud_flash, COLLISION_FRAME + 120, False, (0, 0, -8))

# Post-collision ringdown: knot1 (survivor) spins at origin
for f in range(COLLISION_FRAME + 1, TOTAL_FRAMES + 1):
    t_spin = 30.0 + (f - COLLISION_FRAME) * 0.1
    insert_kf(knot1, f, (0, 0, 0), (0, 0, t_spin))
    # [C5] label_knot1 tracks survivor at origin, elevated for visibility
    insert_kf(label_knot1, f, (0, 0, 1.5))

    gx = -0.9 + (f / float(TOTAL_FRAMES)) * 2.0
    gy = -1.0 + get_gamma_intensity(f) * 0.7
    tracker_dot.location = (gx, gy, -9)
    tracker_dot.keyframe_insert("location", frame=f)

bpy.context.scene.frame_set(1)
bpy.context.view_layer.update()
print("ECF Simulation V40.1-FIX (Excentric Orbits, Regime II) — generated successfully!")
