import bpy
import importlib


def stringify(iterable, delimiter):
    return delimiter.join(map(str, iterable))


def version_clamp(version, min_version, max_version):
    return max(min(version, max_version), min_version)


version_map = {
    (4, 0) : (4, 0),
    (4, 1) : (4, 0),
    (4, 2) : (4, 0),
    (4, 3) : (4, 3),
    (4, 4) : (4, 3),
    (4, 5) : (4, 3),
    (4, 6) : (4, 3),
    (5, 0) : (5, 0),
}

original_version = bpy.app.version[:2]
version_tuple = version_clamp(
    original_version, min_version=min(version_map), max_version=max(version_map))
module_version = version_map[version_tuple]


try:
    version_module = importlib.import_module(
        "." + stringify(module_version, delimiter="_"), package=__package__)
except Exception:
    raise NotImplementedError(f"Blender version \"{stringify(original_version, delimiter='.')}\" is not supported.")


toggle_input_mode = version_module.toggle_input_mode
original_class_dict = version_module.original_class_dict
register = version_module.register
unregister = version_module.unregister