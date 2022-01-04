"""This module handle copy job"""
import shutil
from pathlib import Path

def copy(path, target):
    """Copy path to destionation path

    Args:
        path (Path): Source path
        target (Path): Destination path
    """
    # target = Path(target, path.name)
    try:
        shutil.copyfile(path, Path(target, path.name))
    except Exception:  # pylint: disable=broad-except
        shutil.copytree(path, Path(target, path.name))
