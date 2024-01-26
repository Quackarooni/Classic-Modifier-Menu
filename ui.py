import bpy
from bpy.types import Panel, Menu

from bl_ui import properties_data_modifier

ModifierButtonsPanel = properties_data_modifier.ModifierButtonsPanel
ModifierAddMenu = properties_data_modifier.ModifierAddMenu


def fetch_user_preferences(attr_id=None):
    prefs = bpy.context.preferences.addons[__package__].preferences

    if attr_id is None:
        return prefs
    else:
        return getattr(prefs, attr_id)


class DATA_PT_modifiers(ModifierButtonsPanel, Panel):
    bl_label = "Modifiers"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type != 'GPENCIL'

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()
        modifier_label = prefs.modifier_menu_label
        asset_label = prefs.asset_menu_label

        if prefs.stacking == 'VERTICAL':
            sublayout = layout
        elif prefs.stacking == 'HORIZONTAL':
            sublayout = layout.row()

        if prefs.display_as == "DROPDOWN":
            sublayout.menu("OBJECT_MT_modifier_add", text=modifier_label)
            if prefs.show_assets:
                sublayout.menu("OBJECT_MT_modifier_add_assets", text=asset_label)
                
        elif prefs.display_as == "BUTTON":
            sublayout.operator("wm.call_menu", text=modifier_label, icon='ADD').name = "OBJECT_MT_modifier_add"
            if prefs.show_assets:
                sublayout.operator("wm.call_menu", text=asset_label, icon='ADD').name = "OBJECT_MT_modifier_add_assets"

        layout.template_modifiers()


class OBJECT_MT_modifier_add(ModifierAddMenu, Menu):
    bl_label = ""
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    @staticmethod
    def draw_column(layout, header, menu_name, icon):
        header_mode = fetch_user_preferences("modifier_headers")
        col = layout.column()

        if header_mode != 'HIDE':
            if header_mode != 'WITH_ICONS':
                icon = 'NONE'

            col.label(text=header, icon=icon)
            col.separator()
        col.menu_contents(menu_name)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        ob_type = context.object.type
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
            self.draw_column(row, header="Edit", menu_name="OBJECT_MT_modifier_add_edit", icon='EDITMODE_HLT')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'VOLUME'}:
            self.draw_column(row, header="Generate", menu_name="OBJECT_MT_modifier_add_generate", icon='FILE_3D')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE', 'VOLUME'}:
            self.draw_column(row, header="Deform", menu_name="OBJECT_MT_modifier_add_deform", icon='STROKE')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
            self.draw_column(row, header="Physics", menu_name="OBJECT_MT_modifier_add_physics", icon='PHYSICS')


class OBJECT_MT_modifier_add_edit(ModifierAddMenu, Menu):
    bl_label = "Edit"

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()

        ob_type = context.object.type
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'DATA_TRANSFER')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
            self.operator_modifier_add(layout, 'MESH_CACHE')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            self.operator_modifier_add(layout, 'MESH_SEQUENCE_CACHE')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'NORMAL_EDIT')
            self.operator_modifier_add(layout, 'WEIGHTED_NORMAL')
            self.operator_modifier_add(layout, 'UV_PROJECT')
            self.operator_modifier_add(layout, 'UV_WARP')
            self.operator_modifier_add(layout, 'VERTEX_WEIGHT_EDIT')
            self.operator_modifier_add(layout, 'VERTEX_WEIGHT_MIX')
            self.operator_modifier_add(layout, 'VERTEX_WEIGHT_PROXIMITY')

        if prefs.built_in_asset_categories in {'APPEND', 'SHOW_AND_APPEND'}:
            layout.template_modifier_asset_menu_items(catalog_path=self.bl_label)


class OBJECT_MT_modifier_add_generate(ModifierAddMenu, Menu):
    bl_label = "Generate"

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()

        ob_type = context.object.type
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            self.operator_modifier_add(layout, 'ARRAY')
            self.operator_modifier_add(layout, 'BEVEL')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'BOOLEAN')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            self.operator_modifier_add(layout, 'BUILD')
            self.operator_modifier_add(layout, 'DECIMATE')
            self.operator_modifier_add(layout, 'EDGE_SPLIT')
        if ob_type in {'MESH', 'CURVE', 'CURVES', 'FONT', 'SURFACE', 'VOLUME', 'POINTCLOUD'}:
            self.operator_modifier_add(layout, 'NODES')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'MASK')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            self.operator_modifier_add(layout, 'MIRROR')
        if ob_type == 'VOLUME':
            self.operator_modifier_add(layout, 'MESH_TO_VOLUME')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'MULTIRES')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            self.operator_modifier_add(layout, 'REMESH')
            self.operator_modifier_add(layout, 'SCREW')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'SKIN')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            self.operator_modifier_add(layout, 'SOLIDIFY')
            self.operator_modifier_add(layout, 'SUBSURF')
            self.operator_modifier_add(layout, 'TRIANGULATE')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'VOLUME_TO_MESH')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            self.operator_modifier_add(layout, 'WELD')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'WIREFRAME')

        if prefs.built_in_asset_categories in {'APPEND', 'SHOW_AND_APPEND'}:
            layout.template_modifier_asset_menu_items(catalog_path=self.bl_label)


class OBJECT_MT_modifier_add_deform(ModifierAddMenu, Menu):
    bl_label = "Deform"

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()

        ob_type = context.object.type
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
            self.operator_modifier_add(layout, 'ARMATURE')
            self.operator_modifier_add(layout, 'CAST')
            self.operator_modifier_add(layout, 'CURVE')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'DISPLACE')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
            self.operator_modifier_add(layout, 'HOOK')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'LAPLACIANDEFORM')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
            self.operator_modifier_add(layout, 'LATTICE')
            self.operator_modifier_add(layout, 'MESH_DEFORM')
            self.operator_modifier_add(layout, 'SHRINKWRAP')
            self.operator_modifier_add(layout, 'SIMPLE_DEFORM')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            self.operator_modifier_add(layout, 'SMOOTH')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'CORRECTIVE_SMOOTH')
            self.operator_modifier_add(layout, 'LAPLACIANSMOOTH')
            self.operator_modifier_add(layout, 'SURFACE_DEFORM')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
            self.operator_modifier_add(layout, 'WARP')
            self.operator_modifier_add(layout, 'WAVE')
        if ob_type == 'VOLUME':
            self.operator_modifier_add(layout, 'VOLUME_DISPLACE')

        if prefs.built_in_asset_categories in {'APPEND', 'SHOW_AND_APPEND'}:
            layout.template_modifier_asset_menu_items(catalog_path=self.bl_label)


class OBJECT_MT_modifier_add_physics(ModifierAddMenu, Menu):
    bl_label = "Physics"

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()

        ob_type = context.object.type
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'CLOTH')
            self.operator_modifier_add(layout, 'COLLISION')
            self.operator_modifier_add(layout, 'DYNAMIC_PAINT')
            self.operator_modifier_add(layout, 'EXPLODE')
            self.operator_modifier_add(layout, 'FLUID')
            self.operator_modifier_add(layout, 'OCEAN')
            self.operator_modifier_add(layout, 'PARTICLE_INSTANCE')
            self.operator_modifier_add(layout, 'PARTICLE_SYSTEM')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
            self.operator_modifier_add(layout, 'SOFT_BODY')

        if prefs.built_in_asset_categories in {'APPEND', 'SHOW_AND_APPEND'}:
            layout.template_modifier_asset_menu_items(catalog_path=self.bl_label)


class OBJECT_MT_modifier_add_assets(ModifierAddMenu, Menu):
    bl_label = "Assets"
    bl_options = {'SEARCH_ON_KEY_PRESS'}

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()
        ob_type = context.object.type
        if layout.operator_context == 'EXEC_REGION_WIN':
            layout.operator_context = 'INVOKE_REGION_WIN'
            layout.operator("wm.search_single_menu", text="Search...", icon='VIEWZOOM').menu_idname = self.bl_idname
            layout.separator()

        layout.separator()
        self.operator_modifier_add(layout, 'NODES')
        layout.separator()
        #TODO - Add poll function to only display these menus if their catalogs exist
        if prefs.built_in_asset_categories in {'SHOW', 'SHOW_AND_APPEND'}:
            layout.menu("OBJECT_MT_modifier_add_edit_assets")
            layout.menu("OBJECT_MT_modifier_add_generate_assets")
            layout.menu("OBJECT_MT_modifier_add_deform_assets")
            layout.menu("OBJECT_MT_modifier_add_physics_assets")
            layout.separator()
        layout.menu_contents("OBJECT_MT_modifier_add_root_catalogs")


class ModifierAssetMenu:
    def draw(self, context):
        self.layout.template_modifier_asset_menu_items(catalog_path=self.bl_label)

class OBJECT_MT_modifier_add_edit_assets(ModifierAssetMenu, ModifierAddMenu, Menu):
    bl_label = OBJECT_MT_modifier_add_edit.bl_label

class OBJECT_MT_modifier_add_generate_assets(ModifierAssetMenu, ModifierAddMenu, Menu):
    bl_label = OBJECT_MT_modifier_add_generate.bl_label

class OBJECT_MT_modifier_add_deform_assets(ModifierAssetMenu, ModifierAddMenu, Menu):
    bl_label = OBJECT_MT_modifier_add_deform.bl_label

class OBJECT_MT_modifier_add_physics_assets(ModifierAssetMenu, ModifierAddMenu, Menu):
    bl_label = OBJECT_MT_modifier_add_physics.bl_label


overriding_classes = (
    DATA_PT_modifiers,
    OBJECT_MT_modifier_add,
    OBJECT_MT_modifier_add_edit,
    OBJECT_MT_modifier_add_generate,
    OBJECT_MT_modifier_add_deform,
    OBJECT_MT_modifier_add_physics,
)

created_classes = (
    OBJECT_MT_modifier_add_assets,
    OBJECT_MT_modifier_add_edit_assets,
    OBJECT_MT_modifier_add_generate_assets,
    OBJECT_MT_modifier_add_deform_assets,
    OBJECT_MT_modifier_add_physics_assets,
)


def register():
    for cls in overriding_classes:
        bpy.utils.register_class(cls)

    for cls in created_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in overriding_classes:
        bpy.utils.register_class(getattr(properties_data_modifier, cls.__name__))

    for cls in created_classes:
        bpy.utils.unregister_class(cls)