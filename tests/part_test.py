import pytest
from constraint_manager.part import Part
from helpers.utils import *

part = Part('rgmii_part_123')



def test_part_interfaces():
  assert(list(part.interfaces.keys()) == ['rgmii'])

def test_part_props():
  assert(part.name == 'rgmii_part_123')
  
