from doe import doe_pbdesign, doe_ccf, doe_bbdesign
from copy import copy


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


if __name__ == '__main__':

    # some simple verification
    x = [1, 2, 3]
    res = calc_min_max(x=x)
    assert res == [[1.5, 2.5, 3.05], [1.5, 2.5, 2.95], [0.5, 1.5, 3.05], [0.5, 1.5, 2.95]]
