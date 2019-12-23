import sys

import pytest

from constraint_manager import list
from helpers.utils import *


class Object(object):
  pass

obj = Object()


def test_list_interfaces():
  obj.list_command = 'interfaces'
  out = list.list(obj)
  assert(out != '')
def test_list_parts():
  obj.list_command = 'parts'
  out = list.list(obj)
  assert(out != '')
def test_list_designs():
  obj.list_command = 'designs'
  out = list.list(obj)
  assert(out != '')
