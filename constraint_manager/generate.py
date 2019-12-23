from .design import Design
import logging

LOGGER = logging.getLogger(__name__)

def generate(args):
    """ Generates constraints of the specified design

    :param args: Technically any object, typically comes from an argparse Namespace object, but any that has the required attributes also works
    :type args: object
    """
    design = Design(args.design_name)
    constraints = design.gen_constraints()
    if args.output == 'stdout':
        print(constraints)
    else:
        with open(str(args.output), 'w+') as f:
            f.write(constraints)