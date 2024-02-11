from .keymap_ui import KeymapItemDef, KeymapStructure, KeymapLayout
from .operators import (
    INVOKE_OT_ADD_GPENCIL_SHADERFX_MENU, 
    INVOKE_OT_CLASSIC_MODIFIER_MENU, 
    INVOKE_OT_ASSET_MODIFIER_MENU, 
    INVOKE_OT_ADD_GPENCIL_MODIFIER_MENU, 
    INVOKE_OT_ADD_GPENCIL_SHADERFX_MENU,
    INVOKE_OT_ADD_CONSTRAINTS_MENU,
    INVOKE_OT_ADD_BONE_CONSTRAINTS_MENU,
    )

keymap_info = {
    "keymap_name" : "Property Editor",
    "space_type" : "PROPERTIES",
}

keymap_defs = (
    (INVOKE_OT_CLASSIC_MODIFIER_MENU.bl_idname, 'A', True, None),
    (INVOKE_OT_ASSET_MODIFIER_MENU.bl_idname, 'NONE', False, None),
    (INVOKE_OT_ADD_GPENCIL_MODIFIER_MENU.bl_idname, 'A', True, None),
    (INVOKE_OT_ADD_GPENCIL_SHADERFX_MENU.bl_idname, 'A', True, None),
    (INVOKE_OT_ADD_CONSTRAINTS_MENU.bl_idname, 'A', True, None),
    (INVOKE_OT_ADD_BONE_CONSTRAINTS_MENU.bl_idname, 'A', True, None),
)


keymap_structure = KeymapStructure([
    KeymapItemDef(INVOKE_OT_CLASSIC_MODIFIER_MENU.bl_idname, **keymap_info, shift=True, key_type='A'),
    KeymapItemDef(INVOKE_OT_ASSET_MODIFIER_MENU.bl_idname, **keymap_info),
    KeymapItemDef(INVOKE_OT_ADD_GPENCIL_MODIFIER_MENU.bl_idname, **keymap_info, shift=True, key_type='A'),
    KeymapItemDef(INVOKE_OT_ADD_GPENCIL_SHADERFX_MENU.bl_idname, **keymap_info, shift=True, key_type='A'),
    KeymapItemDef(INVOKE_OT_ADD_CONSTRAINTS_MENU.bl_idname, **keymap_info, shift=True, key_type='A'),
    KeymapItemDef(INVOKE_OT_ADD_BONE_CONSTRAINTS_MENU.bl_idname, **keymap_info, shift=True, key_type='A'),
    ]
)


keymap_layout = KeymapLayout(layout_structure=keymap_structure)


def register():
    keymap_structure.register()


def unregister():
    keymap_structure.unregister()
