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
#    vversion 3 of the License, or (at your option) any later version.
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
Collection of trial functions
python version 3.5 / casadi 3.4.5
- author:
    Thilo Bronnenmeyer, kiteswarms 2018
    Jochem De Schutter, alu-fr 2018
"""

import csv
import collections
import awebox.tools.vector_operations as vect_op
import awebox.viz.tools as tools
import casadi.tools as cas
import numpy as np
import awebox.tools.struct_operations as struct_op
from awebox.logger.logger import Logger as awelogger

def generate_trial_data_csv(trial, name, freq, rotation_representation):
    """
    Generate an output .csv file containing all information from the trial
    :param trial: trial whose data is to be stored in the .csv
    :param name: name of the .csv
    :param freq: sampling frequency for output
    :return: None
    """

    # get dictionaries
    plot_dict = interpolate_data(trial, freq)
    write_csv_dict = init_write_csv_dict(plot_dict)

    # write into .csv
    with open(name + '.csv', 'w') as point_cloud:
        pcdw = csv.DictWriter(point_cloud, delimiter=',', fieldnames=write_csv_dict)
        pcdw.writeheader()
        for k in range(plot_dict['time_grids']['ip'].shape[0]):
            write_data_row(pcdw, plot_dict, write_csv_dict, plot_dict['time_grids']['ip'], k, rotation_representation)

    return None

def init_write_csv_dict(plot_dict):
    """
    Initialize dictionary used to write into .csv
    :param plot_dict: data dictionary containing all data for the .csv with the necessary structure
    :return: Empty dictionary used to write into .csv
    """

    # initialize ordered dict
    write_csv_dict = collections.OrderedDict()

    # create empty entries corresponding to the structure of plot_dict
    for variable_type in ['xd', 'xa', 'xl', 'u', 'outputs']:
        for variable in list(plot_dict[variable_type].keys()):

            # check for sub_variables in case there are some
            if type(plot_dict[variable_type][variable]) is dict:
                for sub_variable in list(plot_dict[variable_type][variable].keys()):
                    variable_length = len(plot_dict[variable_type][variable][sub_variable])
                    for index in range(variable_length):
                        write_csv_dict[variable_type + '_' + variable + '_' + sub_variable + '_' + str(index)] = None

            # continue without sub_variables in case there are none
            else:
                variable_length = len(plot_dict[variable_type][variable])
                for index in range(variable_length):
                    write_csv_dict[variable_type + '_' + variable + '_' + str(index)] = None

    # add time stamp
    write_csv_dict['time'] = None

    # add architecture information
    write_csv_dict['nodes'] = None
    write_csv_dict['parent'] = None
    write_csv_dict['kites'] = None
    write_csv_dict['cross_tether'] = None

    return write_csv_dict

def interpolate_data(trial, freq):
    """
    Interpolate data trial data with a given sampling frequency
    :param trial: trial whose data is to be interpolated
    :param freq: sampling frequency
    :return: dictionary with trial data, interpolation time grid
    """

    # extract info
    tf = trial.optimization.V_final['theta', 't_f', 0]  # TODO: phase fix tf

    # number of interpolating points
    N = int(freq * tf)

    # recalibrate plot_dict
    plot_dict = trial.visualization.plot_dict
    V_plot = trial.optimization.V_opt

    V_final = trial.optimization.V_final
 #   V_plot = V_final
 #   periodicity = V_final['xd', 0, 'v_sq'] - V_final['xd', -1, 'v_sq']
   # print('v_sq_diff')
  #  print(periodicity)
 #   periodicity = V_final['xd', 0, 'v_sd'] - V_final['xd', -1, 'v_sd']
 #   print('v_sd_diff')
#    print(periodicity)
   # periodicity = V_final['xd', 0, 'i_sq'] - V_final['xd', -1, 'i_sq']
  #  print('i_sq_diff')
#    print(periodicity)
  #  periodicity = V_final['xd', 0, 'i_sd'] - V_final['xd', -1, 'i_sd']
 #   print('i_sd_diff')
  #  print(periodicity)

    name = trial.name
    print(name)
    print('diam_t')
    print(V_final['theta', 'diam_t',0])
    
  #
 #   print(V_final['theta',  'k_gear',0])
#    periodicity = V_final['xd', 0, 'v_sq'] 
 #   print('v_sq_diff_0')
 #   print(periodicity)
  #  periodicity = V_final['xd', 0, 'v_sd'] 
   # print('v_sd_0')
    #print(periodicity)
#    periodicity = V_final['xd', 0, 'i_sq'] 
 #   print('i_sq_0')
  #  print(periodicity)
   # periodicity = V_final['xd', 0, 'i_sd'] 
#    print('i_sd_0')
 #   print(periodicity)




#    periodicity = V_final['xd', -1, 'v_sq']
  #  print('v_sq_diff_T')
   # print(periodicity)
 #   periodicity = V_final['xd', -1, 'v_sd']
#    print('v_sd_T')
 #   print(periodicity)
  #  periodicity = V_final['xd', -1, 'i_sq']
   # print('i_sq_T')
   # print(periodicity)
  #  periodicity = V_final['xd', -1, 'i_sd']
 #   print('i_sd_T')
#    print(periodicity)





    p_fix_num = trial.optimization.p_fix_num
    output_vals = trial.optimization.output_vals
    time_grids = trial.optimization.time_grids
    integral_outputs_final = trial.optimization.integral_outputs_final
    cost_fun = trial.nlp.cost_components[0]
    cost = struct_op.evaluate_cost_dict(cost_fun, V_plot, p_fix_num)
    name = trial.name
    parametric_options = trial.options
    V_ref = trial.optimization.V_ref
    #plot_dict = tools.recalibrate_visualization(V_plot, plot_dict, output_vals, integral_outputs_final, parametric_options, time_grids, cost, name, V_ref, N=N)

    return plot_dict


def write_data_row(pcdw, plot_dict, write_csv_dict, tgrid_ip, k, rotation_representation):
    """
    Write one row of data into the .csv file
    :param pcdw: dictWriter object
    :param plot_dict: dictionary containing trial data
    :param write_csv_dict: csv helper dict used to write the trial data into the .csv
    :param k: time step in trajectory
    :return: None
    """

    # loop over variables
    for variable_type in ['xd', 'xa', 'xl', 'u', 'outputs']:
        for variable in list(plot_dict[variable_type].keys()):

            # check whether sub_variables exist
            if type(plot_dict[variable_type][variable]) == dict:
                for sub_variable in list(plot_dict[variable_type][variable].keys()):
                    var = plot_dict[variable_type][variable][sub_variable]
                    variable_length = len(var)
                    for index in range(variable_length):
                        write_csv_dict[variable_type + '_' + variable + '_' + sub_variable + '_' + str(index)] = str(var[index][k])

            # continue if no sub_variables exist
            else:

                # convert rotations from dcm to euler
                if variable[0] == 'r' and rotation_representation == 'euler':
                    dcm = []
                    for i in range(9):
                        dcm = cas.vertcat(dcm, plot_dict[variable_type][variable][i][k])

                    var = vect_op.rotationMatrixToEulerAngles(cas.reshape(dcm,3,3))

                    for index in range(3):
                        write_csv_dict[variable_type + '_' + variable + '_' + str(index)] = str(var[index])
                elif rotation_representation not in ['euler', 'dcm']:
                    awelogger.logger.error('Error: Only euler angles and direct cosine matrix supported.')
                else:
                    var = plot_dict[variable_type][variable]
                    variable_length = len(var)
                    for index in range(variable_length):
                        write_csv_dict[variable_type + '_' + variable + '_' + str(index)] = str(var[index][k])

    write_csv_dict['time'] = tgrid_ip[k]

    parent_map = plot_dict['architecture'].parent_map
    if k < plot_dict['architecture'].number_of_nodes-1:
        node = list(parent_map.keys())[k]
        write_csv_dict['nodes']  = str(node)
        write_csv_dict['parent'] = str(parent_map[node])
        if k < len(plot_dict['architecture'].kite_nodes):
            write_csv_dict['kites']  = plot_dict['architecture'].kite_nodes[k]
        else:
            write_csv_dict['kites']  = None
    else:
        write_csv_dict['nodes']  = None
        write_csv_dict['parent'] = None
        write_csv_dict['kites']  = None

    write_csv_dict['cross_tether'] = int(plot_dict['options']['user_options']['system_model']['cross_tether'])

    # write out sorted row
    ordered_dict = collections.OrderedDict(sorted(list(write_csv_dict.items()), key=lambda t: t[0]))
    pcdw.writerow(ordered_dict)

    return None

def generate_optimal_model(trial, param_options = None):

    """
    Generate optimal model dict based on both optimized parameter values
    as numerical values of constant parameters.
    :param trial: trial containing OCP solution and model information
    :return: model dict containing all relevant functions.
    """

    # fill in variables structure
    variables  = []
    for var_type in list(trial.model.variables.keys()):
        if var_type != 'theta':
            variables.append(cas.SX.sym(var_type,trial.model.variables[var_type].shape[0]))
        else:
            for var in list(trial.model.variables_dict['theta'].keys()):
                if var != 't_f':
                    variables.append(cas.SX(trial.optimization.V_opt['theta',var]))
                else:
                    if trial.optimization.V_opt['theta','t_f'].shape[0] == 1:
                        t_f = trial.optimization.V_opt['theta','t_f']
                        variables.append(cas.SX(t_f))
                    else:
                        t_f = trial.visualization.plot_dict['output_vals'][1]['final', 'time_period', 'val']
                        variables.append(cas.SX(t_f))
    variables = trial.model.variables(cas.vertcat(*variables))

    # fill in parameters structure
    parameters = trial.model.parameters(0.0)
    if param_options is None:
        param_options = trial.options['solver']['initialization']['sys_params_num']
    for param_type in list(param_options.keys()):
        if isinstance(param_options[param_type],dict):
            for param in list(param_options[param_type].keys()):
                if isinstance(param_options[param_type][param],dict):
                    for subparam in list(param_options[param_type][param].keys()):
                        parameters['theta0',param_type,param,subparam] = param_options[param_type][param][subparam]

                else:
                    parameters['theta0',param_type,param] = param_options[param_type][param]

    # create dae object based on numerical parameters
    import awebox.mdl.dae as dae
    model_dae = dae.Dae(
        variables,
        parameters,
        trial.model.dynamics,
        trial.model.integral_outputs_fun,
        param = 'num')

    # build model rootfinder
    model_dae.build_rootfinder()

    # create function arguments
    f_args = [model_dae.dae['x'], model_dae.dae['p'], model_dae.dae['z']]

    # create model dict
    model = {}
    model['dae'] = model_dae.dae
    model['constraints'] = cas.Function('constraints', [*f_args], [trial.model.constraints_fun(variables, parameters)])
    model['outputs'] = cas.Function('outputs', [*f_args], [trial.model.outputs_fun(variables, parameters)])
    model['scaling'] = trial.model.scaling
    model['var_bounds'] = trial.model.variable_bounds
    model['var_bounds_fun'] = cas.Function(
        'var_bounds',
        [*f_args],
        [generate_var_bounds_fun(trial.model)(variables)]
        )
    model['t_f'] = t_f.full()[0][0]
    model['rootfinder'] = model_dae.rootfinder

    return model

def generate_var_bounds_fun(model):

    var_constraints = []
    var_bounds = model.variable_bounds
    for var_type in list(model.variables.keys()):

        if var_type in ['xd','u','xa']:

            for var in list(model.variables_dict[var_type].keys()):

                var_array = (type(var_bounds[var_type][var]['ub']) == np.ndarray)
                if var_array:
                    for i in range(var_bounds[var_type][var]['ub'].shape[0]):

                        if var_bounds[var_type][var]['ub'][i] != np.inf:
                            var_constraints.append(
                                model.variables[var_type,var,i] - var_bounds[var_type][var]['ub'][i]
                            )

                        if var_bounds[var_type][var]['lb'][i] != -np.inf:
                            var_constraints.append(
                                - model.variables[var_type,var,i] + var_bounds[var_type][var]['lb'][i]
                            )
                else:
                        if var_bounds[var_type][var]['ub'] != np.inf:
                            var_constraints.append(
                                model.variables[var_type,var] - var_bounds[var_type][var]['ub']
                            )

                        if var_bounds[var_type][var]['lb'] != -np.inf:
                            var_constraints.append(
                                - model.variables[var_type,var] + var_bounds[var_type][var]['lb']
                            )

    return cas.Function('var_bounds', [model.variables], [cas.vertcat(*var_constraints)])
