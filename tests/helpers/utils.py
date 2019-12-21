from constraint_manager import constraint
from constraint_manager.constraint_manager import ConstraintManager
import sys

def gen_generated_clock_props():
  props                    = {}
  props['clk_name']        = 'blah'
  props['get_src_clk_cmd'] = 'get_pins I_CLK'
  props['get_dst_clk_cmd'] = 'get_pins O_CLK'
  props['divide_by']       = 4

  return props

def gen_input_max_props():
  props                    = {}
  props['equation']        = '$trce_dly_max + $tsu'
  props['signal_group']    = '$input_ports'
  props['get_clk_cmd']     = 'get_pins I_CLK'

  return props


def gen_constraint_props(kind):
  if kind == 'in_max':
    props = gen_input_max_props()
  elif kind == 'generated_clk':
    props = gen_generated_clock_props()
  else:
    props = None 
  return props

constraint_name = 'test'

def get_constraint_instance(kind):
  cstr_factory = constraint.Constraint.factory(kind)
  props = gen_constraint_props(kind)
  cstr = cstr_factory(constraint_name, props)
  return cstr


def util_test_constraint_identity(kind, resolved_class):
  cstr = get_constraint_instance(kind)
  assert type(cstr) is resolved_class

def util_test_constraint_props(kind):
  cstr = get_constraint_instance(kind)
  assert(cstr.name == constraint_name)
  expected = gen_constraint_props(kind)
  if expected != None:
    for prop, value in expected.items():
      assert(getattr(cstr, prop) == value)

def get_expected_input_max(kind, props):
    return f"set_input_delay -max {props['equation']} -clock {props['get_clk_cmd']} {props['signal_group']}"

def get_expected_generated_clock(kind, props):
    return f"create_generated_clock -name {props['clk_name']} -divide_by {props['divide_by']} -source {props['get_src_clk_cmd']} {props['get_dst_clk_cmd']}"


def get_expected_constraint(kind):
  props = gen_constraint_props(kind)
  if kind == 'in_max':
    props = get_expected_input_max(kind, props)
  elif kind == 'generated_clk':
    props = get_expected_generated_clock(kind, props)
  else:
    expected = None
  return props

def util_test_gen_constraint(kind):
  cstr = get_constraint_instance(kind)
  expected = get_expected_constraint(kind)
  actual = cstr.gen_constraint()
  assert(expected==actual)

def util_test_constraint_manager(capsys, args):
  try:
    cstr_mgr = ConstraintManager(args)
    out, err = capsys.readouterr()
    return out, err, True
  except:
    return '', sys.exc_info(), False