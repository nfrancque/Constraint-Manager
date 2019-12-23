from .interface import gen_part_config_dict
from .utils_pkg import get_path_by_name, ppformat, read_yaml


def gen_config_dict(interfaces):
    """ Generates the configuration dictionary for any part

    :param interfaces: A list of interfaces the part will be expected to implement
    :type interfaces: list
    :return: Returns the configuration dictionary for a part implementing these interfaces
    :rtype: dict
    """
    ret = {interface_name: gen_part_config_dict(
        interface_name) for interface_name in interfaces}
    for interface_name, interface in ret.items():
        for _, prop in interface.items():
            prop['value'] = prop['default']
    return ret


class Part:
    """The Part class contains information about a part that interfaces with an FPGA.  A part may have one or more interfaces defined,
         and must provide all pre-defined part constants for that interface.
    """

    def __init__(self, part_name):
        yaml_file = get_path_by_name('parts', part_name)
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
        yaml_dict = read_yaml(yaml_file)
        for if_name, props in yaml_dict.items():
            self.interfaces[if_name] = self.parse_interface(props)
