import pytest

from constraint_manager import constraint
from helpers.utils import *

# Identity tests

def test_unimplemented_identity():
  util_test_constraint_identity('blah', constraint.UnimplementedConstraint)

def test_generated_clock_identity():
  util_test_constraint_identity('generated_clk', constraint.GeneratedClockConstraint)

def test_input_max_identity():
  util_test_constraint_identity('in_max', constraint.InputMaxConstraint)

# Property tests

def test_unimplemented_props():
  util_test_constraint_props('blah')

def test_generated_clock_props():
  util_test_constraint_props('generated_clk')

def test_input_max_props():
  util_test_constraint_props('in_max')

# Constraint generation tests

def test_unimplemented_gen_constraint():
  util_test_gen_constraint('blah')

def test_generated_clock_gen_constraint():
  util_test_gen_constraint('generated_clk')

def test_input_max_gen_constraint():
  util_test_gen_constraint('in_max')


# Configuration dictionary tests

def test_constraint_gen_config_dict():
  config_dicts = constraint.gen_config_dict()
  for kind, config_dict in config_dicts.items():
    for prop in config_dict['test'].values():
      assert(prop == '')
