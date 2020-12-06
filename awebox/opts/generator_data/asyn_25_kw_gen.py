import numpy as np


def data_dict():

    data_dict = {}

    data_dict['name'] = 'asyn_25_kw_gen'
    data_dict['type'] = 'asyn'
    data_dict['control_var'] = 'asyn'
    data_dict['generator_max_power'] = 25*10**3
    data_dict['model_bounds'] = True
    data_dict['gear_train'] = False
    data_dict['gear_train']['optimize'] = False
    data_dict['generator'] = winch_el()
    data_dict['ground_station'] = winch_mech()

    return data_dict


def winch_el():

    winch_el = {}

    winch_el['r_r'] = 0.0727
    winch_el['l'] = 0.00297
    winch_el['v_n'] = 4.09
    winch_el['u_n'] = 231
    winch_el['j_winch'] = 0.328

    return winch_el



def winch_mech():

    winch_mech = {}

    winch_mech['n'] = 6
    winch_mech['r_gen'] = 0.1615
    winch_mech['m_gen'] = 50
    winch_mech['f_c'] = 0


    return winch_mech
