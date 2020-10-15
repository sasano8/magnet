import os

class FileInfo:
    def __init__(self, file_name: str, path: str):
        self.file_name = file_name
        self.path = path


def enumrate_models_py(root_file_path: str):
    """
    Enumrate models.py's path as sqlalchemy model definition.
    This operation is useful for automatically importing sqlalchemy models.
    """
    target_dir = os.path.dirname(root_file_path)

    for reload_dir in [target_dir]:
        for subdir, dirs, files in os.walk(reload_dir):
            for file in files:
                yield FileInfo(
                    file_name=file,
                    path=subdir + os.sep + file
                )


def import_modules(root_file_path: str, target_file_names: list = ["models.py"]):
    """models.pyを収集し、全てインポートする"""
    import importlib

    cd = os.path.dirname(root_file_path)
    dir_name = os.path.basename(cd)

    arr = list(enumrate_models_py(root_file_path))

    for target_file_name in target_file_names:
        # logger.info("Scanning models.py")
        for file in filter(lambda x: x.file_name == target_file_name, arr):
            # TODO: python3.9ぐらいでremove suffixが実装されるのでそれ使う
            file_path = file.path[:-3]  # remove .py

            file_path = file_path.replace(cd, "").lstrip("/")
            file_path = file_path.replace("/", ".")
            module = dir_name + "." + file_path
            # logger.info(module)
            importlib.import_module(module)

