import BaseFunction as bf
import numpy as np


def curve_interpolation(D, N, k, param, knot):
    '''
    Given a set of N data points, D0, D1, ..., Dn and a degree k,
    find a B-spline curve of degree k defined by N control points
    that passes all data points in the given order.
    :param D: data points (N x 2)
    :param N: the number of data points
    :param k: degree
    :param param: parameters
    :param knot: knot vector
    :return: control points (N x 2)
    '''
    Nik = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            Nik[i][j] = bf.BaseFunction(j, k+1, param[i], knot)
    print(Nik)
    # P =  np.zeros((N, 2))        # control points
    Nik_inv = np.linalg.inv(Nik)
    print(Nik_inv)
    P = np.dot(Nik_inv, D)
    return P


def curve_approximation(D, N, H, k, param, knot):
    '''
    Given a set of N data points, D0, D1, ..., Dn, a degree k,
    and a number H, where N > H > k >= 1, find a B-spline curve
    of degree k defined by H control points that satisfies the
    following conditions:
        1. this curve contains the first and last data points;
        2. this curve approximates the data polygon in the sense
        of least square;
    :param D: data points (N x 2)
    :param H: the number of control points
    :param k: degree
    :param param: parameters
    :param knot: knot vector
    :return: control points (H x 2)
    '''
    P = np.zeros((H, 2))
    if H >= N or H <= k:
        print('Parameter H is out of range')
        return P

    P[0] = D[0]
    P[H-1] = D[N-1]
    Qk = np.zeros((N-2, 2))
    Nik = np.zeros((N, H))
    for i in range(N):
        for j in range(H):
            Nik[i][j] = bf.BaseFunction(j, k+1, param[i], knot)
    print(Nik)

    for j in range(1, N-1):
        Qk[j-1] = D[j] - Nik[j][0]*P[0] - Nik[j][H-1]*P[H-1]

    N_part = Nik[1: N - 1, 1: H - 1]
    print(N_part)
    Q = np.dot(N_part.transpose(), Qk)
    print(Q)
    M = np.dot(np.transpose(N_part), N_part)
    P[1:H-1] = np.dot(np.linalg.inv(M), Q)
    print(P)
    return P


def curve(P, N, k, param, knot):
    '''
    Calculate B-spline curve.
    :param P: Control points
    :param N: the number of control points
    :param k: degree
    :param param: parameters
    :param knot: knot vector
    :return: data point on the b-spline curve
    '''
    Nik = np.zeros((len(param), N))

    for i in range(len(param)):
        for j in range(N):
            Nik[i][j] = bf.BaseFunction(j, k+1, param[i], knot)
    D = np.dot(Nik, P)
    return D