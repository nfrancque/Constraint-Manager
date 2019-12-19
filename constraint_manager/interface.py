import yaml
from .constraint import Constraint
from .utils_pkg import ppformat, IF_DIR
from pprint import pprint
from os.path import join as path_join

class Interface:
  def __init__(self, if_name):
    yaml_file = path_join(IF_DIR, if_name + '.yml')
    self.parse_yaml(yaml_file)
    self.name = if_name
    # pprint(self, width=1, indent=4)
  def __str__(self):
    return ppformat(self.__dict__)
  def __repr__(self):
    return str(self)

  class PartConstant:
    def __init__(self, name, props):
      self.name    = name
      self.desc    = props['desc']
      self.default = props['default']
      self.value   = None
  def __str__(self):
    return ppformat(self.__dict__)
  def __repr__(self):
    return str(self)

  class DesignVariable:
    def __init__(self, name, props):
      self.name    = name
      self.desc    = props['desc']
      self.default = props['default']
      self.value   = None
    def __str__(self):
      return ppformat(self.__dict__)
    def __repr__(self):
      return str(self)

  class SignalGroup:
    def __init__(self, name, props):
      self.name  = name
      self.value = props
    def __str__(self):
      return ppformat(self.__dict__)
    def __repr__(self):
      return str(self)

  class Signal:
    def __init__(self, name):
      self.name        = name
      self.value       = None
    def __str__(self):
      return ppformat(self.__dict__)
    def __repr__(self):
      return str(self)


  def parse_part_constants(self, from_yaml):
    part_constants = {}
    for name, props in from_yaml.items():
      part_constants[name] = self.PartConstant(name, props)
    return part_constants

  def parse_dsn_variables(self, from_yaml):
    dsn_variables = {}
    for name, props in from_yaml.items():
      dsn_variables[name] = self.DesignVariable(name, props)
    return dsn_variables

  def parse_signals(self, from_yaml):
    signals = {}
    for name in from_yaml:
      signals[name] = self.Signal(name)
    return signals

  def parse_signal_groups(self, from_yaml):
    signal_groups = {}
    for name, props in from_yaml.items():
      signal_groups[name] = self.SignalGroup(name, props)
    return signal_groups   

  def parse_constraints(self, from_yaml):
    constraints = []
    for kind, constraints_dicts in from_yaml.items():
      for name, props in constraints_dicts.items():
        concrete_constraint = Constraint.factory(kind)
        constraints.append(concrete_constraint(name, props))
    return constraints 


  def parse_yaml(self, yaml_file):
    # print('Parsing yaml ' + yaml_file + '...')
    with open(yaml_file, 'r') as f:
      try:
        yaml_dict = yaml.safe_load(f)
      except yaml.YAMLError as exc:
        print(exc)
    # pprint(yaml_dict)
    self.part_constants = self.parse_dsn_variables(yaml_dict['part_constants'])
    self.dsn_variables = self.parse_dsn_variables(yaml_dict['dsn_variables'])
    self.signals = self.parse_signals(yaml_dict['signals'])
    self.signal_groups = self.parse_signal_groups(yaml_dict['signal_groups'])
    self.constraints = self.parse_constraints(yaml_dict['constraints'])
  def gen_constraints(self):
    constraints = []
    for constraint in self.constraints:
      cstr_str = constraint.gen_constraint()
      # print(cstr_str)
      if cstr_str != None:
        cstr_str = self.variable_sub(cstr_str)
        constraints.append(cstr_str)
    return constraints
  def variable_sub(self, raw_constraint):
    constraint = raw_constraint
    for prop in ['part_constants', 'dsn_variables', 'signal_groups', 'signals']:
      constraint = self._variable_sub(constraint, prop)

    return constraint
  def _variable_sub(self, raw_constraint, prop):
    constraint = raw_constraint
    for name, obj in getattr(self,prop).items():
      constraint = constraint.replace('$' + name, str(obj.value))   
    return constraint

# TODO : Delete when tested-ish
if __name__ == '__main__':
  interface = Interface('rgmii')


