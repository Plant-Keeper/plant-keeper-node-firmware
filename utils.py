"""
Generate model to scale analog data to user defined range
Source: http://code.activestate.com/recipes/578914-simple-linear-regression-with-pure-python/


"""

import math


def mean(xs):
    return sum(xs) / len(xs)


def std(xs, m):
    normalizer = len(xs) - 1
    return math.sqrt(sum((pow(x - m, 2) for x in xs)) / normalizer)


def pearson_r(xs, ys, m_x, m_y):
    sum_xy = 0
    sum_sq_v_x = 0
    sum_sq_v_y = 0

    for (x, y) in zip(xs, ys):
        var_x = x - m_x
        var_y = y - m_y
        sum_xy += var_x * var_y
        sum_sq_v_x += pow(var_x, 2)
        sum_sq_v_y += pow(var_y, 2)
    return sum_xy / math.sqrt(sum_sq_v_x * sum_sq_v_y)


def fit(x, y):
    """
    Fit and generate model function
    :param x: list
    :param y:
    :return:
    """
    m_x = mean(x)
    m_y = mean(y)
    r = pearson_r(x, y, m_x, m_y)

    b = r * (std(y, m_y) / std(x, m_x))
    a = m_y - b * m_x

    def model(_x):
        return b * _x + a

    return model
