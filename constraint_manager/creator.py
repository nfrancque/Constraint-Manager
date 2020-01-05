""" Implements creation of interfaces, designs, and parts
Writes out configuration data to yaml files
"""


import logging
from os import makedirs
from os.path import exists as path_exists
from os.path import join as path_join

from .design import gen_config_dict as dsn_gen_config_dict
from .interface import gen_config_dict as if_gen_config_dict
from .part import gen_config_dict as part_gen_config_dict
from .utils_pkg import write_yaml

LOGGER = logging.getLogger(__name__)


def create(args):
    """Creates the given type of specification.

    :param args: An object with all required members for this function.  TODO: Document
    :type args: object
    """
    # Delegate work to specific sub function
    cmd_func = globals()['create_' + args.create_command]
    cmd_func(args)
    LOGGER.info('Created %s', args.create_command)


def create_interface(args):
    """Creates an interface.  Given input specification, generates a yaml
    configuration.

    :param args: An object with all required members for this function.  TODO: Document
    :type args: object
    """
    output_dir = path_join(args.output_dir, 'interfaces')
    interface_name = args.interface_name
    config_dict = if_gen_config_dict()
    output_file = path_join(output_dir, interface_name + '.yaml')
    if not path_exists(output_dir):
        makedirs(output_dir, exist_ok=True)
    write_yaml(config_dict, output_file)


def create_design(args):
    """Creates a design.  Given input specification, generates a yaml
    configuration.

    :param args: An object with all required members for this function.  TODO: Document
    :type args: object
    """
    output_dir = path_join(args.output_dir, 'designs', args.design_name)
    design_name = args.design_name
    if not path_exists(output_dir):
        makedirs(output_dir, exist_ok=True)
    config_dicts = dsn_gen_config_dict(args.interfaces)
    for interface, config_dict in config_dicts.items():
        output_file = path_join(
            output_dir, design_name + '_' + interface + '.yaml')
        write_yaml(config_dict, output_file)


def create_part(args):
    """Creates a part.  Given input specification, generates a yaml
    configuration.

    :param args: An object with all required members for this function.  TODO: Document
    :type args: object
    """
    output_dir = path_join(args.output_dir, 'parts')
    part_name = args.part_name
    config_dict = part_gen_config_dict(args.interfaces)
    output_file = path_join(output_dir, part_name + '.yaml')
    if not path_exists(output_dir):
        makedirs(output_dir, exist_ok=True)
    write_yaml(config_dict, output_file)
