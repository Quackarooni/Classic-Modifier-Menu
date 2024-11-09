import bpy
import importlib


def stringify(iterable, delimiter):
    return delimiter.join(map(str, version_tuple))


def version_clamp(version, min_version, max_version):
    return max(min(version, max_version), min_version)


version_map = {
    "4_0" : "4_0",
    "4_1" : "4_0",
    "4_2" : "4_0",
    "4_3" : "4_3",
}


original_version = bpy.app.version[:2]
version_tuple = version_clamp(original_version, min_version=(4, 0), max_version=(4, 3))
module_version = stringify(version_tuple, delimiter="_")
module_version = "." + version_map[module_version]


try:
    version_module = importlib.import_module(module_version, package=__package__)
except Exception:
    raise NotImplementedError(f"Blender version \"{stringify(original_version, delimiter='.')}\" is not supported.")


toggle_input_mode = version_module.toggle_input_mode
original_class_dict = version_module.original_class_dict
register = version_module.register
unregister = version_module.unregister