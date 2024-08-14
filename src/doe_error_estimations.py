from team35_agros import FemModel
from copy import copy
from doe_metrics import calc_doe_meausere, DoEType


def error_estimation(x_base: list, c_base: list):
    # calculates the base scenario
    simulation = FemModel(radiis=x_base, current_density=c_base)
    f1_00 = simulation.fem_simulation()
    print("original f1: ", f1_00)

    # calculates a list of list with the doe position errors
    x = x_base + [c_base[0]]
    x_list = calc_doe_meausere(x, doe_type=DoEType.CCF, delta_pos=0.5, delta_curr=0.05)
    print("Number of evaluations: ", len(x_list))
    f1_max = 0.0
    for x_values in x_list:
        radii_vector = [x_values[i] for i in range(10)]
        reversed = copy(radii_vector)
        reversed.reverse()

        radii_vector = radii_vector + reversed
        print(len(radii_vector), radii_vector)
        # current density
        c_dens = x_values[-1]
        print("current density:", c_dens)
        current_density = 20 * [c_dens]
        print("radii_vector: ", radii_vector)

        simulation = FemModel(radiis=radii_vector, current_density=current_density)
        f1 = simulation.fem_simulation()
        error = f1 - f1_00
        f1_max = max(f1_max, error)

    error_percentage = f1_max / f1_00 * 100.0
    print("Error estimate: ", error_percentage, "[%], absolute:", f1_max)


if __name__ == '__main__':
    print("Calculating the f1 metric in the base layout")
    x_base = [13.5, 12.5, 10.5, 6.5, 8.5, 7.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.5, 8.5, 6.5, 10.5, 12.5, 13.5]
    c_base = 20 * [3.0]

    error_estimation(x_base, c_base)