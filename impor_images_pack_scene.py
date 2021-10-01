import bpy
import os


class ImportImagesPackScenePSDOperator(bpy.types.Operator):
    bl_idname = "object.importimagespackscenepsd"
    bl_label = "Import Image"

    name: bpy.props.StringProperty(
        default='object',
        name='Object name'
    )

    file_name: bpy.props.StringProperty(
        default='--',
        name='file_name'
    )

    path: bpy.props.StringProperty(
        default='//',
        name='path'
    )

    x: bpy.props.IntProperty(
        default=0,
        name='x'
    )

    y: bpy.props.IntProperty(
        default=0,
        name='y'
    )

    width: bpy.props.IntProperty(
        default=100,
        name='width'
    )

    height: bpy.props.IntProperty(
        default=100,
        name='height'
    )

    level: bpy.props.IntProperty(
        default=0,
        name='level'
    )

    margin: bpy.props.FloatProperty(
        default=0,
        name='margin'
    )

    emission: bpy.props.BoolProperty(
        default=False,
        name='emission'
    )


    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.translate(value=(1, -1, -0))
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

        ob = context.active_object
        ob.name = self.name


        ob.scale[0] = self.width
        ob.scale[1] = self.height

        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        ob.location[0] = self.x
        ob.location[1] = -self.y
        ob.location[2] = self.margin * self.level

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')


        mat = bpy.data.materials.new(self.file_name + ':' + str(self.level) + '___' + os.path.basename(self.path))
        ob.data.materials.append(mat)
        mat.use_nodes = True

        bsdf = mat.node_tree.nodes["Principled BSDF"]
        
        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image = bpy.data.images.load(self.path)
        texImage.hide = True

        mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
        mat.node_tree.links.new(bsdf.inputs['Alpha'], texImage.outputs['Alpha'])

        mat.blend_method = 'CLIP'

        return {'FINISHED'}