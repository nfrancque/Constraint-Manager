import yaml
from interface import Interface
from part import Part
from utils_pkg import ppformat, DESIGN_DIR
from pprint import pprint
from os.path import splitext, join as path_join
from glob import glob

class Design:
  def __init__(self, yaml_dir):
    self.parse_yamls(yaml_dir)
    # pprint(self, width=1, indent=4)
  def __str__(self):
    return ppformat(self.__dict__)
  def __repr__(self):
    return str(self)


  def parse_interface(self, interface, from_yaml):
    for name, props in from_yaml['dsn_variables'].items():
      interface.dsn_variables[name].value = props['value']
    for name, props in from_yaml['signals'].items():
      interface.signals[name].value = props

    # TODO : Avoid instantiating same interface twice
    part = Part(from_yaml['part'])
    interface.part_constants = part.interfaces[interface.name].part_constants


    return interface


  def parse_yaml(self, yaml_file):
    # print('Parsing yaml ' + yaml_file + '...')

    file_name, ext = splitext(yaml_file)
    name, interface_name = file_name.rsplit('_', 1)
    interface = Interface(interface_name)
    with open(yaml_file, 'r') as f:
      try:
        yaml_dict = yaml.safe_load(f)
      except yaml.YAMLError as exc:
        print(exc)

    self.interfaces.append(self.parse_interface(interface, yaml_dict))


  def parse_yamls(self, yaml_dir):
    self.interfaces = []
    yaml_files = glob(path_join(yaml_dir, '*.yml'))
    for yaml_file in yaml_files:
      self.parse_yaml(yaml_file)

  def gen_constraints(self):
    constraints = []
    for interface in self.interfaces:
      if_constraints = interface.gen_constraints()
      # print(if_constraints)
      constraints.extend(if_constraints)
    return constraints


# TODO : Delete when tested-ish
if __name__ == '__main__':
  design = Design(['dsn1_red_rgmii'])
  constraints = design.gen_constraints()
  print('Final constraints: ' + ppformat(constraints))


