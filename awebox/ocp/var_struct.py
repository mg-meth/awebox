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
'''
keep the variable construction separate,
so that non-sequential code can be used non-sequentially
python-3.5 / casadi-3.4.5
- authors: elena malz 2016
           rachel leuthold, jochem de schutter alu-fr 2017-20
'''

import casadi.tools as cas
import awebox.tools.struct_operations as struct_op
import awebox.ocp.collocation as collocation



def setup_nlp_v(nlp_numerics_options, model, Collocation=None):

    # extract necessary inputs
    variables_dict = model.variables_dict
    nk = nlp_numerics_options['n_k']

    # check if phase fix and adjust theta accordingly
    if nlp_numerics_options['phase_fix']:
        theta = get_phase_fix_theta(variables_dict)
    else:
        theta = variables_dict['theta']

    # define interval struct entries for controls and states
    entry_tuple = (
        cas.entry('xd', repeat = [nk+1], struct = variables_dict['xd']),
        )

    # add additional variables according to provided options
    if nlp_numerics_options['discretization'] == 'direct_collocation':

        if nlp_numerics_options['collocation']['u_param'] == 'zoh':
            entry_tuple += (
                cas.entry('u',  repeat = [nk],   struct = variables_dict['u']),
            )

        # add algebraic variables at interval except for radau case
        if nlp_numerics_options['collocation']['scheme'] != 'radau':
            if nlp_numerics_options['lift_xddot']:
                entry_tuple += (
                    cas.entry('xddot', repeat = [nk], struct= variables_dict['xddot']), # depends on implementation (e.g. not present for radau collocation)
                )
            if nlp_numerics_options['lift_xa']:
                entry_tuple += (cas.entry('xa', repeat = [nk],   struct= variables_dict['xa']),) # depends on implementation (e.g. not present for radau collocation)
                if 'xl' in list(variables_dict.keys()):
                    entry_tuple += (cas.entry('xl', repeat = [nk],   struct= variables_dict['xl']),)  # depends on implementation (e.g. not present for radau collocation)

        # add collocation node variables
        if Collocation is None:
            message = 'a None instance of Collocation was passed to the NLP variable structure generator'
            raise Exception(message)

        d = nlp_numerics_options['collocation']['d'] # interpolating polynomial order
        coll_var = Collocation.get_collocation_variables_struct(variables_dict, nlp_numerics_options['collocation']['u_param'])
        entry_tuple += (cas.entry('coll_var', struct = coll_var, repeat= [nk,d]),)

    elif nlp_numerics_options['discretization'] == 'multiple_shooting':

        entry_tuple += (
            cas.entry('u',  repeat = [nk],   struct = variables_dict['u']),
        )

        # add slack variables for inequalities
        if nlp_numerics_options['slack_constraints'] == True and model.constraints_dict['inequality']:
            entry_tuple += (cas.entry('us',  repeat = [nk],   struct = model.constraints_dict['inequality']),)

        # multiple shooting: add algebraic variables at interval if lifted
        if nlp_numerics_options['lift_xddot']:
            entry_tuple += (
                cas.entry('xddot', repeat = [nk], struct= variables_dict['xddot']), # depends on implementation (e.g. not present for radau collocation)
            )
        if nlp_numerics_options['lift_xa']:
            entry_tuple += (cas.entry('xa', repeat = [nk],   struct= variables_dict['xa']),) # depends on implementation (e.g. not present for radau collocation)
            if 'xl' in list(variables_dict.keys()):
                entry_tuple += (cas.entry('xl', repeat = [nk],   struct= variables_dict['xl']),)  # depends on implementation (e.g. not present for radau collocation)

    # add global entries
    # when the global variables are before the discretized variables, it leads to prettier kkt matrix spy plots
    entry_list = [
        cas.entry('theta', struct = theta),
        cas.entry('phi',   struct = model.parameters_dict['phi']),
        cas.entry('xi',    struct = get_xi_struct()),
        entry_tuple
    ]

    # generate structure
    V = cas.struct_symMX(entry_list)

    return V

def get_phase_fix_theta(variables_dict):

    entry_list = []
    for name in list(variables_dict['theta'].keys()):
        if name == 't_f':
            entry_list.append(cas.entry('t_f', shape = (2,1)))
        else:
            entry_list.append(cas.entry(name, shape = variables_dict['theta'][name].shape))

    theta = cas.struct_symSX(entry_list)

    return theta

def get_xi_struct():
    xi = cas.struct_symMX([(cas.entry('xi_0'), cas.entry('xi_f'))])

    return xi
