#
#    This file is part of awebox.
#
#    awebox -- A modeling and optimization framework for multi-kite AWE systems.
#    Copyright (C) 2017-2019 Jochem De Schutter, Rachel Leuthold, Moritz Diehl,
#                            ALU Freiburg.
#    Copyright (C) 2018-2019 Thilo Bronnenmeyer, Kiteswarms Ltd.
#    Copyright (C) 2016      Elena Malz, Sebastien Gros, Chalmers UT.
#
#    awebox is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 3 of the License, or (at your option) any later version.
#
#    awebox is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with awebox; if not, write to the Free Software Foundation,
#    Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#
###################################
# Class Model contains physics description necessary to model the tree-structure multi-kite system
###################################

from . import atmosphere
from . import wind
from . import system
from . import dynamics as dyn

import awebox.tools.print_operations as print_op
import time
from . import dae
from awebox.logger.logger import Logger as awelogger


class Model(object):
    def __init__(self):
        self.__status = 'Model not yet built.'
        self.__outputs = None
        self.__type = 'Model'
        self.__winch = None
        """ ### self.__winch """

    def build(self, options, winch, architecture):
        """ ### winch """
        awelogger.logger.info('Building model...')

        if self.__status == 'I am a model.':
            awelogger.logger.info('Model already built.')
            return None
        else:
            self.__timings = {}
            timer = time.time()
            self.__architecture = architecture
            self.__generate_system_parameters(options, winch)
            """ ### winch """
            self.__generate_atmosphere(options['atmosphere'])
            self.__generate_wind(options['wind'])
            self.__generate_system_dynamics(options, winch)
            """ ### winch """
            self.__generate_variable_bounds(options)
            self.__generate_parameter_bounds(options)
            self.__generate_constraints(options)
            self.__options = options

            self.__winch = winch
            """ ### self.__winch """

            self.__timings['overall'] = time.time()-timer

            self.__status = 'I am a model.'
            awelogger.logger.info('Model built.')
            awelogger.logger.info('Model construction time: %s', print_op.print_single_timing(self.__timings['overall']))
            awelogger.logger.info('')

    def __generate_system_parameters(self, options, winch):
        """ ### winch """

        self.__parameters, self.__parameters_dict = system.generate_system_parameters(options, self.__architecture)

        return None

    def __generate_atmosphere(self, atmosphere_options):

        awelogger.logger.info('generate atmosphere...')

        self.__atmos = atmosphere.Atmosphere(atmosphere_options, self.__parameters)

        return None

    def __generate_wind(self, wind_model_options):

        awelogger.logger.info('generate wind...')

        self.__wind = wind.Wind(wind_model_options, self.__parameters)
        self.__wind_options = wind_model_options

        return None


    def __generate_system_dynamics(self,options, winch):
        """ winch ### """
        awelogger.logger.info('generate system dynamics...')
        [variables,
        variables_dict,
        scaling,
        dynamics,
        outputs,
        outputs_fun,
        outputs_dict,
        constraint_out,
        constraint_out_fun,
        holonomic_fun,
        integral_outputs,
        integral_outputs_fun,
        integral_scaling] = dyn.make_dynamics(options, winch, self.__atmos, self.__wind, self.__parameters, self.__architecture)
        """ ### winch """

        self.__kite_dof = options['kite_dof']
        self.__kite_geometry = {} #options['geometry']

        self.__variables = variables
        self.__variables_dict = variables_dict
        self.__scaling = scaling
        self.__dynamics = dynamics
        self.__outputs = outputs
        self.__outputs_fun = outputs_fun
        self.__outputs_dict = outputs_dict
        self.__constraint_out = constraint_out
        self.__constraint_out_fun = constraint_out_fun
        self.__holonomic_fun = holonomic_fun
        self.__integral_outputs = integral_outputs
        self.__integral_outputs_fun = integral_outputs_fun
        self.__integral_scaling = integral_scaling

        self.__output_components = [outputs_fun, outputs_dict]

        return None

    def get_dae(self):
        """Generate DAE object for casadi integrators, rootfinder,...
        """

        awelogger.logger.info('generate dae object')
        model_dae = dae.Dae(self.__variables, self.__parameters, self.__dynamics, self.__integral_outputs_fun)
        model_dae.build_rootfinder()

        return model_dae

    def __generate_variable_bounds(self, options):

        awelogger.logger.info('generate variable bounds...')

        # define bounds for all system variables (except pfix) in SI units
        variable_bounds = system.define_bounds(options['system_bounds'],
                                               self.__variables)
        # scale bounds for optimization solver
        self.__variable_bounds = system.scale_bounds(variable_bounds,
                                                     self.__scaling)
        return None

    def __generate_parameter_bounds(self,options):

        awelogger.logger.info('generate parameter bounds...')

        # define bounds for variable optimization parameters
        param_bounds = {}
        for name in list(self.__parameters_dict['phi'].keys()):
            param_bounds[name] = {}

            param_bounds[name]['lb'] = 0.
            param_bounds[name]['ub'] = 1.

        self.__parameter_bounds = param_bounds
        return None

    def __generate_constraints(self, options):

        awelogger.logger.info('generate constraints..')

        constraints, constraints_fun, constraints_dict = dyn.generate_constraints(
                           options, self.__variables,self.__parameters,self.__constraint_out(self.__constraint_out_fun(self.__variables, self.__parameters)))

        self.__constraints = constraints
        self.__constraints_fun = constraints_fun
        self.__constraints_dict = constraints_dict

        return None


    @property
    def kite_geometry(self):
        return self.__kite_geometry

    @kite_geometry.setter
    def kite_geometry(self, geometry_options):
        self.__kite_geometry = geometry_options
        return None

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        awelogger.logger.warning('Cannot set status object.')

    @property
    def outputs(self):
        return self.__outputs

    @outputs.setter
    def outputs(self, value):
        awelogger.logger.warning('Cannot set outputs object.')

    @property
    def outputs_fun(self):
        return self.__outputs_fun

    @outputs_fun.setter
    def outputs_fun(self, value):
        awelogger.logger.warning('Cannot set outputs_fun object.')

    @property
    def outputs_dict(self):
        return self.__outputs_dict

    @outputs_dict.setter
    def outputs_dict(self, value):
        awelogger.logger.warning('Cannot set outputs_dict object.')

    @property   #todo: write setters
    def variables(self):
        return self.__variables

    @property
    def variable_bounds(self):
        return self.__variable_bounds

    @property
    def parameters(self):
        return self.__parameters

    @property
    def parameters_dict(self):
        return self.__parameters_dict

    @property
    def parameter_bounds(self):
        return self.__parameter_bounds

    @property
    def constraints(self):
        return self.__constraints

    @property
    def constraints_dict(self):
        return self.__constraints_dict

    @property
    def constraints_fun(self):
        return self.__constraints_fun

    @property
    def scaling(self):
        return self.__scaling

    @property
    def dynamics(self):
        return self.__dynamics

    @property
    def architecture(self):
        return self.__architecture

    @property
    def integral_outputs(self):
        return self.__integral_outputs

    @integral_outputs.setter
    def integral_outputs(self, value):
        awelogger.logger.warning('Cannot set integral_outputs object.')

    @property
    def integral_outputs_fun(self):
        return self.__integral_outputs_fun

    @integral_outputs_fun.setter
    def integral_outputs_fun(self, value):
        awelogger.logger.warning('Cannot set integral_outputs_fun object.')

    @property
    def integral_scaling(self):
        return self.__integral_scaling

    @integral_scaling.setter
    def integral_scaling(self, value):
        awelogger.logger.warning('Cannot set integral_scaling object.')

    @property
    def atmos(self):
        return self.__atmos

    @atmos.setter
    def atmos(self, value):
        awelogger.logger.warning('Cannot set atmos object.')

    @property
    def wind(self):
        return self.__wind

    @wind.setter
    def wind(self, value):
        awelogger.logger.warning('Cannot set wind object.')

    @property
    def wind_options(self):
        return self.__wind_options

    @wind_options.setter
    def wind_options(self, value):
        awelogger.logger.warning('Cannot set wind_options object.')

    @property
    def variables_dict(self):
        return self.__variables_dict

    @variables_dict.setter
    def variables_dict(self, value):
        awelogger.logger.warning('Cannot set variables_dict object.')

    @property
    def kite_dof(self):
        return self.__kite_dof

    @kite_dof.setter
    def kite_dof(self, value):
        awelogger.logger.warning('Cannot set kite_dof object.')

    @property
    def timings(self):
        return self.__timings

    @timings.setter
    def timings(self, value):
        awelogger.logger.warning('Cannot set timings object.')

    @property
    def holonomic_fun(self):
        return self.__holonomic_fun

    @holonomic_fun.setter
    def holonomic_fun(self, value):
        awelogger.logger.warning('Cannot set holonomic_fun object.')

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        awelogger.logger.warning('Cannot set type object.')

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        awelogger.logger.warning('Cannot set options object.')
