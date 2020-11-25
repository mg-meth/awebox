import numpy as np


def data_dict(options):

    data_dict = {}

    options['user_options']['generator']['type'] = 'asyn'
    options['model']['tether']['control_var'] = 'asyn'
    options['model']['model_bounds']['voltage']['include'] = True
    options['quality']['test_param']['generator_max_power'] = 25*10**3
    
    data_dict['winch_name'] = 'asyn_25_kw_gen'
    data_dict['asyn'] = winch_el(options)
    data_dict['winch_geometry'] = winch_geometry(options)



    return data_dict


def winch_el(options):

    winch_el = {}

    winch_el['r_r'] = 0.0727
    winch_el['l'] = 0.00297
    winch_el['v_n'] = 4.09
    winch_el['u_n'] = 231
    winch_el['j_winch'] = 0.328
    winch_el['f_c'] = 0
    
    return winch_el



def winch_geometry(options):

    winch_geometry = {}

    winch_geometry['n'] = 6
    winch_geometry['radius'] = 0.1615
    
    options['params']['ground_station']['r_gen'] = winch_geometry['radius']
    options['params']['ground_station']['m_gen'] = 50

    #kein ddl_t_max und dddl_t_max


    return winch_geometry




















































































    
