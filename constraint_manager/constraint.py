import yaml
from .utils_pkg import ppformat
from pprint import pprint, pformat
from copy import copy

def constraint_kind_to_class():
  return {
    'generated_clk' : GeneratedClockConstraint,
    'in_max'        : InputMaxConstraint

  }


class Constraint:
  def factory(kind):

    try:
      return constraint_kind_to_class()[kind]
    except KeyError:
      print('Warning: ' + kind + ' is not an implemented constraint.  Try misc?')
      return UnimplementedConstraint
  def __init__(self, name, props):
    self.name = name
  def __str__(self):
    ret = {'constraint_type' : self.__class__.__name__}
    ret.update(copy(self.__dict__))
    return ppformat(ret)
  def __repr__(self):
    return str(self)

  def gen_constraint(self):
    return None


class UnimplementedConstraint(Constraint):
  def __init__(self, name, props):
    super().__init__(name, props)



class GeneratedClockConstraint(Constraint):
  def __init__(self, name, props):
    super().__init__(name, props)
    self.clk_name        = props['clk_name']
    self.get_src_clk_cmd = props['get_src_clk_cmd']
    self.get_dst_clk_cmd = props['get_dst_clk_cmd']
    self.divide_by       = props['divide_by']

  def gen_constraint(self):
    return f'create_generated_clock -name {self.clk_name} -divide_by {self.divide_by} -source {self.get_src_clk_cmd} {self.get_dst_clk_cmd}'

class InputMaxConstraint(Constraint):
  def __init__(self, name, props):
    super().__init__(name, props)
    self.equation     = props['equation']
    self.signal_group = props['signal_group']
    self.get_clk_cmd     = props['get_clk_cmd']
  def gen_constraint(self):

    return f'set_input_delay -max {self.equation} -clock {self.get_clk_cmd} {self.signal_group}'
