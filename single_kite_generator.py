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
options['user_options']['generator'] = awe.pmsm_25_kw_gen.data_dict()

# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 5

# don't include induction effects, use simple tether drag
options['user_options']['induction_model'] = 'not_in_use'
options['user_options']['tether_drag_model'] = 'split'

options['user_options']['wind']['u_ref'] = 5

options['solver']['max_iter'] = 40000
options['solver']['max_cpu_time'] = 2.e4

options['nlp']['n_k'] = 60
options['solver']['max_iter'] = 2

##################
# OPTIMIZE TRIAL #
##################
options['solver']['linear_solver'] = 'mumps'

# initialize and optimize trial
trial = awe.Trial(options, 'rachel_awebox_generator')
trial.build()
trial.optimize(final_homotopy_step='initial')
#options 1 oder 2
V_final = trial.optimization.V_final
V_solution_scaled = trial.nlp.V(trial.optimization.solution['x'])
V_final['coll_var', :, :, 'xd', 'xd_i_s_0'] #V_final['xd', :, 'q21']
V_solution_scaled['coll_var', :, :, 'xd', 'xd_i_s_0']
print(options['user_options'])
trial.plot('level_3')



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
options['user_options']['system_model']['kite_dof'] = 6
options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()
options['user_options']['generator'] = awe.pmsm_25_kw_gen.data_dict()

# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 5

# don't include induction effects, use simple tether drag
options['user_options']['induction_model'] = 'not_in_use'
options['user_options']['tether_drag_model'] = 'split'

options['user_options']['wind']['u_ref'] = 5

options['solver']['max_iter'] = 40000
options['solver']['max_cpu_time'] = 2.e4

options['nlp']['n_k'] = 60

##################
# OPTIMIZE TRIAL #
##################
options['solver']['linear_solver'] = 'mumps'

# initialize and optimize trial
trial = awe.Trial(options, 'rachel_awebox_generator')
trial.build()
trial.optimize()
print(options['user_options'])
trial.plot('level_3')



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
options['user_options']['system_model']['kite_dof'] = 6
options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()
options['user_options']['generator'] = awe.pmsm_25_kw_gen.data_dict()

# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 5

# don't include induction effects, use simple tether drag
options['user_options']['induction_model'] = 'not_in_use'
options['user_options']['tether_drag_model'] = 'split'

options['user_options']['wind']['u_ref'] = 10

options['solver']['max_iter'] = 40000
options['solver']['max_cpu_time'] = 2.e4

options['nlp']['n_k'] = 60

##################
# OPTIMIZE TRIAL #
##################
options['solver']['linear_solver'] = 'mumps'

# initialize and optimize trial
trial = awe.Trial(options, 'rachel_awebox_generator')
trial.build()
trial.optimize()
print(options['user_options'])
trial.plot('level_3')
plt.show()




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
options['user_options']['generator'] = awe.pmsm_25_kw_gen.data_dict()

# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 3

# don't include induction effects, use simple tether drag
options['user_options']['induction_model'] = 'not_in_use'
options['user_options']['tether_drag_model'] = 'split'

options['user_options']['wind']['u_ref'] = 5

options['solver']['max_iter'] = 40000
options['solver']['max_cpu_time'] = 2.e4

options['nlp']['n_k'] = 60

##################
# OPTIMIZE TRIAL #
##################
options['solver']['linear_solver'] = 'mumps'

# initialize and optimize trial
trial = awe.Trial(options, 'rachel_awebox_generator')
trial.build()
trial.optimize()
print(options['user_options'])
trial.plot('level_3')
plt.show()




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
options['user_options']['system_model']['kite_dof'] = 6
options['user_options']['kite_standard'] = awe.ampyx_data.data_dict()
options['user_options']['generator'] = awe.pmsm_25_kw_gen.data_dict()

# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 3

# don't include induction effects, use simple tether drag
options['user_options']['induction_model'] = 'not_in_use'
options['user_options']['tether_drag_model'] = 'split'

options['user_options']['wind']['u_ref'] = 5

options['solver']['max_iter'] = 40000
options['solver']['max_cpu_time'] = 2.e4

options['nlp']['n_k'] = 60

##################
# OPTIMIZE TRIAL #
##################
options['solver']['linear_solver'] = 'mumps'

# initialize and optimize trial
trial = awe.Trial(options, 'rachel_awebox_generator')
trial.build()
trial.optimize()
print(options['user_options'])
trial.plot('level_3')
plt.show()





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
options['user_options']['generator'] = awe.pmsm_25_kw_gen.data_dict()

# trajectory should be a single pumping cycle with initial number of five windings
options['user_options']['trajectory']['type'] = 'power_cycle'
options['user_options']['trajectory']['system_type'] = 'lift_mode'
options['user_options']['trajectory']['lift_mode']['windings'] = 3

# don't include induction effects, use simple tether drag
options['user_options']['induction_model'] = 'not_in_use'
options['user_options']['tether_drag_model'] = 'split'

options['user_options']['wind']['u_ref'] = 10

options['solver']['max_iter'] = 40000
options['solver']['max_cpu_time'] = 2.e4

options['nlp']['n_k'] = 60

##################
# OPTIMIZE TRIAL #
##################
options['solver']['linear_solver'] = 'mumps'

# initialize and optimize trial
trial = awe.Trial(options, 'rachel_awebox_generator')
trial.build()
trial.optimize()
print(options['user_options'])
trial.plot('level_3')
plt.show()
