from utilities.util import (generate_weighted_connected_graph,
                            generate_random_cluster,
                            generate_cover)
import networkx as nx


#############################################
# CHECKERS ##################################
#############################################


# assert that g is a connected graph
def check_graph_connectivity(g):
    assert nx.is_connected(g)


# assert that g is a weighted graph
def check_graph_weights(g, max_weight=100):
    for u, v in g.edges():
        assert 0 <= g[u][v]['weight'] <= max_weight


# assert that cluster is connected
def check_cluster_connectivity(g, c):
    check_graph_connectivity(nx.subgraph(g, list(c)))


# assert that cluster is in the requested size
def check_cluster_size(c, min_size, max_size):
    assert min_size <= len(c) <= max_size


# assert cover is in the requested size
def check_cover_size(cover, requested_size):
    assert len(cover) >= requested_size


# assert cover is a correct coverage of graph nodes
def check_cover_correctness(cover, graph_nodes):
    assert frozenset.union(*([c for c in cover])) == set(graph_nodes)


# assert each cluster in the cover is in the requested size
def check_cover_clusters_size(cover, min_cluster_size, max_cluster_size):
    for c in cover:
        check_cluster_size(c, min_cluster_size, max_cluster_size)


#############################################
# TESTS #####################################
#############################################


def test_generate_weighted_connected_graph_connectivity():
    for size in range(1, 100):
        g = generate_weighted_connected_graph(size)
        check_graph_connectivity(g)


def test_generate_weighted_connected_graph_weights():
    for size in range(1, 101, 20):
        for max_weight in range(50):
            g = generate_weighted_connected_graph(size, max_weight=max_weight)
            check_graph_weights(g, max_weight)


def test_generate_random_cluster_connectivity():
    for size in range(1, 100):
        g = generate_weighted_connected_graph(size)
        for _ in range(10):
            c = generate_random_cluster(g)
            check_cluster_connectivity(g, c)


def test_generate_random_cluster_min_max_size():
    for size in range(1, 30):
        g = generate_weighted_connected_graph(size)
        for i in range(1, size):
            for j in range(i, size):
                c = generate_random_cluster(g, min_cluster_size=i, max_cluster_size=j)
                check_cluster_connectivity(g, c)


def test_generate_cover_coverage():
    for graph_size in range(1, 40):
        g = generate_weighted_connected_graph(graph_size)
        for requested_cover_size in range(1, graph_size):
            cover = generate_cover(g, requested_cover_size)
            check_cover_size(cover, requested_cover_size)
            check_cover_correctness(cover, g.nodes())


def test_generate_cover_min_max_cluster_size():
    for graph_size in range(1, 20):
        g = generate_weighted_connected_graph(graph_size)
        for i in range(1, graph_size):
            for j in range(i, graph_size):
                cover = generate_cover(g, 1, min_cluster_size=i, max_cluster_size=j)
                check_cover_size(cover, 1)
                check_cover_correctness(cover, g.nodes())
                check_cover_clusters_size(cover, i, j)
