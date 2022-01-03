"""This module deals with the management of actions that come as requests"""
from web.settings import PATH_CODING
from .list import list_dir
from .common import root_path
from .sec import decode_path
from .sec import encode_path


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
            'path': path.parts,
            'parent': encode_path(path.parent, procedure=PATH_CODING),
            'files': list_dir(path, atrs)
        }
    except Exception:
        raise ProcessError(500, "error listing",
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
