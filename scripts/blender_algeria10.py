import bpy
import os
from math import radians

# 10s Algeria video — Blender 3D opener: the Algerian flag waving.
# 3 s @ 30 fps (90 frames), 1280x720, Cycles CPU, no denoising
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
scene.frame_end = 90
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

bpy.ops.object.light_add(type='POINT', location=(0, -3, 2))
warm = bpy.context.active_object
warm.data.energy = 60.0
warm.data.color = (1.0, 0.85, 0.6)

# Flag: subdivided grid, stood upright, flag texture, wave modifier.
bpy.ops.mesh.primitive_grid_add(x_subdivisions=40, y_subdivisions=28, size=3.0,
                                location=(0, 0, 1.2))
flag = bpy.context.active_object
flag.scale = (1.0, 0.667, 1.0)
flag.rotation_euler = (radians(90), 0, 0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

mat = bpy.data.materials.new(name='Flag')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Roughness'].default_value = 0.6
bsdf.inputs['Metallic'].default_value = 0.0
tex = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
tex.image = bpy.data.images.load(os.path.join(os.getcwd(), 'assets/algeria-flag.png'))
mat.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
flag.data.materials.append(mat)

wave = flag.modifiers.new(name='Wave', type='WAVE')
wave.wave_height = 0.08
wave.wave_width = 1.2
wave.wave_speed = 0.5
wave.lifetime = 0

bpy.ops.object.camera_add(location=(0, -5.5, 1.6))
cam = bpy.context.active_object
scene.camera = cam
empty = bpy.data.objects.new('Target', None)
scene.collection.objects.link(empty)
empty.location = (0, 0, 1.2)
track = cam.constraints.new(type='TRACK_TO')
track.target = empty
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
cam.keyframe_insert(data_path='location', frame=1)
cam.location = (0, -4.2, 1.3)
cam.keyframe_insert(data_path='location', frame=90)

print('RENDER DONE')
bpy.ops.render.render(animation=True)
