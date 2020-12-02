#!/usr/bin/python3

import awebox as awe
import matplotlib.pyplot as plt

########################
# SET-UP TRIAL OPTIONS #
########################

wind_ref = [7, 8, 9, 10]
name = []
for w in wind_ref:
    name += ['double_no_gen_wind_ref_' + str(w) + '_log_wind']

print(name)



# make default options object
options = awe.Options(True)

# single kite with point-mass model
options['user_options']['system_model']['architecture'] = {1:0, 2:1, 3:1}
options['user_options']['system_model']['kite_dof'] = 3
options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()

# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 3
options['solver']['max_iter'] = 40000
options['solver']['max_cpu_time'] = 2.e4
""" ### """


# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 3

wind = wind_ref[0]
options['user_options']['wind']['u_ref'] = wind

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
trial = awe.Trial(options, name[0])
trial.build()
trial.optimize()
trial.quality.print_results()
trial.plot('level_3')
trial.write_to_csv()

#!/usr/bin/python3

import awebox as awe
import matplotlib.pyplot as plt

########################
# SET-UP TRIAL OPTIONS #
########################

# make default options object
options = awe.Options(True)

# single kite with point-mass model
options['user_options']['system_model']['architecture'] = {1:0, 2:1, 3:1}
options['user_options']['system_model']['kite_dof'] = 3
options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()

options['solver']['max_iter'] = 40000
options['solver']['max_cpu_time'] = 2.e4
""" ### """

options['nlp']['n_k'] = 60

# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 3

wind = wind_ref[1]
options['user_options']['wind']['u_ref'] = wind

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
trial = awe.Trial(options, name[1])
trial.build()
trial.optimize()
trial.quality.print_results()
trial.plot('level_3')
trial.write_to_csv()

#!/usr/bin/python3

import awebox as awe
import matplotlib.pyplot as plt

########################
# SET-UP TRIAL OPTIONS #
########################

# make default options object
options = awe.Options(True)

# single kite with point-mass model
options['user_options']['system_model']['architecture'] = {1:0, 2:1, 3:1}
options['user_options']['system_model']['kite_dof'] = 3
options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()


options['solver']['max_iter'] = 40000
options['solver']['max_cpu_time'] = 2.e4
""" ### """


# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 3

wind = wind_ref[2]
options['user_options']['wind']['u_ref'] = wind

#options['model']['system_bounds']['u']['dkappa'] = [-1.0, 1.0]
options['nlp']['n_k'] = 60

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
trial = awe.Trial(options, name[2])
trial.build()
trial.optimize()
trial.quality.print_results()
trial.plot('level_3')
trial.write_to_csv()

#!/usr/bin/python3

import awebox as awe
import matplotlib.pyplot as plt

########################
# SET-UP TRIAL OPTIONS #
########################

# make default options object
options = awe.Options(True)

# single kite with point-mass model
options['user_options']['system_model']['architecture'] = {1:0, 2:1, 3:1}
options['user_options']['system_model']['kite_dof'] = 3
options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()


options['solver']['max_iter'] = 40000
options['solver']['max_cpu_time'] = 2.e4
""" ### """


# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 3

wind = wind_ref[3]
options['user_options']['wind']['u_ref'] = wind

#options['model']['system_bounds']['u']['dkappa'] = [-1.0, 1.0]

#options['model']['system_bounds']['xd']['l_t'] = [1.0e-2, 1.0e3]
#options['solver']['initialization']['xd']['l_t'] = 1.0e3 # initial guess

# don't include induction effects, use simple tether drag
options['user_options']['induction_model'] = 'not_in_use'
options['user_options']['tether_drag_model'] = 'split'
options['nlp']['n_k'] = 60

# initial tether length guess
#options['solver']['initialization']['xd']['l_t'] = 200.0 # initial guess

##################
# OPTIMIZE TRIAL #
##################

options['solver']['linear_solver'] = 'mumps'
#options['solver']['initialization']['fix_tether_length'] = True

# initialize and optimize trial
trial = awe.Trial(options, name[3])
trial.build()
trial.optimize()
trial.quality.print_results()
trial.plot('level_3')
trial.write_to_csv()

plt.show()
