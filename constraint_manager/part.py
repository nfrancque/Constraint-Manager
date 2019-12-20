import yaml
from .interface import Interface
from .utils_pkg import ppformat, PART_DIR
from pprint import pprint
from os.path import splitext, join as path_join

class Part:
  """The Part class contains information about a part that interfaces with an FPGA.  A part may have one or more interfaces defined, 
     and must provide all pre-defined part constants for that interface.
  """
  def __init__(self, part_name):
    yaml_file = path_join(PART_DIR, part_name + '.yml')
    self.name = part_name
    self.parse_yaml(yaml_file)
  def __str__(self):
    return ppformat(self.__dict__)
  def __repr__(self):
    return str(self)


  def parse_interface(self, from_yaml):
    """ Parses an interface of this part and returns the properties of that interface
    
    :param from_yaml: dictionary containing all properties for the given interface
    :type from_yaml: dict
    :return: Returns a dictionary of properties for this interface
    :rtype: dict
    """
    interface = {}
    for name, props in from_yaml.items():
      interface[name] = props['value']
    return interface


  def parse_yaml(self, yaml_file):
    """ Parses the given yaml file describing a part into a Part object
    
    :param yaml_file: The filename of the yaml description
    :type yaml_file: string
    """
    self.interfaces = {}
    with open(yaml_file, 'r') as f:
      try:
        yaml_dict = yaml.safe_load(f)
      except yaml.YAMLError as exc:
        print(exc)
    for if_name, props in yaml_dict.items():
      self.interfaces[if_name] = self.parse_interface(props)





