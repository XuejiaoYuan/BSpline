import parameter_selection as ps
import numpy as np
import bspline_curve as bc
import bspline_surface as bs
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def curve_inter_figure():
    '''
    Input: Data points
    '''
    D_X = [1, 1, 0, -0.5, 1.5, 3, 4, 4.2, 4]
    D_Y = [0, 1, 2, 3, 4, 3.5, 3, 2.5, 2]
    D = [D_X, D_Y]
    D_N = len(D_X)
    k = 2               # degree

    '''
    Step 1. Calculate parameters
    '''
    # p_uniform = ps.uniform_spaced(D_N)
    # print(p_uniform)

    # p_chord_length = ps.chord_length(D_N, D)
    # print(p_chord_length)

    p_centripetal = ps.centripetal(D_N, D)
    # print(p_centripetal)

    '''
    Step 2. Calculate knot vector
    '''
    knot = ps.knot_vector(p_centripetal, k, D_N)
    print(knot)

    '''
    Step 3. Calculate control points
    '''
    P_inter = bc.curve_interpolation(D, D_N, k, p_centripetal, knot)
    # print(P_inter)

    fig = plt.figure()
    for i in range(D_N):
        plt.scatter(D[0][i], D[1][i], color='r')
        plt.scatter(P_inter[0][i], P_inter[1][i], color='b')
    for i in range(D_N - 1):
        tmp_x = [P_inter[0][i], P_inter[0][i+1]]
        tmp_y = [P_inter[1][i], P_inter[1][i+1]]
        plt.plot(tmp_x, tmp_y, color='b')

    '''
    Step 4. Calculate the points on the b-spline curve
    '''
    piece_num = 80
    p_piece = np.linspace(0, 1, piece_num)
    P_piece = bc.curve(P_inter, D_N, k, p_piece, knot)
    # print(P_piece)
    for i in range(piece_num - 1):
        tmp_x = [P_piece[0][i], P_piece[0][i+1]]
        tmp_y = [P_piece[1][i], P_piece[1][i+1]]
        plt.plot(tmp_x, tmp_y, color='g')
    plt.show()


def curve_approx_figure():
    D_X = [1, 1, 0, -0.5, 1.5, 3, 4, 4.2, 4]
    D_Y = [0, 1, 2, 3, 4, 3.5, 3, 2.5, 2]
    D = [D_X, D_Y]

    D_N = len(D_X)
    k = 4           # degree
    H = 8           # the number of control points

    '''
    Step 1. Calculate the parameters
    '''
    p_centripetal = ps.centripetal(D_N, D)

    '''
    Step 2. Calculate the knot vector
    '''
    knot = ps.knot_vector(p_centripetal, k, D_N)

    '''
    Step 3. Calculate the control points
    '''
    P_control = bc.curve_approximation(D, D_N, H, k, p_centripetal, knot)
    # print(P_control)

    fig = plt.figure()
    for i in range(H):
        plt.scatter(P_control[0][i], P_control[1][i], color='b')

    for i in range(D_N):
        plt.scatter(D[0][i], D[1][i], color='r')

    for i in range(H - 1):
        tmp_x = [P_control[0][i], P_control[0][i+1]]
        tmp_y = [P_control[1][i], P_control[1][i+1]]
        plt.plot(tmp_x, tmp_y, color='b')

    '''
    Step 4. Calculate the points on the b-spline curve
    '''
    piece_num = 80
    p_piece = np.linspace(0, 1, piece_num)
    p_centripetal_new = ps.centripetal(H, P_control)
    knot_new = ps.knot_vector(p_centripetal_new, k, H)
    P_piece = bc.curve(P_control, H, k, p_piece, knot_new)

    # print(P_piece)
    for i in range(piece_num - 1):
        tmp_x = [P_piece[0][i], P_piece[0][i+1]]
        tmp_y = [P_piece[1][i], P_piece[1][i+1]]
        plt.plot(tmp_x, tmp_y, color='g')
    plt.show()


def surface_inter_figure():
    D_X = [[0.0, 3, 6, 7],
           [0.0, 3, 6, 7],
           [0.0, 3, 6, 7]]
    D_Y = [[2, 2, 2, 2],
           [5, 5, 5, 5],
           [10, 10, 10, 10]]
    D_Z = [[0, -2, -5, -8],
           [0, -3, -5, -9],
           [0, -2, -5, -8]]

    D = [D_X, D_Y, D_Z]

    k = 2
    q = 2

    '''
    Step 1. Calculate control surface's control points
    '''
    P_control, knot_uv = bs.surface_interpolation(D, k, q)

    '''
    Step 2. Calculate the points on the b-spline surface
    '''
    piece_uv = [20, 30]
    P_piece = bs.surface(P_control, k, q, piece_uv, knot_uv)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(D_X)):
        for j in range(len(D_X[0])):
            ax.scatter(D_X[i][j], D_Y[i][j], D_Z[i][j], color='r')
            ax.scatter(P_control[0][i][j], P_control[1][i][j], P_control[2][i][j], color='b')

    for i in range(len(D_X)):
        for j in range(len(D_X[0]) - 1):
            tmp_x = [P_control[0][i][j], P_control[0][i][j + 1]]
            tmp_y = [P_control[1][i][j], P_control[1][i][j + 1]]
            tmp_z = [P_control[2][i][j], P_control[2][i][j + 1]]
            ax.plot(tmp_x, tmp_y, tmp_z, color='b')

    for i in range(len(D_X)-1):
        for j in range(len(D_X[0])):
            tmp_x = [P_control[0][i][j], P_control[0][i + 1][j]]
            tmp_y = [P_control[1][i][j], P_control[1][i + 1][j]]
            tmp_z = [P_control[2][i][j], P_control[2][i + 1][j]]
            ax.plot(tmp_x, tmp_y, tmp_z, color='b')

    for i in range(len(P_piece[0])-1):
        for j in range(len(P_piece[0][0])):
            tmp_x = [P_piece[0][i][j], P_piece[0][i+1][j]]
            tmp_y = [P_piece[1][i][j], P_piece[1][i+1][j]]
            tmp_z = [P_piece[2][i][j], P_piece[2][i+1][j]]
            ax.plot(tmp_x, tmp_y, tmp_z, color='g')

    for i in range(len(P_piece[0])):
        for j in range(len(P_piece[0][0])-1):
            tmp_x = [P_piece[0][i][j], P_piece[0][i][j+1]]
            tmp_y = [P_piece[1][i][j], P_piece[1][i][j+1]]
            tmp_z = [P_piece[2][i][j], P_piece[2][i][j+1]]
            ax.plot(tmp_x, tmp_y, tmp_z, color='g')

    plt.show()


def surface_approx_figure():
    D_X = [[0.0, 3, 6, 7, 9, 15],
           [0.0, 3, 6, 7, 9, 15],
           [0.0, 3, 6, 7, 9, 15],
           [0.0, 3, 6, 7, 9, 15],
           [0.0, 3, 6, 7, 9, 15]]
    D_Y = [[2, 2, 2, 2, 2, 2],
           [5, 5, 5, 5, 5, 5],
           [10, 10, 10, 10, 10, 10],
           [15, 15, 15, 15, 15, 15],
           [20, 20, 20, 20, 20, 20]]
    D_Z = [[0, -2, -5, -8, -10, -14],
           [0, -3, -5, -9, -12, -15],
           [0, -2, -5, -8, -11, -16],
           [-1, -4, -6, -8, -11.5, -15],
           [1, -2, -4, -8, -11, -16]]

    D = [D_X, D_Y, D_Z]

    k = 2
    q = 3
    E = len(D_X) - 1
    F = len(D_X[0]) - 1

    '''
    Step 1. Calculate control surface's control points
    '''
    P_control = bs.surface_approximation(D, k, q, E, F)

    '''
    Step 2. Calculate the points on the b-spline surface
    '''
    piece_uv = [20, 30]
    knot_uv =[[], []]
    tmp_param = np.zeros((1, E))
    for i in range(F):
        D_col_X = [x[i] for x in P_control[0]]
        D_col_Y = [y[i] for y in P_control[1]]
        D_col = [D_col_X, D_col_Y]
        tmp_param = tmp_param + np.array(ps.centripetal(E, D_col))
    param_u = np.divide(tmp_param, F).tolist()[0]

    param_v = []
    tmp_param = np.zeros((1, F))
    for i in range(E):
        D_row_X = P_control[0][i]
        D_row_Y = P_control[1][i]
        D_row = [D_row_X, D_row_Y]
        tmp_param = tmp_param + np.array(ps.centripetal(F, D_row))
        # param_v.append(np.average(np.array(tmp_param)))
    param_v = np.divide(tmp_param, E).tolist()[0]

    knot_uv[0] = ps.knot_vector(param_u, k, E)
    knot_uv[1] = ps.knot_vector(param_v, q, F)

    P_piece = bs.surface(P_control, k, q, piece_uv, knot_uv)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(D_X)):
        for j in range(len(D_X[0])):
            ax.scatter(D_X[i][j], D_Y[i][j], D_Z[i][j], color='r')
    for i in range(len(P_control[0])):
        for j in range(len(P_control[0][0])):
            ax.scatter(P_control[0][i][j], P_control[1][i][j], P_control[2][i][j], color='b')

    for i in range(len(P_control[0])):
        for j in range(len(P_control[0][0]) - 1):
            tmp_x = [P_control[0][i][j], P_control[0][i][j + 1]]
            tmp_y = [P_control[1][i][j], P_control[1][i][j + 1]]
            tmp_z = [P_control[2][i][j], P_control[2][i][j + 1]]
            ax.plot(tmp_x, tmp_y, tmp_z, color='b')

    for i in range(len(P_control[0]) - 1):
        for j in range(len(P_control[0][0])):
            tmp_x = [P_control[0][i][j], P_control[0][i + 1][j]]
            tmp_y = [P_control[1][i][j], P_control[1][i + 1][j]]
            tmp_z = [P_control[2][i][j], P_control[2][i + 1][j]]
            ax.plot(tmp_x, tmp_y, tmp_z, color='b')

    for i in range(len(P_piece[0]) - 1):
        for j in range(len(P_piece[0][0])):
            tmp_x = [P_piece[0][i][j], P_piece[0][i + 1][j]]
            tmp_y = [P_piece[1][i][j], P_piece[1][i + 1][j]]
            tmp_z = [P_piece[2][i][j], P_piece[2][i + 1][j]]
            ax.plot(tmp_x, tmp_y, tmp_z, color='g')

    for i in range(len(P_piece[0])):
        for j in range(len(P_piece[0][0]) - 1):
            tmp_x = [P_piece[0][i][j], P_piece[0][i][j + 1]]
            tmp_y = [P_piece[1][i][j], P_piece[1][i][j + 1]]
            tmp_z = [P_piece[2][i][j], P_piece[2][i][j + 1]]
            ax.plot(tmp_x, tmp_y, tmp_z, color='g')

    plt.show()


curve_inter_figure()
#
# curve_approx_figure()
#
# surface_inter_figure()
#
# surface_approx_figure()