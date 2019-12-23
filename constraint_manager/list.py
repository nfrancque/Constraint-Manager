import logging

from .utils_pkg import list_names

LOGGER = logging.getLogger(__name__)


def list(args):
    """Lists the given information by printing to console.

    :param args: Technically any object, typically comes from an argparse Namespace object, but any that has the required attributes also works
    :type args: object
    """
    print(args.list_command.capitalize() + ':')
    print('\n'.join(list_names(args.list_command)))
