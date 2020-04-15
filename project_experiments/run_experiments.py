from project_experiments.experiments import (graph_density_experiment,
                                             cover_size_experiment,
                                             k_integer_experiment)

EXPERIMENTS_TYPES = {'1': 'normal', '2': 'small'}


def run_experiments(experiments_type):
    print('Running Graph Density Experiment...')
    graph_density_experiment(experiments_type)
    print('Finished!\n')

    print('Running Cover Size Experiment...')
    cover_size_experiment(experiments_type)
    print('Finished!\n')

    print('Running K Integer Experiment...')
    k_integer_experiment(experiments_type)
    print('Finished!\n')


def main():
    print('Welcome to Sparse Partitions Mini-Project!\n')
    while True:
        opt = input('\n'.join(['Please choose one of the following options:',
                               '1 - Run original mini-project experiments (might take over an hour)',
                               '2 - Run small-scale experiments (takes about 10 minutes, but might be less accurate)',
                               '3 - Quit program\n']))
        if opt in EXPERIMENTS_TYPES:
            experiment_type = EXPERIMENTS_TYPES[opt]
            run_experiments(experiment_type)
            break

        elif opt == '3':
            return


if __name__ == '__main__':
    main()
