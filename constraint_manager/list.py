from .utils_pkg import list_names
import logging

LOGGER = logging.getLogger(__name__)

def list(args):
  cmd_func = globals()['list_' + args.list_command]
  listed = cmd_func(args)
  print(args.list_command.capitalize() + ':')
  print('\n'.join(listed))

def list_interfaces(args):
  return list_names('interfaces')

def list_parts(args):
  return list_names('parts')

def list_designs(args):
  return list_names('designs')

