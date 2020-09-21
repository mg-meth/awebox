#
#    This file is part of awebox.
#
#    awebox -- A modeling and optimization framework for multi-kite AWE systems.
#    Copyright (C) 2017-2020 Jochem De Schutter, Rachel Leuthold, Moritz Diehl,
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
"""
flow functions for the vortex based model
_python-3.5 / casadi-3.4.5
- author: rachel leuthold, alu-fr 2020
"""

import awebox.mdl.aero.induction_dir.general_dir.flow as general_flow
import awebox.mdl.aero.induction_dir.vortex_dir.biot_savart as biot_savart
import awebox.mdl.aero.induction_dir.vortex_dir.tools as vortex_tools

import awebox.mdl.aero.induction_dir.general_dir.geom as general_geom
import awebox.mdl.aero.induction_dir.actuator_dir.flow as actuator_flow
import awebox.mdl.aero.induction_dir.vortex_dir.filament_list as vortex_filament_list
import awebox.tools.print_operations as print_op

import awebox.tools.vector_operations as vect_op

import casadi.tools as cas
import awebox.mdl.aero.induction_dir.tools_dir.unit_normal as unit_normal
import pdb
#
def get_induced_velocity_at_kite(options, filament_list, variables, architecture, kite_obs, n_hat=None):
    x_obs = variables['xd']['q' + str(kite_obs) + str(architecture.parent_map[kite_obs])]
    u_ind = get_induced_velocity_at_observer(options, filament_list, x_obs, n_hat=n_hat)
    return u_ind


def get_induced_velocity_at_observer(options, filament_list, x_obs, n_hat=None):

    filament_list = vortex_filament_list.append_observer_to_list(filament_list, x_obs)

    include_normal_info = False
    try:
        this_will_fail_if_n_hat_is_None = n_hat.shape
        include_normal_info = True
        filament_list = vortex_filament_list.append_normal_to_list(filament_list, n_hat)
    except:
        32.0

    u_ind = make_symbolic_filament_and_sum(options, filament_list, include_normal_info)
    return u_ind


def get_induction_factor_at_kite(options, filament_list, wind, variables, parameters, architecture, kite_obs, n_hat=vect_op.xhat()):

    x_obs = variables['xd']['q' + str(kite_obs) + str(architecture.parent_map[kite_obs])]

    parent = architecture.parent_map[kite_obs]
    u_zero_vec = actuator_flow.get_uzero_vec(options, wind, parent, variables, parameters, architecture)
    u_zero = vect_op.smooth_norm(u_zero_vec)

    a_calc = get_induction_factor_at_observer(options, filament_list, x_obs, u_zero, n_hat=n_hat)

    return a_calc


def get_induction_factor_at_observer(options, filament_list, x_obs, u_zero, n_hat=vect_op.xhat()):
    u_ind = get_induced_velocity_at_observer(options, filament_list, x_obs, n_hat=n_hat)
    a_calc = -1. * u_ind / u_zero
    return a_calc


def make_symbolic_filament_and_sum(options, filament_list, include_normal_info=False):

    epsilon = options['induction']['vortex_epsilon']

    # define the symbolic function
    n_symbolics = filament_list.shape[0]
    seg_data_sym = cas.SX.sym('seg_data_sym', (n_symbolics, 1))

    if include_normal_info:
        filament_sym = biot_savart.filament_normal(seg_data_sym, epsilon=epsilon)
    else:
        filament_sym = biot_savart.filament(seg_data_sym, epsilon=epsilon)

    filament_fun = cas.Function('filament_fun', [seg_data_sym], [filament_sym])

    # evaluate the symbolic function
    u_ind = vortex_tools.evaluate_symbolic_on_segments_and_sum(filament_fun, filament_list)

    return u_ind
