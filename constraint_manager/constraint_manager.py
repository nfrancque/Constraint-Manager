import argparse
from .utils_pkg import write_yaml, list_names
from .design import Design, gen_config_dict as dsn_gen_config_dict
from .interface import gen_config_dict as if_gen_config_dict
from .part import gen_config_dict as part_gen_config_dict
from glob import glob
from os.path import join as path_join, exists as path_exists, dirname, basename, splitext
from os import makedirs, environ
from pprint import pprint
import sys
import logging

class ConstraintManager:
  """ The ConstraintManager class implements the frontend interface to the constraint manager.
      It primarily control input/output locations.

  """
  def __init__(self):

    args = self.parse_args()
    self._configure_logging(args.log_level)

    cmd_function = getattr(self, args.command)
    cmd_function(args)






  def parse_args(self):


    # Top level parser
    parser = argparse.ArgumentParser(description='Manages constraint specifications and generates sdc constraints.  Set environment variable ')
    parser.add_argument('--log-level', default = 'info', help='Configures internal logging level.  ', choices=['info', 'error', 'warning', 'debug', 'critical'])
    subparsers = parser.add_subparsers(dest='command', required=True)


    # Generate parser
    generate_parser     = subparsers.add_parser('generate', help='Generate a .sdc file constraining all interfaces in a design')
    generate_parser.add_argument('design_name', default = 'sample', help='The name of the design to generate constraints for. Defaults to a sample.', choices=list_names('designs'))
    generate_parser.add_argument('-o', '--output', default = 'stdout', help='The file to output constraints to.  Defaults to console print.')

    # Create parser
    create_parser = subparsers.add_parser('create', help='Create new constraint information')
    create_subparsers = create_parser.add_subparsers(dest='create_command', required=True)

    # Create interface parser
    create_if_parser = create_subparsers.add_parser('interface', help='Create a new interface')
    create_if_parser.add_argument('-o', '--output-dir', default = 'constraint_manager_out', help='The directory to output yaml\'s to.')
    create_if_parser.add_argument('interface_name', help='The name of your new interface')

    # Create part parser
    create_part_parser = create_subparsers.add_parser('part', help='Create a new part')
    create_part_parser.add_argument('-o', '--output-dir', default = 'constraint_manager_out', help='The directory to output yaml\'s to.')
    create_part_parser.add_argument('part_name', help='The name of your new part')
    create_part_parser.add_argument('-i', '--interfaces', help='The interfaces implemented by this part (space separated list).', nargs='+', required=True)

    # Create design parser
    create_dsn_parser = create_subparsers.add_parser('design', help='Create a new design')
    create_dsn_parser.add_argument('-o', '--output-dir', default = 'constraint_manager_out', help='The directory to output yaml\'s to.')
    create_dsn_parser.add_argument('design_name', help='The name of your new design')
    create_dsn_parser.add_argument('-i', '--interfaces', help='The interfaces implemented by this design (space separated list).', nargs='+', required=True)

    # List parser
    list_parser     = subparsers.add_parser('list', help='List information from tool repository')
    list_parser.add_argument('list_command', help='Which type of information to list', choices=['interfaces', 'parts'])



    args = parser.parse_args()

    return args




  def generate(self, args):
    parser = argparse.ArgumentParser()

    self.design = Design(args.design_name)
    constraints = self.design.gen_constraints()
    if (args.output == 'stdout'):
      print(constraints)
    else:
      with open(str(args.output), 'w+') as f:
        f.write(constraints)   

  def create(self, args):
    cmd_func = getattr(self, 'create_' + args.create_command)
    cmd_func(args)
    print('Created ' + args.create_command)

  def list(self, args):
    cmd_func = getattr(self, 'list_' + args.list_command)
    listed = cmd_func(args)
    print(args.list_command.capitalize() + ':')
    print('\n'.join(listed))

  def list_interfaces(self, args):
    return list_names('interfaces')

  def list_parts(self, args):
    return list_names('parts')

  def create_interface(self, args):
    output_dir = path_join(args.output_dir, 'interfaces')
    interface_name = args.interface_name
    config_dict = if_gen_config_dict()
    output_file = path_join(output_dir, interface_name + '.yaml')
    if (not path_exists(output_dir)):
      makedirs(output_dir, exist_ok=True)
    write_yaml(config_dict, output_file)

  def create_design(self, args):
    output_dir = path_join(args.output_dir, 'designs', args.design_name)
    design_name = args.design_name
    if (not path_exists(output_dir)):
      makedirs(output_dir, exist_ok=True)
    config_dicts = dsn_gen_config_dict(args.interfaces)
    for interface, config_dict in config_dicts.items():
      output_file = path_join(output_dir, design_name + '_' + interface + '.yaml')
      write_yaml(config_dict, output_file)

  def create_part(self, args):
    output_dir = path_join(args.output_dir, 'parts')
    part_name = args.part_name
    config_dict = part_gen_config_dict(args.interfaces)
    output_file = path_join(output_dir, part_name + '.yaml')
    if (not path_exists(output_dir)):
      makedirs(output_dir, exist_ok=True)
    write_yaml(config_dict, output_file)


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
