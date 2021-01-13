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
"""
def get_winch_cstr(options, atmos, wind, variables_si, parameters, outputs, architecture):
    cstr_list = mdl_constraint.MdlConstraintList()
    if options['generator']['type'] != None and options['generator']['type'] != 'experimental':
        radius_winch = parameters['theta0','ground_station','r_gen']
        j_gen = parameters['theta0','ground_station','j_gen']
        j_winch = parameters['theta0','ground_station','j_winch']
        #v_sq = variables_si['u']['v_sq']
        l_t = variables_si['xd']['l_t']
        dl_t = variables_si['xd']['dl_t']
        ddl_t = variables_si['xd']['ddl_t']
        dddl_t = variables_si['xddot']['dddl_t']
        lam = variables_si['xa']['lambda10']
        print(variables_si.keys())
        #dlam = variables_si['xadot']['lambda10']
    #    ld = parameters['theta0','generator','l_d']
        lq = parameters['theta0','generator','l_q']
        rs = parameters['theta0','generator','r_s']
        p_p = parameters['theta0','generator','p_p']
        phi_f = parameters['theta0','generator','phi_f']

        v_sq_ode = variables_si['xddot']['dv_sq'] - variables_si['u']['dv_sq']
        v_sq_ode = cstr_op.Constraint(expr=v_sq_ode, name='v_sq_ode', cstr_type='eq')
        cstr_list.append(v_sq_ode)
        v_sq = variables_si['xd']['v_sq']

        i_sq = (lam*l_t*radius_winch**2 - (j_gen + j_winch)) / (1.5*p_p*phi_f*radius_winch)
        ode = -v_sq + rs * i_sq - dl_t/radius_winch * p_p * phi_f + lq / (1.5*p_p*phi_f*radius_winch) * ( lam*dl_t*radius_winch**2 - (j_gen + j_winch)*dddl_t)    #dlam*l_t*radius_winch**2 +

        winch_cstr = cstr_op.Constraint(expr=ode, name='winch', cstr_type='eq')
        cstr_list.append(winch_cstr)

    return cstr_list

"""
def get_winch_cstr(options, atmos, wind, variables_si, parameters, outputs, architecture):

    cstr_list = mdl_constraint.MdlConstraintList()

    t_em = cas.DM(0.)

    if options['generator']['type'] != None and options['generator']['type'] != 'experimental':
        if not options['tether']['use_wound_tether']:
            raise ValueError('Invalid user_options: use_wound_tether = False, when you use a generator model with ODEs it have to be True')
        if options['ground_station']['in_lag_dyn']:
            raise ValueError('Invalid user_options: in_lag_dyn = True, when you use a generator model with ODEs it have to be False or when you dont want to use the default winch')

        t_em = t_em_ode(options, variables_si, outputs, parameters, architecture)


    if not options['ground_station']['in_lag_dyn']:

        radius_winch = parameters['theta0','ground_station','r_gen']            #not optinal
        j_gen = parameters['theta0','ground_station','j_gen']
        j_winch = parameters['theta0','ground_station','j_winch']
        f_winch = parameters['theta0','ground_station','f_winch']
        l_t_full = variables_si['theta']['l_t_full']
        phi = (l_t_full- variables_si['xd']['l_t']) / radius_winch
        omega = - variables_si['xd']['dl_t'] / radius_winch
        domega =  -variables_si['xddot']['ddl_t'] / radius_winch
        t_tether = -variables_si['xa']['lambda10'] * variables_si['xd']['l_t'] * radius_winch
        t_frict = -f_winch * omega
        t_inertia = j_winch * domega
        t_inertia += variables_si['theta']['diam_t']**2 / 4 * np.pi * parameters['theta0', 'tether', 'rho']*radius_winch**3 * (omega*omega + domega*phi) #

        rhs = t_tether + t_em + t_frict
        lhs = t_inertia


        omega = variables_si['xd']['dl_t'] / radius_winch
        domega = variables_si['xddot']['ddl_t'] / radius_winch
        phi = (l_t_full- variables_si['xd']['l_t']) / radius_winch

        rhs = (j_gen+j_winch)*variables_si['xddot']['ddl_t']/radius_winch
        rhs += variables_si['theta']['diam_t']**2 / 4 * np.pi * parameters['theta0', 'tether', 'rho']*radius_winch**3 * (-omega*omega + domega*phi)
        lhs = variables_si['xa']['lambda10'] * variables_si['xd']['l_t'] * radius_winch - t_em



        if options['generator']['gear_train']['used']:
            j_gen = parameters['theta0','ground_station','j_gen']
            j_winch = parameters['theta0','ground_station','j_winch']   #normaly rigid body
            f_gen = parameters['theta0','ground_station','f_gen']

            k = variables_si['theta']['k_gear']

            t_win = j_winch*variables_si['xddot']['ddl_t']/radius_winch+ options['scaling']['theta']['diam_t']**2 / 4 * np.pi * parameters['theta0', 'tether', 'rho']*radius_winch**3 * (-omega*omega + domega*phi) #
            j_gen *= k**2
            t_tether = -variables_si['xa']['lambda10'] * variables_si['xd']['l_t'] * radius_winch

            t_gen = j_gen*variables_si['xddot']['ddl_t']/radius_winch
            lhs = -t_gen - t_win
            rhs = t_tether + k*t_em #+ omega*(f_winch + f_gen*k**2)






        if options['generator']['gear_train']['used']:

            k   = variables_si['theta']['k_gear']
#            dk  = variables_si['xddot']['dk_gear']

 #           dk_ineq         = dk
  
#          dk_ineq_cstr    = cstr_op.Constraint(expr=dk_ineq, name='dk_ineq', cstr_type='eq')
   #         cstr_list.append(dk_ineq_cstr)
#
            len_zstl    = 0.1
            delta_r     = 0.05
            rho_zstl    = 2700
            j_zstl      = np.pi *len_zstl *rho_zstl *(-3 *k *radius_winch**2 *delta_r**2 + 2 *k**2 *delta_r**3 *radius_winch + 2 *delta_r *radius_winch**3 - 1/2 *k**3 *delta_r**4)

            j_gen_zstl = k**3 *j_gen + j_zstl

            t_tether = variables_si['xa']['lambda10'] * variables_si['xd']['l_t'] * radius_winch

            t_angular_momentum          = (j_gen_zstl + k*j_winch) *domega
            t_angular_momentum_tether   = k* variables_si['theta']['diam_t']**2 / 4 *np.pi *parameters['theta0', 'tether', 'rho']
            t_angular_momentum_tether  *= radius_winch**3 *(-omega *omega + domega *phi)

            rhs =   t_angular_momentum + t_angular_momentum_tether
            rhs +=  omega *(f_winch *k**3)
            lhs =   t_tether *k - k**2 *t_em










        if options['generator']['type'] == 'pmsm':
            generator = generator_ode(options, variables_si, outputs, parameters, architecture)
            cstr_list.append(generator)
#            sign = variables_si['u']['sign']
#            sign_eq = sign**2 - 4*sign + 3
#            sign_ineq = -variables_si['u']['v_sq']/(sign)
#            sign_eq = cstr_op.Constraint(expr=sign_eq, name='sign_eq', cstr_type='eq')
#            cstr_list.append(sign_eq)
#            sign_ineq = cstr_op.Constraint(expr=sign_ineq, name='sign_ineq', cstr_type='ineq')
#            cstr_list.append(sign_ineq)
            #sign = p_el_sign(options, variables_si, outputs, parameters, architecture)
            #cstr_list.append(sign)



        torque = lhs - rhs

        print("torque")
        print(torque)
        winch_cstr = cstr_op.Constraint(expr=torque, name='winch', cstr_type='eq')
        cstr_list.append(winch_cstr)



    return cstr_list




def t_em_ode(options, variables_si, outputs, parameters, architecture):

    if options['generator']['type'] == 'pmsm':
    #    i_sd = variables_si['xd']['i_sd']
        i_sq = variables_si['xd']['i_sq']
        ld = parameters['theta0','generator','l_d']
        lq = parameters['theta0','generator','l_q']
        rs = parameters['theta0','generator','r_s']
        p_p = parameters['theta0','generator','p_p']
        phi_f = parameters['theta0','generator','phi_f']
        t_em = 3/2 * p_p * (i_sq * phi_f)   #(ld - lq) * i_sd*i_sq +

    return t_em

def generator_ode(options, variables_si, outputs, parameters, architecture):

    cstr_list = mdl_constraint.MdlConstraintList()

    if options['generator']['type'] == 'pmsm':
        if options['generator']['dv_sd']:
    #    v_sd = variables_si['u']['v_sd']
            v_sd_ode = variables_si['xddot']['dv_sd'] - variables_si['u']['dv_sd']
            v_sd_ode = cstr_op.Constraint(expr=v_sd_ode, name='v_sd_ode', cstr_type='eq')
            cstr_list.append(v_sd_ode)
            v_sd = variables_si['xd']['v_sd']
            i_sd = variables_si['xd']['i_sd']
            di_sd = variables_si['xddot']['di_sd']

    #    v_sq = variables_si['u']['v_sq']
        v_sq_ode = variables_si['xddot']['dv_sq'] - variables_si['u']['dv_sq']
        v_sq_ode = cstr_op.Constraint(expr=v_sq_ode, name='v_sq_ode', cstr_type='eq')
        cstr_list.append(v_sq_ode)
        v_sq = variables_si['xd']['v_sq']
        i_sq = variables_si['xd']['i_sq']
        di_sq = variables_si['xddot']['di_sq']
        ld = parameters['theta0','generator','l_d']
        lq =parameters['theta0','generator','l_q']
        rs = parameters['theta0','generator','r_s']
        phi_f = parameters['theta0','generator','phi_f']
        p_p = parameters['theta0','generator','p_p']


        omega = -variables_si['xd']['dl_t'] / parameters['theta0','ground_station','r_gen']
        i_sq_ode = -v_sq + rs*i_sq + phi_f*omega*p_p + lq*di_sq

        if options['generator']['dv_sd']:
            i_sq_ode += omega*p_p*i_sd*ld
            i_sd_ode = -v_sd + rs*i_sd - omega*p_p*i_sq*lq + ld*di_sd

        if options['generator']['gear_train']['used']:
            k = variables_si['theta']['k_gear']

            r_gen       = parameters['theta0','ground_station','r_gen']
            omega       = k* variables_si['xd']['dl_t'] / r_gen
            i_sq_ode    = -v_sq + rs*i_sq - phi_f*omega*p_p + lq*di_sq

            if options['generator']['dv_sd']:
                i_sq_ode += -omega*p_p*i_sd*ld
                i_sd_ode = -v_sd + rs*i_sd + omega*p_p*i_sq*lq + ld*di_sd

        print("i_sq_ode")
        print(i_sq_ode)

        i_sq_cstr = cstr_op.Constraint(expr=i_sq_ode, name='gen1', cstr_type='eq')
        cstr_list.append(i_sq_cstr)

        if options['generator']['dv_sd']:
            print('i_sd_ode')
            print(i_sd_ode)
            i_sd_cstr = cstr_op.Constraint(expr=i_sd_ode, name='gen0', cstr_type='eq')
            cstr_list.append(i_sd_cstr)
    return cstr_list


def alte_func():
    omega = variables_si['xd']['dl_t'] / parameters['theta0','ground_station','r_gen']

    #    i_sq_ode = v_sq + rs*i_sq + lq*di_sq + p_p*omega*phi_f + p_p*omega*ld*i_sd
    #    i_sd_ode = v_sd + rs*i_sd + ld*di_sd - p_p*omega*lq*i_sq

    #    i_sq_ode = p_p*omega * (ld*i_sd + phi_f) + i_sq*rs + lq*di_sq - v_sq
    #    i_sd_ode = p_p*omega*lq*i_sq + i_sd*rs + ld*di_sd - v_sd

    i_sq_ode = v_sq + rs*i_sq + phi_f*omega*p_p + lq*di_sq
        #i_sd_ode = v_sd + lq*i_sq*omega

    #    i_sd_cstr = cstr_op.Constraint(expr=i_sd_ode, name='gen0', cstr_type='eq')
    #    cstr_list.append(i_sd_cstr)




    """
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

            omega = - variables_si['xd']['dl_t'] / radius_winch
            t_gen = k**2*j_gen*domega
            t_win = j_winch*domega + options['scaling']['theta']['diam_t']**2 / 4 * np.pi * parameters['theta0', 'tether', 'rho']*radius_winch**3 * (omega*omega + domega*phi) #
            lhs = t_gen + t_win
            rhs = t_tether + omega*(f_winch + f_gen*k**2) + k*t_em
    """

    rhs = j_winch*variables_si['xddot']['ddl_t']/radius_winch
    lhs = -variables_si['xa']['lambda10'] * variables_si['xd']['l_t'] * radius_winch - t_em
    torque = rhs - lhs








def p_el_sign(options, variables_si, outputs, parameters, architecture):

    n_k = options['aero']['vortex']['n_k']
    d = options['aero']['vortex']['d']
    sign = variables_si['u']['sign']
    vortex_wake_nodes = options['induction']['vortex_wake_nodes']

    cstr_list = cstr_op.ConstraintList()

    rings = vortex_wake_nodes - 1

    for ring in range(rings):
        wake_node = ring
        for ndx in range(n_k):
            for ddx in range(d):

                local_name = 'p_el_sign_' + str(ring) + '_' + str(ndx) + '_' + str(ddx)
                ndx_shed = n_k - 1  - wake_node
                ddx_shed = d - 1

                already_shed = False
                if (ndx > ndx_shed):
                    already_shed = True
                elif ((ndx == ndx_shed) and (ddx == ddx_shed)):
                    already_shed = True

                if already_shed:
                    sign_eq = sign - 1.
                else:
                    sign_eq = sign + 1

                print(sign_eq)

                sign_eq = cstr_op.Constraint(expr = sign_eq, name = local_name, cstr_type='eq')
                cstr_list.append(sign_eq)

    return cstr_list





def get_strength_constraint(options, V, Outputs, model):

    n_k = options['n_k']
    d = options['collocation']['d']

    comparison_labels = options['induction']['comparison_labels']
    wake_nodes = options['induction']['vortex_wake_nodes']
    rings = wake_nodes - 1
    kite_nodes = model.architecture.kite_nodes

    strength_scale = tools.get_strength_scale(options)

    Xdot = struct_op.construct_Xdot_struct(options, model.variables_dict)(0.)

    cstr_list = cstr_op.ConstraintList()

    any_vor = any(label[:3] == 'vor' for label in comparison_labels)
    if any_vor:

        for kite in kite_nodes:
            for ring in range(rings):
                wake_node = ring

                for ndx in range(n_k):
                    for ddx in range(d):

                        local_name = 'vortex_strength_' + str(kite) + '_' + str(ring) + '_' + str(ndx) + '_' + str(ddx)

                        variables = struct_op.get_variables_at_time(options, V, Xdot, model.variables, ndx, ddx)
                        wg_local = tools.get_ring_strength(variables, kite, ring)

                        ndx_shed = n_k - 1 - wake_node
                        ddx_shed = d - 1

                        # working out:
                        # n_k = 3
                        # if ndx = 0 and ddx = 0 -> shed: wn >= n_k
                        #     wn: 0 sheds at ndx = 2, ddx = -1 : unshed,    period = 0
                        #     wn: 1 sheds at ndx = 1, ddx = -1 : unshed,    period = 0
                        #     wn: 2 sheds at ndx = 0, ddx = -1 : unshed,    period = 0
                        #     wn: 3 sheds at ndx = -1, ddx = -1 : SHED      period = 1
                        #     wn: 4 sheds at ndx = -2,                      period = 1
                        #     wn: 5 sheds at ndx = -3                       period = 1
                        #     wn: 6 sheds at ndx = -4                       period = 2
                        # if ndx = 1 and ddx = 0 -> shed: wn >= n_k - ndx
                        #     wn: 0 sheds at ndx = 2, ddx = -1 : unshed,
                        #     wn: 1 sheds at ndx = 1, ddx = -1 : unshed,
                        #     wn: 2 sheds at ndx = 0, ddx = -1 : SHED,
                        #     wn: 3 sheds at ndx = -1, ddx = -1 : SHED
                        # if ndx = 0 and ddx = -1 -> shed:
                        #     wn: 0 sheds at ndx = 2, ddx = -1 : unshed,
                        #     wn: 1 sheds at ndx = 1, ddx = -1 : unshed,
                        #     wn: 2 sheds at ndx = 0, ddx = -1 : SHED,
                        #     wn: 3 sheds at ndx = -1, ddx = -1 : SHED

                        already_shed = False
                        if (ndx > ndx_shed):
                            already_shed = True
                        elif ((ndx == ndx_shed) and (ddx == ddx_shed)):
                            already_shed = True

                        if already_shed:

                            # working out:
                            # n_k = 3
                            # period_0 -> wn 0, wn 1, wn 2 -> floor(ndx_shed / n_k)
                            # period_1 -> wn 3, wn 4, wn 5

                            period_number = int(np.floor(float(ndx_shed)/float(n_k)))
                            ndx_shed_w_periodicity = ndx_shed - period_number * n_k

                            gamma_val = Outputs['coll_outputs', ndx_shed_w_periodicity, ddx_shed, 'aerodynamics', 'circulation' + str(kite)]
                            wg_ref = 1. * gamma_val / strength_scale
                        else:
                            wg_ref = 0.

                        local_resi = (wg_local - wg_ref)

                        local_cstr = cstr_op.Constraint(expr = local_resi,
                                                        name = local_name,
                                                        cstr_type='eq')
                        cstr_list.append(local_cstr)

    return cstr_list
