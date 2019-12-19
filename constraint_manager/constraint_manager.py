import argparse
from .utils_pkg import DESIGN_DIR
from .design import Design
from glob import glob
from os.path import join as path_join
from pprint import pprint
from sys import stdout
import sys
class ConstraintManager:
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument('--yaml_dir', default = DESIGN_DIR, help='The directory containing design specification yamls')
    parser.add_argument('-o', '--output', default = stdout, help='The file to output constraints to')
    self.args   = parser.parse_args()
    self.design = Design(self.args.yaml_dir)
    constraints = '\n'.join(self.design.gen_constraints()) + '\n'
    if (self.args.output == stdout):
      print(constraints)
    else:
      with open(str(self.args.output), 'w+') as f:
        f.write(constraints)


def main():
  constraint_manager = ConstraintManager()


if __name__ == '__main__':
  sys.path.append('..')
  main()
