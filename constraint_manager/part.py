import yaml
from .interface import Interface
from .utils_pkg import ppformat, PART_DIR
from pprint import pprint
from os.path import splitext, join as path_join

class Part:
  def __init__(self, part_name):
    yaml_file = path_join(PART_DIR, part_name + '.yml')
    self.parse_yaml(yaml_file)
    # pprint(self, width=1, indent=4)
  def __str__(self):
    return ppformat(self.__dict__)
  def __repr__(self):
    return str(self)


  def parse_interface(self, if_name, from_yaml):
    interface = Interface(if_name)
    for name, props in from_yaml.items():
      interface.part_constants[name].value = props['value']
    return interface


  def parse_yaml(self, yaml_file):
    # print('Parsing yaml ' + yaml_file + '...')
    self.interfaces = {}
    with open(yaml_file, 'r') as f:
      try:
        yaml_dict = yaml.safe_load(f)
      except yaml.YAMLError as exc:
        print(exc)
    for if_name, props in yaml_dict.items():
      self.interfaces[if_name] = self.parse_interface(if_name, props)




# TODO : Delete when tested-ish
if __name__ == '__main__':
  design = Part('rgmii_part_123')


