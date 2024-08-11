from math import inf
from operator import itemgetter

from artap.algorithm_genetic import NSGAII
from artap.problem import Problem
from artap.individual import Individual
from team35_agros import FemModel
from artap.results import Results

from copy import copy, deepcopy
from sklearn.metrics import max_error

from doe import doe_ccf, doe_pbdesign, doe_bbdesign

global x_base  # this will be the examined layout


class F2Estimation(Problem):
    def set(self):
        self.name = """ The goal of this calculation to estimate the error in a single case with different doe metrics. """

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
            {"name": "x11", "bounds": [-0.5, 0.5]},
            {"name": "x12", "bounds": [-0.5, 0.5]},
            {"name": "x13", "bounds": [-0.5, 0.5]},
            {"name": "x14", "bounds": [-0.5, 0.5]},
            {"name": "x15", "bounds": [-0.5, 0.5]},
            {"name": "x16", "bounds": [-0.5, 0.5]},
            {"name": "x17", "bounds": [-0.5, 0.5]},
            {"name": "x18", "bounds": [-0.5, 0.5]},
            {"name": "x19", "bounds": [-0.5, 0.5]},
            {"current": "x20", "bounds": [-0.15, 0.15]},
        ]

        self.costs = [{"name": "f_1", "criteria": "minimize"}]

    def evaluate(self, individual):
        x = individual.vector

        radii_vector = [x_base[i] + x[i] for i in range(20)]
        print("radii_vector: ", radii_vector)
        simulation = FemModel(radiis=radii_vector, current_density=current_density)
        f1 = simulation.fem_simulation()
        return [-f1]


if __name__ == "__main__":
    print("Calculating the f1 metric in the base layout")
    x_base = [13.5, 12.5, 10.5, 6.5, 8.5, 7.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.5, 8.5, 6.5, 10.5, 12.5, 13.5]
    current_density = 20 * [3.0]

    # calculates the base scenario
    simulation = FemModel(radiis=x_base, current_density=current_density)
    f1 = simulation.fem_simulation()
    print("original f1: ", f1)

    problem = F2Estimation()
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
