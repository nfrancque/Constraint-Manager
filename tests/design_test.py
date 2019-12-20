import pytest
from constraint_manager.design import Design, Interface
from constraint_manager.utils_pkg import DESIGN_DIR
from helpers.utils import *

design = Design(DESIGN_DIR)



def test_design_class():
  assert(type(design) is Design)

def test_design_attributes_classes():
  for interface in design.interfaces:
  	assert(type(interface) is Interface)
  
