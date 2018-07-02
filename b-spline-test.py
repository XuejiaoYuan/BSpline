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

    param = sorted(D_X)
    print(param)

    # p_centripetal = ps.centripetal(D_N, D)
    # print(p_centripetal)

    '''
    Step 2. Calculate knot vector
    '''
    knot = ps.knot_vector_test(param, k, D_N)
    print(knot)

    '''
    Step 3. Calculate control points
    '''
    P_inter = bc.curve_interpolation(D, D_N, k, param, knot)
    print(P_inter)

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

curve_inter_figure()