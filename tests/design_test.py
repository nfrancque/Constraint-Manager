import pytest

from constraint_manager.design import Design, Interface, gen_config_dict
from helpers.utils import *

design = Design('sample')



def test_design_class():
  assert(type(design) is Design)

def test_design_attributes_classes():
  for interface in design.interfaces:
  	assert(type(interface) is Interface)
  
# Configuration dictionary tests

def test_design_gen_config_dict():
  config_dicts = gen_config_dict(['rgmii'])
  for kind, config_dict in config_dicts.items():
    for k, v in config_dict.items():
      assert(k != None)
      assert(v != None)
