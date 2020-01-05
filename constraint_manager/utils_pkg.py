""" Simple utils package for common functions

"""

import logging
from glob import glob
from os import environ, path, scandir
from os.path import abspath, basename
from os.path import join as path_join
from os.path import splitext
import pprint
import sys

import yaml

LOGGER = logging.getLogger(__name__)


def ppformat(*args):
    """ pformat wrapper with desireable parameters
    :param args: arguments to format
    :return formatted version of input data
    """
    if sys.version_info.minor == 6:
        pprint._sorted = lambda x: x # pylint: disable=protected-access
    elif sys.version_info.minor == 7:
        pprint.sorted = lambda x: x

    if sys.version_info.minor == 8:
        # pylint: disable=unexpected-keyword-arg
        return pprint.pformat(args, width=200, indent=2, sort_dicts=False)

    return pprint.pformat(args, width=200, indent=2)

def update_from_dict(src_dict, dst_obj, props):
    """ Updates items of a class from a dict
    :param src_dict: The dict that has information
    :type src_dict: dict
    :param dst_obj: An object that needs information
    :type dst_obj: Object
    :param props:  The properties to transfer
    :type props: list
    """
    for prop in props:
        if prop in src_dict:
            setattr(dst_obj, prop, src_dict[prop])


CWD = path.dirname(path.abspath(__file__))
MODULE_PATH = abspath(path_join(CWD, '..'))

# pylint: disable=too-many-ancestors
class MyDumper(yaml.SafeDumper):
    """ A class to dump yaml with blank lines
    """
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def write_yaml(obj, filename):
    """ Wrapper to open yaml file and write object
    :param obj:  object to dump
    :type obj: Object
    :param filename: the filename to write to
    :type filename: str
    """
    with open(filename, 'w+') as file:
        yaml.dump(obj, file, Dumper=MyDumper, sort_keys=False)


def read_yaml(filename):
    """ Wrapper to open yaml file and read object
    :param filename: the filename to read from
    :type filename: str

    :return The object representation of the yaml file
    :rtype: Object
    """
    with open(filename, 'r') as file:
        try:
            yaml_dict = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            LOGGER.info(exc)
            yaml_dict = {}
    return yaml_dict


def list_all(kind, use_local_repo=True):
    """ List all of given kind
    :param kind:  {interface, part, design}
    :type kind: str
    :param use_local_repo: Whether to look at local repo
    :type use_local_repo: Boolean

    :return list of things found for the given kind
    :rtype list
    """
    if kind == 'designs':
        def search_lambda(search_dir):
            return [f.path for f in scandir(search_dir) if f.is_dir()]
    else:
        def search_lambda(search_dir):
            return glob(path_join(search_dir, '*.yaml'))

    ret = search_lambda(path_join(MODULE_PATH, kind))
    if use_local_repo:
        try:
            ret.extend(search_lambda(
                path_join(environ.get('CONSTRAINT_MANAGER_LOCAL_REPO'), kind)))
        except TypeError:
            pass
        except FileNotFoundError:
            pass
    return ret


def get_path_by_name(kind, name):
    """ Returns the absolute path of the configuration file
    of the given name and kind
    :param kind: {interface, design, part}
    :type kind: str
    :param name: the name
    :type name: str

    :return The absolute path
    :rtype str
    """
    try:
        return map_names(kind)[name]
    except KeyError:
        LOGGER.error('Unable to find %s in path of %s', name, kind)
        sys.exit(1)


def map_names(kind, use_local_repo=True):
    """ Returns a dictionary of the form {name : path}
    for each name of this kind
    :param kind: {interface, design, part}
    :type kind: str
    :param use_local_repo: Whether to look at local repo
    :type use_local_repo: Boolean

    :return The dictionary mapping of paths
    :rtype dict
    """
    return {splitext(basename(path))[
        0]: path for path in list_all(kind, use_local_repo)}


def list_names(kind, use_local_repo=True):
    """ Returns a list of all names for this kind
    :param kind: {interface, design, part}
    :type kind: str
    :param use_local_repo: Whether to look at local repo
    :type use_local_repo: Boolean

    :return The list of names
    :rtype list
    """
    return map_names(kind, use_local_repo).keys()
