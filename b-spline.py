import parameter_selection as ps
import numpy as np
import bspline_curve as bc
import bspline_surface as bs
import matplotlib.pyplot as plt


def curve_inter_figure():
    # D = np.array([[0, 0], [1, 3], [3, 4], [4, 3], [5, 5]])
    D = np.array([[1, 0], [1, 1], [0, 2], [-0.5, 3], [1.5, 4],
                 [3, 3.5], [4, 3], [4.2, 2.5], [4, 2]])
    D_N = len(D)
    k = 2

    # p_uniform = ps.uniform_spaced(D_N)
    # print(p_uniform)

    # p_chord_length = ps.chord_length(P_N, P)
    # print(p_chord_length)

    p_centripetal = ps.centripetal(D_N, D)
    print(p_centripetal)

    knot = ps.knot_vector(p_centripetal, k, D_N)
    print(knot)

    P_inter = bc.curve_interpolation(D, D_N, k, p_centripetal, knot)
    print(P_inter)

    fig = plt.figure()
    for i in range(D_N):
        plt.scatter(D[i][0], D[i][1], color='b')
        plt.scatter(P_inter[i][0], P_inter[i][1], color='g')
    for i in range(D_N - 1):
        # tmp_x = [D[i][0], D[i+1][0]]
        # tmp_y = [D[i][1], D[i+1][1]]
        # plt.plot(tmp_x, tmp_y, color='b')
        tmp_x = [P_inter[i][0], P_inter[i + 1][0]]
        tmp_y = [P_inter[i][1], P_inter[i + 1][1]]
        plt.plot(tmp_x, tmp_y, color='g')

    piece_num = 20
    p_piece = np.linspace(0, 1, piece_num)
    print(p_piece)
    # knot_piece = ps.knot_vector(p_piece, k, piece_num)
    # print(knot_piece)
    P_piece = bc.curve(P_inter, D_N, k, p_piece, knot)
    print(P_piece)
    for i in range(piece_num - 1):
        tmp_x = [P_piece[i][0], P_piece[i + 1][0]]
        tmp_y = [P_piece[i][1], P_piece[i + 1][1]]
        plt.plot(tmp_x, tmp_y, color='r')
    plt.show()


def curve_approx_figure():
    D = np.array([[1, 0], [1, 1], [0, 2], [-0.5, 3], [1.5, 4],
                 [3, 3.5], [4, 3], [4.2, 2.5], [4, 2]])
    # D = np.array([[0, 0], [1, 3], [3, 4], [4, 3], [5, 5]])
    D_N = len(D)
    k = 4
    H = 8

    p_centripetal = ps.centripetal(D_N, D)
    knot = ps.knot_vector(p_centripetal, k, D_N)
    P_control = bc.curve_approximation(D, D_N, H, k, p_centripetal, knot)
    print(P_control)

    fig = plt.figure()
    for i in range(H):
        plt.scatter(P_control[i][0], P_control[i][1], color='g')

    for i in range(D_N):
        plt.scatter(D[i][0], D[i][1], color='b')

    for i in range(H-1):
        tmp_x = [P_control[i][0], P_control[i+1][0]]
        tmp_y = [P_control[i][1], P_control[i+1][1]]
        plt.plot(tmp_x, tmp_y, color='g')

    # for i in range(D_N-1):
    #     tmp_x = [D[i][0], D[i+1][0]]
    #     tmp_y = [D[i][1], D[i+1][1]]
    #     plt.plot(tmp_x, tmp_y, color='b')

    piece_num = 80
    p_piece = np.linspace(0, 1, piece_num)
    p_centripetal_new = ps.centripetal(H, P_control)
    knot_new = ps.knot_vector(p_centripetal_new, k, H)
    P_piece = bc.curve(P_control, H, k, p_piece, knot_new)

    print(P_piece)
    for i in range(piece_num - 1):
        tmp_x = [P_piece[i][0], P_piece[i+1][0]]
        tmp_y = [P_piece[i][1], P_piece[i+1][1]]
        plt.plot(tmp_x, tmp_y, color='r')
    plt.show()


def surface_inter_figure():
    D = [[[ 0, 0, 0], [ 3, 20, 0], [ 6, 40, -5]],
         [[20, 7, 0], [23, 20, 0], [26, 43, -5]],
         [[40, 7, 0], [43, 20, 0], [46, 43, -5]]]

    k = 3
    q = 3

    P_control = bs.surface_interpolation(D, k, q)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(D)):
        for j in range(len(D[0])):
            ax.scatter(D[i][j][0], D[i][j][1], D[0][j][2], color='r')
            ax.scatter(P_control[i][j][0], P_control[i][j][1], P_control[i][j][2], color='b')
    plt.show()



# curve_inter_figure()

# curve_approx_figure()

surface_inter_figure()