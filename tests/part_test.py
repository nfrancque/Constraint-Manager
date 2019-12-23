import pytest

from constraint_manager.part import Part, gen_config_dict
from helpers.utils import *

part = Part('rgmii_part_123')



def test_part_interfaces():
  assert(list(part.interfaces.keys()) == ['rgmii'])

def test_part_props():
  assert(part.name == 'rgmii_part_123')


# Configuration dictionary tests

def test_part_gen_config_dict():
  config_dicts = gen_config_dict(['rgmii'])
  for kind, config_dict in config_dicts.items():
    for k, v in config_dict.items():
      assert(k != None)
      assert(v != None)
