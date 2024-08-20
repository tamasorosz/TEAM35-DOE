from artap.algorithm_genetic import NSGAII
from artap.problem import Problem
from artap.individual import Individual
from team35_agros import FemModel
from artap.results import Results
import pylab as plt

from doe_error_estimations import error_estimation
from doe_metrics import DoEType

global x_base  # this will be the examined layout
CURRENT_BASE = 3.0


class F2EstimationSymmetric(Problem):
    def set(self):
        self.name = """ Calculation of the different errors considering symmetrical errors during the calculations. """

        self.parameters = [
            {"name": "x0", "bounds": [5.05, 30.0]},
            {"name": "x1", "bounds": [5.05, 30.0]},
            {"name": "x2", "bounds": [5.05, 30.0]},
            {"name": "x3", "bounds": [5.05, 30.0]},
            {"name": "x4", "bounds": [5.05, 30.0]},
            {"name": "x5", "bounds": [5.05, 30.0]},
            {"name": "x6", "bounds": [5.05, 30.0]},
            {"name": "x7", "bounds": [5.05, 30.0]},
            {"name": "x8", "bounds": [5.05, 30.0]},
            {"name": "x9", "bounds": [5.05, 30.0]},
            {"name": "current", "bounds": [2.95, 3.05]},
        ]

        self.costs = [{"name": "f_1", "criteria": "minimize"}, {"name": "f_2", "criteria": "minimize"}]

    def evaluate(self, individual):
        x = individual.vector

        # The examined case
        #x_base = [13.5, 12.5, 10.5, 6.5, 8.5, 7.5, 6.5, 6.5, 6.5, 6.5]
        #c_base = [3.0]

        #x_base = [x_base[i] + x[i] for i in range(10)] # positional errors
        #c_base = 20 * [c_base[0] + x[10]] # currents

        x_base = x[:10]
        c_base = 20 * [x[10]]
        f1, f2 = error_estimation(x_base, c_base, doe_method=DoEType.MINMAX, is_current=True, is_optimization=True)

        return [f1, f2]


if __name__ == "__main__":
    problem = F2EstimationSymmetric()
    algorithm = NSGAII(problem)
    algorithm.options["max_population_number"] = 40
    algorithm.options["max_population_size"] = 40
    algorithm.options['max_processes'] = 1
    algorithm.run()

    results = Results(problem)

    list_of_inds = results.problem.individuals

    print("List of individuals: \n")
    for elem in list_of_inds:
        print(elem, "\n")

    table = results.pareto_values()

    print("Pareto - values after the last iteration:")
    print(table)

    x_values = [item[0] for item in table]
    y_values = [item[1] for item in table]
    plt.plot(x_values,y_values, 'o')
    plt.grid()

    plt.xlabel(r'$F_1/B_0$ [%]', fontsize=16)
    plt.ylabel(r'$F_2/F1$ [%]', fontsize=16)
    plt.show()
