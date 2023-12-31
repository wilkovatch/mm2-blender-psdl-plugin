# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Script copyright (C) Wilhelm Kovatch

import bpy, bmesh
from .common.scene_input import SceneInput


class BlenderSceneInput(SceneInput):
    def __init__(self):
        self.win = bpy.context.window_manager

    def init_progress_bar(self):
        self.win.progress_begin(0, 10000)

    def set_progress_bar(self, value):
        self.win.progress_update(value * 10000)

    def end_progress_bar(self):
        self.win.progress_end()

    def get_object_list(self):
        return bpy.data.objects

    def get_object_name(self, obj):
        return obj.name

    def get_rotation(self, obj):
        return obj.rotation_quaternion.to_euler()

    def get_property_container(self, obj):
        return obj

    def get_vertices_num(self, obj):
        if hasattr(obj, "data"):
            return len(obj.data.vertices) if hasattr(obj.data, "vertices") else 0
        elif hasattr(obj, "verts"):
            return len(obj.verts)
        else:
            return 0

    def get_vertex(self, obj, i):
        if hasattr(obj, "data"):
            v_local = obj.data.vertices[i].co
            v_global = obj.matrix_world @ v_local
            return v_global
        else:
            return obj.verts[i].co

    def get_polygons_num(self, obj):
        if hasattr(obj, "data"):
            return len(obj.data.polygons) if hasattr(obj.data, "polygons") else 0
        elif hasattr(obj, "faces"):
            return len(obj.faces)
        else:
            return 0

    def get_polygon(self, obj, i):
        if hasattr(obj, "data"):
            ff1 = obj.data.polygons[i].vertices
            ff = [ff1[0], ff1[1], ff1[2]]
        else:
            ff1 = obj.faces[i].verts
            ff = [ff1[0].index, ff1[1].index, ff1[2].index]
        return ff

    def get_position(self, obj):
        return obj.location

    def get_scale(self, obj):
        return obj.scale

    def create_composed_mesh(self):
        return bmesh.new()

    def create_and_add_composed_mesh_from_object(self, obj, new_block):
        newb = bmesh.new()
        newb.from_mesh(obj.data)
        newb.transform(obj.matrix_world)
        temp_mesh = bpy.data.meshes.new(".temp")
        newb.to_mesh(temp_mesh)
        new_block.from_mesh(temp_mesh)
        bpy.data.meshes.remove(temp_mesh)
        newb.verts.ensure_lookup_table()
        return newb

    def destroy_composed_mesh(self, mesh):
        mesh.free()

    def remove_doubles(self, new_block, epsilon):
        bmesh.ops.remove_doubles(new_block, verts=new_block.verts, dist=epsilon)
        new_block.verts.ensure_lookup_table()
        new_block.faces.ensure_lookup_table()
