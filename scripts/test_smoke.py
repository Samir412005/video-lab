#!/usr/bin/env python3
"""Phase 2 capability test B — Smoke (Blender mantaflow, CPU).

Tests whether a small gas smoke simulation is feasible on the cloud
runner: bake a 48-frame smoke plume (domain resolution 32) and render it
with a Principled Volume material. If the bake or the render is too slow,
the production film uses particles/atmosphere instead of real smoke.

Run headless:  blender -b --python scripts/test_smoke.py
Output: render_smoke/frame_0001.png ... frame_0048.png (48 frames,
1280x720, 24 fps). NOTE: use Blender's "####" placeholder in the
filepath — Blender does NOT interpret "%04d", it appends the frame
number to the filename, which broke the ffmpeg step in run #2.
"""
import bpy
import os

OUT = os.path.join(os.getcwd(), "render_smoke")
os.makedirs(OUT, exist_ok=True)
CACHE = os.path.join(os.getcwd(), "smoke_cache")
os.makedirs(CACHE, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 48
scene.cycles.use_denoising = False  # apt Blender 4.0.2: no OpenImageDenoiser
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 48
scene.render.filepath = os.path.join(OUT, "frame_####.png")
scene.render.image_settings.file_format = "PNG"

# World: dim, so the smoke reads.
# Blender 5.0's default file ships no "World" data-block — get-or-create
# (same fix as test_cinematic.py run #2; direct ["World"] KeyErrors).
world = bpy.data.worlds.get("World")
if world is None:
    world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.02, 0.02, 0.03, 1.0)
bg.inputs["Strength"].default_value = 1.0

# Ground
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
ground = bpy.context.active_object
mat = bpy.data.materials.new("Ground")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.05, 0.06, 1.0)
ground.data.materials.append(mat)

# --- Smoke domain ---------------------------------------------------------
bpy.ops.mesh.primitive_cube_add(size=4.0, location=(0, 0, 2.0))
domain = bpy.context.active_object
domain.name = "SmokeDomain"
mod = domain.modifiers.new("Fluid", "FLUID")
mod.fluid_type = "DOMAIN"
d = mod.domain_settings
d.domain_type = "GAS"
d.resolution_max = 32
d.use_noise = False
d.cache_directory = CACHE
d.cache_frame_start = 1
d.cache_frame_end = 48
# Volume material so the smoke is visible in Cycles.
vol_mat = bpy.data.materials.new("SmokeVolume")
vol_mat.use_nodes = True
vol = vol_mat.node_tree.nodes.new("ShaderNodeVolumePrincipled")
vol.inputs["Density"].default_value = 1.0
vol.inputs["Color"].default_value = (0.7, 0.7, 0.75, 1.0)
out = vol_mat.node_tree.nodes["Material Output"]
vol_mat.node_tree.links.new(vol.outputs["Volume"], out.inputs["Volume"])
domain.data.materials.append(vol_mat)

# --- Flow object (smoke source) -------------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, location=(0, 0, 0.6))
flow = bpy.context.active_object
flow.name = "SmokeFlow"
mod2 = flow.modifiers.new("Fluid", "FLUID")
mod2.fluid_type = "FLOW"
f = mod2.flow_settings
f.flow_type = "SMOKE"
f.flow_behavior = "INFLOW"
f.density = 1.0
f.use_initial_velocity = True
f.velocity_factor = 1.5

# --- Light + camera ---------------------------------------------------------
bpy.ops.object.light_add(type="AREA", location=(3, -3, 5))
light = bpy.context.active_object
light.data.energy = 600
light.data.shape = "DISK"
light.data.size = 3.0
light.data.color = (1.0, 0.9, 0.7)

bpy.ops.object.camera_add(location=(5.0, -5.0, 3.0))
cam = bpy.context.active_object
cam.data.lens = 50
scene.camera = cam
track = cam.constraints.new(type="TRACK_TO")
track.target = domain
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"

print("Baking smoke (48 frames, resolution 32) ...")
# bake_all() looks at the ACTIVE object — after the camera was created
# the domain is no longer active, so bake fails with "no Fluid modifier
# found" (run #4). Make the domain active first.
bpy.context.view_layer.objects.active = domain
domain.select_set(True)
bpy.ops.fluid.bake_all()
print("SMOKE BAKE DONE")
print("Rendering 48 frames (smoke test) ...")
bpy.ops.render.render(animation=True)
print("SMOKE DONE")
