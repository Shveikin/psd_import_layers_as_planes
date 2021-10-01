
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

    prefix: bpy.props.StringProperty(
        name='Object name prefix',
        description='Префикс',
        default='',
    )
    
    emission: bpy.props.BoolProperty(
        name='Emission material',
        description='Texture',
        default=True,
    )

    scale: bpy.props.FloatProperty(
        name='Scale',
        description='Масштаб',
        default=0.5,
        min=0.1,
        soft_max=1,
        subtype='FACTOR'
    )

    margin: bpy.props.FloatProperty(
        name='Margin',
        description='Отступ между слоями',
        default=0.2,
        min=0,
        soft_max=1,
        subtype='FACTOR'
    )

    def waiting(self, show):
        print('wait...')

    def execute(self, context):
        dir = (os.path.dirname(self.filepath) if bpy.path.abspath("//")=='' else bpy.path.abspath("//")) + "_" + os.path.basename(self.filepath)
        if (not os.path.isdir(dir)):
            os.mkdir(dir, 0o666)

        psd = PSDImage.open(self.filepath)
        self.waiting(True)

        level = 0
        for layer in psd:
            imageName = dir + '\\' + layer.name + '.png'
            layer.composite().save(imageName)
            
            bpy.ops.object.importimagespackscenepsd(
                name = self.prefix + '_' + layer.name,
                file_name = os.path.basename(self.filepath),
                path = imageName,
                x = (layer.left *2) * self.scale,
                y = (layer.top *2) * self.scale,
                width = (layer.width) * self.scale,
                height = (layer.height) * self.scale,
                level = level,
                margin = self.margin,
                emission = False
            )

            level+=1
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
