import bpy
import importlib

version_map = {
    "4_0" : "4_0",
    "4_1" : "4_0",
    "4_2" : "4_0",
    "4_3" : "4_3",
}
version_tuple = tuple(map(str, bpy.app.version[:2]))
version = "_".join(version_tuple)
version = "." + version_map[version]

try:
    version_module = importlib.import_module(version, package=__package__)
except Exception:
    print(version)
    raise NotImplementedError(f"Blender version \"{'.'.join(version_tuple[:2])}\" is not supported.")

toggle_input_mode = version_module.toggle_input_mode
original_class_dict = version_module.original_class_dict
register = version_module.register
unregister = version_module.unregister