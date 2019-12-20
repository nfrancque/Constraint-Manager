import pytest
from constraint_manager.interface import Interface
from helpers.utils import *



interface = Interface('rgmii')

def test_interface_props():
	assert(interface.name == 'rgmii')
	assert(type(interface) is Interface)
	for signal_group in interface.signal_groups.values():
		assert(type(signal_group) is Interface.SignalGroup)
	for part_constant in interface.part_constants.values():
		assert(type(part_constant) is Interface.PartConstant)
	for dsn_variable in interface.dsn_variables.values():
		assert(type(dsn_variable) is Interface.DesignVariable)
	for signal in interface.signals.values():
		assert(type(signal) is Interface.Signal)




