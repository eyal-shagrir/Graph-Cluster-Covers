import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

GRAPH_GENERATION_TRIES = 1000000
PROBABILITY_STEP = 0.01


def draw_graph(g):
    nx.draw(g, with_labels=True)
    plt.show()
    plt.close()


def generate_graph(n, p=0.5):
    """
    :param n: number of nodes
    :param p: probability for choosing edge
    :return:
    random Erdős–Rényi graph with n nodes, and edges chosen in probability of 0.5
    for more details: https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93R%C3%A9nyi_model
    """
    seed = np.random.randint(1, 100)
    return nx.fast_gnp_random_graph(n, p, seed)


def generate_connected_graph(n, p=0.5):
    """
    generates a connected graph with n nodes in probability p
    if it doesn't succeed in 1000000 tries, it raises p by 0.01
    :param n: number of nodes in graph
    :param p: probability for edge existence
    :return: a connected graph g
    """
    if n <= 1:
        return generate_graph(n)
    for _ in range(GRAPH_GENERATION_TRIES):
        g = generate_graph(n, p)
        if nx.is_connected(g):
            return g
        p += PROBABILITY_STEP


def weight_graph_edges(g, max_weight=100):
    """
    assigns each edge in g a weight between 0 and max_weight
    :param g: graph
    :param max_weight: upper limit to edges weights
    :return: None
    """
    for u, v in g.edges():
        g[u][v]['weight'] = np.random.randint(0, max_weight + 1)


def generate_weighted_connected_graph(n, p=0.5, max_weight=100):
    """
    generates a weighted connected graph with n nodes in probability p
    if it doesn't succeed in 1000000 tries, it raises p by 0.01
    :param n: number of nodes in graph
    :param p: probability for edge existence
    :param max_weight: upper limit to edges weights
    :return: a wighted connected graph g
    """
    g = generate_connected_graph(n, p=p)
    weight_graph_edges(g, max_weight)
    return g


def generate_random_cluster(g, min_cluster_size=0, max_cluster_size=0):
    """
    a very simple function that generates a random cluster.
    every iteration it chooses a random node from the cluster,
    and then randomly one of its neighbours to join to the cluster.
    :param g: graph
    :param min_cluster_size: minimum nodes in a cluster
    :param max_cluster_size: maximum nodes in a cluster
    :return: a cluster, i.e. a clique of nodes in g,
             in random size between min_cluster_size and max_cluster_size
    """
    n = nx.number_of_nodes(g)
    cluster = set()
    if n == 0 or min_cluster_size > max_cluster_size:
        return frozenset(cluster)
    if not min_cluster_size:
        min_cluster_size = 1
    if not max_cluster_size:
        max_cluster_size = n
    cluster_size = np.random.randint(min_cluster_size, max_cluster_size + 1)
    u = np.random.choice(list(g.nodes()))
    cluster.add(u)
    while len(cluster) < cluster_size:
        u = np.random.choice(list(cluster))
        v = np.random.choice(list(g.neighbors(u)))
        cluster.add(v)
    return frozenset(cluster)


def generate_cover(g, cover_size, min_cluster_size=0, max_cluster_size=0):
    """
    generates a requested clusters cover that covers all nodes in g.
    each iteration it adds a cluster to the cover, until there is full nodes coverage.
    that means that the cover size might be larger than cover_size.
    :param g: graph
    :param cover_size: size of requested cover
    :param min_cluster_size: minimum nodes in a cluster
    :param max_cluster_size: maximum nodes in a cluster
    :return: a cover with at least cover_size clusters.
            e.g. a set of tuples, each tuple represents a cluster of nodes
    """
    nodes = set(g.nodes())
    n = nx.number_of_nodes(g)
    clusters = set()
    if min_cluster_size and max_cluster_size:
        # too many restrictions may cause infinite loop trying to find impossible number of clusters in certain size
        cover_size = 1
    min_cluster_size = min_cluster_size if min_cluster_size != 0 else 1
    max_cluster_size = max_cluster_size if max_cluster_size != 0 else n
    i = 0
    while i < cover_size or nodes != frozenset.union(*list(clusters)):
        fs = generate_random_cluster(g, min_cluster_size, max_cluster_size)
        if fs not in clusters:
            clusters.add(fs)
            i += 1
    return clusters


def cluster_induced_graph(g, cluster):
    """
    :param g: graph
    :param cluster: a cluster in graph g
    :return: the induced graph by the nodes and edges of cluster in g
    """
    return nx.subgraph(g, list(cluster))


def calculate_node_radius(g, v):
    """
    calculates the node radius of v in graph g by the formula:
    Rad(v, g) = max(dist(v, w) | for every w in g)
    i.e. the maximum weight path in g from node v to some other node
    :param g: graph
    :param v: node v in g
    :return: radius of v in g
    """
    easiest_paths_weights = nx.single_source_dijkstra_path_length(g, v)
    return max(easiest_paths_weights.values())


def calculate_graph_radius(g):
    """
    calculates the radius of graph g by the formula:
    Rad(g) = min(Rad(v, g) | for every v in g)
    i.e. the minimum of all nodes radii in g

    This parameter is used as an indicator of the "cluster size",
    by approximating the weight of the paths between the nodes in the cluster.

    :param g: graph
    :return: radius of g
    """
    nodes_radii = {}
    for v in g.nodes():
        nodes_radii[v] = calculate_node_radius(g, v)
    return min(nodes_radii.values())


def calculate_collection_radius(g, collection):
    """
    calculates the radius of collection in graph g by the formula:
    Rad(g) = max(Rad(g(cluster)) | for every cluster in g),
             when g(s) in the induced graph by cluster in g
    i.e. the maximum of all clusters radii in collection

    This parameter is used as an indicator of the "collection size",
    by approximating the "cluster size" of each cluster.

    More generally the "collection size" is one of the two main criterias
    for evaluating the quality of a graph's cluster coverage.
    It represents the amount of "internal communication" in each cluster.
    Intuitively, the bigger the size of a cluster, the harder it is to communicate inside it.
    While technically, the bigger the size of a cluster,
    the heavier the paths between the nodes in it.

    :param g: graph
    :param collection: a collection of clusters in g
           (usually the collection sent is a node coverage of g)
    :return: radius of collection
    """
    clusters_radii = {}
    for cluster in collection:
        induced_graph = cluster_induced_graph(g, cluster)
        induced_graph_radius = calculate_graph_radius(induced_graph)
        clusters_radii[cluster] = induced_graph_radius
    return max(clusters_radii.values())


def calculate_node_degree_in_collection(collection, v):
    """
    calculates the degree of node v in collection by the formula:
    deg(v, collection) = the number of clusters in collection, v belongs to

    :param collection: collection of clusters
    :param v: node
    :return: degree of v in collection
    """
    counter = 0
    for cluster in collection:
        if v in cluster:
            counter += 1
    return counter


def calculate_collection_degree(collection):
    """
    calculates the degree of collection by the formula:
    deg(collection) = max(deg(v, collection) for each v appears in collection)

    This parameter is used as an indicator of the collection sparsity,
    by approximating how many clusters share the same nodes.

    More generally, the collection sparsity is one of the two main criterias
    for evaluating the quality of a graph's cluster coverage.
    It represents the amount of "external communication" between each cluster.
    Intuitively, the more sparse the collection is,
    the harder it is to communicate between its clusters.
    While technically, the more sparse the collection is,
    the smaller the amount of nodes they share.

    :param collection: collection of clusters
    :return: degree of collection
    """
    nodes_abundances = {}
    for v in frozenset.union(*list(collection)):
        nodes_abundances[v] = calculate_node_degree_in_collection(collection, v)
    return max(nodes_abundances.values())


def get_collection_data(g, collection):
    collection_radius = calculate_collection_radius(g, collection)
    collection_degree = calculate_collection_degree(collection)
    return collection_radius, collection_degree
