# Graph Cluster Covers

This project is an implementation of the main algorithm presented by B. Awerbuch and D. Peleg, in their article "Sparse Partitions", which suggests techniques to represent arbitrary networks in an efficient and simple way.

In this manner, networks are simply graphs, and their representation, dealt with in this article, is called **clustered representation of networks**, which is in practice a collection of clusters in some graph `G` (i.e. the network), that cover its vertices set.

The algorithm, called "MAX_COVER", is given a graph `G` and a cluster cover of it `S`, and it constructs a **coarsening cluster cover** `T`, that is considered a more qualitative representation of the network `G`, according to the two principles of a qualitative cluster cover presented by Awerbuch an Peleg:
    
        1. Clusters "size" 
    
        2. Cover sparsity

### Experiments

This project contains some experiments that examine and compare the algorithm's outputs, when given different types of graphs and cluster covers as inputs.

More details regarding the experiments and their results and conclusions are found in the attached report.


### Usage
In order to run the experiments:

    python -m experiments.run_experiments
    
In order to run some test file:
 
    python -m pytest tests/<test file>

### Meta

This project was written by Eyal Shagrir and was advised by Prof. Michael Elkin, as part of his course "Mini-Project on Embeddings of Graphs" taught in Ben-Gurion University of the Negev.

As mentioned before, this project is based on the article "Sparse Partitions", written by Baruch Awerbuch and David Peleg, and published in Proceedings of the 31st Annual IEEE Symposium on Foundations of Computer Science, 1990, pp. 503--513.  

