"""This modele contains common function used in code module"""
import os


def root_path():
    """Return the root path for file system independend by platflerm

    Returns:
        str: The root path
    """
    return os.path.abspath(os.sep)
