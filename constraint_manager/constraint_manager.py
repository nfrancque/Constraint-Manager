#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

""" Top level main interface to the constraint manager
Capable of command line creation of configuration files
and generation of sdc constraints from them.
"""

import logging
import sys
from os import environ, getcwd
from os.path import join as path_join

import argcomplete

from . import cli, creator, generator, lister

# pylint: disable=too-few-public-methods
class ConstraintManager:
    """The ConstraintManager class implements the frontend interface to the
    constraint manager.

    It primarily control input/output locations. By default it searches
    in a repository contained in the tool and
    `pwd`/constraint_manager_out (default export location). Set the
    environment variable CONSTRAINT_MANAGER_LOCAL_REPO to modify the
    location of the latter.
    """

    def __init__(self, args):
        self.args = args

        self._configure_logging(args.log_level)




    def run(self):
        """ Determine what command needs to be run and call it.
        """
        if self.args.command == 'create':
            creator.create(self.args)
        elif self.args.command == 'generate':
            generator.generate(self.args)
        elif self.args.command == 'list':
            lister.list(self.args)

    @staticmethod
    def _configure_logging(log_level):
        """Configure logging based on log_level string."""
        level = getattr(logging, log_level.upper())
        logging.basicConfig(
            filename=None, format="%(levelname)7s - %(message)s", level=level
        )


def get_parser():
    """ Simple wrapper around cli.get_parser to
    make publicly available

    :return parser:  A parser
    :rtype: argparse.ArgumentParser

    """
    return cli.get_parser()


def main(args=None):
    """ Main entry point.  Sets environment variables
    if necessary, instantiates a configured
    ConstraintManager and runs it.

    """
    if 'CONSTRAINT_MANAGER_LOCAL_REPO' not in environ:
        environ['CONSTRAINT_MANAGER_LOCAL_REPO'] = path_join(
            getcwd(), 'constraint_manager_out')

    if args is None:
        parser = get_parser()
        argcomplete.autocomplete(parser)
        args = parser.parse_args()
    constraint_manager = ConstraintManager(args)
    constraint_manager.run()



if __name__ == '__main__':
    sys.path.append('..')
    main()
