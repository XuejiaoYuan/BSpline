import numpy as np


def uniform_spaced(n):
    '''
    Calculate parameters using the uniform spaced method.
    :param n: the number of the data points
    :return: parameters
    '''
    parameters = np.linspace(0, 1, n)
    return parameters


def chord_length(n, P):
    '''
    Calculate parameters using the chord length method.
    :param n: the number of the data points
    :param P: data points
    :return: parameters
    '''
    parameters = np.zeros((1, n))
    for i in range(1, n):
        dis = np.sqrt(np.sum(np.square(P[i] - P[i-1])))     # square计算各元素的平方
        parameters[0][i] = parameters[0][i-1] + dis
    for i in range(1, n):
        parameters[0][i] = parameters[0][i]/parameters[0][n-1]
    return parameters[0]


def centripetal(n, P):
    '''
    Calculate parameters using the centripetal method.
    :param n: the number of data points
    :param P: data points
    :return: parameters
    '''
    a = 0.5
    parameters = np.zeros((1, n))
    for i in range(1, n):
        dis = np.sqrt(np.sum(np.square(P[i] - P[i-1])))
        parameters[0][i] = parameters[0][i-1] + np.power(dis, a)
    for i in range(1, n):
        parameters[0][i] = parameters[0][i] / parameters[0][n-1]
    return parameters[0]


def knot_vector(param, k, n):
    '''
    Generate knot vector.
    :param param: parameters
    :param k: degree
    :param n: the number of data points
    :return: knot vector
    '''
    m = n + k + 1
    knot = np.zeros((1, m))
    for i in range(k + 1):
        knot[0][i] = 0
    for i in range(m - k - 1, m):
        knot[0][i] = 1
    for i in range(k + 1, m - k - 1):
        for j in range(i - k, i):
            knot[0][i] = knot[0][i] + param[j]
        knot[0][i] = knot[0][i] / k
    return knot[0]