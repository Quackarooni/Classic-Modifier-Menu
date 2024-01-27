import bpy
from bpy.types import Operator
from .ui import OBJECT_MT_modifier_add_assets, OBJECT_MT_gpencil_modifier_add


class InvokeMenuBaseClass:
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        # NOTE: This operator only exists to add a poll to the add modifier shortcut in the property editor.
        space = context.space_data
        return space and space.type == 'PROPERTIES' and space.context == cls.space_context

    def invoke(self, context, event):
        return bpy.ops.wm.call_menu(name=self.menu_id)


class INVOKE_OT_CLASSIC_MODIFIER_MENU(InvokeMenuBaseClass, Operator):
    bl_idname = "object.invoke_classic_modifier_menu"
    bl_label = "Add Modifier"
    menu_id = "OBJECT_MT_modifier_add"
    space_context = 'MODIFIER'

    @classmethod
    def poll(cls, context):
        is_space_valid = super().poll(context)
        obj = context.active_object

        return is_space_valid and obj and obj.type != 'GPENCIL'


class INVOKE_OT_ASSET_MODIFIER_MENU(InvokeMenuBaseClass, Operator):
    bl_idname = "object.invoke_asset_modifier_menu"
    bl_label = "Add Asset Modifier"
    menu_id = OBJECT_MT_modifier_add_assets.__name__
    space_context = 'MODIFIER'

    @classmethod
    def poll(cls, context):
        is_space_valid = super().poll(context)
        obj = context.active_object

        return is_space_valid and obj and obj.type != 'GPENCIL'


class INVOKE_OT_ADD_GPENCIL_MODIFIER_MENU(InvokeMenuBaseClass, Operator):
    bl_idname = "object.invoke_add_gpencil_modifier_menu"
    bl_label = "Add Modifier"
    menu_id = OBJECT_MT_gpencil_modifier_add.__name__
    space_context = 'MODIFIER'

    @classmethod
    def poll(cls, context):
        is_space_valid = super().poll(context)
        obj = context.active_object

        return is_space_valid and obj and obj.type == 'GPENCIL'


class INVOKE_OT_ADD_GPENCIL_SHADERFX_MENU(InvokeMenuBaseClass, Operator):
    bl_idname = "object.invoke_add_gpencil_shaderfx_menu"
    bl_label = "Add Effect"
    menu_id = "OBJECT_MT_gpencil_shaderfx_add"
    space_context = 'SHADERFX'

    # Poll function isn't extended because currently
    # only grease pencil objects have the space context 'SHADERFX'
    


classes = (
    INVOKE_OT_CLASSIC_MODIFIER_MENU,
    INVOKE_OT_ASSET_MODIFIER_MENU,
    INVOKE_OT_ADD_GPENCIL_MODIFIER_MENU,
    INVOKE_OT_ADD_GPENCIL_SHADERFX_MENU,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
