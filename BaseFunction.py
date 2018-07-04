def BaseFunction(i, k, u, knot):
    '''
    Calculate base function using Cox-deBoor function.
    :param i: index of base function
    :param k: order (degree + 1)
    :param u: parameter
    :param knot: knot vector
    :return: base function
    '''
    Nik_u = 0
    if k == 1:
        if u >= knot[i] and u < knot[i + 1]:
            Nik_u = 1.0
        else:
            Nik_u = 0.0
    else:
        length1 = knot[i + k - 1] - knot[i]
        length2 = knot[i + k] - knot[i + 1]
        if not length1 and not length2:
            Nik_u = 0
        elif not length1:
            Nik_u = (knot[i + k] - u) / length2 * BaseFunction(i + 1, k - 1, u, knot)
        elif not length2:
            Nik_u = (u - knot[i]) / length1 * BaseFunction(i, k - 1, u, knot)
        else:
            Nik_u = (u - knot[i]) / length1 * BaseFunction(i, k - 1, u, knot) + \
                    (knot[i + k] - u) / length2 * BaseFunction(i + 1, k - 1, u, knot)
    return Nik_u
