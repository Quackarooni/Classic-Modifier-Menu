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
bl_info = {
    "name": "Classic Modifier Menu",
    "author": "Quackers",
    "description": "Addon for restoring the pre-4.0 style of the 'Add Modifiers' menu.",
    "blender": (4, 0, 0),
    "version" : (1, 1, 2),
    "location": "Properties",
    "category": "Interface",
}


import bpy
import sys

from . import operators, ui, keymaps, prefs 
modules = (operators, ui, keymaps, prefs,)


def reload_prepended_and_appended_draw_funcs():
    addons = bpy.context.preferences.addons
    addons = addons.keys()[:addons.find(__name__)]

    variables_to_look_up = set(ui.original_class_dict.keys())

    for mod_name in addons:
        module = sys.modules.get(mod_name)
        if module is None or module.register == register:
            continue

        # Get register variables
        var_names = list(module.register.__code__.co_names)

        # Get module and direct_submodule variables
        var_names.extend([item for item in dir(module) if not item.startswith("__")])

        if modules := getattr(module, "modules", None):
            for module in modules:
                var_names.extend([item for item in dir(module) if not item.startswith("__")])
                
        matches = variables_to_look_up.intersection(set(var_names))
        if matches:
            module.unregister()
            module.register()
            print(f"Classic Modifier Menu: Re-registered dependent module '{mod_name}'. - {matches}")
                
    return


def register():
    for module in modules:
        module.register()

    reload_prepended_and_appended_draw_funcs()
    

def unregister():
    for module in modules:
        module.unregister()

    reload_prepended_and_appended_draw_funcs()
    

if __name__ == "__main__":
    register()
