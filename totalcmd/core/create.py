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


def create_file(path, name):
    """Create file with name specified in path

    Args:
        path (Path): The path where file is created
        name (str): Name of path
    """
    target = Path(path, name)
    target.open('w',encoding="utf-8").write('')
