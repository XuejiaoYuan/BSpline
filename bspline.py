import matplotlib.pyplot as plt
import numpy as np
from BaseFunction import BaseFunction
from U_quasi_uniform import U_quasi_uniform
from mpl_toolkits.mplot3d import Axes3D

X = []
Y = []
shadow = []
block = []

with open('res_g12/shadow_block_m1_d1_h8_min0.txt', 'r') as file:
    file_lines = file.readlines()
    for line in file_lines:
        line_str = line.strip('\n')
        str = line.split(' ')
        row_x = []
        row_y = []
        row_shadow = []
        row_block = []
        for index in range(int(len(str)/4)):
            row_x.append(float(str[4 * index]))
            row_y.append(float(str[4 * index+1]))
            row_shadow.append(float(str[4 * index+2]))
            row_block.append(float(str[4 * index+3]))
        X.append(row_x)
        Y.append(row_y)
        shadow.append(row_shadow)
        block.append(row_block)


test_X = []
test_Y = []
test_shadow = []
test_block = []
with open('res_g12/shadow_block_m1_d1_h8_min0.txt', 'r') as file:
    file_lines = file.readlines()
    for line in file_lines:
        line_str = line.strip('\n')
        str = line.split(' ')
        row_x = []
        row_y = []
        row_shadow = []
        row_block = []
        for index in range(int(len(str)/4)):
            row_x.append(float(str[4*index]))
            row_y.append(float(str[4*index+1]))
            row_shadow.append(float(str[4*index+2]))
            row_block.append(float(str[4*index+3]))
        test_X.append(row_x)
        test_Y.append(row_y)
        test_shadow.append(row_shadow)
        test_block.append(row_block)


# 控制点X，Y，Z坐标
# X = [[0, 0, 0, 3, 6],
#      [20, 20, 20, 23, 26],
#      [40, 40, 40, 43, 46],
#      [60, 60, 60, 63, 66]];
# Y = [[0, 0, 0, 20, 40],
#      [0, 7, 7, 20, 43],
#      [0, 7, 7, 20, 43],
#      [0, 0, 0, 20, 40]];
# Z = [[60, 30, 0, 0, -5],
#      [50, 30, 0, 0, -5],
#      [60, 30, 0, 0, -5],
#      [60, 30, 0, 0, -5]];
M = len(X)
N = len(X[0])
Z = block

# 绘制控制点连线网格
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# for i in range(M):
#     for j in range(N):
#         ax.scatter(test_X[i][j], test_Y[i][j], test_block[i][j])

# for i in range(M):
#     for j in range(N):
#         ax.scatter(X[i][j], Y[i][j], Z[i][j])
#     for j in range(N-1):
#         tmp_x = [X[i][j], X[i][j+1]]
#         tmp_y = [Y[i][j], Y[i][j+1]]
#         tmp_z = [Z[i][j], Z[i][j+1]]
#         ax.plot(tmp_x, tmp_y, tmp_z, color='b')
#
# for j in range(N):
#     for i in range(M-1):
#         tmp_x = [X[i][j], X[i+1][j]]
#         tmp_y = [Y[i][j], Y[i+1][j]]
#         tmp_z = [Z[i][j], Z[i+1][j]]
#         ax.plot(tmp_x, tmp_y, tmp_z, color='b')

# 绘制B样条网格
FLAG_U = 2              # B样条类型
FLAG_V = 2
k = 2                   # k，l是网格的u向和v向的次数
l = 2
n = N - 1
m = M - 1
piece_u = M            # u向节点向量的细分
piece_v = N
Nik_u = np.zeros((N, 1))
Nik_v = np.zeros((M, 1))

# 1. u方向细分
X_M_piece = np.zeros((M, piece_u))  # 沿着u方向的网格
Y_M_piece = np.zeros((M, piece_u))
Z_M_piece = np.zeros((M, piece_u))
if FLAG_U == 1:
    NodeVector_u = np.linspace(0, 1, n+k+2)                 # 均匀B样条的u向节点向量
    u = np.linspace(k/(n+k+1), (n+1)/(n+k+1), piece_u)      # u向节点分成若干份

    for i in range(M):
        for j in range(piece_u):
            for ii in range(n+1):
                Nik_u[ii][0] = BaseFunction(ii, k, u[j], NodeVector_u)
            X_M_piece[i][j] = np.dot(X[i], Nik_u)
            Y_M_piece[i][j] = np.dot(Y[i], Nik_u)
            Z_M_piece[i][j] = np.dot(Z[i], Nik_u)
if FLAG_U == 2:
    NodeVector_u = U_quasi_uniform(n, k)                    # 准均匀B样条的u向节点向量
    u = np.linspace(0, 1-0.0001, piece_u)                   # u向节点分成若干份

    for i in range(M):
        for j in range(piece_u):
            for ii in range(n+1):
                Nik_u[ii][0] = BaseFunction(ii, k, u[j], NodeVector_u)
            X_M_piece[i][j] = np.dot(X[i], Nik_u)
            Y_M_piece[i][j] = np.dot(Y[i], Nik_u)
            Z_M_piece[i][j] = np.dot(Z[i], Nik_u)

# 2. v方向细分
X_MN_piece = np.zeros((piece_v, piece_u))
Y_MN_piece = np.zeros((piece_v, piece_u))
Z_MN_piece = np.zeros((piece_v, piece_u))
if FLAG_V == 1:
    NodeVector_v = np.linspace(0, 1, m+l+2)                 # 均匀B样条的v向节点向量
    v = np.linspace(l/(m+l+1), (m+1)/(m+l+1), piece_v)

    for i in range(piece_u):
        for j in range(piece_v):
            for ii in range(m+1):
                Nik_v[ii][0] = BaseFunction(ii, l, v[j], NodeVector_v)
            X_MN_piece[j][i] = np.dot(Nik_v.transpose(), X_M_piece[:, i])
            Y_MN_piece[j][i] = np.dot(Nik_v.transpose(), Y_M_piece[:, i])
            Z_MN_piece[j][i] = np.dot(Nik_v.transpose(), Z_M_piece[:, i])
if FLAG_V == 2:
    NodeVector_v = U_quasi_uniform(m, l)                    # 均匀B样条的v向节点向量
    v = np.linspace(0, 1-0.0001, piece_v)

    for i in range(piece_u):
        for j in range(piece_v):
            for ii in range(m+1):
                Nik_v[ii][0] = BaseFunction(ii, l, v[j], NodeVector_v)
            X_MN_piece[j][i] = np.dot(Nik_v.transpose(), X_M_piece[:, i])
            Y_MN_piece[j][i] = np.dot(Nik_v.transpose(), Y_M_piece[:, i])
            Z_MN_piece[j][i] = np.dot(Nik_v.transpose(), Z_M_piece[:, i])


for j in range(piece_u):
    for i in range(piece_v-1):
        tmp_x = [X_MN_piece[i][j], X_MN_piece[i+1][j]]
        tmp_y = [Y_MN_piece[i][j], Y_MN_piece[i+1][j]]
        tmp_z = [Z_MN_piece[i][j], Z_MN_piece[i+1][j]]
        ax.plot(tmp_x, tmp_y, tmp_z, color='g')

for i in range(piece_v):
    for j in range(piece_u-1):
        tmp_x = [X_MN_piece[i][j], X_MN_piece[i][j+1]]
        tmp_y = [Y_MN_piece[i][j], Y_MN_piece[i][j+1]]
        tmp_z = [Z_MN_piece[i][j], Z_MN_piece[i][j+1]]
        ax.plot(tmp_x, tmp_y, tmp_z, color='g')

# print(X_MN_piece)
# print('\n')
# print(Y_MN_piece)
# print('\n')
# print(Z_MN_piece)

plt.show()

bias_x = 600
scale_x = 1180.0 / 0.9999
bias_y = 100
scale_y = -580.0 / 0.9999
dis = np.zeros((M, N))

NodeVector_u = U_quasi_uniform(n, k)
NodeVector_v = U_quasi_uniform(m, l)
X_MN = np.zeros((M, N))
Y_MN = np.zeros((M, N))
Z_MN = np.zeros((M, N))
for test_i in range(M):
    for test_j in range(N):
        u = (test_X[test_i][test_j] + bias_x) / scale_x
        v = (test_Y[test_i][test_j] + bias_y) / scale_y
        X_M = np.zeros((M, 1))
        Y_M = np.zeros((M, 1))
        Z_M = np.zeros((M, 1))
        for i in range(M):
            for ii in range(n+1):
                Nik_u[ii][0] = BaseFunction(ii, k, u, NodeVector_u)
           # print(Nik_u)
            X_M[i][0] = np.dot(X[i], Nik_u)
            Y_M[i][0] = np.dot(Y[i], Nik_u)
            Z_M[i][0] = np.dot(Z[i], Nik_u)
        for ii in range(m+1):
            Nik_v[ii][0] = BaseFunction(ii, l, v, NodeVector_v)
        # print(Nik_v)
        X_MN[test_i][test_j] = np.dot(Nik_v.transpose(), X_M[:, 0])
        Y_MN[test_i][test_j] = np.dot(Nik_v.transpose(), Y_M[:, 0])
        Z_MN[test_i][test_j] = np.dot(Nik_v.transpose(), Z_M[:, 0])
        ax.scatter(X_MN[test_i][test_j], Y_MN[test_i][test_j], Z_MN[test_i][test_j])
print(X_MN)
print('\n')
print(Y_MN)
print('\n')
print(Z_MN)
plt.show()


print('test')