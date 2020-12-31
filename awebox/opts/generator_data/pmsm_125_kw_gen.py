import numpy as np


def data_dict():

    data_dict = {}

    data_dict['name'] = 'pmsm_125_kw_gen'
    data_dict['type'] = 'pmsm'
    data_dict['control_var'] = 'pmsm'
    data_dict['generator_max_power'] = 1.25e5
    data_dict['model_bounds'] = True                                             #'model_bounds' -> 'power_el' -> 'include'

    data_dict['gear_train'] = {}
    data_dict['gear_train']['used'] = False
    data_dict['gear_train']['optimize'] = False
    data_dict['gear_train']['min'] = 1/10
    data_dict['gear_train']['max'] = 10
    data_dict['gear_train']['j_gen_var'] = True

    data_dict['dv_sd'] = True
    data_dict['generator'] = winch_el()
    data_dict['ground_station'] = winch_mech()

    return data_dict


def winch_el():

    winch_el = {}

    winch_el['dot_v_sd_max'] = 500
    winch_el['dot_v_sd_min'] = -500
    winch_el['dot_v_sq_max'] = 500
    winch_el['dot_v_sq_min'] = -500
    winch_el['l_d'] = 0.001
    winch_el['l_q'] = 0.001
    winch_el['r_s'] = 0.02
    winch_el['p_p'] = 4
    winch_el['phi_f'] = 0.892

    return winch_el



def winch_mech():
    #default with generator (guessed values of FEcreate drum)
    #usable without electric generator

    winch_mech = {}

    winch_mech['name'] = 'winch_265_mm'
    winch_mech['in_lag_dyn'] = False
    winch_mech['r_gen'] = 0.265                                                 #outer radius of fecreate winch #4500 titanium
    winch_mech['r_gen_inner'] = 0.24                                            #guessed inner radius of fecreate winch
    winch_mech['rho_winch'] = 2700                                              #aluminum density
    winch_mech['m_gen'] = 50                                                         #generator mass guessed

    winch_mech['j_gen'] = 1.57
    winch_mech['j_winch'] = 1.2*  np.pi/2 * (winch_mech['r_gen']**4 - winch_mech['r_gen_inner']**4) * winch_mech['rho_winch']

#    winch_mech['j_winch'] = winch_mech['j_gen'] + winch_mech['j_winch']           #generator/motor and winch one rigid body if 'gear_train' active => j_gen and j_winch will be used separately
 #   winch_mech['m_gen'] = winch_mech['m_gen'] + np.pi/2 * (winch_mech['r_gen']**2 - winch_mech['r_gen_inner']**2) * winch_mech['rho_winch']               #generator/motor and winch one rigid body
    winch_mech['k_gear'] = 1
    winch_mech['f_winch'] = 0
    winch_mech['f_gen'] = 0


    return winch_mech
