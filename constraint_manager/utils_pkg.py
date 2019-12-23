import logging
from glob import glob
from os import environ, path, scandir
from os.path import abspath, basename
from os.path import join as path_join
from os.path import splitext
from pprint import pformat
import sys

import yaml

LOGGER = logging.getLogger(__name__)


def ppformat(*args):
    return pformat(args, width=200, indent=2, sort_dicts=False)


def update_from_dict(src_dict, dst_obj, props):

    for prop in props:
        if prop in src_dict:
            setattr(dst_obj, prop, src_dict[prop])


CWD = path.dirname(path.abspath(__file__))
MODULE_PATH = abspath(path_join(CWD, '..'))


class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def write_yaml(obj, filename):
    with open(filename, 'w+') as file:
        yaml.dump(obj, file, Dumper=MyDumper, sort_keys=False)


def read_yaml(filename):
    with open(filename, 'r') as file:
        try:
            yaml_dict = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            LOGGER.info(exc)
            yaml_dict = {}
    return yaml_dict


def list_all(kind, use_local_repo=True):
    search_dir = path_join(CWD, kind)
    if kind == 'designs':
        def search_lambda(search_dir): return [
            f.path for f in scandir(search_dir) if f.is_dir()]
    else:
        def search_lambda(search_dir): return glob(
            path_join(search_dir, '*.yaml'))
    ret = search_lambda(path_join(MODULE_PATH, kind))
    if use_local_repo:
        try:
            ret.extend(search_lambda(
                path_join(environ.get('CONSTRAINT_MANAGER_LOCAL_REPO'), kind)))
        except TypeError:
            pass
    return ret


def get_path_by_name(kind, name):
    try:
        return map_names(kind)[name]
    except KeyError:
        LOGGER.error(f'Unable to find {name} in path of {kind}')
        sys.exit(1)


def map_names(kind, use_local_repo=True):
    return {splitext(basename(path))[
        0]: path for path in list_all(kind, use_local_repo)}


def list_names(kind, use_local_repo=True):
    return map_names(kind).keys()
