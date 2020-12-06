import casadi.tools as cas

import awebox.tools.vector_operations as vect_op
import awebox.tools.constraint_operations as cstr_op
import awebox.tools.print_operations as print_op

import awebox.mdl.aero.kite_dir.frames as frames
import awebox.mdl.aero.kite_dir.tools as tools
import awebox.mdl.aero.indicators as indicators
import awebox.mdl.mdl_constraint as mdl_constraint
import numpy as np


from awebox.logger.logger import Logger as awelogger


def get_winch_cstr(options, atmos, wind, variables_si, parameters, outputs, architecture):

    cstr_list = mdl_constraint.MdlConstraintList()

    if options['generator']['type'] != None and options['generator']['type'] != 'experimental':

        t_em = t_em_ode(options, variables_si, outputs, parameters, architecture)

        radius_winch = parameters['theta0','ground_station','r_gen']            #not optinal
        j_winch = parameters['theta0','ground_station','j_winch']
        f_winch = parameters['theta0','ground_station','f_winch']
        l_t_full = variables_si['theta']['l_t_full']
        phi = (l_t_full- variables_si['xd']['l_t']) / radius_winch
        omega = - variables_si['xd']['dl_t'] / radius_winch
        domega =  -variables_si['xddot']['ddl_t'] / radius_winch
        t_tether = -variables_si['xa']['lambda10'] * variables_si['xd']['l_t'] * radius_winch
        t_frict = -f_winch * omega
        t_inertia = j_winch * domega
        #t_inertia += options['scaling']['theta']['diam_t']**2 / 4 * np.pi * parameters['theta0', 'tether', 'rho']*radius**3 * (omega*omega + domega*phi) #

        rhs = t_tether + t_em + t_frict
        lhs = t_inertia

        if options['generator']['gear_train']['used']:
            j_gen = parameters['theta0','ground_station','j_gen']
            j_winch = parameters['theta0','ground_station','j_winch'] - j_gen   #normaly rigid body
            f_gen = parameters['theta0','ground_station','f_gen']

            if options['generator']['gear_train']['optimize']:

                k = variables_si['xd']['k_gear']
                dk = variables_si['xddot']['dk_gear']                           #const ratio
                k_cstr = cstr_op.Constraint(expr=dk, name='k_gear_const', cstr_type='eq')
                cstr_list.append(k_cstr)

            else:

                k = parameters['theta0','ground_station','k_gear']

            t_gen = k**2*j_gen*domega
            t_win = j_winch*domega + options['scaling']['theta']['diam_t']**2 / 4 * np.pi * parameters['theta0', 'tether', 'rho']*radius_winch**3 * (omega*omega + domega*phi) #
            lhs = t_gen + t_win
            rhs = t_tether + omega*(f_winch + f_gen*k**2) + k*t_em


        torque = rhs - lhs

        winch_cstr = cstr_op.Constraint(expr=torque, name='winch', cstr_type='eq')
        cstr_list.append(winch_cstr)

        if options['generator']['type'] == 'pmsm':
            generator = generator_ode(options, variables_si, outputs, parameters, architecture)
            cstr_list.append(generator)

    return cstr_list

def t_em_ode(options, variables_si, outputs, parameters, architecture):

    if options['generator']['type'] == 'pmsm':
        i_sd = variables_si['xd']['i_sd']
        i_sq = variables_si['xd']['i_sq']
        ld = parameters['theta0','generator','l_d']
        lq = parameters['theta0','generator','l_q']
        rs = parameters['theta0','generator','r_s']
        p_p = parameters['theta0','generator','p_p']
        phi_f = parameters['theta0','generator','phi_f']
        t_em = 3/2 * p_p * ((ld - lq) * i_sd*i_sq + i_sq * phi_f)

    return t_em

def generator_ode(options, variables_si, outputs, parameters, architecture):

    cstr_list = mdl_constraint.MdlConstraintList()

    omega = -variables_si['xd']['dl_t'] / parameters['theta0','ground_station','r_gen']
    if options['generator']['type'] == 'pmsm':
        v_sd = variables_si['u']['v_sd']
        v_sq = variables_si['u']['v_sq']
        i_sd = variables_si['xd']['i_sd']
        i_sq = variables_si['xd']['i_sq']
        di_sd = variables_si['xddot']['di_sd']
        di_sq = variables_si['xddot']['di_sq']
        ld = parameters['theta0','generator','l_d']
        lq =parameters['theta0','generator','l_q']
        rs = parameters['theta0','generator','r_s']
        phi_f = parameters['theta0','generator','phi_f']
        p_p = parameters['theta0','generator','p_p']

        i_sq_ode = v_sq + rs*i_sq + lq*di_sq + p_p*omega*phi_f + p_p*omega*ld*i_sd
        i_sd_ode = v_sd + rs*i_sd + ld*di_sd - p_p*omega*lq*i_sq

        i_sd_cstr = cstr_op.Constraint(expr=i_sd_ode, name='gen0', cstr_type='eq')
        cstr_list.append(i_sd_cstr)

        i_sq_cstr = cstr_op.Constraint(expr=i_sq_ode, name='gen1', cstr_type='eq')
        cstr_list.append(i_sq_cstr)

    return cstr_list
