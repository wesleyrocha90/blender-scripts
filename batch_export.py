# Exporta cada um dos objetos selecionados pro seu próprio arquivo

import bpy
import os

# os exports sao colocados na pasta [Projeto]\models\exporteds
filepath = bpy.data.filepath
dirname = os.path.dirname(filepath)

if not dirname:
    raise Exception("Blend file is not saved")
while os.path.split(dirname)[1] != 'models':
    dirname = os.path.split(dirname)[0]
exportePath = os.path.join(dirname, 'exporteds')


scene = bpy.context.scene

obj_active = scene.objects.active
selection = bpy.context.selected_objects

bpy.ops.object.select_all(action='DESELECT')

for obj in selection:

    obj.select = True
    scene.objects.active = obj

    name = bpy.path.clean_name(obj.name)
    fn = os.path.join(exportePath, name)

    bpy.ops.export_scene.fbx(filepath=fn+'.fbx', use_selection=True)

    obj.select = False

#volta ao que tava antes
scene.objects.active = obj_active
for obj in selection:
    obj.select = True
