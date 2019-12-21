import yaml
from .constraint import Constraint, gen_config_dict as constraint_gen_config_dict
from .utils_pkg import ppformat, get_path_by_name
from pprint import pprint
from os.path import join as path_join


def gen_part_config_dict(interface_name):
  interface = Interface(interface_name)
  return {k : v.__dict__ for (k, v) in interface.part_constants.items()}

def gen_dsn_variables_config_dict(interface_name):
  interface = Interface(interface_name)
  return {k : v.__dict__ for (k, v) in interface.dsn_variables.items()}

def gen_signals_config_dict(interface_name):
  interface = Interface(interface_name)
  return {k : v.__dict__ for (k, v) in interface.signals.items()}


def gen_config_dict():


  ret  = {}
  for prop in ('part_constants', 'dsn_variables'):
    ret[prop] = {'example_name' : {

      'desc' : 'Some description',
      'default' : 0
    }
  }

  ret['signals'] = ['some_signal']
  ret['signal_groups'] = {
    'signal_group' : 'signal_names'
  }

  ret['constraints'] = constraint_gen_config_dict()


  return ret


class Interface:
  """ The Interface class defines a protocol interface to a part (RGMII, SPI, etc.).  It contains attributes to help map an interface to constraints.
    
  """
  def __init__(self, if_name):
    yaml_file = get_path_by_name('interfaces', if_name)
    self.parse_yaml(yaml_file)
    self.name = if_name
    # pprint(self, width=1, indent=4)
  def __str__(self):
    return ppformat(self.__dict__)
  def __repr__(self):
    return str(self)

  class PartConstant:
    """ The PartConstant class contains information about values that are expected to be constant in this interface for any given part we are interfacing with.
        We can therefore reference a part from the repository and not require the user to input those values to generate the constraint
    """

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
    """ The DesignVariable class contains information about values expected to vary for each design that implements this interface.  
    """
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
    """ The SignalGroup class specifies a mapping of generic group names for this interface to actual groups of signals in the design to be able to generically specify
        the constraint equation in terms of its groups.    
    """
    def __init__(self, name, props):
      self.name  = name
      self.value = props
    def __str__(self):
      return ppformat(self.__dict__)
    def __repr__(self):
      return str(self)

  class Signal:
    """ The Signal class specifies a mapping of generic signal names for this interface to actual signals in the design to be able to generically specify
        the constraint equation in terms of its signals.    
    """
    def __init__(self, name):
      self.name        = name
      self.value       = None
    def __str__(self):
      return ppformat(self.__dict__)
    def __repr__(self):
      return str(self)


  def parse_part_constants(self, from_yaml):
    """ Parses the part constants of this interface.
    
    :param from_yaml: A nested dictionary mapping part constant names to their information.  See :class:`constraint_manager.Interface.PartConstant for props formatting.
    :type from_yaml: dict
    :return: Returns a dictionary of PartConstant variables mapped by name
    :rtype: dict
    """
    part_constants = {}
    for name, props in from_yaml.items():
      part_constants[name] = self.PartConstant(name, props)
    return part_constants

  def parse_dsn_variables(self, from_yaml):
    """ Parses the part constants of this interface.
    
    :param from_yaml: A nested dictionary mapping design variables to their information.  See :class:`constraint_manager.Interface.DesignVariable for props formatting.
    :type from_yaml: dict
    :return: Returns a dictionary of DesignVariable variables mapped by name
    :rtype: dict
    """
    dsn_variables = {}
    for name, props in from_yaml.items():
      dsn_variables[name] = self.DesignVariable(name, props)
    return dsn_variables

  def parse_signals(self, from_yaml):
    """ Parses the signals of this interface.
    
    :param from_yaml: A nested dictionary mapping signals to their information.  See :class:`constraint_manager.Interface.Signal for props formatting.
    :type from_yaml: dict
    :return: Returns a dictionary of Signal variables mapped by name
    :rtype: dict
    """
    signals = {}
    for name in from_yaml:
      signals[name] = self.Signal(name)
    return signals

  def parse_signal_groups(self, from_yaml):
    """ Parses the signal groups of this interface.
    
    :param from_yaml: A nested dictionary mapping signal groups to their information.  See :class:`constraint_manager.Interface.SignalGroupo for props formatting.
    :type from_yaml: dict
    :return: Returns a dictionary of SignalGroup variables mapped by name
    :rtype: dict
    """
    signal_groups = {}
    for name, props in from_yaml.items():
      signal_groups[name] = self.SignalGroup(name, props)
    return signal_groups   

  def parse_constraints(self, from_yaml):
    """ Parses the signals of this interface.
    
    :param from_yaml: A nested dictionary mapping kinds of constraints->concrete constraint type, which is itself a dictionary of constraints by name.  See :class:`constraint_manager.Interface.Signal for props formatting.
    :type from_yaml: dict
    :return: Returns a dictionary of Constraint variables mapped by name
    :rtype: dict
    """
    constraints = []
    for kind, constraints_dicts in from_yaml.items():
      for name, props in constraints_dicts.items():
        concrete_constraint = Constraint.factory(kind)
        constraints.append(concrete_constraint(name, props))
    return constraints 


  def parse_yaml(self, yaml_file):
    """ Parses the yaml file for this interface.
    
    :param yaml_file: The filename of the yaml file specifying this interface
    :type from_yaml: str
    """
    with open(yaml_file, 'r') as f:
      try:
        yaml_dict = yaml.safe_load(f)
      except yaml.YAMLError as exc:
        LOGGER.info(exc)
    self.part_constants = self.parse_part_constants(yaml_dict['part_constants'])
    self.dsn_variables = self.parse_dsn_variables(yaml_dict['dsn_variables'])
    self.signals = self.parse_signals(yaml_dict['signals'])
    self.signal_groups = self.parse_signal_groups(yaml_dict['signal_groups'])
    self.constraints = self.parse_constraints(yaml_dict['constraints'])
  def gen_constraints(self):
    """ Generates all constraints for this interface.  Variable subsitution is performed as per :func:`constraint_manager.Interface.variable_sub`
        Expressed as a list of constraint lines to later be put into a string for export.
    
    :return: Returns a list of strings each containing a valid sdc constraint
    :rtype: dict
    """
    constraints = []
    for constraint in self.constraints:
      cstr_str = constraint.gen_constraint()
      if cstr_str != None:
        cstr_str = self.variable_sub(cstr_str)
        constraints.append(cstr_str)
    return constraints
  def variable_sub(self, raw_constraint):
    """ Variable substitution is performed by searching part_constants, dsn_variables, signal_groups, 
        and signals (in that order) and mapping $[var_name] for self.var_type[var_name].value.
        Where var_type is one of the above mentioned attributes, and var_name is any key 
        in their dictionaries.
    :param raw_constraint: The string containing the sdc constraint before variable substitution.
    :type raw_constraint: str
    :return: Returns a string after all variable substitutions have been performed.
    :rtype: dict
    """
    constraint = raw_constraint
    for prop in ['part_constants', 'dsn_variables', 'signal_groups', 'signals']:
      constraint = self._variable_sub(constraint, prop)

    return constraint
  def _variable_sub(self, raw_constraint, prop):
    """ Performs the actual variable substitution on the constraint for a given instance attribute.
    :param raw_constraint: The string containing the sdc constraint before variable substitution.
    :type raw_constraint: str
    :param prop: A string matching the attribute name of this instance to look in for variable substitution.
    :type prop: str
    :return: Returns a string after all variable substitutions have been performed.
    :rtype: dict
    """
    constraint = raw_constraint
    for name, obj in getattr(self,prop).items():
      constraint = constraint.replace('$' + name, str(obj.value))   
    return constraint




