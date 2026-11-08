# test_scene.py — builds a simple animated 3D title scene and renders frames.
# Runs headless: blender -b --python scripts/test_scene.py
# Output: render/frame_0001.png ... (96 frames, 24 fps, 1280x720, Cycles CPU)
import bpy
import math
import os

os.makedirs('render', exist_ok=True)

# Clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 24
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 96  # 4 seconds
scene.render.filepath = 'render/frame_'
scene.render.image_settings.file_format = 'PNG'

# Dark blue world background
world = bpy.data.worlds['World']
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.02, 0.03, 0.08, 1.0)
bg.inputs[1].default_value = 1.0

# Sun light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.active_object
sun.data.energy = 3.0
sun.rotation_euler = (math.radians(50), 0, math.radians(30))

# Ground plane
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
ground = bpy.context.active_object
gmat = bpy.data.materials.new('Ground')
gmat.use_nodes = True
gmat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.05, 0.06, 0.12, 1.0)
gmat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.9
ground.data.materials.append(gmat)

# Gold title text, facing the camera
bpy.ops.object.text_add(location=(0, 0, 0.5))
text = bpy.context.active_object
text.data.body = 'VIDEO LAB'
text.data.size = 2.2
text.data.extrude = 0.15
text.data.align_x = 'CENTER'
text.data.align_y = 'CENTER'
text.rotation_euler = (math.radians(90), 0, 0)
gold = bpy.data.materials.new('Gold')
gold.use_nodes = True
bsdf = gold.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.9, 0.7, 0.2, 1.0)
bsdf.inputs['Metallic'].default_value = 0.8
bsdf.inputs['Roughness'].default_value = 0.3
text.data.materials.append(gold)
text.keyframe_insert(data_path='location', frame=1)
text.location = (0, 0, 1.5)
text.keyframe_insert(data_path='location', frame=96)

# Three spinning cubes
colors = [(0.8, 0.2, 0.2, 1.0), (0.2, 0.7, 0.3, 1.0), (0.2, 0.4, 0.9, 1.0)]
positions = [(-3.5, 1.5, 0.7), (3.5, 1.5, 0.7), (0, 2.5, 0.7)]
for i, (color, pos) in enumerate(zip(colors, positions)):
    bpy.ops.mesh.primitive_cube_add(size=1.4, location=pos)
    cube = bpy.context.active_object
    mat = bpy.data.materials.new(f'Cube{i}')
    mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = color
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.4
    cube.data.materials.append(mat)
    cube.rotation_euler = (0, 0, 0)
    cube.keyframe_insert(data_path='rotation_euler', frame=1)
    cube.rotation_euler = (0, 0, math.radians(360))
    cube.keyframe_insert(data_path='rotation_euler', frame=96)

# Camera on a slow dolly, always looking at the title
bpy.ops.object.empty_add(location=(0, 0, 1.2))
target = bpy.context.active_object
target.name = 'LookTarget'
bpy.ops.object.camera_add(location=(-3, -9, 3))
cam = bpy.context.active_object
cam.name = 'Camera'
track = cam.constraints.new(type='TRACK_TO')
track.target = target
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
scene.camera = cam
cam.location = (-3, -9, 3)
cam.keyframe_insert(data_path='location', frame=1)
cam.location = (3, -9, 3)
cam.keyframe_insert(data_path='location', frame=96)

bpy.ops.render.render(animation=True)
print('RENDER DONE')
