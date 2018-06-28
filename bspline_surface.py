import numpy as np
import parameter_selection as ps
import bspline_curve as bc


def surface_interpolation(D, p, q):
    '''
    Given a grid of (M x N) data points Dij and a degree (p, q),
    find a B-spline surface of degree (p, q) defined by (M x N)
    control points that passes all data points in the given order.
    :param D: data points
    :param p: degree of u direction
    :param q: degree of v direction
    :return: control points and knot vectors
    '''
    D_X = D[0]
    D_Y = D[1]
    D_Z = D[2]

    M = len(D_X)
    N = len(D_X[0])
    Q = [np.zeros((len(D_X), len(D_X[0]))).tolist(),
         np.zeros((len(D_Y), len(D_Y[0]))).tolist(),
         np.zeros((len(D_Z), len(D_Z[0]))).tolist()]
    knot_uv = [[], []]

    # calculate parameters and knot vector
    # D_col_X = D_X[0]
    # D_col_Y = [y[0] for y in D_Y]
    # D_col = [D_col_X, D_col_Y]
    # param_u = ps.centripetal(M, D_col)
    # knot_u = ps.knot_vector(param_u, p, M)
    #
    # D_row_X = D_X[0]
    # D_row_Y = D_Y[0]
    # D_row = [D_row_X, D_row_Y]
    # param_v = ps.centripetal(N, D_row)
    # knot_v = ps.knot_vector(param_v, q, N)
    #
    # knot_uv[0] = knot_u
    # knot_uv[1] = knot_v

    param_u = []
    tmp_param = np.zeros((1, M))
    for i in range(N):
        D_col_X = [x[i] for x in D_X]
        D_col_Y = [y[i] for y in D_Y]
        D_col_Z = [z[i] for z in D_Z]
        D_col = [D_col_X, D_col_Y, D_col_Z]
        tmp_param = tmp_param + np.array(ps.centripetal(M, D_col))
        # tmp_param = ps.centripetal(N, D_row)
        # param_u.append(np.average(np.array(tmp_param)))
    param_u = np.divide(tmp_param, N).tolist()[0]

    param_v = []
    tmp_param = np.zeros((1, N))
    for i in range(M):
        D_row_X = D_X[i]
        D_row_Y = D_Y[i]
        D_row_Z = D_Z[i]
        D_row = [D_row_X, D_row_Y, D_row_Z]
        tmp_param = tmp_param + np.array(ps.centripetal(N, D_row))
        # param_v.append(np.average(np.array(tmp_param)))
    param_v = np.divide(tmp_param, M).tolist()[0]

    knot_uv[0] = ps.knot_vector(param_u, p, M)
    knot_uv[1] = ps.knot_vector(param_v, q, N)

    print(param_u)
    print(param_v)

    # calculate control points for every column
    for i in range(N):
        D_col_X = [x[i] for x in D_X]
        D_col_Y = [y[i] for y in D_Y]
        D_col_Z = [z[i] for z in D_Z]
        D_col = [D_col_X, D_col_Y, D_col_Z]
        Q_col = bc.curve_interpolation(D_col, M, p, param_u, knot_uv[0])
        for j in range(M):
            Q[0][j][i] = Q_col[0][j]
            Q[1][j][i] = Q_col[1][j]
            Q[2][j][i] = Q_col[2][j]

    P = Q
    # calculate control points for every row
    for i in range(M):
        Q_row = [Q[0][i], Q[1][i], Q[2][i]]
        P_ = bc.curve_interpolation(Q_row, N, q, param_v, knot_uv[1])
        P[0][i] = P_[0]
        P[1][i] = P_[1]
        P[2][i] = P_[2]

    return P, knot_uv


def surface_approximation(D, p, q, E, F):
    '''
    Given a grid of (M x N) data points Dij, a degree (p, q), and e and f
    satisfying M > E > p >= 1 and N > F > q >= 1, find a B-spline surface
    of degree (p, q) defined by (E x F) control points Pij that approximates
    the data point grid in the given order.
    :param D: data points
    :param p: degree of u direction
    :param q: degree of v direction
    :return: control points
    '''
    D_X = D[0]
    D_Y = D[1]
    D_Z = D[2]

    M = len(D_X)
    N = len(D_X[0])

    knot_uv = [[], []]

    # calculate parameters and knot vector
    tmp_param = np.zeros((1, M))
    for i in range(N):
        D_col_X = [x[i] for x in D_X]
        D_col_Y = [y[i] for y in D_Y]
        D_col_Z = [z[i] for z in D_Z]
        D_col = [D_col_X, D_col_Y, D_col_Z]
        tmp_param = tmp_param + np.array(ps.centripetal(M, D_col))
    param_u = np.divide(tmp_param, N).tolist()[0]

    param_v = []
    tmp_param = np.zeros((1, N))
    for i in range(M):
        D_row_X = D_X[i]
        D_row_Y = D_Y[i]
        D_row_Z = D_Z[i]
        D_row = [D_row_X, D_row_Y, D_row_Z]
        tmp_param = tmp_param + np.array(ps.centripetal(N, D_row))
    param_v = np.divide(tmp_param, M).tolist()[0]

    knot_uv[0] = ps.knot_vector(param_u, p, M)
    knot_uv[1] = ps.knot_vector(param_v, q, N)

    # calculate control points for every column
    Q = [np.zeros((E, N)).tolist(),
         np.zeros((E, N)).tolist(),
         np.zeros((E, N)).tolist()]
    for i in range(N):
        D_col_X = [x[i] for x in D_X]
        D_col_Y = [y[i] for y in D_Y]
        D_col_Z = [z[i] for z in D_Z]
        D_col = [D_col_X, D_col_Y, D_col_Z]
        Q_col = bc.curve_approximation(D_col, M, E, p, param_u, knot_uv[0])
        print(Q_col)
        for j in range(E):
            Q[0][j][i] = Q_col[0][j]
            Q[1][j][i] = Q_col[1][j]
            Q[2][j][i] = Q_col[2][j]

    # calculate control points for every row
    P = [np.zeros((E, F)).tolist(),
         np.zeros((E, F)).tolist(),
         np.zeros((E, F)).tolist()]
    for i in range(E):
        Q_row = [Q[0][i], Q[1][i], Q[2][i]]
        P_ = bc.curve_approximation(Q_row, N, F, q, param_v, knot_uv[1])
        P[0][i] = P_[0]
        P[1][i] = P_[1]
        P[2][i] = P_[2]

    return P


def surface(P, p, q, piece_uv, knot_uv):
    '''
    Calculate points on the surface.
    :param P: control points
    :param p: degree of u direction (u)
    :param q: degree of v direction (v)
    :param piece_uv: the number of points on u/v direction
    :return: data points on the surface
    '''
    P_X = P[0]
    P_Y = P[1]
    P_Z = P[2]
    M = len(P_X)
    N = len(P_X[0])

    param_u = np.linspace(0, 1, piece_uv[0])
    param_v = np.linspace(0, 1, piece_uv[1])

    Nik_u = np.zeros((piece_uv[0], M)).tolist()
    Nik_v = np.zeros((piece_uv[1], N)).tolist()

    D_tmp = [np.zeros((piece_uv[0], N)).tolist(),
             np.zeros((piece_uv[0], N)).tolist(),
             np.zeros((piece_uv[0], N)).tolist()]

    knot_u = knot_uv[0]
    for i in range(N):
        P_control_X = [x[i] for x in P_X]
        P_control_Y = [y[i] for y in P_Y]
        P_control_Z = [z[i] for z in P_Z]
        P_control = [P_control_X, P_control_Y, P_control_Z]
        D_col = bc.curve(P_control, M, p, param_u, knot_u)
        for j in range(len(D_col[0])):
            D_tmp[0][j][i] = D_col[0][j]
            D_tmp[1][j][i] = D_col[1][j]
            D_tmp[2][j][i] = D_col[2][j]

    D = [np.zeros((piece_uv[0], piece_uv[1])).tolist(),
         np.zeros((piece_uv[0], piece_uv[1])).tolist(),
         np.zeros((piece_uv[0], piece_uv[1])).tolist()]

    knot_v = knot_uv[1]
    for i in range(piece_uv[0]):
        P_control = [D_tmp[0][i], D_tmp[1][i], D_tmp[2][i]]
        D_ = bc.curve(P_control, N, q, param_v, knot_v)
        D[0][i] = D_[0]
        D[1][i] = D_[1]
        D[2][i] = D_[2]

    return D
