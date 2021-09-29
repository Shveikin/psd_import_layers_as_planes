
from genericpath import exists
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy_extras.io_utils import ImportHelper
from mathutils import Vector

import os
import sys

root = os.path.dirname(__file__)

sys.path.append(root)
sys.path.append(root + "/psd")
sys.path.append(root + "/psd/psd_tools")



from psd_tools import PSDImage


def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y

    verts = [
        Vector((-1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, -1 * scale_y, 0)),
        Vector((-1 * scale_x, -1 * scale_y, 0)),
    ]

    edges = []
    faces = [[0, 1, 2, 3]]

    mesh = bpy.data.meshes.new(name="New Object Mesh")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_add_object(Operator, ImportHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.psd_import_as_planes"
    bl_label = "Import as planes"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: bpy.props.StringProperty(
        default='*.psd',
        options={'HIDDEN'}
    )
    
    some_boolean: bpy.props.BoolProperty(
        name='emission material',
        description='Texture',
        default=True,
    )


    def execute(self, context):
        dir = (os.path.dirname(self.filepath) if bpy.path.abspath("//")=='' else bpy.path.abspath("//")) + os.path.basename(self.filepath)
        if (not os.path.isdir(dir)):
            os.mkdir(dir, 0o666)


        psd = PSDImage.open(self.filepath)

        for layer in psd:
            # print('id - name',layer.layer_id, layer.name)

            # print("\t", layer.top)

            # print(layer.left, layer.width)
            # print("\t", layer.height)
            imageName = dir + '\\' + layer.name + '.png'
            layer.composite().save(imageName)


        # 

        # # if self.some_boolean:
        # #     PSDImage

        # print('Selected file:', self.filepath)
        # print('File name:', filename)
        # print('File extension:', extension)
        # print('Some Boolean:', self.some_boolean)
        return {'FINISHED'}

        


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="PSD import layers as planes",
        icon='IMAGE_RGB'
    )


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.psd_import_as_planes", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping