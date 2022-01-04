"""This module handle creation requests"""
from pathlib import Path


def create_dir(path, name):
    """Create directiony with name specified in path

    Args:
        path (Path): The path where directory is created
        name (str): Name of path
    """
    target = Path(path, name)
    target.mkdir()
