""" Implements a constraint abstraction using an abstract class
implemented by several concrete types.  Given a property dictionary
is designed to generate a constraint string to represent itself.
"""

import logging
from copy import copy

from .utils_pkg import ppformat, update_from_dict

LOGGER = logging.getLogger(__name__)


def get_class_from_string(kind):
    """Util to get a concrete constraint class from a string specifying the
    kind of constraint.

    :param kind: String representing a constraint kind
    :type kind: str
    :return: A concrete Constraint class
    :rtype: Constraint
    """
    if kind == 'generated_clk':
        return GeneratedClockConstraint
    if kind == 'in_max':
        return InputMaxConstraint
    if kind == 'in_min':
        return InputMinConstraint
    if kind == 'out_max':
        return OutputMaxConstraint
    if kind == 'out_min':
        return OutputMinConstraint

    LOGGER.warning('%s is not an implemented constraint.  Try misc?', kind)
    return Constraint


def gen_config_dict():
    """Generates the configuration dictionaries for all types of constraints.

    :return: A nested dictionary for input configuration of constraints.
    :rtype: dict
    """
    return {kind: _gen_config_dict(kind)
            for kind in ('generated_clk', 'in_max')}


def _gen_config_dict(kind):
    """Generates the configuration dictionary for the given constraint kind.

    :param kind: String representing a constraint kind
    :type kind: str
    :return: A dictionary for input configuration of this constraint.
    :rtype: dict
    """
    prop_names = get_class_from_string(kind).prop_names
    return {'test': {prop_name: '' for prop_name in prop_names}}


def factory(kind):
    """Factory to generate a concrete constraint constructor.

    :param kind: The kind of constraint to be created
    :type kind: string
    :return: Returns a concrete class generator to be constructed later.
    :rtype: Class
    """
    return get_class_from_string(kind)


class Constraint:
    """The Constraint class is an abstract class that should never be used
    directly.

    It only defines the interface to a constraint.  Instead, use
    :func:`Constraint.factory` to get a constraint constructor.
    """
    # pylint:disable=unused-argument
    def __init__(self, name, props):
        self.name = name

    def __str__(self):
        ret = {'constraint_type': self.__class__.__name__}
        ret.update(copy(self.__dict__))
        return ppformat(ret)

    def __repr__(self):
        return str(self)

    # pylint:disable=no-self-use
    def gen_constraint(self):
        """Generates the sdc constraint string for this constraint.  No
        variable substitution is performed, here is it expressed purely in
        terms of the inputs.

        :return: Returns a string containing an sdc command to express this constraint.
        :rtype: string
        """
        return None


#pylint:disable=too-few-public-methods
class GeneratedClockConstraint(Constraint):
    """GeneratedClockConstraint class.

    Contains information about an sdc create_generated_clk command
    """
    prop_names = ['clk_name', 'get_src_clk_cmd',
                  'get_dst_clk_cmd', 'divide_by']

    def __init__(self, name, props):
        super().__init__(name, props)
        update_from_dict(props, self, self.prop_names)

    def gen_constraint(self):
        # pylint: disable=no-member
        return (f'create_generated_clock -name {self.clk_name} '
                f'-divide_by {self.divide_by} -source {self.get_src_clk_cmd} '
                f'{self.get_dst_clk_cmd}'
               )

#pylint:disable=too-few-public-methods
class InputMaxConstraint(Constraint):
    """InputMaxConstraint class.

    Contains information about an sdc set_input_delay -max command
    """
    prop_names = ['clk_name', 'equation', 'signal_group', 'get_clk_cmd']

    def __init__(self, name, props):
        super().__init__(name, props)
        update_from_dict(props, self, self.prop_names)

    def gen_constraint(self):
        # pylint: disable=no-member
        return (f'set_input_delay -max {self.equation} '
                f'-clock {self.get_clk_cmd} {self.signal_group}'
               )

#pylint:disable=too-few-public-methods
class InputMinConstraint(Constraint):
    """InputMinConstraint class.

    Contains information about an sdc set_input_delay -min command
    """
    prop_names = ['clk_name', 'equation', 'signal_group', 'get_clk_cmd']

    def __init__(self, name, props):
        super().__init__(name, props)
        update_from_dict(props, self, self.prop_names)

    def gen_constraint(self):
        # pylint: disable=no-member
        return (f'set_input_delay -min {self.equation} '
                f'-clock {self.get_clk_cmd} {self.signal_group}'
               )

#pylint:disable=too-few-public-methods
class OutputMaxConstraint(Constraint):
    """OutputMaxConstraint class.

    Contains information about an sdc set_output_delay -max command
    """
    prop_names = ['clk_name', 'equation', 'signal_group', 'get_clk_cmd']

    def __init__(self, name, props):
        super().__init__(name, props)
        update_from_dict(props, self, self.prop_names)

    def gen_constraint(self):
        # pylint: disable=no-member
        return (f'set_output_delay -max {self.equation} '
                f'-clock {self.get_clk_cmd} {self.signal_group}'
               )

#pylint:disable=too-few-public-methods
class OutputMinConstraint(Constraint):
    """OutputMinConstraint class.

    Contains information about an sdc set_output_delay -min command
    """
    prop_names = ['clk_name', 'equation', 'signal_group', 'get_clk_cmd']

    def __init__(self, name, props):
        super().__init__(name, props)
        update_from_dict(props, self, self.prop_names)

    def gen_constraint(self):
        # pylint: disable=no-member
        return (f'set_output_delay -min {self.equation} '
                f'-clock {self.get_clk_cmd} {self.signal_group}'
               )
