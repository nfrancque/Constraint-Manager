import yaml
from .utils_pkg import ppformat, update_from_dict
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
    prop_names = ['clk_name', 'get_src_clk_cmd', 'get_dst_clk_cmd', 'divide_by']
    update_from_dict(props, self, prop_names)


  def gen_constraint(self):
    return f'create_generated_clock -name {self.clk_name} -divide_by {self.divide_by} -source {self.get_src_clk_cmd} {self.get_dst_clk_cmd}'

class InputMaxConstraint(Constraint):
  def __init__(self, name, props):
    super().__init__(name, props)
    prop_names = ['clk_name', 'equation', 'signal_group', 'get_clk_cmd']
    update_from_dict(props, self, prop_names)

  def gen_constraint(self):

    return f'set_input_delay -max {self.equation} -clock {self.get_clk_cmd} {self.signal_group}'
