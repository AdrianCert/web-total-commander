"""This module deals with the management of actions that come as requests"""
from web.settings import PATH_CODING
from .list import list_dir
from .list import dict_pack
from .list import list_parts
from .common import root_path
from .sec import decode_path
from .sec import encode_path
from .open import open_with_default_program as f_open
from .rename import rename as f_rename
from .create import create_dir as f_mkdir
from .create import create_file as f_mkfile
from .remove import rm_tree as f_remove


class ProcessError(Exception):
    """Exception raised for errors in the process function.

    Attributes:
        status -- process status code
        reason -- process status short message
        message -- process status long message
    """

    def __init__(self, status, reason, message=None):
        self.status = 200
        self.reason = reason
        self.message = message or status
        super().__init__(self.message)

    def __str__(self):
        return f'{self.status} {self.reason} : {self.message}'


def process_invalid(dic):
    """Processes the case if the request is invalid

    Args:
        dic (dict): Dictionary with the necessary data to make the request

    Raises:
        ProcessError: The exception is made when an error
        occurred during processing
    """
    raise ProcessError(400, "Invalid Action",
                       f"Action {dic.get('action') or ''} is invalid")


def process_list(dic):
    """Process the case if a listing is desired

    Args:
        dic (dict): Dictionary with the necessary data to make the request

    Raises:
        ProcessError: The exception is made when an error
        occurred during processing

    Returns:
        dict: Dictionary with relevant data
    """
    process_list.default_path = encode_path(root_path(),
                                            procedure=PATH_CODING)

    try:
        path = decode_path(dic.get('node', process_list.default_path),
                           procedure=PATH_CODING)
        atrs = dic.get('atrs', None)
        atrs = atrs.split(',') if atrs else []
        return {
            'parts': list_parts(path),
            'parent': dict_pack(path.parent, 'dir', atrs),
            'files': list_dir(path, atrs)
        }
    except Exception:
        raise ProcessError(500, "error listing",
                           "Action can not be done") from None


def process_open(dic):
    """Process the case if a open is desired

    Args:
        dic (dict): Dictionary with the necessary data to make the request

    Raises:
        ProcessError: The exception is made when an error
        occurred during processing

    Returns:
        dict: Dictionary with relevant data
    """
    try:
        path = decode_path(dic.get('node'), procedure=PATH_CODING)
        f_open(path)
        return ''
    except Exception:
        raise ProcessError(502, "error open",
                           "Action can not be done") from None


def process_rename(dic):
    """Process the case if a rename is desired

    Args:
        dic (dict): Dictionary with the necessary data to make the request

    Raises:
        ProcessError: The exception is made when an error
        occurred during processing

    Returns:
        dict: Dictionary with relevant data
    """
    try:
        path = decode_path(dic.get('node'), procedure=PATH_CODING)
        return f_rename(path, dic.get('value'))
    except Exception:
        raise ProcessError(502, "error rename",
                           "Action can not be done") from None


def process_mkdir(dic):
    """Process the case if a creating directory is desired

    Args:
        dic (dict): Dictionary with the necessary data to make the request

    Raises:
        ProcessError: The exception is made when an error
        occurred during processing

    Returns:
        dict: Dictionary with relevant data
    """
    try:
        path = decode_path(dic.get('node'), procedure=PATH_CODING)
        return f_mkdir(path, dic.get('value'))
    except Exception:
        raise ProcessError(502, "error mkdir",
                           "Action can not be done") from None


def process_mkfile(dic):
    """Process the case if a creating file is desired

    Args:
        dic (dict): Dictionary with the necessary data to make the request

    Raises:
        ProcessError: The exception is made when an error
        occurred during processing

    Returns:
        dict: Dictionary with relevant data
    """
    try:
        path = decode_path(dic.get('node'), procedure=PATH_CODING)
        return f_mkfile(path, dic.get('value'))
    except Exception:
        raise ProcessError(503, "error on make file",
                           "Action can not be done") from None


def process_remove(dic):
    """Process the case if a remove file/dir is desired

    Args:
        dic (dict): Dictionary with the necessary data to make the request

    Raises:
        ProcessError: The exception is made when an error
        occurred during processing

    Returns:
        dict: Dictionary with relevant data
    """
    try:
        path = decode_path(dic.get('node'), procedure=PATH_CODING)
        return f_remove(path)
    except Exception:
        raise ProcessError(504, "error rm_tree",
                           "Action can not be done") from None


def process(dic):
    """Manage action requests

    Invokes specific functions and returns information wrapped
    by other metadata. These are:
        ok -- value indicating whether the action was performed successfully
        status -- a number that encodes what happened
        reason -- a short message related status
        content -- returned information that specific calls

    Args:
        dic (dict): Dictionary with the necessary data to make the request

    Returns:
        dict: Dictionary with relevant data
    """
    process.action = {
        'list': process_list,
        'open': process_open,
        'rename': process_rename,
        'mkdir': process_mkdir,
        'mkfile': process_mkfile,
        'remove': process_remove,
        'invalid': process_invalid
    }
    f_process = process.action.get(dic.get('action', 'invalid'),
                                   process_invalid)
    try:
        return {
            'ok': True,
            'status': 200,
            'reason': "The action was successfully processed",
            'content': f_process(dic) or ""
        }
    except ProcessError as error:
        return {
            'ok': False,
            'status': error.status,
            'reason': error.reason,
            'content': ""
        }
