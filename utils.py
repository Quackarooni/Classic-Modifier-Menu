import bpy


if bpy.app.version >= (4, 5):
    def is_menu_search(context, _layout):
        return getattr(context, "is_menu_search", False)
else:
    def is_menu_search(_context, layout):
        return layout.operator_context == 'INVOKE_REGION_WIN'


def fetch_user_preferences(attr_id=None):
    prefs = bpy.context.preferences.addons[__package__].preferences

    if attr_id is None:
        return prefs
    else:
        return getattr(prefs, attr_id)


def fetch_translation_context(class_name):
    type_class = getattr(bpy.types, class_name)
    type_props = type_class.bl_rna.properties["type"]

    return type_props.translation_context


def fetch_menu_items(class_name, category_name=None, exclude=None):
    type_class = getattr(bpy.types, class_name)
    type_props = type_class.bl_rna.properties["type"]

    if exclude is None:
        exclude = {}

    items = []

    if category_name is None:
        for item in type_props.enum_items_static_ui:
            if item.identifier not in exclude:
                items.append(item)
    else:
        category = None
        for item in type_props.enum_items_static_ui:
            if item.identifier == "":
                category = item.name
                continue

            if item.identifier in exclude:
                continue

            if category == category_name:
                items.append(item)

    return tuple(items)
