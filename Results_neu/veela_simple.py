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


zus = 'lag: mein winch'

    # make default options object
options = awe.Options(internal_access = True)

    # single kite with point-mass model
options['user_options']['system_model']['architecture'] = {1:0}
options['user_options']['system_model']['kite_dof'] = 6
options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()
options['user_options']['generator'] = awe.pmsm_125_kw_gen.data_dict()
#options['user_options']['generator']['gear_train']['used'] = True
#options['user_options']['generator']['gear_train']['optimize'] = True
options['user_options']['generator']['dv_sd'] = False
#options['user_options']['generator']['control_var'] = 'ddl_t'
#options['model']['tether']['control_var'] = 'ddl_t'
#options['user_options']['generator']['type'] = None

    # trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['lift_mode']['windings'] = 3

options['solver']['max_iter'] = 4000
options['solver']['max_cpu_time'] = 1.e4
    #options['model']['ground_station']['ddl_t_max'] = 95.04

options['user_options']['wind']['u_ref'] = 5

options['nlp']['n_k'] = 60
    #options['model']['system_bounds']['u']['dkappa'] = [-1.0, 1.0]

    #options['model']['system_bounds']['xd']['l_t'] = [1.0e-2, 1.0e3]
    #options['solver']['initialization']['xd']['l_t'] = 1.0e3 # initial guess

    # don't include induction effects, use simple tether drag
options['user_options']['induction_model'] = 'not_in_use'
options['user_options']['tether_drag_model'] = 'split'
    # initial tether length guess
    #options['solver']['initialization']['xd']['l_t'] = 200.0 # initial guess
if options['user_options']['generator']:
    gen = options['user_options']['generator']['name']
    if options['user_options']['generator']['gear_train']['used']:
        gear = True
        if options['user_options']['generator']['gear_train']['optimize']:
            opti_gear = True
        else:
            opti_gear = False

    else:
        gear = False
        opti_gear = False
    if options['user_options']['generator']['dv_sd']:
        dv_sd = True
    else:
        dv_sd = False
else:
    gen = None
    gear = False
    opti_gear = False
    dv_sd = False

name = zus + ' archi: ' + str(options['user_options']['system_model']['architecture']) + ', kite_dof: ' + str (options['user_options']['system_model']['kite_dof']) + ', u_ref: ' + str(options['user_options']['wind']['u_ref']) + ', n_k: ' + str(options['nlp']['n_k']) + ', windings: ' + str(options['user_options']['trajectory']['lift_mode']['windings']) + ', generator: ' +str(gen) + ', used: ' + str(gear) + ', opti: ' + str(opti_gear) + ', dvsd: ' + str(dv_sd)

    ##################
    # OPTIMIZE TRIAL #
    ##################

options['solver']['linear_solver'] = 'mumps'
    #options['solver']['initialization']['fix_tether_length'] = True

    # initialize and optimize trial
trial = awe.Trial(options, name)
trial.build()
trial.optimize()
#quality_print_results = trial.quality.return_results()


"""
pdb.set_trace()

V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
pfn = trial.optimization.p_fix_num

u = V_solution_scaled['u']
u_ref = cas.vertcat(*trial.optimization.V_ref['u'])
W_u = pfn['p', 'weights', 'u']

print("U")
for i, u_teil in enumerate(u):
    print(cas.mtimes((cas.mtimes(((u[i]-u_ref[i]).T, W_u)), (u[i]-u_ref[i]))))

#pfn['p']['ref']

u_reg = cas.mtimes((cas.mtimes(((u[0]-u_ref[0]).T, W_u)), (u[0]-u_ref[0])))
track_u = cas.mtimes((W_u.T, u_reg))

W_tracking = pfn['cost', 'tracking']


theta = V_solution_scaled['theta']
theta_ref = pfn['p', 'ref', 'theta']
W_theta = pfn['p', 'weights', 'theta']

print("THETA")
print(cas.mtimes((cas.mtimes(((theta-theta_ref).T, W_theta)), (theta-theta_ref))))





x = V_solution_scaled['xd']
W_x = pfn['p', 'weights', 'xd']
x_ref = pfn['p', 'ref', 'xd']

x_reg = cas.mtimes((cas.mtimes(((x[0]-x_ref[0]).T, W_x)), (x[0]-x_ref[0])))
track_x = cas.mtimes((W_x.T, x_reg))




f_fun_track = track_u + track_x
print("f_fun_track")
print(f_fun_track)




cost_fun = trial.nlp.cost_components[0]
cost = struct_op.evaluate_cost_dict(cost_fun, V_solution_scaled, pfn)
for cost_name in cost.keys():
    print(cost_name + ': ' + str(cost[cost_name]))
f_fun_eval = trial.nlp.f_fun(V_solution_scaled, pfn)
print('f_fun:' + str(f_fun_eval))



pdb.set_trace()







#V_final = trial.optimization.V_final
#V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
#cost_fun = trial.nlp.cost_components[0]
#cost = struct_op.evaluate_cost_dict(cost_fun, V_solution_scaled, 4)
#for cost_name in cost.keys():
#    print(cost_name + ': ' + str(cost[cost_name]))
#f_fun_eval = trial.nlp.f_fun(V_solution_scaled, 4)
#print('f_fun:' + str(f_fun_eval))


"""
trial.plot('level_3')
    #pdb.set_trace()

#print(V_final['xa', :, 'lambda10'])
#print(V_solution_scaled['xa', :, 'lambda10'])


#print(V_final['xd', :, 'i_sd'],V_final['xd', :, 'i_sq'])
#print(V_solution_scaled['xd', :, 'i_sd'],V_solution_scaled['xd', :, 'i_sq'])

#solve_succed(quality_print_results, name)

plt.show()
input()


wind_ref = [5,6,7]
name = []

for w in wind_ref:
    name = 'single_kite_bubble_opti_q_only_' + str(w) + '_log_wind'
    print(name)


    # make default options object
    options = awe.Options(True)

    # single kite with point-mass model
    options = awe.Options(internal_access = True)

        # single kite with point-mass model
    options['user_options']['system_model']['architecture'] = {1:0}
    options['user_options']['system_model']['kite_dof'] = 6
    options['user_options']['kite_standard'] = awe.bubbledancer_data.data_dict()
    #options['model']['tether']['control_var'] = 'dddl_t'
    options['user_options']['generator'] = awe.pmsm_125_kw_gen.data_dict()
    #options['user_options']['generator']['gear_train']['used'] = True
    #options['user_options']['generator']['gear_train']['optimize'] = True

        # trajectory should be a single pumping cycle with initial number of five windings
    options['user_options']['trajectory']['type'] = 'power_cycle'
    options['user_options']['trajectory']['system_type'] = 'lift_mode'
    options['user_options']['trajectory']['lift_mode']['windings'] = 3

    options['solver']['max_iter'] = 2000
    options['solver']['max_cpu_time'] = 1.e4
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

    options['solver']['linear_solver'] = 'mumps'
    #options['solver']['initialization']['fix_tether_length'] = True

    # initialize and optimize trial
    trial = awe.Trial(options, name)
    trial.build()
    trial.optimize()
    #quality_print_results = trial.quality.return_results()
    trial.plot('level_3')
    trial.write_to_csv()
    #pdb.set_trace()
    #solve_succed(quality_print_results, name)

    V_final = trial.optimization.V_final
    V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
    #print(V_final['xd', :, 'i_sd'],V_final['xd', :, 'i_sq'])
    #print(V_solution_scaled['xd', :, 'i_sd'],V_solution_scaled['xd', :, 'i_sq'])
plt.show()
