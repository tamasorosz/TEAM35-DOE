from sklearn.metrics import mean_squared_error, max_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
from math import pi


def f1_score(b, b_0=2e-3):
    """ idea: check the results with different regression metrics
    :return: the first one gives back the origirnal problem
    """
    b0 = [b_0] * len(b)

    return max_error(b0, b), mean_absolute_error(b0, b), mean_squared_error(b0, b), r2_score(b0, b), mean_absolute_percentage_error(b0, b)


def f2_losses(r: list):
    """The power loss depends on the current if it can be varied."""
    return sum(2 * pi * turn.r_0 * turn.current ** 2 for turn in r)


def f2_masses(r: list):
    return sum(turn.r_0 for turn in r)