"""This module deals with opening files"""
import subprocess
import os
import platform


def open_with_default_program(path):
    """Open file with its defaul program

    Args:
        path (Path/str): The path file with will be open
    """
    open_with_default_program.f = {
        'Darwin': lambda x: subprocess.call(['open', x]),
        'Windows': os.startfile,
        'unix': lambda x: subprocess.call(['xdg-open', x])
    }
    procedure = open_with_default_program.f.get(platform.system(),
                                                open_with_default_program.f.get('unix'))

    return procedure(str(path))
