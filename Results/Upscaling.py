#!/usr/bin/python3
#awelogger.logger.setLevel(10)
import awebox as awe
import matplotlib.pyplot as plt
import pdb
from awebox.logger.logger import Logger as awelogger


wind_ref = [5,6,7]
b_list = [20, 50, 100]

#dann noch mit 5mw generator

for b in b_list:
    for w in wind_ref:
        name = 'upscaling\single_kite_5_mw\single_kite_' + str(w) + '_log_wind' + '_b_' + str(b) + 'UPSCALING'

        print(name)


        # make default options object
        options = awe.Options(True)

        # single kite with point-mass model
        options['user_options']['system_model']['architecture'] = {1:0}
        options['user_options']['system_model']['kite_dof'] = 6
        options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()
        options['user_options']['generator'] = awe.pmsm_5_mw_gen.data_dict()

        b_ref = options['user_options']['kite_standard']['geometry']['b_ref']

        print('erst alt: m, dann neu: m')
        m_ref = options['user_options']['kite_standard']['geometry']['m_k']
        print(m_ref)
        kappa = 2.4
        options['user_options']['kite_standard']['geometry']['m_k'] = m_ref*(b/b_ref)**kappa
        print(options['user_options']['kite_standard']['geometry']['m_k'])

        print('erst alt: j, dann neu: j')
        print(options['user_options']['kite_standard']['geometry']['j'])
        j_ref = options['user_options']['kite_standard']['geometry']['j']
        kappa = 2.4
        for n_no, ro in enumerate(j_ref):
            for n_j, j in enumerate(ro):
                options['user_options']['kite_standard']['geometry']['j'][n_no][n_j] = j*(b/b_ref)**(kappa+2)

        print(options['user_options']['kite_standard']['geometry']['j'])
        # trajectory should be a single pumping cycle with initial number of five windings
        options['user_options']['trajectory']['type'] = 'power_cycle'
        options['user_options']['trajectory']['system_type'] = 'lift_mode'
        options['user_options']['trajectory']['lift_mode']['windings'] = 3
        options['solver']['max_iter'] = 2000
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
        trial.plot('level_3')
        trial.write_to_csv()
        #pdb.set_trace()

        V_final = trial.optimization.V_final
        V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
        print(V_final['xd', :, 'i_sd'],V_final['xd', :, 'i_sq'])
        print(V_solution_scaled['xd', :, 'i_sd'],V_solution_scaled['xd', :, 'i_sq'])




for b in b_list:
    for w in wind_ref:
        name = 'upscaling\single_kite_no_gen\single_kite_' + str(w) + '_log_wind' + '_b_' + str(b) + 'UPSCALING'

        print(name)


        # make default options object
        options = awe.Options(True)

        # single kite with point-mass model
        options['user_options']['system_model']['architecture'] = {1:0}
        options['user_options']['system_model']['kite_dof'] = 6
        options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()
        options['user_options']['generator'] = awe.pmsm_5_mw_gen.data_dict()

        b_ref = options['user_options']['kite_standard']['geometry']['b_ref']

        print('erst alt: m, dann neu: m')
        m_ref = options['user_options']['kite_standard']['geometry']['m_k']
        print(m_ref)
        kappa = 2.4
        options['user_options']['kite_standard']['geometry']['m_k'] = m_ref*(b/b_ref)**kappa
        print(options['user_options']['kite_standard']['geometry']['m_k'])

        print('erst alt: j, dann neu: j')
        print(options['user_options']['kite_standard']['geometry']['j'])
        j_ref = options['user_options']['kite_standard']['geometry']['j']
        kappa = 2.4
        for n_no, ro in enumerate(j_ref):
            for n_j, j in enumerate(ro):
                options['user_options']['kite_standard']['geometry']['j'][n_no][n_j] = j*(b/b_ref)**(kappa+2)

        print(options['user_options']['kite_standard']['geometry']['j'])
        # trajectory should be a single pumping cycle with initial number of five windings
        options['user_options']['trajectory']['type'] = 'power_cycle'
        options['user_options']['trajectory']['system_type'] = 'lift_mode'
        options['user_options']['trajectory']['lift_mode']['windings'] = 3
        options['solver']['max_iter'] = 2000
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
        trial.plot('level_3')
        trial.write_to_csv()
        #pdb.set_trace()

        V_final = trial.optimization.V_final
        V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
        print(V_final['xd', :, 'i_sd'],V_final['xd', :, 'i_sq'])
        print(V_solution_scaled['xd', :, 'i_sd'],V_solution_scaled['xd', :, 'i_sq'])





w_ref = [5]
for w in wind_ref:
    name = 'upscaling\single_kite_5_mw\single_kite_' + str(w) + '_log_wind_boeing(anstatt_b_aendern)'

    print(name)


    # make default options object
    options = awe.Options(True)

    # single kite with point-mass model
    options['user_options']['system_model']['architecture'] = {1:0}
    options['user_options']['system_model']['kite_dof'] = 6
    options['user_options']['kite_standard'] = awe.boeing747_data.data_dict()
    options['user_options']['generator'] = awe.pmsm_5_mw_gen.data_dict()

    # trajectory should be a single pumping cycle with initial number of five windings
    options['user_options']['trajectory']['type'] = 'power_cycle'
    options['user_options']['trajectory']['system_type'] = 'lift_mode'
    options['user_options']['trajectory']['lift_mode']['windings'] = 3
    options['solver']['max_iter'] = 10000
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
    trial.plot('level_3')
    trial.write_to_csv()
    #pdb.set_trace()

    V_final = trial.optimization.V_final
    V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
    print(V_final['xd', :, 'i_sd'],V_final['xd', :, 'i_sq'])
    print(V_solution_scaled['xd', :, 'i_sd'],V_solution_scaled['xd', :, 'i_sq'])
