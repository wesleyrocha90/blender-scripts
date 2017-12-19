bl_info = {
    "name": "Export for unity (Simple Games Brasil)",
    "description": "",
    "author": "",
    "version": (0, 0, 1),
    "blender": (2, 70, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

import bpy
import os
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )


# ------------------------------------------------------------------------
#    store properties in the active scene
# ------------------------------------------------------------------------

class MySettings(PropertyGroup):

    ifSelectedObjects = BoolProperty(
        name="Only Selected Objects",
        description="Enable to export only selecteds objects",
        default = True
        )
        
    ifApplyTransforms = BoolProperty(
        name="Apply Transforms",
        description="Enable to to apply transforms before export",
        default = True
        )

    pathToExport = StringProperty(
        name="Destination",
        description="Destination where the objects will be exported to",
        subtype='DIR_PATH',
        maxlen=1024,
        )

# ------------------------------------------------------------------------
#    operators
# ------------------------------------------------------------------------

class ExportOperator(Operator):
    bl_idname = "export.operator"
    bl_label = "Export"

    def execute(self, context):
        scene = context.scene
        myexport = scene.my_export
        
        # all code here
        originalObjActive = scene.objects.active
        originalObjSelected = context.selected_objects
        
        if not myexport.ifSelectedObjects:
            bpy.ops.object.select_all(action='SELECT')
        selection = context.selected_objects
        
        for obj in selection:
            obj.select = True
            scene.objects.active = obj
            
            name = bpy.path.clean_name(obj.name)
            fn = os.path.join(myexport.pathToExport, name)
            
            bpy.ops.object.transform_apply(location = False, rotation = True, scale = True)
            bpy.ops.export_scene.fbx(filepath = fn + '.fbx', use_selection = True)
            
            obj.select = False
        
        # come things back as they are before
        scene.objects.active = originalObjActive
        for obj in originalObjSelected:
            obj.select = True
        
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    my tool in objectmode
# ------------------------------------------------------------------------

class ExportPane(Panel):
    bl_idname = "ExportPane"
    bl_label = "Export to Unity"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "SimpleGames"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        myexport = scene.my_export

        layout.prop(myexport, "ifSelectedObjects")
        layout.prop(myexport, "ifApplyTransforms")
        layout.prop(myexport, "pathToExport")
        layout.operator("export.operator", icon = "EXPORT")

# ------------------------------------------------------------------------
# register and unregister
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.my_export = PointerProperty(type=MySettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.my_export

# pra criar um addon é só apagar essas linhas abaixo
if __name__ == "__main__":
    register()