from doe import doe_pbdesign, doe_ccf, doe_bbdesign
from copy import copy
from enum import Enum


# from team35_agros import FemModel

class DoEType(Enum):
    PB = 1
    CCF = 2
    BB = 3


def calc_min_max(x: list, delta_pos=0.5, delta_curr=0.05):
    """

    :param x: list of the optimization vector
    :param delta_pos: positioning error
    :param delta_curr: current setting error
    :return: list of vectors, which should be resolved to calculate the
    """
    x_p = [x[i] + delta_pos for i in range(len(x) - 1)]
    x_n = [x[i] - delta_pos for i in range(len(x) - 1)]

    # 1
    x_pp = copy(x_p)
    x_pp.append(x[-1] + delta_curr)

    # 2
    x_pn = copy(x_p)
    x_pn.append(x[-1] - delta_curr)

    # 3
    x_np = copy(x_n)
    x_np.append(x[-1] + delta_curr)

    # 4
    x_nn = copy(x_n)
    x_nn.append(x[-1] - delta_curr)

    return [x_pp, x_pn, x_np, x_nn]


def calc_doe_meausere(x: list, doe_type: DoEType, delta_pos=0.5, delta_curr=0.05):
    n = len(x)

    doe_lists = []

    if doe_type == DoEType.PB:
        doe_lists = doe_pbdesign(n)

    elif doe_type == DoEType.BB:
        doe_lists = doe_bbdesign(n)

    elif doe_type == DoEType.CCF:
        doe_lists = doe_ccf(n)

    result_list = []
    print("length of the doe list:", len(doe_lists))
    for doe_factors in doe_lists:
        # position errors
        temp = [doe_factors[i] * delta_pos + x[i] for i in range(len(doe_factors) - 1)]
        # error in the current setup
        temp.extend([doe_factors[-1] * delta_curr + x[-1]])
        result_list.append(copy(temp))
    return result_list


if __name__ == '__main__':
    # some simple verification
    x = [1, 2, 3]
    res = calc_min_max(x=x)
    assert res == [[1.5, 2.5, 3.05], [1.5, 2.5, 2.95], [0.5, 1.5, 3.05], [0.5, 1.5, 2.95]]

    # verify doe selection
    x = [1, 2, 3,4,5,6,7,8,9,10,11]
    res = calc_doe_meausere(x=x, doe_type=DoEType.BB)
    print(res)
    assert res == [[0.5, 1.5, 3.0], [0.5, 2.5, 3.0], [1.5, 1.5, 3.0], [1.5, 2.5, 3.0], [0.5, 2.0, 2.95],
                   [0.5, 2.0, 3.05], [1.5, 2.0, 2.95], [1.5, 2.0, 3.05], [1.0, 1.5, 2.95], [1.0, 1.5, 3.05],
                   [1.0, 2.5, 2.95], [1.0, 2.5, 3.05], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]]
