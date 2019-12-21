from pprint import pformat
from os import path, environ, scandir
import yaml
from glob import glob
from os.path import join as path_join, splitext, basename, abspath
import logging

LOGGER = logging.getLogger(__name__)

def ppformat(*args):
  return pformat(args, width=200, indent=2, sort_dicts=False)

def update_from_dict(src_dict, dst_obj, props):

  for prop in props:
    if (prop in src_dict):
      setattr(dst_obj, prop, src_dict[prop])

cwd = path.dirname(path.abspath(__file__))
module_path = abspath(path_join(cwd, '..'))



class MyDumper(yaml.SafeDumper):
  # HACK: insert blank lines between top-level objects
  # inspired by https://stackoverflow.com/a/44284819/3786245
  def write_line_break(self, data=None):
      super().write_line_break(data)

      if len(self.indents) == 1:
          super().write_line_break()

def write_yaml(obj, filename):
  with open(filename, 'w+') as f:
    yaml.dump(obj, f, Dumper=MyDumper, sort_keys=False)



def list_all(kind, use_local_repo=True):
  search_dir = path_join(cwd, kind)
  if (kind == 'designs'):
    search_lambda = lambda search_dir : [f.path for f in scandir(search_dir) if f.is_dir() ]    
  else:
    search_lambda = lambda search_dir : glob(path_join(search_dir, '*.yaml'))
  ret = search_lambda(path_join(module_path, kind))
  if (use_local_repo):
    try:
      ret.extend(search_lambda(path_join(environ.get('CONSTRAINT_MANAGER_LOCAL_REPO'), kind)))
    except TypeError as exc:
      pass
  return ret



def get_path_by_name(kind, name):
  try:
    return map_names(kind)[name]
  except KeyError:
    LOGGER.error(f'Unable to find {name} in path of {kind}')
    exit(1)

def map_names(kind, use_local_repo=True):
  return {splitext(basename(path))[0] : path for path in list_all(kind, use_local_repo)}


def list_names(kind, use_local_repo=True):
  return map_names(kind).keys()




