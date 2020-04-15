from utilities.util import (generate_weighted_connected_graph,
                            generate_cover,
                            get_collection_data)
from algorithm.max_cover import max_cover
from matplotlib import pyplot as plt
import numpy as np
from collections import OrderedDict

RESULTS_PARAMS = OrderedDict([('Rad(S)', 0),
                              ('Rad(T)', 1),
                              ('Deg(S)', 2),
                              ('Deg(T)', 3)])
NUM_OF_RESULTS_PARAMS = len(RESULTS_PARAMS)
PLOT_GRAPH_INDEX = 2

NUM_OF_NODES = 100
EXPERIMENTS_PARAMS = {'sampled graphs': {'normal': 5, 'small': 2},
                      'sampled covers': {'normal': 5, 'small': 2},
                      'k integers': {'normal': [1, 4, 7, 10], 'small': [4, 7]},
                      'probability step': {'normal': 0.05, 'small': 0.2},
                      'k limit': {'normal': 40, 'small': 15}}

DEBUG = False


def plot_experiment_results(results, x_axis, x_label, title=''):
    for field, index in RESULTS_PARAMS.items():
        plt.plot(x_axis, results[:, index], label=field)

        if (index + 1) % PLOT_GRAPH_INDEX == 0:
            plt.xlabel(x_label)
            plt.legend()
            plt.title(title)
            plt.show()


def k_integer_experiment(experiment_type='normal'):
    sampled_graphs = EXPERIMENTS_PARAMS['sampled graphs'][experiment_type]
    sampled_covers = EXPERIMENTS_PARAMS['sampled covers'][experiment_type]
    k_limit = EXPERIMENTS_PARAMS['k limit'][experiment_type]

    cover_size = 20
    max_cluster_size = 15

    results = np.zeros((k_limit, NUM_OF_RESULTS_PARAMS))

    for _ in range(sampled_graphs):
        g = generate_weighted_connected_graph(NUM_OF_NODES)

        for _ in range(sampled_covers):

            cover = generate_cover(g, cover_size, max_cluster_size=max_cluster_size)
            cover_radius, cover_degree = get_collection_data(g, cover)

            for k in range(1, k_limit + 1):
                coarsening_cover = max_cover(cover, k)
                coarsening_radius, coarsening_degree = get_collection_data(g, coarsening_cover)

                results[k - 1] += cover_radius, coarsening_radius, cover_degree, coarsening_degree

    results /= (sampled_graphs * sampled_covers)

    x_axis = [k for k in range(1, k_limit + 1)]
    plot_experiment_results(results, x_axis, 'k', title='K Integer Experiment')


def cover_size_experiment(experiment_type='normal'):
    sampled_graphs = EXPERIMENTS_PARAMS['sampled graphs'][experiment_type]
    k_integers = EXPERIMENTS_PARAMS['k integers'][experiment_type]

    cover_types = [(5, 30, 0),
                   (10, 20, 0),
                   (20, 10, 30),
                   (30, 5, 20),
                   (40, 5, 15),
                   (50, 0, 10)]

    results = np.zeros((len(cover_types), NUM_OF_RESULTS_PARAMS))

    for _ in range(sampled_graphs):
        g = generate_weighted_connected_graph(NUM_OF_NODES, p=0.5)
        for i, (cover_size, min_cluster_size, max_cluster_size) in enumerate(cover_types):
            cover = generate_cover(g, cover_size, min_cluster_size=min_cluster_size, max_cluster_size=max_cluster_size)

            cover_radius, cover_degree = get_collection_data(g, cover)

            for k in k_integers:
                coarsening_cover = max_cover(cover, k)
                coarsening_radius, coarsening_degree = get_collection_data(g, coarsening_cover)

                results[i] += cover_radius, coarsening_radius, cover_degree, coarsening_degree

    results /= (sampled_graphs * len(k_integers))

    x_axis = [cover_type[0] for cover_type in cover_types]
    plot_experiment_results(results, x_axis, 'cover size', title='Cover Size Experiment')


def graph_density_experiment(experiment_type='normal'):
    sampled_graphs = EXPERIMENTS_PARAMS['sampled graphs'][experiment_type]
    sampled_covers = EXPERIMENTS_PARAMS['sampled covers'][experiment_type]
    k_integers = EXPERIMENTS_PARAMS['k integers'][experiment_type]
    probability_step = EXPERIMENTS_PARAMS['probability step'][experiment_type]

    cover_size = 20
    max_cluster_size = 15

    probabilities = [0.01 + probability_step * i for i in range(int(1 / probability_step))]
    if DEBUG:
        print(probabilities)

    results = np.zeros((len(probabilities), NUM_OF_RESULTS_PARAMS))

    for i, p in enumerate(probabilities):

        for _ in range(sampled_graphs):
            g = generate_weighted_connected_graph(NUM_OF_NODES, p=p)
            for _ in range(sampled_covers):

                cover = generate_cover(g, cover_size, max_cluster_size=max_cluster_size)
                cover_radius, cover_degree = get_collection_data(g, cover)

                for k in k_integers:
                    coarsening_cover = max_cover(cover, k)
                    coarsening_radius, coarsening_degree = get_collection_data(g, coarsening_cover)

                    results[i] += cover_radius, coarsening_radius, cover_degree, coarsening_degree

        results[i] /= (sampled_graphs * sampled_covers * len(k_integers))

    plot_experiment_results(results, probabilities, 'edge probability', title='Graph Density Experiment')
