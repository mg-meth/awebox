### Approximation of the "pmsm_125_kw_gen"

def data_dict():

    data_dict = {}

    data_dict['name'] = 'exp_pmsm_125_kw_gen'
    data_dict['type'] = 'experimental'
    data_dict['generator_max_power'] = 1.25*10**5
    data_dict['model_bounds'] = True
    data_dict['gear_train'] = False
    data_dict['gear_train']['optimize'] = False
    data_dict['generator'] = winch_el()
    data_dict['ground_station'] = winch_mech()

    return data_dict


def winch_el():
    #p_el = 1 + o + t + o^2 + t^2 + ot + o^3 + t^3 + o^2t + t^2o + o^2t^2

    winch_el = {}

    winch_el['a_0'] = -1140.6556243450698       #J/s                            1
    winch_el['a_1'] = -112.56875364206388       #Nm/rad                         o
    winch_el['a_2'] = 1.2009611896052341        #rad/s                          t
    winch_el['a_3'] = -0.40349444067608153      #Nms/rad^2                      o^2
    winch_el['a_4'] = 0.0012880888105898103     #rad/Nm * rad/s                 t^2
    winch_el['a_5'] = 1.2483255506212512        #-                              ot
    winch_el['a_6'] = -0.0015043660991787343    #Nms^2/rad^3                    o^3
    winch_el['a_7'] = -5.107046891652327e-08    #rad^3/N^2m^2 * rad/s           t^3
    winch_el['a_8'] = 0.002074005326109074      #s/rad                          o^2t
    winch_el['a_9'] = -6.981231974561795e-05    #rad/Nm                         t^2o
    winch_el['a_10'] = -1.3844102546945359e-06  #s/rad * 1/Nm                   o^2t^2

    return winch_el


def winch_mech():

    winch_mech = {}

    winch_mech['r_gen'] = 0.25
    winch_mech['j_winch'] = 1.57                                                #normally not used
    winch_mech['f_c'] = 0   	                                                #normally not used

    return winch_mech
