from sat import Sat
import matplotlib.pyplot as plt

def plot_position(sats):
    ax = plt.figure().add_subplot(projection='3d')
    for i, sat in enumerate(sats):
        line, = ax.plot(sat.position_iso[0, :], sat.position_iso[1, :], sat.position_iso[2, :],linestyle='--')
        line.set_label(f'sat_{i}')
    ax.legend()
    plt.show()

def plot_c1(sats: list[Sat], t, description):
    ax = plt.figure().add_subplot()
    ax.set_xlabel('T')
    ax.set_ylabel(description)
    for sat in sats:
        ax.plot(t, sat.c1)

    plt.title(f'{description}(T)')

    plt.show()
