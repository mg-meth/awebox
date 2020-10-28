#!/usr/bin/python3

import awebox as awe
import matplotlib.pyplot as plt

########################
# SET-UP TRIAL OPTIONS #
########################

# make default options object
options = awe.Options(True)

# single kite with point-mass model
options['user_options']['system_model']['architecture'] = {1:0}
options['user_options']['system_model']['kite_dof'] = 3
options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()


import numpy as np
import casadi as cas
options['model']['system_bounds']['xd']['q'] =  [np.array([-cas.inf, -cas.inf, 100.0]), np.array([cas.inf, cas.inf, cas.inf])]
options['user_options']['generator']['type'] = 'pmsm'
options['user_options']['winch'] = awe.no_gen.data_dict()   #problem: wenn deaktiviert kann das programm winch nicht in das programm hinzufügen
options['model']['tether']['control_var'] = 'pmsm'
options['model']['model_bounds']['voltage']['include'] = True

options['solver']['max_iter'] = 4000
#options['solver']['max_cpu_time'] = 2.e4
"""  """


# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 5

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
trial = awe.Trial(options, 'single_gen')
trial.build()
trial.optimize()
trial.plot('level_3')
trial.write_to_csv()

plt.show()
