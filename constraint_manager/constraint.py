import logging
from copy import copy

from .utils_pkg import ppformat, update_from_dict

LOGGER = logging.getLogger(__name__)


def get_class_from_string(kind):
    """ Util to get a concrete constraint class from a string specifying the kind of constraint.

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

    LOGGER.warning(f'{kind} is not an implemented constraint.  Try misc?')
    return UnimplementedConstraint


def gen_config_dict():
    """ Generates the configuration dictionaries for all types of constraints.

    :return: A nested dictionary representing the structure required for input configuration of constraints.
    :rtype: dict
    """
    return {kind: _gen_config_dict(kind)
            for kind in ('generated_clk', 'in_max')}


def _gen_config_dict(kind):
    """ Generates the configuration dictionary for the given constraint kind

    :param kind: String representing a constraint kind
    :type kind: str
    :return: A dictionary representing the structure required for input configuration of this constraint.
    :rtype: dict
    """
    prop_names = get_class_from_string(kind).prop_names
    return {'test': {prop_name: '' for prop_name in prop_names}}


def factory(kind):
    """ Factory to generate a concrete constraint constructor.

    :param kind: The kind of constraint to be created
    :type kind: string
    :return: Returns a concrete class generator to be constructed later.
    :rtype: Class

    """
    return get_class_from_string(kind)


class Constraint:
    """ The Constraint class is an abstract class that should never be used directly.
            It only defines the interface to a constraint.  Instead, use :func:`Constraint.factory`
            to get a constraint constructor.

    """

    def __init__(self, name, props):
        self.name = name

    def __str__(self):
        ret = {'constraint_type': self.__class__.__name__}
        ret.update(copy(self.__dict__))
        return ppformat(ret)

    def __repr__(self):
        return str(self)

    def gen_constraint(self):
        """ Generates the sdc constraint string for this constraint.  No variable
                substitution is performed, here is it expressed purely in terms of the inputs

                :return: Returns a string containing an sdc command to express this constraint.
                :rtype: string

        """
        return None


class UnimplementedConstraint(Constraint):
    """ Unimplemented Constraint class.  Ignored in final design constraints, used mostly as a placeholder.
    """
    prop_names = []

    def __init__(self, name, props):
        super().__init__(name, props)


class GeneratedClockConstraint(Constraint):
    """ GeneratedClockConstraint class.  Contains information about an sdc create_generated_clk command

    """
    prop_names = ['clk_name', 'get_src_clk_cmd',
                  'get_dst_clk_cmd', 'divide_by']

    def __init__(self, name, props):
        super().__init__(name, props)
        update_from_dict(props, self, self.prop_names)

    def gen_constraint(self):
        return f'create_generated_clock -name {self.clk_name} -divide_by {self.divide_by} -source {self.get_src_clk_cmd} {self.get_dst_clk_cmd}'


class InputMaxConstraint(Constraint):
    """ InputMaxConstraint class.  Contains information about an sdc set_input_delay -max command

    """
    prop_names = ['clk_name', 'equation', 'signal_group', 'get_clk_cmd']

    def __init__(self, name, props):
        super().__init__(name, props)
        update_from_dict(props, self, self.prop_names)

    def gen_constraint(self):

        return f'set_input_delay -max {self.equation} -clock {self.get_clk_cmd} {self.signal_group}'


class InputMinConstraint(Constraint):
    """ InputMinConstraint class.  Contains information about an sdc set_input_delay -min command

    """
    prop_names = ['clk_name', 'equation', 'signal_group', 'get_clk_cmd']

    def __init__(self, name, props):
        super().__init__(name, props)
        update_from_dict(props, self, self.prop_names)

    def gen_constraint(self):

        return f'set_input_delay -min {self.equation} -clock {self.get_clk_cmd} {self.signal_group}'


class OutputMaxConstraint(Constraint):
    """ OutputMaxConstraint class.  Contains information about an sdc set_output_delay -max command

    """
    prop_names = ['clk_name', 'equation', 'signal_group', 'get_clk_cmd']

    def __init__(self, name, props):
        super().__init__(name, props)
        update_from_dict(props, self, self.prop_names)

    def gen_constraint(self):

        return f'set_output_delay -max {self.equation} -clock {self.get_clk_cmd} {self.signal_group}'


class OutputMinConstraint(Constraint):
    """ OutputMinConstraint class.  Contains information about an sdc set_output_delay -min command

    """
    prop_names = ['clk_name', 'equation', 'signal_group', 'get_clk_cmd']

    def __init__(self, name, props):
        super().__init__(name, props)
        update_from_dict(props, self, self.prop_names)

    def gen_constraint(self):

        return f'set_output_delay -min {self.equation} -clock {self.get_clk_cmd} {self.signal_group}'
