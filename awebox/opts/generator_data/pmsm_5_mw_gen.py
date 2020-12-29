import numpy as np


def data_dict():

    data_dict = {}

    data_dict['name'] = 'pmsm_5_mw_gen'
    data_dict['type'] = 'pmsm'
    data_dict['control_var'] = 'pmsm'
    data_dict['generator_max_power'] = 5e6
    data_dict['model_bounds'] = True                                             #'model_bounds' -> 'power_el' -> 'include'

    data_dict['gear_train'] = {}
    data_dict['gear_train']['used'] = False
    data_dict['gear_train']['optimize'] = False
    data_dict['gear_train']['min'] = 1/10
    data_dict['gear_train']['max'] = 10
    data_dict['gear_train']['j_gen_var'] = False

    data_dict['dv_sd'] = True
    data_dict['generator'] = winch_el()
    data_dict['ground_station'] = winch_mech()

    return data_dict


def winch_el():

    winch_el = {}

    winch_el['dot_v_sd_max'] = 1000
    winch_el['dot_v_sd_min'] = -1000
    winch_el['dot_v_sq_max'] = 1000
    winch_el['dot_v_sq_min'] = -1000
    winch_el['l_d'] = 3.56e-4
    winch_el['l_q'] = 3.56e-4
    winch_el['r_s'] = 1.25e-3
    winch_el['p_p'] = 4
    winch_el['phi_f'] = 2.51

    return winch_el



def winch_mech():
    #default with generator (guessed values of FEcreate drum)
    #usable without electric generator
    
    winch_mech = {}

#    winch_mech['r_gen'] = 0.1925
          #muss schauen ob überschrieben wird
    #kein ddl_t_max und dddl_t_max
    winch_mech['name'] = 'winch_265_mm'
    winch_mech['in_lag_dyn'] = False

    winch_mech['r_gen'] = 0.265                                                 #outer radius of fecreate winch
    winch_mech['r_gen_inner'] = 0.24                                            #guessed inner radius of fecreate winch
    winch_mech['rho_winch'] = 2700
    winch_mech['m_gen'] = 5057                                           #stainless stell density

    winch_mech['j_gen'] = 268
    winch_mech['j_winch'] =  np.pi/2 * (winch_mech['r_gen']**4 - winch_mech['r_gen_inner']**4) * winch_mech['rho_winch']

    winch_mech['m_gen'] = winch_mech['m_gen'] + np.pi/2 * (winch_mech['r_gen']**2 - winch_mech['r_gen_inner']**2) * winch_mech['rho_winch']               #generator/motor and winch one rigid body
    winch_mech['k_gear'] = 1
    winch_mech['f_winch'] = 0
    winch_mech['f_gen'] = 0


    return winch_mech




#Performance of two 5 MW Permanent Magnet Wind Turbine Generators using Surface Mounted d Interior Mounted Magnets
