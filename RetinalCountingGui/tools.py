import numpy as np


# generate element for morph
def morph_elemt(n):
    # Make this faster later if necessary, probably good enough for now
    h = (n - 1) / 2.
    mat = np.ones((n, n))
    for i in range(n):
        for j in range(n):
            if (i - h) ** 2 + (j - h) ** 2 > h ** 2 + .5:
                mat[i, j] = 0
    print(mat)
    return mat

