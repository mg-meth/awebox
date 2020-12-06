import numpy as np


def data_dict():

    data_dict = {}

    data_dict['name'] = 'exp_9_kw_gen'
    data_dict['type'] = 'experimental'
    data_dict['model_bounds'] = True
    data_dict['gear_train'] = False
    data_dict['gear_train']['optimize'] = False
    data_dict['generator'] = winch_el()
    data_dict['ground_station'] = winch_mech()

    return data_dict


def winch_el():
    #p_el = 1 + o + t + o^2 + t^2 + ot + o^3 + t^3 + o^2t + t^2o + o^2t^2

    winch_el = {}

    winch_el['a_0'] = 293.5816          #J/s
    winch_el['a_1'] = 0                 #Nm/rad
    winch_el['a_2'] = 0                 #rad/s
    winch_el['a_3'] = 3.5852 * 10**-2   #Nms/rad^2
    winch_el['a_4'] = 6.6592 * 10**-2   #rad/Nm * rad/s
    winch_el['a_5'] = 1.03              #-
    winch_el['a_6'] = 0                 #Nms^2/rad^3
    winch_el['a_7'] = 0                 #rad^3/N^2m^2 * rad/s
    winch_el['a_8'] = 0                 #s/rad
    winch_el['a_9'] = 0                 #rad/Nm
    winch_el['a_10'] = 0                #s/rad * 1/Nm

    return winch_el



def winch_mech():

    winch_mech = {}

    winch_mech['r_gen'] = 0.25	                                                #normally not used

    return winch_mech
