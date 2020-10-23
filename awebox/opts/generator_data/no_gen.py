import numpy as np


def data_dict():

    data_dict = {}
    data_dict['winch_name'] = 'no_gen'

    data_dict['winch_el'] = winch_el()
    data_dict['winch_geometry'] = winch_geometry()
    data_dict['winch_tether'] = winch_tether()

    return data_dict


def winch_el():

    winch_el = {}

    winch_el['a_0'] = 0
    winch_el['a_1'] = 0
    winch_el['a_2'] = 0
    winch_el['a_3'] = 0
    winch_el['a_4'] = 0
    winch_el['a_5'] = 1

    return winch_el



def winch_geometry():

    winch_geometry = {}

    winch_geometry['radius_drum'] = 1

    return winch_geometry




def winch_tether():

    winch_tether = {}

    return winch_tether


















































































    
