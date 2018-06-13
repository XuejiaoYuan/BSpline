import numpy as np

def U_quasi_uniform(n, k):
    NodeVector = np.zeros((1, n+k+2))
    piecewise = n - k + 1       # 曲线的段数
    if piecewise == 1:
        for i in range(n+1, n+k+2):
            NodeVector[0][i] = 1
    else:
        flag = 1
        while flag != piecewise:
            NodeVector[0][k+flag] = NodeVector[0][k+flag-1] + 1/piecewise
            flag = flag + 1
        NodeVector[0][n+1:n+k+2] = 1
    return NodeVector[0]
