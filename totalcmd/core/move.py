"""This module handle the rename jobs"""
from pathlib import Path

def move(path, target):
    """Rename file path with value

    Args:
        path (Path): The path witch will be moved
        value (Path): Targert path
    """
    target = Path(target, path.name)
    path.replace(target)
