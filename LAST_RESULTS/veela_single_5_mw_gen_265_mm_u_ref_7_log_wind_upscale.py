#!/usr/bin/python3
from awebox.logger.logger import Logger as awelogger
#awelogger.logger.setLevel(10)
import awebox as awe
import matplotlib.pyplot as plt
import pdb
import awebox.tools.struct_operations as struct_op
import casadi as cas

########################
# SET-UP TRIAL OPTIONS #
########################

def solve_succed(quality_print_results, name):
    filename = 'solve_succed.txt'
    with open(filename) as f:
        n_neu = 0
        line_lst = []
        for n, line in enumerate(f):
            n_neu = n+1
            line_lst += [line]
    with open(filename, 'w') as f:
        string = ''
        for l in line_lst:
            if l != '\n':
                string += l + '\n'
        string += '\n' + name + ' : ' + quality_print_results
        f.write(string)


b_var = [5.5, 7.5, 10, 12.5, 15, 20, 25, 30]
w = 7
wd = 3
n_k = 60
tim = 1e3

for b in b_var:

    name = 'veela_single_5_mw_gen_265_mm_u_ref_' + '7' + '_log_wind' + '_upscale_b_' + str(b) + '_n_k_' + str(n_k) + '_wd_' +  str(wd)

        # make default options object
    options = awe.Options(True)

        # single kite with point-mass model
    options['user_options']['system_model']['architecture'] = {1:0}
    options['user_options']['system_model']['kite_dof'] = 6
    options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()
    options['user_options']['generator'] = awe.pmsm_5_mw_gen.data_dict()
    #options['user_options']['generator']['gear_train']['used'] = True
    #options['user_options']['generator']['gear_train']['optimize'] = True
    #options['user_options']['generator']['dv_sd'] = False
    #options['user_options']['generator']['control_var'] = 'dddl_t'
    #options['model']['tether']['control_var'] = 'dddl_t'
    #options['user_options']['generator']['type'] = None


    aspect_ratio = 5.5**2/3

    options['user_options']['kite_standard']['geometry']['c_ref'] = b/aspect_ratio
    options['user_options']['kite_standard']['geometry']['s_ref'] = b**2/aspect_ratio


    print( options['user_options']['kite_standard']['geometry']['j'])
    kappa = 2.4
    options['user_options']['kite_standard']['geometry']['j'] = options['user_options']['kite_standard']['geometry']['j'] * (b/options['user_options']['kite_standard']['geometry']['b_ref'])**(kappa + 2)
    options['user_options']['kite_standard']['geometry']['m_k'] = options['user_options']['kite_standard']['geometry']['m_k'] * (b/options['user_options']['kite_standard']['geometry']['b_ref'])**(kappa)
    options['user_options']['kite_standard']['geometry']['b_ref'] = b

        # trajectory should be a single pumping cycle with initial number of five windings
    options['user_options']['trajectory']['system_type'] = 'lift_mode'
    options['user_options']['trajectory']['type'] = 'power_cycle'
    options['user_options']['trajectory']['lift_mode']['windings'] = wd

    options['solver']['max_iter'] = 4000
    options['solver']['max_cpu_time'] = tim
        #options['model']['ground_station']['ddl_t_max'] = 95.04

    options['user_options']['wind']['u_ref'] = w
    options['nlp']['n_k'] = n_k
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

        # initialize and optimize trial
    trial = awe.Trial(options, name)
    trial.build()
    trial.optimize()
    quality_print_results = trial.quality.return_results()
    solve_succed(quality_print_results, name)
    trial.write_to_csv()