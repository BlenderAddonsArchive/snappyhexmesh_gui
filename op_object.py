# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
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

# <pep8-80 compliant>

# ----------------------------------------------------------------------------
# Object related functionality
from .op_gen import *

# ----------------------------------------------------------------------------

def get_object_bbox_coords(obj):
    """Returns two vectors which contain the minimum and maximum coordinates
    for bounding box for object obj
    """

    # Acknowledgement: Here is nice explanation of obj.bound_box and example
    # for using Blender's bounding box data in python by zeffii:
    # https://blender.stackexchange.com/questions/32283/what-are-all-values-in-bound-box

    worldify = lambda p: obj.matrix_world @ mathutils.Vector(p[:])
    coords = [worldify(p).to_tuple() for p in obj.bound_box[:]]
    rotated = list(zip(*coords[::]))
    min_bbox = [min(c) for c in rotated]
    max_bbox = [max(c) for c in rotated]

    return min_bbox, max_bbox


def get_global_bbox_coords():
    """Returns two vectors which contain the minimum and maximum coordinates
    for bounding box for all mesh objects included in export
    """

    all_mins=[];
    all_maxs=[];
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if not obj.shmg_include_in_export:
            continue

        obj_min_bbox, obj_max_bbox = get_object_bbox_coords(obj)
        all_mins.append(obj_min_bbox)
        all_maxs.append(obj_max_bbox)

    rot_min = zip(*all_mins[::])
    global_min_bbox = [min(c) for c in rot_min]
    rot_max = zip(*all_maxs[::])
    global_max_bbox = [max(c) for c in rot_max]

    return global_min_bbox, global_max_bbox


def block_mesh_cell_count(bb_min, bb_max, gui):
    """Returns number of cells in Block Mesh and updates
    block_mesh_* data in gui. bb_min and bb_max are
    minimum and maximum bounding box coordinates.
    """

    sl = gui.cell_side_length

    for i in range(0,3):
        bm_min = math.floor(bb_min[i] / sl)
        bm_max = math.ceil(bb_max[i] / sl)
        gui.block_mesh_delta[i] = bm_max - bm_min
        gui.block_mesh_min[i] = math.floor(bb_min[i] / sl) * sl
        gui.block_mesh_max[i] = math.ceil(bb_max[i] / sl) * sl

    bm_count = gui.block_mesh_delta[0] * \
               gui.block_mesh_delta[1] * \
               gui.block_mesh_delta[2]

    return bm_count
