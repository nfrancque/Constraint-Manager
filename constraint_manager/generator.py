""" Implements generation of sdc constraints for the given design

"""
import logging

from .design import Design

LOGGER = logging.getLogger(__name__)


def generate(args):
    """Generates constraints of the specified design.

    :param args: Technically any object, typically comes from
    an argparse Namespace object, but any that has the
    required attributes also works
    :type args: object
    """
    design = Design(args.design_name)
    constraints = design.gen_constraints()
    if args.output == 'stdout':
        print(constraints)
    else:
        with open(str(args.output), 'w+') as file:
            file.write(constraints)
