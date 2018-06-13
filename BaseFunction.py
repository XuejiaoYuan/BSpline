
def BaseFunction(i, k, u, NodeVector):
    Nik_u = 0
    if k == 0:
        if u >= NodeVector[i] and u < NodeVector[i+1]:
            Nik_u = 1.0
        else:
            Nik_u = 0.0
    else:
        length1 = NodeVector[i+k] - NodeVector[i]
        length2 = NodeVector[i+k+1] - NodeVector[i+1]
        if length1 == 0.0:
            length1 = 1.0
        if length2 == 0.0:
            length2 = 1.0
        Nik_u = (u - NodeVector[i]) / length1 * BaseFunction(i, k-1, u, NodeVector) \
                + (NodeVector[i+k+1] - u) / length2 * BaseFunction(i+1, k-1, u, NodeVector)
    return Nik_u
