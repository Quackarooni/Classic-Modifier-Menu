import bpy
from bpy.types import Panel, Menu
from bpy.app.translations import (
    pgettext_n as n_,
)

from bl_ui import properties_data_modifier, properties_data_shaderfx, properties_constraint
from ..utils import (
    fetch_user_preferences, 
    fetch_menu_items,
    fetch_translation_context,
    )

ModifierButtonsPanel = properties_data_modifier.ModifierButtonsPanel
ModifierAddMenu = properties_data_modifier.ModifierAddMenu
ObjectConstraintPanel = properties_constraint.ObjectConstraintPanel
BoneConstraintPanel = properties_constraint.BoneConstraintPanel


def geometry_nodes_supported(obj_type):
    return obj_type in {
        'MESH', 'CURVE', 'CURVES',
        'FONT', 'VOLUME', 'POINTCLOUD', 'GREASEPENCIL',
    }


class SearchToTypeMenu:
    bl_options = {'SEARCH_ON_KEY_PRESS'}


class DATA_PT_modifiers(ModifierButtonsPanel, Panel):
    bl_label = "Modifiers"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()
        modifier_label = prefs.modifier_menu_label
        asset_label = prefs.asset_menu_label
        ob_type = context.object.type

        if prefs.stacking == 'VERTICAL':
            sublayout = layout
        elif prefs.stacking == 'HORIZONTAL':
            sublayout = layout.row()

        if prefs.display_as == "DROPDOWN":
            sublayout.menu("OBJECT_MT_modifier_add", text=modifier_label)
            if prefs.show_assets:
                sublayout.menu("OBJECT_MT_modifier_add_assets", text=asset_label)
                
        elif prefs.display_as == "BUTTON":
            sublayout.operator("object.invoke_classic_modifier_menu", text=modifier_label, icon='ADD')
            if prefs.show_assets and geometry_nodes_supported(ob_type):
                sublayout.operator("object.invoke_asset_modifier_menu", text=asset_label, icon='ADD')

        layout.template_modifiers()


class OBJECT_MT_modifier_add(SearchToTypeMenu, ModifierAddMenu, Menu):
    bl_label = ""
    bl_description = "Add a procedural operation/effect to the active object"

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob

    @staticmethod
    def draw_column(layout, header, menu_name, icon):
        prefs = fetch_user_preferences()
        header_mode = prefs.modifier_headers
        col = layout.column()

        if header_mode != 'HIDE':
            if header_mode != 'WITH_ICONS':
                icon = 'NONE'

            col.label(text=header, icon=icon)
            col.separator()
        
        if prefs.display_as == 'BUTTON' and layout.operator_context == 'INVOKE_REGION_WIN':
            col.menu(menu_name)
        else:
            col.menu_contents(menu_name)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        ob_type = context.object.type
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE', 'GREASEPENCIL'}:
            self.draw_column(row, header="Edit", menu_name="OBJECT_MT_modifier_add_edit", icon='EDITMODE_HLT')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'VOLUME', 'GREASEPENCIL'}:
            self.draw_column(row, header="Generate", menu_name="OBJECT_MT_modifier_add_generate", icon='FILE_3D')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE', 'VOLUME', 'GREASEPENCIL'}:
            self.draw_column(row, header="Deform", menu_name="OBJECT_MT_modifier_add_deform", icon='STROKE')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
            self.draw_column(row, header="Physics", menu_name="OBJECT_MT_modifier_add_physics", icon='PHYSICS')
        if ob_type in {'GREASEPENCIL'}:
            self.draw_column(row, header="Color", menu_name="OBJECT_MT_modifier_add_color", icon='OVERLAY')


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
        if ob_type in {'MESH', 'CURVE', 'CURVES', 'FONT', 'POINTCLOUD'}:
            self.operator_modifier_add(layout, 'MESH_SEQUENCE_CACHE')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'NORMAL_EDIT')
            self.operator_modifier_add(layout, 'WEIGHTED_NORMAL')
            self.operator_modifier_add(layout, 'UV_PROJECT')
            self.operator_modifier_add(layout, 'UV_WARP')
            self.operator_modifier_add(layout, 'VERTEX_WEIGHT_EDIT')
            self.operator_modifier_add(layout, 'VERTEX_WEIGHT_MIX')
            self.operator_modifier_add(layout, 'VERTEX_WEIGHT_PROXIMITY')

        if ob_type == 'GREASEPENCIL':
            self.operator_modifier_add(layout, 'GREASE_PENCIL_TEXTURE')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_TIME')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_VERTEX_WEIGHT_PROXIMITY')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_VERTEX_WEIGHT_ANGLE')

        if prefs.built_in_asset_categories in {'APPEND', 'SHOW_AND_APPEND'}:
            layout.template_modifier_asset_menu_items(catalog_path=self.bl_label)


class OBJECT_MT_modifier_add_generate(ModifierAddMenu, Menu):
    bl_label = "Generate"

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()
        ob_type = context.object.type

        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            if geometry_nodes_supported(ob_type):
                self.operator_modifier_add_asset(layout, n_('Array'), icon='MOD_ARRAY')
            else:
                self.operator_modifier_add(layout, 'ARRAY')

            self.operator_modifier_add(layout, 'BEVEL')
        if ob_type == 'MESH':
            self.operator_modifier_add(layout, 'BOOLEAN')
        if ob_type in {'MESH', 'CURVE', 'FONT', 'SURFACE'}:
            self.operator_modifier_add(layout, 'BUILD')
            if geometry_nodes_supported(ob_type):
                self.operator_modifier_add_asset(layout, n_('Curve to Tube'), icon='MOD_CURVE_TO_TUBE')
            self.operator_modifier_add(layout, 'DECIMATE')
            self.operator_modifier_add(layout, 'EDGE_SPLIT')
        if geometry_nodes_supported(ob_type):
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
            if geometry_nodes_supported(ob_type):
                self.operator_modifier_add_asset(layout, n_('Scatter on Surface'), icon='MOD_SCATTER_ON_SURFACE')
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
        if ob_type == 'GREASEPENCIL':
            self.operator_modifier_add_asset(layout, n_('Array'), icon='MOD_ARRAY')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_BUILD')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_DASH')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_ENVELOPE')
            self.operator_modifier_add(layout, 'NODES')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_LENGTH')
            self.operator_modifier_add(layout, 'LINEART')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_MIRROR')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_MULTIPLY')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_OUTLINE')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_SIMPLIFY')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_SUBDIV')

        if geometry_nodes_supported(ob_type):
            self.layout.separator(type='LINE')
            self.operator_modifier_add(layout, 'ARRAY', text=n_("Array (Legacy)"), no_icon=True)

        if prefs.built_in_asset_categories in {'APPEND', 'SHOW_AND_APPEND'}:
            layout.template_modifier_asset_menu_items(catalog_path=self.bl_label, skip_essentials=True)


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
        if ob_type == 'GREASEPENCIL':
            self.operator_modifier_add(layout, 'GREASE_PENCIL_ARMATURE')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_HOOK')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_LATTICE')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_NOISE')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_OFFSET')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_SHRINKWRAP')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_SMOOTH')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_THICKNESS')

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


class OBJECT_MT_modifier_add_color(ModifierAddMenu, Menu):
    bl_label = "Color"

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()

        ob_type = context.object.type
        if ob_type == 'GREASEPENCIL':
            self.operator_modifier_add(layout, 'GREASE_PENCIL_COLOR')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_OPACITY')
            self.operator_modifier_add(layout, 'GREASE_PENCIL_TINT')

        if prefs.built_in_asset_categories in {'APPEND', 'SHOW_AND_APPEND'}:
            layout.template_modifier_asset_menu_items(catalog_path=self.bl_label)


class OBJECT_MT_modifier_add_assets(ModifierAddMenu, SearchToTypeMenu, Menu):
    bl_label = "Assets"
    bl_description = "Add a modifier nodegroup to the active object"

    @staticmethod
    def draw_built_in_menus(layout, context):
        ob = context.object

        prefs = fetch_user_preferences()
        if prefs.built_in_asset_categories in {'SHOW', 'SHOW_AND_APPEND'}:
            layout.menu("OBJECT_MT_modifier_add_edit_assets")
            layout.menu("OBJECT_MT_modifier_add_generate_assets")
            layout.menu("OBJECT_MT_modifier_add_deform_assets")

        if ob.type == "GREASEPENCIL":
            if prefs.built_in_asset_categories in {'SHOW', 'SHOW_AND_APPEND'}:
                layout.menu("OBJECT_MT_modifier_add_color_assets")

        if ob.type == "MESH":
            layout.menu("OBJECT_MT_modifier_add_normals_assets")

        if ob.type != "GREASEPENCIL":
            if prefs.built_in_asset_categories in {'SHOW', 'SHOW_AND_APPEND'}:
                layout.menu("OBJECT_MT_modifier_add_physics_assets")
            layout.separator()

    def draw(self, context):
        layout = self.layout
        if layout.operator_context == 'EXEC_REGION_WIN':
            layout.operator_context = 'INVOKE_REGION_WIN'
            layout.operator("wm.search_single_menu", text="Search...", icon='VIEWZOOM').menu_idname = self.bl_idname
            layout.separator()

        layout.separator()
        self.operator_modifier_add(layout, 'NODES')
        layout.separator()
        #TODO - Add poll function to only display these menus if their catalogs exist
        self.draw_built_in_menus(layout, context) 

        layout.menu_contents("OBJECT_MT_modifier_add_root_catalogs")


class ModifierAssetMenu:
    def draw(self, context):
        skip_essentials = getattr(self, "skip_essentials", False)
        self.layout.template_modifier_asset_menu_items(catalog_path=self.bl_label, skip_essentials=skip_essentials)

class OBJECT_MT_modifier_add_edit_assets(ModifierAssetMenu, ModifierAddMenu, Menu):
    bl_label = OBJECT_MT_modifier_add_edit.bl_label

class OBJECT_MT_modifier_add_generate_assets(ModifierAssetMenu, ModifierAddMenu, Menu):
    bl_label = OBJECT_MT_modifier_add_generate.bl_label
    skip_essentials = True

class OBJECT_MT_modifier_add_deform_assets(ModifierAssetMenu, ModifierAddMenu, Menu):
    bl_label = OBJECT_MT_modifier_add_deform.bl_label

class OBJECT_MT_modifier_add_physics_assets(ModifierAssetMenu, ModifierAddMenu, Menu):
    bl_label = OBJECT_MT_modifier_add_physics.bl_label

class OBJECT_MT_modifier_add_color_assets(ModifierAssetMenu, ModifierAddMenu, Menu):
    bl_label = OBJECT_MT_modifier_add_color.bl_label

class OBJECT_MT_modifier_add_normals_assets(ModifierAssetMenu, ModifierAddMenu, Menu):
    bl_label = "Normals"

class DropdownPanelBaseclass:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        layout = self.layout
        prefs = fetch_user_preferences()

        if prefs.display_as == "DROPDOWN":
            layout.menu(self.menu_id, text=self.label)
        elif prefs.display_as == "BUTTON":
            layout.operator(self.OPERATOR_ID, text=self.label, icon='ADD')

        self.post_draw(layout)

    def post_draw(layout):
        ...
    

class DATA_PT_shader_fx(DropdownPanelBaseclass, Panel):
    bl_label = "Effects"
    bl_context = "shaderfx"

    menu_id = "OBJECT_MT_gpencil_shaderfx_add"
    OPERATOR_ID = "object.invoke_add_gpencil_shaderfx_menu"
    label = "Add Effect"

    @staticmethod
    def post_draw(layout):
        layout.template_shaderfx()


class OBJECT_PT_constraints(DropdownPanelBaseclass, Panel):
    bl_label = "Object Constraints"
    bl_context = "constraint"

    menu_id = "OBJECT_MT_constraint_add"
    OPERATOR_ID = "object.invoke_add_constraints_menu"
    label = "Add Object Constraint"

    @classmethod
    def poll(cls, context):
        return (context.object)
        
    @staticmethod
    def post_draw(layout):
        layout.template_constraints(use_bone_constraints=False)


class BONE_PT_constraints(DropdownPanelBaseclass, Panel):
    bl_label = "Bone Constraints"
    bl_context = "bone_constraint"

    menu_id = "BONE_MT_constraint_add"
    OPERATOR_ID = "pose.invoke_add_constraints_menu"
    label = "Add Bone Constraint"

    @classmethod
    def poll(cls, context):
        return (context.object)

    @staticmethod
    def post_draw(layout):
        layout.template_constraints(use_bone_constraints=True)


class FlatMenuBaseclass(SearchToTypeMenu):
    bl_label = ""

    @staticmethod
    def draw_column(layout, header, menu_name, icon):
        prefs = fetch_user_preferences()
        header_mode = prefs.modifier_headers
        
        col = layout.column()

        if header_mode != 'HIDE':
            if header_mode != 'WITH_ICONS':
                icon = 'NONE'

            col.label(text=header, icon=icon)
            col.separator()
        
        if prefs.display_as == 'BUTTON' and layout.operator_context == 'INVOKE_REGION_WIN':
            col.menu(menu_name)
        else:
            col.menu_contents(menu_name)

    @classmethod
    def draw_operator_column(cls, layout, header, types, icon='NONE'):
        header_mode = fetch_user_preferences("modifier_headers")
        text_ctxt = cls.TRANSLATION_CONTEXT
        
        col = layout.column()

        if header_mode != 'HIDE':
            if header_mode != 'WITH_ICONS':
                icon = 'NONE'

            col.label(text=header, icon=icon)
            col.separator()

        for op_type in types:
            col.operator(cls.OPERATOR_ID, text=op_type.name, icon=op_type.icon, text_ctxt=text_ctxt).type = op_type.identifier


class ColumnMenuBaseclass:
    def draw(self, context):
        text_ctxt = self.TRANSLATION_CONTEXT
        for enum_item in self.OPERATOR_ITEMS:
            self.layout.operator(self.OPERATOR_ID, text=enum_item.name, icon=enum_item.icon, text_ctxt=text_ctxt).type = enum_item.identifier


class OBJECT_MT_gpencil_shaderfx_add(FlatMenuBaseclass, Menu):
    bl_description = "Add a visual effect to the active grease pencil object"

    OPERATOR_ID = "object.shaderfx_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="ShaderFx")
    OPERATOR_ITEMS = fetch_menu_items(class_name="ShaderFx")

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type == 'GREASEPENCIL'

    def draw(self, _context):
        layout = self.layout.row()

        if layout.operator_context == 'INVOKE_REGION_WIN':
            header = "Effect"
        else:
            header = "Add Effect"

        self.draw_operator_column(layout, header=header, icon='SHADERFX', types=self.OPERATOR_ITEMS)


class OBJECT_MT_constraint_add(FlatMenuBaseclass, Menu):
    bl_description = "Add a constraint to the active object"

    OPERATOR_ID = "object.constraint_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="Constraint")

    def draw(self, _context):
        layout = self.layout.row()

        self.draw_column(layout, header="Motion Tracking", menu_name="OBJECT_MT_constraint_add_motion_tracking", icon='TRACKING')
        self.draw_column(layout, header="Transform", menu_name="OBJECT_MT_constraint_add_transform", icon='OBJECT_HIDDEN')
        self.draw_column(layout, header="Tracking", menu_name="OBJECT_MT_constraint_add_tracking", icon='TRACKER')
        self.draw_column(layout, header="Relationship", menu_name="OBJECT_MT_constraint_add_relationship", icon='DRIVER')


class OBJECT_MT_constraint_add_motion_tracking(ColumnMenuBaseclass, Menu):
    bl_label = "Motion Tracking"

    OPERATOR_ID = "object.constraint_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="Constraint")
    OPERATOR_ITEMS = fetch_menu_items(class_name="Constraint", category_name="Motion Tracking")


class OBJECT_MT_constraint_add_transform(ColumnMenuBaseclass, Menu):
    bl_label = "Transform"

    OPERATOR_ID = "object.constraint_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="Constraint")
    OPERATOR_ITEMS = fetch_menu_items(class_name="Constraint", category_name="Transform")


class OBJECT_MT_constraint_add_tracking(ColumnMenuBaseclass, Menu):
    bl_label = "Tracking"

    OPERATOR_ID = "object.constraint_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="Constraint")
    OPERATOR_ITEMS = fetch_menu_items(class_name="Constraint", category_name="Tracking", exclude={'IK', 'SPLINE_IK'})


class OBJECT_MT_constraint_add_relationship(ColumnMenuBaseclass, Menu):
    bl_label = "Relationship"

    OPERATOR_ID = "object.constraint_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="Constraint")
    OPERATOR_ITEMS = fetch_menu_items(class_name="Constraint", category_name="Relationship")


class BONE_MT_constraint_add(FlatMenuBaseclass, Menu):
    bl_description = "Add a constraint to the active bone"

    OPERATOR_ID = "pose.constraint_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="Constraint")

    def draw(self, _context):
        layout = self.layout.row()

        self.draw_column(layout, header="Motion Tracking", menu_name="BONE_MT_constraint_add_motion_tracking", icon='TRACKING')
        self.draw_column(layout, header="Transform", menu_name="BONE_MT_constraint_add_transform", icon='OBJECT_HIDDEN')
        self.draw_column(layout, header="Tracking", menu_name="BONE_MT_constraint_add_tracking", icon='TRACKER')
        self.draw_column(layout, header="Relationship", menu_name="BONE_MT_constraint_add_relationship", icon='DRIVER')


class BONE_MT_constraint_add_motion_tracking(ColumnMenuBaseclass, Menu):
    bl_label = "Motion Tracking"

    OPERATOR_ID = "pose.constraint_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="Constraint")
    OPERATOR_ITEMS = fetch_menu_items(class_name="Constraint", category_name="Motion Tracking")


class BONE_MT_constraint_add_transform(ColumnMenuBaseclass, Menu):
    bl_label = "Transform"

    OPERATOR_ID = "pose.constraint_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="Constraint")
    OPERATOR_ITEMS = fetch_menu_items(class_name="Constraint", category_name="Transform")


class BONE_MT_constraint_add_tracking(ColumnMenuBaseclass, Menu):
    bl_label = "Tracking"

    OPERATOR_ID = "pose.constraint_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="Constraint")
    OPERATOR_ITEMS = fetch_menu_items(class_name="Constraint", category_name="Tracking")

class BONE_MT_constraint_add_relationship(ColumnMenuBaseclass, Menu):
    bl_label = "Relationship"

    OPERATOR_ID = "pose.constraint_add"
    TRANSLATION_CONTEXT = fetch_translation_context(class_name="Constraint")
    OPERATOR_ITEMS = fetch_menu_items(class_name="Constraint", category_name="Relationship")


def reload_menus():
    menus = (
        OBJECT_MT_modifier_add,
        OBJECT_MT_modifier_add_assets,
        OBJECT_MT_gpencil_shaderfx_add, 
        OBJECT_MT_constraint_add,
        BONE_MT_constraint_add, 
        )

    for menu in menus:
        bpy.utils.unregister_class(menu)
        bpy.utils.register_class(menu)


def toggle_input_mode(self, context):
    if self.input_mode == 'TYPE_TO_SEARCH':
        if not hasattr(SearchToTypeMenu, "bl_options"):
            SearchToTypeMenu.bl_options = {'SEARCH_ON_KEY_PRESS'}
            reload_menus()
    elif self.input_mode == 'ACCELERATOR_KEYS':
        if hasattr(SearchToTypeMenu, "bl_options"):
            delattr(SearchToTypeMenu, "bl_options")
        reload_menus()
    else:
        raise ValueError(f"'{self.input_mode}' is an unsupported value for {self}")


overriding_classes = (
    DATA_PT_modifiers,
    OBJECT_MT_modifier_add,
    OBJECT_MT_modifier_add_edit,
    OBJECT_MT_modifier_add_generate,
    OBJECT_MT_modifier_add_deform,
    OBJECT_MT_modifier_add_physics,
    OBJECT_MT_modifier_add_color,
    DATA_PT_shader_fx,
    OBJECT_PT_constraints,
    BONE_PT_constraints,
)

created_classes = (
    OBJECT_MT_modifier_add_assets,
    OBJECT_MT_modifier_add_edit_assets,
    OBJECT_MT_modifier_add_generate_assets,
    OBJECT_MT_modifier_add_deform_assets,
    OBJECT_MT_modifier_add_physics_assets,
    OBJECT_MT_modifier_add_color_assets,
    OBJECT_MT_gpencil_shaderfx_add,
    OBJECT_MT_constraint_add,
    BONE_MT_constraint_add,
    OBJECT_MT_constraint_add_motion_tracking,
    OBJECT_MT_constraint_add_transform,
    OBJECT_MT_constraint_add_tracking,
    OBJECT_MT_constraint_add_relationship,
    BONE_MT_constraint_add_motion_tracking,
    BONE_MT_constraint_add_transform,
    BONE_MT_constraint_add_tracking,
    BONE_MT_constraint_add_relationship,
)

original_class_dict = {
    "DATA_PT_modifiers" : properties_data_modifier.DATA_PT_modifiers,
    "OBJECT_MT_modifier_add" : properties_data_modifier.OBJECT_MT_modifier_add,
    "OBJECT_MT_modifier_add_edit" : properties_data_modifier.OBJECT_MT_modifier_add_edit,
    "OBJECT_MT_modifier_add_generate" : properties_data_modifier.OBJECT_MT_modifier_add_generate,
    "OBJECT_MT_modifier_add_deform" : properties_data_modifier.OBJECT_MT_modifier_add_deform,
    "OBJECT_MT_modifier_add_physics" : properties_data_modifier.OBJECT_MT_modifier_add_physics,
    "OBJECT_MT_modifier_add_color" : properties_data_modifier.OBJECT_MT_modifier_add_color,
    "DATA_PT_shader_fx" : properties_data_shaderfx.DATA_PT_shader_fx,
    "OBJECT_PT_constraints" : properties_constraint.OBJECT_PT_constraints,
    "BONE_PT_constraints" : properties_constraint.BONE_PT_constraints,
}


def register():
    for cls in overriding_classes:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(original_class_dict[cls.__name__])
        bpy.utils.register_class(cls)

    for cls in created_classes:
        bpy.utils.register_class(cls)

    if bpy.app.version >= (4, 2, 0):
        bpy.utils.register_class(OBJECT_MT_modifier_add_normals_assets)


def unregister():
    for cls in overriding_classes:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)  
        bpy.utils.register_class(original_class_dict[cls.__name__])

    for cls in created_classes:
        bpy.utils.unregister_class(cls)

    if bpy.app.version >= (4, 2, 0):
        bpy.utils.unregister_class(OBJECT_MT_modifier_add_normals_assets)

    SearchToTypeMenu.bl_options = {'SEARCH_ON_KEY_PRESS'}