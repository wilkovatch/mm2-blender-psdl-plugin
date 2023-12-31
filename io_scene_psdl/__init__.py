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

if "bpy" in locals():
    import importlib
    importlib.reload(MainWriter)
else:
    from .common.main_writer import MainWriter

import sys
import bpy
from bpy_extras.io_utils import (
    ExportHelper, ImportHelper
)
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    StringProperty,
    CollectionProperty,
    IntProperty,
    PointerProperty
)
from .scene_input import BlenderSceneInput
bl_info = {
    "name": "Angel Studios PSDL Format",
    "author": "Wilhelm Kovatch",
    "version": (0, 2, 1),
    "blender": (2, 91, 2),
    "location": "File > Export > Angel Studios PSDL Format",
    "description": "Export PSDL files",
    "support": 'COMMUNITY',
    "category": "Export"}

class ExportPSDL(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.psdl"
    bl_label = 'Export PSDL'

    split_non_coplanar_roads: BoolProperty(
        name="Split non-coplanar roads",
        description="Splits non-coplanar roads in two triangular pieces to fix bound issues\n" \
        "(Note: not implemented for divided roads, and breaks other stuff (such as props and galleries))",
        default=False,
    )

    cap_materials: BoolProperty(
        name="Cap PSDL materials to 511 (TESTING ONLY)",
        description="Stock MM2 and tools like MM2 City Toolkit cannot handle PSDL files with more than 511 textures, " \
        "enabling this flag will cap texture IDs to 511 if greater.\nIt will break them though if this happens, " \
        "use it only for testing.\nIf disabled, there is still a cap of 2047 materials.",
        default=False,
    )

    accurate_bai_culling: BoolProperty(
        name="Accurate culling for BAI",
        description="Calculates the BAI culling with more accuracy (SLOW)",
        default=False,
    )

    write_psdl: BoolProperty(
        name="Export PSDL",
        description="Export the PSDL file",
        default=True,
    )

    write_inst: BoolProperty(
        name="Export INST",
        description="Export the INST file",
        default=False,
    )

    write_bai: BoolProperty(
        name="Export BAI",
        description="Export the BAI file",
        default=False,
    )

    write_pathset: BoolProperty(
        name="Export PATHSET",
        description="Export the PATHSET file",
        default=False,
    )

    filename_ext = ".psdl"
    filter_glob: StringProperty(default="*.psdl", options={'HIDDEN'})

    def execute(self, context):
        scene_input = BlenderSceneInput()
        writer = MainWriter(self.properties.filepath, scene_input,
                            self.write_psdl, self.write_inst, self.write_bai, self.write_pathset,
                            self.split_non_coplanar_roads, self.accurate_bai_culling, self.cap_materials)
        writer.write()
        return {'FINISHED'}


def menu_func_export(self, context):
    self.layout.operator(ExportPSDL.bl_idname, text="Angel Studios PSDL (.psdl)")


def register():
    bpy.utils.register_class(ExportPSDL)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ExportPSDL)


if __name__ == "__main__":
    register()
