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


pmsm =          [False, True, True, True, True, True, True, True]
gear_used =     [False, False, False, True, True, False, True, True]
gear_opti =     [False, False, False, True, True, False, True, True]
gear_j_var =    [False, False, False, True, True, False, False, False]
dotv_sd =       [False, False, True, False, True, False, False, True]
control_var =   [True, False, False, False, False, True, False, False]

zus = 'lag: mein winch'

for i in range(1,2):

    p = pmsm[i]
    gear_u = gear_used[i]
    gear_o = gear_opti[i]
    gear_j = gear_j_var[i]
    dv = dotv_sd[i]
    control_v = control_var[i]

        # make default options object
    options = awe.Options(internal_access = True)

        # single kite with point-mass model
    options['user_options']['system_model']['architecture'] = {1:0}
    options['user_options']['system_model']['kite_dof'] = 6
    options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()

    if p:
        options['user_options']['generator'] = awe.pmsm_125_kw_gen.data_dict()

        if gear_u:
            options['user_options']['generator']['gear_train']['used'] = True

        if gear_o:
            options['user_options']['generator']['gear_train']['optimize'] = True

        if gear_j:
            options['user_options']['generator']['gear_train']['j_gen_var'] = True

        if not dv:
            options['user_options']['generator']['dv_sd'] = False

        if control_v:
            options['user_options']['generator']['control_var'] = 'dddl_t'
            options['model']['tether']['control_var'] = 'dddl_t'
            options['user_options']['generator']['type'] = None
            options['user_options']['generator']['ground_station']['in_lag_dyn'] = True

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

    #name = zus + ' archi: ' + str(options['user_options']['system_model']['architecture']) + ', kite_dof: ' + str (options['user_options']['system_model']['kite_dof']) + ', u_ref: ' + str(options['user_options']['wind']['u_ref']) + ', n_k: ' + str(options['nlp']['n_k']) + ', windings: ' + str(options['user_options']['trajectory']['lift_mode']['windings']) + ', generator: ' +str(gen) + ', used: ' + str(gear) + ', opti: ' + str(opti_gear) + ', dvsd: ' + str(dv_sd)
    name = 'pmsm: ' + str(p) + '    gear_use' + str(gear_u) + ' gear_opti' + str(gear_o) + ' gear_j_var' + str(gear_j) + \
    'dv_sd' + str(dv) + 'control_var' + str(control_v)
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
