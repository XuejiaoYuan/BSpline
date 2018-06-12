import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from BaseFunction import BaseFunction

x = []
y = []
shadow = []
block = []

# with open('helio_pos.txt') as file:
#     file_lines = file.readlines()
#     for line in file_lines:
#         line_str = line.strip('\n')
#         str = line_str.split(' ')
#         row_x = []
#         row_y = []
#         for index in len(str)/2:
#             row_x.append(int(str[index]))
#             row_y.append(int(str[index]))
#         x.append(row_x)
#         y.append(row_y)
#
# with open('time_shadow_block_h0.txt', 'r') as file:
#     file_lines = file.readlines()
#     for line in file_lines:
#         line_str = line.strip('\n')
#         str = line_str.split(' ')
#         shadow_day = []
#         block_day = []
#         for index in len(str)/2:
#             shadow_day.append(float(str[index]))
#             block_day.append(float(str[index]))
#         shadow.append(shadow_day)
#         block.append(block_day)

# 控制点X，Y，Z坐标
X = [[0, 0, 0, 3, 6],
     [20, 20, 20, 23 ,26],
     [40, 40, 40, 43, 46],
     [60, 60, 60, 63, 66]];
Y = [[0, 0, 0, 20, 40],
     [0, 7, 7, 20, 43],
     [0, 7, 7, 20, 43],
     [0, 0, 0, 20, 40]];
Z = [[60, 30, 0, 0, -5],
     [50, 30, 0, 0, -5],
     [60, 30, 0, 0, -5],
     [60, 30, 0, 0, -5]];
M = len(X)
N = len(X[0])

# 绘制控制点连线网格
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(M):
    for j in range(N):
        ax.scatter(X[i][j], Y[i][j], Z[i][j])
    for j in range(N-1):
        tmp_x = [X[i][j], X[i][j+1]]
        tmp_y = [Y[i][j], Y[i][j+1]]
        tmp_z = [Z[i][j], Z[i][j+1]]
        ax.plot(tmp_x, tmp_y, tmp_z, color='b')

for j in range(N):
    for i in range(M-1):
        tmp_x = [X[i][j], X[i+1][j]]
        tmp_y = [Y[i][j], Y[i+1][j]]
        tmp_z = [Z[i][j], Z[i+1][j]]
        ax.plot(tmp_x, tmp_y, tmp_z, color='b')

plt.show()

# 绘制B样条网格
FLAG_U = 1  # B样条类型
FLAG_V = 1
k = 2       # k，l是网格的u向和v向的次数
l = 2
n = N - 1
m = M - 1
piece_u = 20    # u向节点向量的细分
piece_v = 20
Nik_u = np.zeros(N, 1)
Nik_v = np.zeros(M, 1)

# 1. u方向细分
if FLAG_U == 1:
    NodeVector_u = np.linspace(0, 1, n+k+2)     # 均匀B样条的u向节点向量
    u = np.linspace(k/(n+k+1), (n+1)/(n+k+1), piece_u)      # u向节点分成若干份

    X_M_piece = np.zeros(M, piece_u)            # 沿着u方向的网格
    Y_M_piece = np.zeros(M, piece_u)
    Z_M_piece = np.zeros(M, piece_u)

    for i in range(M):
        for j in range(piece_u):
            for ii in range(n):
                Nik_u[ii+1][1] = BaseFunction(ii, k, u[j], NodeVector_u)
            X_M_piece[i][j] = X[i]
