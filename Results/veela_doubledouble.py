#!/usr/bin/python3
from awebox.logger.logger import Logger as awelogger
#awelogger.logger.setLevel(10)
import awebox as awe
import matplotlib.pyplot as plt
import pdb

########################
# SET-UP TRIAL OPTIONS #
########################



name = 'TESTdoubledouble'

    # make default options object
options = awe.Options(True)

    # single kite with point-mass model
options['user_options']['system_model']['architecture'] = {1:0, 2:1, 3:1, 4:1, 5:4, 6:4}
options['user_options']['system_model']['kite_dof'] = 6
options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()
options['user_options']['generator'] = awe.pmsm_125_kw_gen.data_dict()


    # trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 3
options['solver']['max_iter'] = 20000
options['solver']['max_cpu_time'] = 2.e4
""" ### """
    #options['model']['ground_station']['ddl_t_max'] = 95.04

options['user_options']['wind']['u_ref'] = 5

options['nlp']['n_k'] = 40
    #options['model']['system_bounds']['u']['dkappa'] = [-1.0, 1.0]

    #options['model']['system_bounds']['xd']['l_t'] = [1.0e-2, 1.0e3]
    #options['solver']['initialization']['xd']['l_t'] = 1.0e3 # initial guess

    # don't include induction effects, use simple tether drag
options['user_options']['induction_model'] = 'not_in_use'
options['user_options']['tether_drag_model'] = 'split'

    # initial tether length guess
    #options['solver']['initialization']['xd']['l_t'] = 200.0 # initial guess

    ##################
    # OPTIMIZE TRIAL #
    ##################

options['solver']['linear_solver'] = 'ma57'
    #options['solver']['initialization']['fix_tether_length'] = True

    # initialize and optimize trial
trial = awe.Trial(options, name)
trial.build()
trial.optimize()
trial.quality.print_results()
quality_print_results = trial.quality.return_results()
trial.plot('level_3')
trial.write_to_csv()
solve_succed(quality_print_results, name)
    #pdb.set_trace()
V_final = trial.optimization.V_final
V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
print(V_final['xd', :, 'i_sd'],V_final['xd', :, 'i_sq'])
print(V_solution_scaled['xd', :, 'i_sd'],V_solution_scaled['xd', :, 'i_sq'])


wind_ref = [2,3,4,5,6,7]
name = []


for w in wind_ref:
    name = 'double_double_kite_125_kw\double_double_kite_' + str(w) + '_log_wind'

    print(name)


    # make default options object
    options = awe.Options(True)

    # single kite with point-mass model
    options['user_options']['system_model']['architecture'] = {1:0, 2:1, 3:1, 4:1, 5:4, 6:4}
    options['user_options']['system_model']['kite_dof'] = 6
    options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()
    options['user_options']['generator'] = awe.pmsm_125_kw_gen.data_dict()


    # trajectory should be a single pumping cycle with initial number of five windings
    options['user_options']['trajectory']['type'] = 'power_cycle'
    options['user_options']['trajectory']['system_type'] = 'lift_mode'
    options['user_options']['trajectory']['lift_mode']['windings'] = 3
    options['solver']['max_iter'] = 40000
    options['solver']['max_cpu_time'] = 4.e4
    """ ### """
    #options['model']['ground_station']['ddl_t_max'] = 95.04

    options['user_options']['wind']['u_ref'] = w

    options['nlp']['n_k'] = 60
    #options['model']['system_bounds']['u']['dkappa'] = [-1.0, 1.0]

    #options['model']['system_bounds']['xd']['l_t'] = [1.0e-2, 1.0e3]
    #options['solver']['initialization']['xd']['l_t'] = 1.0e3 # initial guess

    # don't include induction effects, use simple tether drag
    options['user_options']['induction_model'] = 'not_in_use'
    options['user_options']['tether_drag_model'] = 'split'

    # initial tether length guess
    #options['solver']['initialization']['xd']['l_t'] = 200.0 # initial guess

    ##################
    # OPTIMIZE TRIAL #
    ##################

    options['solver']['linear_solver'] = 'ma57'
    #options['solver']['initialization']['fix_tether_length'] = True

    # initialize and optimize trial
    trial = awe.Trial(options, name)
    trial.build()
    trial.optimize()
    trial.quality.print_results()
    quality_print_results = trial.quality.return_results()
    trial.plot('level_3')
    trial.write_to_csv()
    solve_succed(quality_print_results, name)
    #pdb.set_trace()

    V_final = trial.optimization.V_final
    V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
    print(V_final['xd', :, 'i_sd'],V_final['xd', :, 'i_sq'])
    print(V_solution_scaled['xd', :, 'i_sd'],V_solution_scaled['xd', :, 'i_sq'])


for w in wind_ref:
    name = 'double_double_kite_no_gen\double_double_kite_' + str(w) + '_log_wind'

    print(name)


    # make default options object
    options = awe.Options(True)

    # single kite with point-mass model
    options['user_options']['system_model']['architecture'] = {1:0, 2:1, 3:1, 4:1, 5:4, 6:4}
    options['user_options']['system_model']['kite_dof'] = 6
    options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()


    # trajectory should be a single pumping cycle with initial number of five windings
    options['user_options']['trajectory']['type'] = 'power_cycle'
    options['user_options']['trajectory']['system_type'] = 'lift_mode'
    options['user_options']['trajectory']['lift_mode']['windings'] = 3
    options['solver']['max_iter'] = 20000
    options['solver']['max_cpu_time'] = 2.e4
    """ ### """
    #options['model']['ground_station']['ddl_t_max'] = 95.04

    options['user_options']['wind']['u_ref'] = w

    options['nlp']['n_k'] = 60
    #options['model']['system_bounds']['u']['dkappa'] = [-1.0, 1.0]

    #options['model']['system_bounds']['xd']['l_t'] = [1.0e-2, 1.0e3]
    #options['solver']['initialization']['xd']['l_t'] = 1.0e3 # initial guess

    # don't include induction effects, use simple tether drag
    options['user_options']['induction_model'] = 'not_in_use'
    options['user_options']['tether_drag_model'] = 'split'

    # initial tether length guess
    #options['solver']['initialization']['xd']['l_t'] = 200.0 # initial guess

    ##################
    # OPTIMIZE TRIAL #
    ##################

    options['solver']['linear_solver'] = 'ma57'
    #options['solver']['initialization']['fix_tether_length'] = True

    # initialize and optimize trial
    trial = awe.Trial(options, name)
    trial.build()
    trial.optimize()
    trial.quality.print_results()
    quality_print_results = trial.quality.return_results()
    trial.plot('level_3')
    trial.write_to_csv()
    solve_succed(quality_print_results, name)
    #pdb.set_trace()

    V_final = trial.optimization.V_final
    V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
    #print(V_final['xd', :, 'i_sd'],V_final['xd', :, 'i_sq'])
    #print(V_solution_scaled['xd', :, 'i_sd'],V_solution_scaled['xd', :, 'i_sq'])



for w in wind_ref:
    name = 'double_double_5_mw\double_double_kite_' + str(w) + '_log_wind'

    print(name)


    # make default options object
    options = awe.Options(True)

    # single kite with point-mass model
    options['user_options']['system_model']['architecture'] = {1:0, 2:1, 3:1, 4:1, 5:4, 6:4}
    options['user_options']['system_model']['kite_dof'] = 6
    options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()
    options['user_options']['generator'] = awe.pmsm_5_mw_gen.data_dict()


    # trajectory should be a single pumping cycle with initial number of five windings
    options['user_options']['trajectory']['type'] = 'power_cycle'
    options['user_options']['trajectory']['system_type'] = 'lift_mode'
    options['user_options']['trajectory']['lift_mode']['windings'] = 3
    options['solver']['max_iter'] = 20000
    options['solver']['max_cpu_time'] = 2.e4
    """ ### """
    #options['model']['ground_station']['ddl_t_max'] = 95.04

    options['user_options']['wind']['u_ref'] = w

    options['nlp']['n_k'] = 60
    #options['model']['system_bounds']['u']['dkappa'] = [-1.0, 1.0]

    #options['model']['system_bounds']['xd']['l_t'] = [1.0e-2, 1.0e3]
    #options['solver']['initialization']['xd']['l_t'] = 1.0e3 # initial guess

    # don't include induction effects, use simple tether drag
    options['user_options']['induction_model'] = 'not_in_use'
    options['user_options']['tether_drag_model'] = 'split'

    # initial tether length guess
    #options['solver']['initialization']['xd']['l_t'] = 200.0 # initial guess

    ##################
    # OPTIMIZE TRIAL #
    ##################

    options['solver']['linear_solver'] = 'ma57'
    #options['solver']['initialization']['fix_tether_length'] = True

    # initialize and optimize trial
    trial = awe.Trial(options, name)
    trial.build()
    trial.optimize()
    trial.quality.print_results()
    quality_print_results = trial.quality.return_results()
    trial.plot('level_3')
    trial.write_to_csv()
    solve_succed(quality_print_results, name)
    #pdb.set_trace()

    V_final = trial.optimization.V_final
    V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
    print(V_final['xd', :, 'i_sd'],V_final['xd', :, 'i_sq'])
    print(V_solution_scaled['xd', :, 'i_sd'],V_solution_scaled['xd', :, 'i_sq'])
