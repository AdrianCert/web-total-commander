from pathlib import Path
from os import stat
from cryptography.fernet import Fernet

CRYPT_KEY = b'W0kNvxMLCn-0S8ldJG0mPE4PxubMEBKzAHTBNCDyFW4='


def encode_path(path, key=None, procedure=None):
    """Encode path_id acording given procedure

    Args:
        path (Path): The path where operation is performed
        key ([bits], optional): Key used on encription. Defaults to None.
        procedure (str, optional): Procedure name used. Defaults to None.

    Returns:
        str: Encoded path ready for trasmit
    """
    encode_path.procedures = {
        "fernet": lambda x, k: Fernet(k).encrypt(x.encode()).decode(),
        "direct": lambda x, k: x
    }
    if key is None:
        key = CRYPT_KEY
    if procedure is None:
        procedure = 'direct'
    f_procedure = encode_path.procedures.get(procedure) \
        or encode_path.procedures.get('direct')
    f_message = str(path)
    return f_procedure(f_message, key)


def decode_path(path, key=None, procedure=None):
    """Decode path_id acording given procedure

    Args:
        path (str): The path where operation is performed
        key ([bits], optional): Key used on decription. Defaults to None.
        procedure (str, optional): Procedure name used. Defaults to None.

    Returns:
        Path : Decoded path ready to use
    """
    decode_path.procedures = {
        "fernet": lambda x, k: Fernet(k).decrypt(x.encode()).decode(),
        "direct": lambda x, k: Path(x)
    }
    if key is None:
        key = CRYPT_KEY
    if procedure is None:
        procedure = 'direct'
    f_procedure = decode_path.procedures.get(procedure) \
        or decode_path.procedures.get('direct')
    f_message = path
    return f_procedure(f_message, key)


def windows_lookup_sd(path):
    """Lookup for security description on windows

    Args:
        path (Path): The path where operation is performed

    Returns:
        tuple: return tuple with owner username, group and uid
    """
    import win32security as wins
    sd = wins.GetFileSecurity(path, wins.OWNER_SECURITY_INFORMATION)
    owner_sid = sd.GetSecurityDescriptorOwner()
    return wins.LookupAccountSid(None, owner_sid)


def unix_lookup_sd(path):
    """Lookup for security description on unix

    Args:
        path (Path): The path where operation is performed

    Returns:
        tuple: return tuple with owner username, group and uid
    """
    from pwd import getpwuid
    from grp import getgrgid
    path_stat = stat(path)
    return (
        getpwuid(path_stat.st_uid).pw_name,
        getgrgid(path_stat.st_gid).gr_name,
        path_stat.st_uid
    )


LOOKUP_SD_PROCEDURES = [
    unix_lookup_sd,
    windows_lookup_sd,
]


def lookup_sd_path(path, procedure=None):
    """Lookup for security description for specicic path

    Args:
        path (Path): The path where operation is performed
        procedure (iter, optional): Iterator throught all the
        procedure used. Defaults to None.

    Returns:
        tuple: return tuple with owner username, group and uid
    """
    if procedure is None:
        procedure = iter(LOOKUP_SD_PROCEDURES)
    if procedure is False:
        return ('user', 'group', 0)
    try:
        return next(procedure, False)(path)
    except ImportError:
        return lookup_sd_path(path, procedure)
