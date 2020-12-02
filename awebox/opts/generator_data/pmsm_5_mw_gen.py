import numpy as np


def data_dict():

    data_dict = {}

    data_dict['name'] = 'pmsm_5_mw_gen'
    data_dict['type'] = 'pmsm'
    data_dict['control_var'] = 'pmsm'
    data_dict['generator_max_power'] = 5e6
    data_dict['model_bounds'] = True
    data_dict['generator'] = winch_el()
    data_dict['ground_station'] = winch_mech()

    return data_dict


def winch_el():

    winch_el = {}

    winch_el['voltage_d_max'] = 433
    winch_el['voltage_d_min'] = -433
    winch_el['voltage_q_max'] = 433
    winch_el['voltage_q_min'] = -433
    winch_el['l_d'] = 3.56e-4
    winch_el['l_q'] = 3.56e-4
    winch_el['r_s'] = 1.25e-3
    winch_el['p_p'] = 4
    winch_el['phi_f'] = 2.51

    return winch_el



def winch_mech():

    winch_mech = {}

    winch_mech['r_gen'] = 0.1925
    winch_mech['m_gen'] = 5057      #muss schauen ob überschrieben wird
    winch_mech['j_winch'] = 268
    winch_mech['f_c'] = 0
    #kein ddl_t_max und dddl_t_max

    return winch_mech




#Performance of two 5 MW Permanent Magnet Wind Turbine Generators using Surface Mounted d Interior Mounted Magnets
