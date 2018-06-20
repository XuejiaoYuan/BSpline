import numpy as np


def uniform_spaced(n):
    parameters = np.linspace(0, 1, n)
    return parameters


def chord_length(n, P):
    parameters = np.zeros((1, n))
    for i in range(1, n):
        dis = np.sqrt(np.sum(np.square(P[i] - P[i-1])))     # square计算各元素的平方
        parameters[0][i] = parameters[0][i-1] + dis
    for i in range(1, n):
        parameters[0][i] = parameters[0][i]/parameters[0][n-1]
    return parameters[0]


def centripetal(n, P):
    '''
    :param n: 控制点数目
    :param P: 数据点
    :return: 数据点对应参数
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
    :param param: 参数
    :param k: 阶数
    :param n: 控制点数目
    :return: 节点向量
    '''
    m = n + k
    knot = np.zeros((1, m))
    for i in range(k):
        knot[0][i] = 0
    for i in range(m - k, m):
        knot[0][i] = 1
    for i in range(k, m - k):
        for j in range(i - k + 1, i):
            knot[0][i] = knot[0][i] + param[j]
        knot[0][i] = knot[0][i] / (k - 1)
    return knot[0]