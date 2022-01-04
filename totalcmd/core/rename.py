"""This module handle the rename jobs"""
from pathlib import Path
from .list import dict_pack

def rename(path, value):
    """Rename file path with value

    Args:
        path (Path): The path of file/directory with will be renamed
        value (str): New value for file/directory
    """
    target = Path(path.parent, value)
    path.replace(target)
    return dict_pack(target)
