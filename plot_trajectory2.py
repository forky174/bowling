import numpy as np
from matplotlib import pyplot as plt

def plot_single_trajectory(x, y):
    fig, ax = plt.subplots(figsize=(2,8))

    plt.xlabel('x, m',fontsize=12)
    plt.ylabel('y, m',fontsize=12)

    x_ticks = np.arange(0, 1092, 27.3*13)/1000
    x_minor_ticks = np.arange(0, 1092, 27.3)/1000
    y_ticks = np.arange(0, 20, 1)

    ax.xaxis.set_ticks(x_ticks)
    ax.xaxis.set_ticks(x_minor_ticks, minor=True)
    ax.yaxis.set_ticks(y_ticks)

    ax.grid(alpha=0.3, linewidth=0.5, which='major')
    ax.grid(alpha=0.2, linewidth=0.3, which='minor')

    ax.plot(x, y, linestyle = ' ', marker='.', ms = 4, color='#0066CC')

    ax.set_xlim((0, 1.065))
    ax.set_ylim((0, 19.156))

    plt.show()

def plot_trajectory(x, y, x_raw, y_raw, label, oil_length):
    fig, ax = plt.subplots(figsize=(2,8))

    plt.xlabel('x, m', fontsize=12)
    plt.ylabel('y, m', fontsize=12)

    x_ticks = np.arange(0, 1092, 27.3 * 13) / 1000
    x_minor_ticks = np.arange(0, 1092, 27.3) / 1000
    y_ticks = np.arange(0, 20, 1)

    ax.xaxis.set_ticks(x_ticks)
    ax.xaxis.set_ticks(x_minor_ticks, minor=True)
    ax.yaxis.set_ticks(y_ticks)

    ax.grid(alpha=0.3, linewidth=0.5, which='major')
    ax.grid(alpha=0.2, linewidth=0.3, which='minor')

    ax.axhline(y=oil_length, color='r', linestyle='-')
    ax.text(0.25, oil_length+0.3, 'oil length', fontsize=8, va='center', ha='center', color='r')
    ax.plot(x_raw, y_raw, linestyle=' ', marker='.', ms=4, color='green', label='raw')
    # ax.plot(x, y, linestyle=' ', marker='.', ms=4, color='green', label=label)
    ax.plot(x, y, linestyle='-', linewidth=1, color='blue', label=label)

    ax.set_xlim((0, 1.065))
    ax.set_ylim((0, 19.156))

    ax.legend()
    plt.show()