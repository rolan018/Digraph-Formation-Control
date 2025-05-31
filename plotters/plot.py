from sat import Sat
import matplotlib.pyplot as plt

def plot_position(sats, ref_orbit, limit):
    ax = plt.figure().add_subplot(projection='3d')
    for i, sat in enumerate(sats):
        line, = ax.plot(sat.position_iso[0,:][:limit], sat.position_iso[1,:][:limit], sat.position_iso[2,:][:limit])
        ax.plot(sat.position_iso[0,0], sat.position_iso[1,0], sat.position_iso[2,0], 'rp', markersize=4)
        line.set_linestyle("--")
        line.set_label(r'$sat_{%s}$' % i)
    ax.legend()
    plt.show()

def plot_c1(sats: list[Sat], t, lim, sat_1=None, x_loss_1=None, x_restart_1=None, sat_2=None, x_loss_2=None, x_restart_2=None):
    ax = plt.figure().add_subplot()
    ax.set_xlabel('T, c')
    ax.set_ylabel(r'$C_1$, км')
    for i, sat in enumerate(sats):
        line, = ax.plot(t[:lim], [-c/10000 for c in sat.c1[:lim]])

    if sat_1:
        sat_i = sat_1.split("_")[1]
        if x_loss_1:
            plt.axvline(x=x_loss_1, color='red', ls='--', label=r'$sat_{%s}$ потеря сигнала' % sat_i)
        if x_restart_1:
            plt.axvline(x=x_restart_1, color='blue', ls='--', label=r'$sat_{%s}$ восстановление сигнала' % sat_i)
    if sat_2:
        sat_i = sat_2.split("_")[1]
        if x_loss_2:
            plt.axvline(x=x_loss_2, color='red', ls='--', label=r'$sat_{%s}$ потеря сигнала' % sat_i)
        if x_restart_2:
            plt.axvline(x=x_restart_2, color='blue', ls='--', label=r'$sat_{%s}$ восстановление сигнала' % sat_i)
    ax.legend()
    plt.show()

def plot_1d(t, metrics, description):
    ax = plt.figure().add_subplot()
    ax.set_xlabel('T')
    ax.set_ylabel(description)
    for i, metric in enumerate(metrics):   
        line, = ax.plot(t, metric)
        line.set_label(f'{description}_{i}')
    ax.legend()
    plt.show()

def plot_upr(sats: list[Sat], t, lim):
    ax = plt.figure().add_subplot()
    ax.set_xlabel(r'T, c')
    ax.set_ylabel(r'Управление, $м/c^2$')
    for i, sat in enumerate(sats):
        line, = ax.plot(t[:lim], sat.norm_control[:lim])
    ax.legend()
    plt.show()