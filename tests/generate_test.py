import sys

import pytest

from constraint_manager import generate
from helpers.utils import *


class Object(object):
  pass

obj = Object()


def test_generate_all():
  obj.output = 'stdout'
  obj.design_name = 'sample'
  out = generate.generate(obj)
  assert(out != '')
