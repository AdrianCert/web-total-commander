"""This module is dedicated to listing and displaying files"""
from os import walk, path as os_path
from pathlib import Path
from datetime import datetime
from web.settings import PATH_CODING
from .sec import encode_path
from .sec import lookup_sd_path

TIME_FORMAT = '%Y-%m-%d %H:%M'

IS_FILE_MAP = {
    True: "file",
    False: "dir"
}

ATRS_MAP = {
    'id': lambda x: encode_path(x, procedure=PATH_CODING),
    'name': os_path.basename,
    'owner': lambda x: lookup_sd_path(str(x))[0],
    'perm': lambda x: permissions_string(x.stat()),
    'size': lambda x: x.stat().st_size,
    'atime': lambda x: x.stat().st_atime,
    'mtime': lambda x: x.stat().st_mtime,
    'ctime': lambda x: x.stat().st_ctime,
    'str_atime': lambda x: time2string(x.stat().st_atime),
    'str_mtime': lambda x: time2string(x.stat().st_mtime),
    'str_ctime': lambda x: time2string(x.stat().st_ctime)
}

NR_MOD_MAP = {
    '7': 'rwx',
    '6': 'rw-',
    '5': 'r-x',
    '4': 'r--',
    '0': '---'
}


def permissions_string(stat):
    """Convert st_mode permision numer intro rwx unix like string

    Args:
        st (stat_result object): status of specified path

    Returns:
        str: rwx unix line string
    """
    permission_string = str(oct(stat.st_mode)[-3:])
    return ''.join(NR_MOD_MAP.get(x, x) for x in permission_string)


def time2string(timestamp):
    """Convert timestamp to string

    Args:
        timestamp (float): The timestamp

    Returns:
        str: String value of timestamp
    """
    return datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)


def path_atr(path, atr):
    """Exact path atribute value.

    If it's not avalable will return an empty string

    Args:
        path (str): path to be extracted the atribute
        atr (list[str]): the atribute with will be extracted

    Returns:
        str: value of atributes which is extracted
    """
    try:
        f_atribute = ATRS_MAP.get(atr, lambda x: "")
        return f_atribute(path)
    except Exception:  # pylint: disable=broad-except
        return ""


def dict_pack(path, ptype=None, atrs_list=None):
    """Extract the information for a path and put it in a dictionary

    Args:
        path (str/Path): The path from which the extraction is performed
        ptype (str, optional): Value of type for the path. Defaults to None.
        atrs_list (list[str], optional): List of attributes to be aggregated.
    """
    def get_type(_type):
        return ('type', _type or IS_FILE_MAP.get(path.is_file()))

    if not atrs_list:
        atrs_list = []
    atrs_list.extend(['id', 'name'])

    atrs = [(i, path_atr(path, i)) for i in atrs_list]
    atrs.extend([get_type(ptype)])
    return dict(atrs)


def list_dir(path, atrs=None):
    """Extract all the files and directories from the path within attributes

    Args:
        path (str/Path): The path from which the extraction is performed
        atrs (list[str], optional): List of attributes to be aggregated.

    Returns:
        list[dict]: Returns a list of objects for each file.
        Objects that are a dictionary that contains all the required attributes
    """
    path = Path(path).absolute()
    curr, dirs, files = next(walk(path))  # pylint: disable=unused-variable
    dirs_pack = [dict_pack(path / i, 'dir', atrs) for i in dirs]
    files_pack = [dict_pack(path / i, 'file', atrs) for i in files]
    return dirs_pack + files_pack


if __name__ == "__main__":
    # demonstating work
    import json
    print(json.dumps(list_dir(Path("."), list(ATRS_MAP.keys())), indent=2))
