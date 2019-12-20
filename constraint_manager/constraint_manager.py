import argparse
from .utils_pkg import DESIGN_DIR
from .design import Design
from glob import glob
from os.path import join as path_join
from pprint import pprint
import sys
import logging

class ConstraintManager:
  """ The ConstraintManager class implements the frontend interface to the constraint manager.
      It primarily control input/output locations.

  """
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument('--yaml_dir', default = DESIGN_DIR, help='The directory containing design specification yamls.  Defaults to a sample.')
    parser.add_argument('-o', '--output', default = 'stdout', help='The file to output constraints to.  Defaults to console print.')
    parser.add_argument('--log-level', default = 'info', help='Configures internal logging level.  ', choices=['info', 'error', 'warning', 'debug', 'critical'])
    self.args   = parser.parse_args()
    self._configure_logging(self.args.log_level)
    self.design = Design(self.args.yaml_dir)
    constraints = self.design.gen_constraints()
    if (self.args.output == 'stdout'):
      print(constraints)
    else:
      with open(str(self.args.output), 'w+') as f:
        f.write(constraints)

  @staticmethod
  def _configure_logging(log_level):
      """
      Configure logging based on log_level string
      """
      level = getattr(logging, log_level.upper())
      logging.basicConfig(
          filename=None, format="%(levelname)7s - %(message)s", level=level
    )


def main():
  # console_scripts tags onto main func, do not remove
  constraint_manager = ConstraintManager()






if __name__ == '__main__':
  sys.path.append('..')
  main()
