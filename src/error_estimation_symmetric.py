from artap.algorithm_genetic import NSGAII
from artap.problem import Problem
from artap.individual import Individual
from team35_agros import FemModel
from artap.results import Results

from copy import copy, deepcopy
from sklearn.metrics import max_error

from doe import doe_ccf, doe_pbdesign, doe_bbdesign

global x_base  # this will be the examined layout
CURRENT_BASE = 3.0


class F2EstimationSymmetric(Problem):
    def set(self):
        self.name = """ Calculation of the different errors considering symmetrical errors during the calculations. """

        self.parameters = [
            {"name": "x0", "bounds": [-0.5, 0.5]},
            {"name": "x1", "bounds": [-0.5, 0.5]},
            {"name": "x2", "bounds": [-0.5, 0.5]},
            {"name": "x3", "bounds": [-0.5, 0.5]},
            {"name": "x4", "bounds": [-0.5, 0.5]},
            {"name": "x5", "bounds": [-0.5, 0.5]},
            {"name": "x6", "bounds": [-0.5, 0.5]},
            {"name": "x7", "bounds": [-0.5, 0.5]},
            {"name": "x8", "bounds": [-0.5, 0.5]},
            {"name": "x9", "bounds": [-0.5, 0.5]},
            {"name": "x10", "bounds": [-0.5, 0.5]},
            {"name": "current", "bounds": [-0.15, 0.15]},
        ]

        self.costs = [{"name": "f_1", "criteria": "minimize"}]

    def evaluate(self, individual):
        x = individual.vector

        radii_vector = [x_base[i] + x[i] for i in range(10)]
        reversed = copy(radii_vector)
        reversed.reverse()
        radii_vector = radii_vector + reversed
        print(len(radii_vector),radii_vector)
        # current density
        c_dens = 3.0 + x[10]
        print("current density:", c_dens)
        current_density = 20*[c_dens]
        print("radii_vector: ", radii_vector)
        simulation = FemModel(radiis=radii_vector, current_density=current_density)
        f1 = simulation.fem_simulation()
        return [-f1]


if __name__ == "__main__":
    print("Calculating the f1 metric in the base layout")
    x_base = [13.5, 12.5, 10.5, 6.5, 8.5, 7.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.5, 8.5, 6.5, 10.5, 12.5, 13.5]
    c_base = 20 * [3.0]
    # calculates the base scenario
    simulation = FemModel(radiis=x_base, current_density=c_base)
    f1 = simulation.fem_simulation()
    print("original f1: ", f1)

    problem = F2EstimationSymmetric()
    algorithm = NSGAII(problem)
    algorithm.options["max_population_number"] = 30
    algorithm.options["max_population_size"] = 30
    algorithm.options['max_processes'] = 1
    algorithm.run()

    results = Results(problem)
    optimum = results.find_optimum(name="f_1")
    print("maximal value of the f1:", optimum.costs)
    print("combination of errors:", optimum.vector)
    print("deviation from f1 [%]:", round(abs(f1 + optimum.costs[0]) / f1 * 100))
