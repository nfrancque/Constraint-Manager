from pprint import pformat
def ppformat(*args):
  return pformat(args, width=200, indent=2, sort_dicts=False)

IF_DIR = '../interfaces'      # TODO : Make this real
DESIGN_DIR = '../tmp'
PART_DIR = '../parts'