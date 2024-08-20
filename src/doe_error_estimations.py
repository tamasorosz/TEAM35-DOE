from copy import copy

from team35_agros import FemModel
from doe_metrics import calc_doe_meausere, DoEType

B_00 = 2.0 * 1e-3  # 2 mT


def error_estimation(x_base: list, c_base: list, doe_method=DoEType.PB, is_current=True, is_optimization=False):
    print("Calculation starts")

    # Create the radii vector by mirroring x_base
    reversed_x_base = x_base[::-1]
    radii_vector = x_base + reversed_x_base

    # Perform the initial simulation
    simulation = FemModel(radiis=radii_vector, current_density=c_base)
    f1_00 = simulation.fem_simulation()
    print("Original f1:", f1_00)

    # Generate DOE (Design of Experiments) positions
    if is_current:
        x = x_base[:10] + [c_base[0]]
    else:
        x = x_base[:10]

    x_list = calc_doe_meausere(x, doe_type=doe_method, delta_pos=0.5, delta_curr=0.05, is_curr=is_current)
    print("Number of evaluations:", len(x_list))

    # Calculate maximum error
    f1_max = 0.0
    max_vector = []
    for index, x_values in enumerate(x_list):
        if not is_optimization:
            print(f"Round: {index + 1} of {len(x_list)}")

        # Create a radii vector by mirroring the first 10 x_values
        radii_vector = x_values[:10] + x_values[:10][::-1]

        # Use the last x_value as current density
        if is_current:
            current_density = [x_values[-1]] * 20
        else:
            current_density = c_base

        # Perform the simulation
        simulation = FemModel(radiis=radii_vector, current_density=current_density)
        f1 = simulation.fem_simulation()

        # Update the maximum error
        error = abs(f1 - f1_00)
        if not is_optimization:
            print(f"f1: {f1}, error: {error}, radii_vector: {radii_vector}, current density: {current_density[0]}")

        if f1_max < error:
            f1_max = error
            max_vector = copy(radii_vector)

    if not is_optimization:
        # Calculate and print error percentage
        error_percentage = (f1_max / f1_00) * 100.0
        print(f"Error estimate: {error_percentage:.2f}%, absolute: {f1_max}")
        print(f"Solution vector: {max_vector}")

        simulation = FemModel(radiis=max_vector, current_density=c_base)
        f1_00 = simulation.fem_simulation(with_plot=True)
        print("worst case calculation: ", f1_00)
    else:
        # print(f1_00, (f1_max / f1_00) * 100.0)
        return f1_00/B_00*100.0, (f1_max / f1_00) * 100.0


if __name__ == '__main__':
    print("Calculating the f1 metric in the base layout")
    x_base = [13.5, 12.5, 10.5, 6.5, 8.5, 7.5, 6.5, 6.5, 6.5, 6.5]
    c_base = 20 * [3.0]

    error_estimation(x_base, c_base, doe_method=DoEType.SOBOL, is_current=True)
