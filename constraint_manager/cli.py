import argparse
from .utils_pkg import list_names

def parse_args(argv):

    # Top level parser
    parser = argparse.ArgumentParser(description='Manages constraint specifications and generates sdc constraints. ')
    parser.add_argument('--log-level', default='info', help='Configures internal logging level.  ', choices=['info', 'error', 'warning', 'debug', 'critical'])
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Generate parser
    generate_parser = subparsers.add_parser('generate', help='Generate a .sdc file constraining all interfaces in a design')
    generate_parser.add_argument('design_name', default='sample', help='The name of the design to generate constraints for. Defaults to a sample.', choices=list_names('designs'))
    generate_parser.add_argument('-o', '--output', default='stdout', help='The file to output constraints to.  Defaults to console LOGGER.info.')

    # Create parser
    create_parser = subparsers.add_parser('create', help='Create new constraint information')
    create_subparsers = create_parser.add_subparsers(dest='create_command', required=True)

    # Create interface parser
    create_if_parser = create_subparsers.add_parser('interface', help='Create a new interface')
    create_if_parser.add_argument('-o', '--output-dir', default='constraint_manager_out', help='The directory to output yaml\'s to.')
    create_if_parser.add_argument('interface_name', help='The name of your new interface')

    # Create part parser
    create_part_parser = create_subparsers.add_parser('part', help='Create a new part')
    create_part_parser.add_argument('-o', '--output-dir', default='constraint_manager_out', help='The directory to output yaml\'s to.')
    create_part_parser.add_argument('part_name', help='The name of your new part')
    create_part_parser.add_argument('-i', '--interfaces', help='The interfaces implemented by this part (space separated list).', nargs='+', required=True)

    # Create design parser
    create_dsn_parser = create_subparsers.add_parser('design', help='Create a new design')
    create_dsn_parser.add_argument('-o', '--output-dir', default='constraint_manager_out', help='The directory to output yaml\'s to.')
    create_dsn_parser.add_argument('design_name', help='The name of your new design')
    create_dsn_parser.add_argument('-i', '--interfaces', help='The interfaces implemented by this design (space separated list).', nargs='+', required=True)

    # List parser
    list_parser = subparsers.add_parser('list', help='List information from tool repository')
    list_parser.add_argument('list_command', help='Which type of information to list', choices=['interfaces', 'parts', 'designs'])




    args = parser.parse_args(args=argv)

    return args
