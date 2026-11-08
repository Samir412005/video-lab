import bpy
import random
from math import radians

# «الوقت» — Blender 3D opener: golden cubes rise and assemble into a tower.
# 5 s @ 30 fps (150 frames), 1280x720, Cycles CPU, no denoising
# (Ubuntu's apt Blender 4.0.2 is built WITHOUT OpenImageDenoiser).

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 24
scene.cycles.use_denoising = False
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 150
scene.render.filepath = 'render/frame_'
scene.render.image_settings.file_format = 'PNG'

world = bpy.data.worlds['World']
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.02, 0.03, 0.06, 1)
world.node_tree.nodes['Background'].inputs[1].default_value = 1.0

bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.active_object
sun.data.energy = 3.0
sun.rotation_euler = (radians(50), 0, radians(30))

bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
ground = bpy.context.active_object
mat_ground = bpy.data.materials.new(name='Ground')
mat_ground.use_nodes = True
mat_ground.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.05, 0.06, 0.09, 1)
mat_ground.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.9
ground.data.materials.append(mat_ground)

random.seed(7)
colors = [(1.0, 0.76, 0.0, 1), (1.0, 0.84, 0.2, 1), (0.9, 0.62, 0.0, 1)]
for i in range(6):
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(random.uniform(-2.5, 2.5), random.uniform(-1.5, 1.5), -3 - i * 0.5))
    cube = bpy.context.active_object
    mat = bpy.data.materials.new(name=f'Gold{i}')
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = colors[i % 3]
    bsdf.inputs['Metallic'].default_value = 0.9
    bsdf.inputs['Roughness'].default_value = 0.25
    cube.data.materials.append(mat)
    cube.keyframe_insert(data_path='location', frame=1)
    cube.rotation_euler = (0, 0, radians(random.uniform(-30, 30)))
    cube.keyframe_insert(data_path='rotation_euler', frame=1)
    cube.location = ((i % 2) * 0.4 - 0.2, 0, 0.5 + i * 1.05)
    cube.keyframe_insert(data_path='location', frame=90 + i * 8)
    cube.rotation_euler = (0, 0, 0)
    cube.keyframe_insert(data_path='rotation_euler', frame=90 + i * 8)

bpy.ops.object.camera_add(location=(-8, -11, 5.5))
cam = bpy.context.active_object
scene.camera = cam
empty = bpy.data.objects.new('Target', None)
scene.collection.objects.link(empty)
empty.location = (0, 0, 2.5)
track = cam.constraints.new(type='TRACK_TO')
track.target = empty
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
cam.keyframe_insert(data_path='location', frame=1)
cam.location = (-5, -8, 4.2)
cam.keyframe_insert(data_path='location', frame=150)

print('RENDER DONE')
bpy.ops.render.render(animation=True)
