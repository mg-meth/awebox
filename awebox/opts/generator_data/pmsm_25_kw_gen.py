import numpy as np

def data_dict():

    data_dict = {}

    data_dict['name'] = 'pmsm_125_kw_gen'
    data_dict['type'] = 'pmsm'
    data_dict['control_var'] = 'pmsm'
    data_dict['generator_max_power'] = 1.25e5
    data_dict['model_bounds'] = True                                             #'model_bounds' -> 'power_el' -> 'include'
    data_dict['gear_train'] = False
    data_dict['gear_train']['optimize'] = False
    data_dict['generator'] = winch_el()
    data_dict['ground_station'] = winch_mech()

    return data_dict


def winch_el():

    winch_el = {}

    winch_el['voltage_d_max'] = 48
    winch_el['voltage_d_min'] = -48
    winch_el['voltage_q_max'] = 48
    winch_el['voltage_q_min'] = -48
    winch_el['l_d'] = 0.013e-3
    winch_el['l_q'] = 0.029e-3
    winch_el['r_s'] = 3.3e-3
    winch_el['p_p'] = 4
    winch_el['phi_f'] = 12.1e-3

    return winch_el


def winch_mech():

    winch_mech = {}

    winch_mech['r_gen'] = 0.25
    winch_mech['j_winch'] = 3e-3
    winch_mech['f_c'] = 0

    return winch_mech
