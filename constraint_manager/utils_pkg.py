from pprint import pformat
from os import path
def ppformat(*args):
  return pformat(args, width=200, indent=2, sort_dicts=False)

def update_from_dict(src_dict, dst_obj, props):
  for prop in props:
    if (prop in src_dict):
      setattr(dst_obj, prop, src_dict[prop])

cwd = path.dirname(path.abspath(__file__))


IF_DIR = path.join(cwd, '..', 'interfaces')      # TODO : Make this real
DESIGN_DIR = path.join(cwd, '..', 'sample')
PART_DIR = path.join(cwd, '..', 'parts')