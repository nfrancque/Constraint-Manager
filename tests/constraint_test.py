import pytest
from constraint_manager import constraint


def test_constraint():
	cstr_factory = constraint.Constraint.factory('blah')
	cstr = cstr_factory('test', None)
	assert type(cstr) is constraint.UnimplementedConstraint