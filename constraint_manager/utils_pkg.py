from pprint import pformat
from os import path
def ppformat(*args):
  return pformat(args, width=200, indent=2, sort_dicts=False)

cwd = path.dirname(path.abspath(__file__))


IF_DIR = path.join(cwd, '..', 'interfaces')      # TODO : Make this real
DESIGN_DIR = path.join(cwd, '..', 'sample')
PART_DIR = path.join(cwd, '..', 'parts')