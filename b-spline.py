import parameter_selection as ps
import numpy as np

P = np.array([[0,0], [1,2], [3,4], [4,0], [5, 5]])

P_N = 6

p_uniform = ps.uniform_spaced(P_N)
print(p_uniform)

# p_chord_length = ps.chord_length(P_N, P)
# print(p_chord_length)

# p_centripetal = ps.centripetal(P_N, P)
# print(p_centripetal)

param = np.array([0, 1.0/4, 1.0/3, 2.0/3, 3.0/4, 1])
knot = ps.knot_vector(param, 4, 6)
print(knot)