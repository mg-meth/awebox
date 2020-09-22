#
#    This file is part of awebox.
#
#    awebox -- A modeling and optimization framework for multi-kite AWE systems.
#    Copyright (C) 2017-2020 Jochem De Schutter, Rachel Leuthold, Moritz Diehl,
#                            ALU Freiburg.
#    Copyright (C) 2018-2020 Thilo Bronnenmeyer, Kiteswarms Ltd.
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
various structural tools for the vortex model
_python-3.5 / casadi-3.4.5
- author: rachel leuthold, alu-fr 2019-2020
'''

import casadi.tools as cas
from awebox.logger.logger import Logger as awelogger
import awebox.tools.vector_operations as vect_op
from awebox.logger.logger import Logger as awelogger
import awebox.tools.print_operations as print_op

import numpy as np

import pdb

def get_wake_node_position(variables, kite, tip, wake_node):
    coord_name = 'wx_' + str(kite) + '_' + tip + '_' + str(wake_node)

    wx_local = cas.DM_inf((3, 1))
    try:
        wx_local = variables['xd', coord_name]
    except:
        try:
            wx_local = variables['xd'][coord_name]
        except:
            message = 'wake node position is not in expected position wrt variables.'
            awelogger.logger.error(message)
            raise Exception(message)

    return wx_local

def get_wake_node_velocity(variables, kite, tip, wake_node):
    coord_name = 'dwx_' + str(kite) + '_' + tip + '_' + str(wake_node)

    dwx_local = cas.DM_inf((3, 1))
    try:
        dwx_local = variables['xd', coord_name]
    except:
        try:
            dwx_local = variables['xd'][coord_name]
        except:
            message = 'wake node velocity is not in expected position wrt variables.'
            awelogger.logger.error(message)
            raise Exception(message)

    return dwx_local

def get_ring_strength_si(options, variables, kite, ring):

    wg_local = get_ring_strength(variables, kite, ring)

    wg_scale = get_strength_scale(options)
    wg_rescaled = wg_local * wg_scale

    return wg_rescaled

def get_ring_strength(variables, kite, ring):
    coord_name = 'wg_' + str(kite) + '_' + str(ring)

    wg_local = cas.DM_inf((1, 1))
    try:
        wg_local = variables['xl', coord_name]
    except:
        try:
            wg_local = variables['xl'][coord_name]
        except:
            message = 'vortex ring strength is not in expected position wrt variables.'
            awelogger.logger.error(message)
            raise Exception(message)

    return wg_local

def evaluate_symbolic_on_segments_and_sum(filament_fun, segment_list):

    n_filaments = segment_list.shape[1]
    filament_map = filament_fun.map(n_filaments, 'openmp')
    all = filament_map(segment_list)

    total = cas.sum2(all)

    return total

def get_strength_scale(options):
    gamma_scale = options['aero']['vortex']['gamma_scale']
    return gamma_scale

def append_bounds(g_bounds, fix):

    if (type(fix) == type([])) and fix == []:
        return g_bounds

    else:

        fix_shape = (1,1)
        try:
            fix_shape = fix.shape
        except:
            message = 'An attempt to append bounds was passed a vortex-related constraint with an unaccepted structure.'
            awelogger.logger.error(message)

        g_bounds['ub'].append(cas.DM.zeros(fix_shape))
        g_bounds['lb'].append(cas.DM.zeros(fix_shape))

        return g_bounds

def get_vortex_verification_mu_vals():

    radius = 155.77
    b_ref = 68.

    varrho = radius / b_ref

    mu_center_by_exterior = varrho / (varrho + 0.5)
    mu_min_by_exterior = (varrho - 0.5) / (varrho + 0.5)
    mu_max_by_exterior = 1.

    mu_min_by_path = (varrho - 0.5) / varrho
    mu_max_by_path = (varrho + 0.5) / varrho
    mu_center_by_path = 1.

    mu_vals = {}
    mu_vals['mu_center_by_exterior'] = mu_center_by_exterior
    mu_vals['mu_min_by_exterior'] = mu_min_by_exterior
    mu_vals['mu_max_by_exterior'] = mu_max_by_exterior
    mu_vals['mu_min_by_path'] = mu_min_by_path
    mu_vals['mu_max_by_path'] = mu_max_by_path
    mu_vals['mu_center_by_path'] = mu_center_by_path

    return mu_vals
