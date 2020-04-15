"""
Tests main algorithm correctness, according to the properties presented in the article.
It's supposed to take up to 1 minute.
In order to shorten tests times,
 p, the probability of the graphs may be lowered to anything smaller than 0.5.
"""

from utilities.util import (generate_weighted_connected_graph,
                            generate_cover,
                            calculate_collection_radius,
                            calculate_collection_degree)
from algorithm.max_cover import procedure_cover, max_cover
import numpy as np


#############################################
# CHECKERS ##################################
#############################################

# assert property (1) of PROCEDURE COVER: DT coarsens DR
# assert property (0) of PROCEDURE MAX COVER: T coarsens R
def check_coarsening(r, t):
    for cr in r:
        assert any([cr <= ct for ct in t])


# PROCEDURE COVER CORRECTNESS CHECKERS:

# assert property (2): for every d1, d2 in DT, d1 and d2 are disjoint
def check_dt_disjointness(dt):
    my_set = set.copy(dt)
    for cluster in dt:
        my_set.remove(cluster)
        for other in my_set:
            assert frozenset.isdisjoint(cluster, other)


# assert property (3): |DR| >= |R|^(1-1/k)
def check_dr_bound(dr, r, k):
    assert len(dr) >= np.power(len(r), 1 - (1 / k))


# assert property (4): Rad(DT) <= (2k-1)*Rad(R)
def check_dt_radius(g, dt, r, k):
    dt_radius = calculate_collection_radius(g, dt)
    r_radius = calculate_collection_radius(g, r)
    assert dt_radius <= (2 * k - 1) * r_radius


# PROCEDURE MAX COVER CORRECTNESS CHECKERS:

# assert property (1): Rad(T) <= (2k-1)*Rad(S)
def check_t_radius(g, s, t, k):
    s_radius = calculate_collection_radius(g, s)
    t_radius = calculate_collection_radius(g, t)
    assert t_radius <= (2 * k - 1) * s_radius


# assert property (2): Deg(T) <= 2k*|S|^(1/k)
def check_t_degree(s, t, k):
    t_degree = calculate_collection_degree(t)
    assert t_degree <= 2 * k * np.power(len(s), 1 / k)


#############################################
# TESTS #####################################
#############################################


def test_procedure_cover():
    for size in range(1, 101, 20):
        g = generate_weighted_connected_graph(size)
        cover = generate_cover(g, 1)
        for k in range(1, 10):
            dr, dt = procedure_cover(cover, k)
            check_coarsening(dr, dt)
            check_dt_disjointness(dt)
            check_dr_bound(dr, cover, k)
            check_dt_radius(g, dt, cover, k)


def test_max_cover():
    for size in range(1, 101, 20):
        g = generate_weighted_connected_graph(size)
        cover = generate_cover(g, 1)
        for k in range(1, 10):
            t = max_cover(cover, k)
            check_t_radius(g, cover, t, k)
            check_t_degree(cover, t, k)
            check_coarsening(cover, t)
