#!/usr/bin/env python3
"""Phase 2 capability test A — Cinematic look (Blender Cycles, CPU).

Tests, in one render: PBR materials (gold metal, rough stone, glass),
HDRI studio lighting + warm key + cool rim, camera dolly + orbit,
depth of field, motion blur, and glowing ember particles.
No denoising (apt Blender 4.0.2 has no OpenImageDenoiser).

Run headless:  blender -b --python scripts/test_cinematic.py
Output: render_cine/frame_%04d.png (48 frames, 1280x720, 24 fps)
"""
import bpy
import math
import os

OUT = os.path.join(os.getcwd(), os.environ.get("RENDER_OUT", "render_cine"))
os.makedirs(OUT, exist_ok=True)

# --- Clean scene -------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Render settings ---------------------------------------------------
# Engine selectable via RENDER_ENGINE env var (CYCLES default; EEVEE for
# the real-time comparison test). Both run headless on the Actions runner.
engine = os.environ.get("RENDER_ENGINE", "CYCLES")
scene = bpy.context.scene
scene.render.engine = engine
if engine == "CYCLES":
    scene.cycles.device = "CPU"
    scene.cycles.samples = 64
    scene.cycles.use_denoising = False  # apt Blender 4.0.2: no OpenImageDenoiser
    scene.cycles.max_bounces = 6
else:  # EEVEE (real-time; needs a GL context — may fail headless)
    scene.eevee.taa_render_samples = 64
    scene.eevee.use_motion_blur = True
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 48
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.5
scene.render.filepath = os.path.join(OUT, "frame_%04d.png")
scene.render.image_settings.file_format = "PNG"

# --- World: HDRI studio lighting ---------------------------------------
world = bpy.data.worlds["World"]
world.use_nodes = True
env = world.node_tree.nodes.new("ShaderNodeTexEnvironment")
hdri = os.path.join(os.getcwd(), "assets", "hdri", "studio_small_09_2k.hdr")
env.image = bpy.data.images.load(hdri)
bg = world.node_tree.nodes["Background"]
world.node_tree.links.new(env.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 0.9
print("HDRI loaded:", hdri)

# --- Materials ----------------------------------------------------------
def principled(name, color, metallic=0.0, roughness=0.5, transmission=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if transmission:
        bsdf.inputs["Transmission Weight"].default_value = transmission
    return mat

gold = principled("Gold", (1.0, 0.65, 0.15), metallic=1.0, roughness=0.18)
stone = principled("Stone", (0.25, 0.25, 0.27), metallic=0.0, roughness=0.9)
glass = principled("Glass", (1.0, 1.0, 1.0), metallic=0.0, roughness=0.05,
                   transmission=1.0)

# --- Objects ------------------------------------------------------------
# Pedestal (stone)
bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 1.0))
pedestal = bpy.context.active_object
pedestal.name = "Pedestal"
pedestal.data.materials.append(stone)

# Gold torus (hero subject, floating above the pedestal)
bpy.ops.mesh.primitive_torus_add(major_radius=0.7, minor_radius=0.28,
                                 location=(0, 0, 2.6))
torus = bpy.context.active_object
torus.name = "GoldTorus"
torus.data.materials.append(gold)
torus.rotation_euler = (math.radians(75), 0, 0)
# Slow spin over the shot
torus.keyframe_insert(data_path="rotation_euler", frame=1)
torus.rotation_euler = (math.radians(75), 0, math.radians(40))
torus.keyframe_insert(data_path="rotation_euler", frame=48)

# Glass sphere (reflections / refraction test)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45, location=(1.4, -0.6, 2.6))
sphere = bpy.context.active_object
sphere.name = "GlassSphere"
sphere.data.materials.append(glass)

# Ground plane (dark, slightly reflective)
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
ground = bpy.context.active_object
ground_mat = principled("Ground", (0.05, 0.05, 0.06), roughness=0.4,
                        metallic=0.3)
ground.data.materials.append(ground_mat)

# --- Lights ---------------------------------------------------------------
# Warm key (area)
bpy.ops.object.light_add(type="AREA", location=(4, -4, 5))
key = bpy.context.active_object
key.data.energy = 800
key.data.shape = "DISK"
key.data.size = 3.0
key.data.color = (1.0, 0.85, 0.6)
# Cool rim (area, from behind)
bpy.ops.object.light_add(type="AREA", location=(-4, 4, 4))
rim = bpy.context.active_object
rim.data.energy = 500
rim.data.shape = "DISK"
rim.data.size = 2.5
rim.data.color = (0.5, 0.7, 1.0)

# --- Ember particles ------------------------------------------------------
# Tiny glowing icosphere as the particle instance object.
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.02, location=(0, 0, 0.2))
ember_obj = bpy.context.active_object
ember_obj.name = "Ember"
ember_mat = bpy.data.materials.new("EmberGlow")
ember_mat.use_nodes = True
emis = ember_mat.node_tree.nodes.new("ShaderNodeEmission")
emis.inputs["Color"].default_value = (1.0, 0.45, 0.05, 1.0)
emis.inputs["Strength"].default_value = 8.0
out = ember_mat.node_tree.nodes["Material Output"]
ember_mat.node_tree.links.new(emis.outputs["Emission"], out.inputs["Surface"])
ember_obj.data.materials.append(ember_mat)
ember_obj.hide_render = True  # only the particles are visible

# Emitter: a small disc under the torus.
bpy.ops.mesh.primitive_circle_add(radius=1.2, location=(0, 0, 0.1))
emitter = bpy.context.active_object
emitter.name = "EmberEmitter"
bpy.ops.object.particle_system_add()
ps = emitter.particle_systems[0]
s = ps.settings
s.count = 600
s.frame_start = 1
s.frame_end = 48
s.lifetime = 45
s.normal_factor = 0.4
s.factor_random = 0.8
s.physics_type = "NEWTON"
s.effector_weights.gravity = -0.15  # embers rise
s.render_type = "OBJECT"
s.instance_object = ember_obj
print("Particles: 600 embers, OBJECT render, emission material")

# --- Camera: dolly-in + slight orbit, DOF on the torus --------------------
bpy.ops.object.camera_add(location=(5.5, -5.5, 3.2))
cam = bpy.context.active_object
cam.name = "Camera"
cam.data.lens = 50
cam.data.dof.use_dof = True
cam.data.dof.focus_object = torus
cam.data.dof.aperture_fstop = 2.8
scene.camera = cam
# Track the torus so the orbit stays framed.
track = cam.constraints.new(type="TRACK_TO")
track.target = torus
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"
# Keyframes: dolly in + orbit
cam.location = (5.5, -5.5, 3.2)
cam.keyframe_insert(data_path="location", frame=1)
cam.location = (3.8, -3.8, 2.6)
cam.keyframe_insert(data_path="location", frame=48)

print("Rendering 48 frames (cinematic test) ...")
bpy.ops.render.render(animation=True)
print("CINE DONE")
