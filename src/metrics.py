from sklearn.metrics import max_error
from math import pi


def f1_score(b, b_0=2e-3):
    """ idea: check the results with different regression metrics
    :return: the first one gives back the origirnal problem
    """
    b0 = [b_0] * len(b)

    return max_error(b0, b)


def f2_robustness(f1: list, f1_0: float):
    """
    This metric calculates the robustness of a design with the given

    :param f1: a list of f1  values for any given case which contains a deviation from the ideal
    :param f1_0: the f1 value of the ideal case
    :return:
    """

    return max_error(f1_0, f1)


def f3_losses(r: list):
    """The power loss depends on the current if it can be varied."""
    return sum(2 * pi * turn.r_0 * turn.current ** 2 for turn in r)


def f4_masses(r: list):
    return sum(turn.r_0 for turn in r)
