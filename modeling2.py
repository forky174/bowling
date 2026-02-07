import numpy as np
from scipy import integrate

def slip(t, p, oil_mu, floor_mu, oil_length):

    x, y, u, v, wx, wy, wz = p[0], p[1], p[2], p[3], p[4], p[5], p[6]

    r = 0.109
    g = 9.81

    if y > oil_length:      mu = floor_mu
    else:                   mu = oil_mu

    temp_x = u - r * wy
    temp_y = v + r * wx
    tau = 1 / np.sqrt(temp_x**2 + temp_y**2)
    tau_x = tau * temp_x
    tau_y = tau * temp_y

    return [
        u,
        v,
        -mu * g * tau_x,
        -mu * g * tau_y,
        -2.5 * mu * g * tau_y / r,
        2.5 * mu * g * tau_x / r,
        0
    ]

def roll(t, p, oil_mu, floor_mu, oil_length):

    x, y, u, v, wx, wy, wz = p[0], p[1], p[2], p[3], p[4], p[5], p[6]

    r = 0.109
    g = 9.81

    if y > oil_length:      mu = floor_mu
    else:                   mu = oil_mu

    return [
        u,
        v,
        r * wy,
        -r * wx,
        0,
        0,
        0
    ]

def first_loc_min(array):
    array = array.tolist()
    return [i for i in range(1, len(array)-1) if array[i] < array[i-1] and array[i] < array[i+1]][0]

def model(x0, y0, u0, v0, wx0, wy0, wz0, oil_mu, floor_mu, oil_length):   #initial conditions: ball + lane

    r = 0.109
    lane_length = 18.288

    p0_slip = [x0, y0, u0, v0, wx0, wy0, wz0]
    t0_slip = 0
    t_final_slip = 5
    t_eval_slip = np.linspace(t0_slip, t_final_slip, 250)

    solution_slip = integrate.solve_ivp(slip, (t0_slip, t_final_slip), p0_slip, t_eval=t_eval_slip, args=(oil_mu, floor_mu, oil_length))

    x_slip, y_slip, u_slip, v_slip, wx_slip, wy_slip, wz_slip = solution_slip.y[0], solution_slip.y[1], solution_slip.y[2], solution_slip.y[3], solution_slip.y[4], solution_slip.y[
        5], solution_slip.y[6]
    t_slip = solution_slip.t

    Vc = np.sqrt((u_slip - r * wy_slip) ** 2 + (v_slip + r * wx_slip) ** 2)
    Vc_zero_index = first_loc_min(Vc)

    if y_slip[Vc_zero_index] >= lane_length:

        # print("Шар всё время катиться с проскальзыванием.")

        lane_end = np.where(y_slip > lane_length)[0][0] # если вызывать по этому коэффициенту, это будет вне дорожки; его нужно использовать только для границы с конца
        return (t_slip[:lane_end], x_slip[:lane_end], y_slip[:lane_end], u_slip[:lane_end], v_slip[:lane_end],
                wx_slip[:lane_end], wy_slip[:lane_end], wz_slip[:lane_end])

    # print("Шар начинает катиться без проскальзывания.")

    p0_roll = [x_slip[Vc_zero_index], y_slip[Vc_zero_index], u_slip[Vc_zero_index], v_slip[Vc_zero_index], wx_slip[Vc_zero_index], wy_slip[Vc_zero_index], wz_slip[Vc_zero_index]]

    t0_roll = t_slip[Vc_zero_index]
    t_final_roll = t0_roll + 5
    t_eval_roll = np.linspace(t0_roll, t_final_roll, 250)

    solution_roll = integrate.solve_ivp(roll, (t0_roll, t_final_roll), p0_roll, t_eval=t_eval_roll, args=(oil_mu, floor_mu, oil_length))

    x_roll, y_roll, u_roll, v_roll, wx_roll, wy_roll, wz_roll = solution_roll.y[0], solution_roll.y[1], solution_roll.y[2], solution_roll.y[3], solution_roll.y[4], solution_roll.y[
        5], solution_roll.y[6]
    t_roll = solution_roll.t

    lane_end = np.where(y_roll > lane_length)[0][0]

    return (np.concatenate((t_slip[:Vc_zero_index], t_roll[:lane_end])), np.concatenate((x_slip[:Vc_zero_index], x_roll[:lane_end])), np.concatenate((y_slip[:Vc_zero_index], y_roll[:lane_end])),
            np.concatenate((u_slip[:Vc_zero_index], u_roll[:lane_end])), np.concatenate((v_slip[:Vc_zero_index], v_roll[:lane_end])),
            np.concatenate((wx_slip[:Vc_zero_index], wx_roll[:lane_end])), np.concatenate((wy_slip[:Vc_zero_index], wy_roll[:lane_end])), np.concatenate((wz_slip[:Vc_zero_index], wz_roll[:lane_end])))