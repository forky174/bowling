import numpy as np

def get_initial_parameters(time, x, y, oil_length):

    mask = y < oil_length
    time, x, y = time[mask], x[mask], y[mask]

    coef_x = np.polyfit(time, x, 2)
    coef_y = np.polyfit(time, y, 2)

    p_x = np.poly1d(coef_x)
    p_y = np.poly1d(coef_y)

    x_smoothed = p_x(time)
    y_smoothed = p_y(time)

    x0 = coef_x[2]
    y0 = coef_y[2]

    u0 = coef_x[1]
    v0 = coef_y[1]

    g = 9.81  # m/s^2

    c = coef_y[0] / coef_x[0]
    mu = -2 * coef_y[0] * np.sqrt(1 + c ** 2) / c / g

    return(x0, y0, u0, v0, mu, c)