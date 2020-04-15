import numpy as np


def procedure_cover(R, k):
    """
    Given a collection of clusters R, and integer k,
    the collections DR, DT, constructed by procedure_cover satisfy the following:
        (1) DT coarsens DR (*)
        (2) for every d1, d2 in DT, d1 and d2 are disjoint
        (3) |DR| >= |R|^(1-1/k)
        (4) Rad(DT) <= (2k-1)*Rad(R)

    (*) DT coarsens DR if for every d in DR, there exists d' in DT s.t. d is a subset of d'

    :param R: a collection of clusters
    :param k: integer constant
    :return: collections DR, DT
    """
    U = set.copy(R)
    DR, DT = set(), set()
    while U:
        S = np.random.choice(list(U))
        Z = set()
        Z.add(S)
        while True:
            y = Z
            Y = frozenset.union(*list(y))
            Z = {S for S in U if frozenset.intersection(S, Y)}
            if len(Z) <= np.power((len(R)), (1 / k)) * len(y):
                break
        U -= Z
        DT.add(Y)
        DR |= y
    return DR, DT


def max_cover(S, k):
    """
    Given a graph cover S, and integer k >= 1,
    max cover construct a coarsening cover T (*), that satisfies the following:
        (1) Rad(T) <= (2k-1)Rad(S)
        (2) Deg(T) <= 2k*|S|^(1/k)

    (*) T coarsens S if for every s in S, there exists t in T s.t. s is a subset of T

    :param S: a cover of some graph g
    :param k: integer constant
    :return: coarsening cover T
    """
    R = set.copy(S)
    T = set()
    while R:
        DR, DT = procedure_cover(R, k)
        T |= DT
        R -= DR
    return T

