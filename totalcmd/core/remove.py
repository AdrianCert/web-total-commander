"""This module handle remove jobs"""

def rm_tree(path):
    """Remove recursively files and directories

    Args:
        path (Path): The path what it is remove
    """
    if path.is_file():
        path.unlink()
    else:
        for child in path.glob('*'):
            rm_tree(child)
        path.rmdir()
