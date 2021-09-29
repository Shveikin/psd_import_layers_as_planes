import bpy

bl_info = {
    "name" : "PSDImportayersAsPlanes",
    "author" : "Ilya",
    "description" : "Import layers from psd file",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "import"
}

import os
import sys
root = os.path.dirname(__file__)
sys.path.append(root)

from psdimport import OBJECT_OT_add_object, add_object_manual_map, add_object_button


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)
