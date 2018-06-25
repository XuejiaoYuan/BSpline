import numpy as np
import BaseFunction as bf
import parameter_selection as ps
import bspline_curve as bc


def surface_interpolation(D, p, q):
    M = len(D)
    N = len(D[0])
    Q = []
    for i in range(N):
        D_col = D[:][i]
        param = ps.centripetal(N, D_col)
        knot = ps.knot_vector(param, p, N)
        Q.append(bc.curve_interpolation(D_col, N, p, param, knot))

    P = []
    for i in range(M):
        Q_row = Q[i][:]
        param = ps.centripetal(M, Q_row)
        knot = ps.knot_vector(param, q, M)
        P.append(bc.curve_interpolation(Q_row, M, q, param, knot))

    return P