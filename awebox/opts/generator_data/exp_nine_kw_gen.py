import numpy as np


def data_dict():

    data_dict = {}
    data_dict['winch_name'] = '9_kw_gen'

    data_dict['winch_el'] = winch_el()
    data_dict['winch_geometry'] = winch_geometry()
    data_dict['winch_tether'] = winch_tether()

    return data_dict


def winch_el():

    winch_el = {}

    winch_el['a_0'] = 293.5816
    winch_el['a_1'] = 0
    winch_el['a_2'] = 3.5852 * 10**-2          #0.0004 * (2*np.pi / 60) ** 2
    winch_el['a_3'] = 0
    winch_el['a_4'] = 6.6592 * 10**-2          #0.0666
    winch_el['a_5'] = 1.03                     #0.1079 * 2*np.pi / 60

    return winch_el



def winch_geometry():

    winch_geometry = {}

    winch_geometry['radius_drum'] = 0.53 / 2

    return winch_geometry




def winch_tether():

    winch_tether = {}

    return winch_tether


















































































    
