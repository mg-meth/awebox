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

        radius = parameters['theta0','ground_station','r_gen']
        j_winch = parameters['theta0','ground_station','j_winch']
        f_c = parameters['theta0','ground_station','f_c']
        l_t_full = variables_si['theta']['l_t_full']
        phi = (l_t_full- variables_si['xd']['l_t']) / radius
        omega = - variables_si['xd']['dl_t'] / radius
        domega =  -variables_si['xddot']['ddl_t'] / radius
        t_tether = -variables_si['xa']['lambda10'] * variables_si['xd']['l_t'] * radius
        t_frict = -f_c * omega
        t_inertia = j_winch * domega
        #t_inertia += options['scaling']['theta']['diam_t']**2 / 4 * np.pi * parameters['theta0', 'tether', 'rho']*radius**3 * (omega*omega + domega*phi) #

        rhs = t_tether + t_em + t_frict
        lhs = t_inertia


        i_sd = variables_si['xd']['i_s'][0]
        i_sq = variables_si['xd']['i_s'][1]
        torque = (((6*(0.892*i_sq))-(0.25*((variables_si['xa']['lambda10'])*(variables_si['xd']['l_t']))))+(1.57*((variables_si['xddot']['ddl_t'] )/0.25)))

        print("torque")
        print(torque)
        torque = rhs - lhs

        winch_cstr = cstr_op.Constraint(expr=torque, name='winch', cstr_type='eq')
        cstr_list.append(winch_cstr)

        if options['generator']['type'] == 'pmsm':
            generator = generator_ode(options, variables_si, outputs, parameters, architecture)
            cstr_list.append(generator)

    return cstr_list

def t_em_ode(options, variables_si, outputs, parameters, architecture):

    if options['generator']['type'] == 'pmsm':
        i_sd = variables_si['xd']['i_s'][0]
        i_sq = variables_si['xd']['i_s'][1]
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
        v_sd = variables_si['u']['v_s'][0]
        v_sq = variables_si['u']['v_s'][1]
        i_sd = variables_si['xd']['i_s'][0]
        i_sq = variables_si['xd']['i_s'][1]
        di_sd = variables_si['xddot']['di_s'][0]
        di_sq = variables_si['xddot']['di_s'][1]
        ld = parameters['theta0','generator','l_d']
        lq =parameters['theta0','generator','l_q']
        rs = parameters['theta0','generator','r_s']
        phi_f = parameters['theta0','generator','phi_f']
        p_p = parameters['theta0','generator','p_p']

        i_sq_ode = ((((v_sq+(0.02*i_sq))+(0.001*di_sq))-(0.892*(4*((variables_si['xd']['dl_t'])/0.25))))-((0.001*(4*((variables_si['xd']['dl_t'])/0.25)))*i_sd))
        i_sd_ode = (((v_sd+(0.02*i_sd))+(0.001*di_sd))+((0.001*(4*((variables_si['xd']['dl_t'])/0.25)))*i_sq))

        print("i_sq_ode")
        print(i_sq_ode)
        print("i_sd_ode")
        print(i_sd_ode)

        i_sq_ode = v_sq + rs*i_sq + lq*di_sq + p_p*omega*phi_f + p_p*omega*ld*i_sd
        i_sd_ode = v_sd + rs*i_sd + ld*di_sd - p_p*omega*lq*i_sq

        i_sd_cstr = cstr_op.Constraint(expr=i_sd_ode, name='gen0', cstr_type='eq')
        cstr_list.append(i_sd_cstr)

        i_sq_cstr = cstr_op.Constraint(expr=i_sq_ode, name='gen1', cstr_type='eq')
        cstr_list.append(i_sq_cstr)

    return cstr_list



"""
i_sd_cstr
(30-xd_i_s_0)
i_sq_cstr
(30-xd_i_s_1)
i_sd_ode
@1=0.001, (((u_v_s_0+(0.02*xd_i_s_0))+(@1*xddot_di_s_0))+((@1*(4*((500*xd_dl_t)/0.25)))*xd_i_s_1))
i_sq_ode
@1=0.001, @2=4, @3=((500*xd_dl_t)/0.25), ((((u_v_s_1+(0.02*xd_i_s_1))+(@1*xddot_di_s_1))-(0.892*(@2*@3)))-((@1*(@2*@3))*xd_i_s_0))
(500*theta_l_t_full)
phi
@1=500, (((@1*theta_l_t_full)-(@1*xd_l_t))/0.25)
lambda10
(8322.91*xa_lambda10)
t_inertia
(-(1.57*((500*xddot_ddl_t)/0.25)))
torque
@1=0.25, @2=500, (((6*(0.892*xd_i_s_1))-(@1*((8322.91*xa_lambda10)*(@2*xd_l_t))))+(1.57*((@2*xddot_ddl_t)/@1)))
p_el
(1.5*((u_v_s_0*xd_i_s_0)+(u_v_s_1*xd_i_s_1)))



@1=0.25, @2=500, (((6*(0.892*xd_i_s_1))-(@1*((261.094*xa_lambda10)*(@2*xd_l_t))))+(1.57*((@2*xddot_ddl_t)/@1)))
i_sq_ode
@1=0.001, @2=4, @3=((500*xd_dl_t)/0.25), ((((u_v_s_1+(0.02*xd_i_s_1))+(@1*xddot_di_s_1))-(0.892*(@2*@3)))-((@1*(@2*@3)*xd_i_s_0))
i_sd_ode
@1=0.001, (((u_v_s_0+(0.02*xd_i_s_0))+(@1*xddot_di_s_0))+((@1*(4*((500*xd_dl_t)/0.25)))*xd_i_s_1))
"""
