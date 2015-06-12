"""
    Degree distributions for graphs.
    """
#Representing directed graphs
EX_GRAPH0 = {0:set([1, 2]), 1:set([]), 2:set([])}
EX_GRAPH1 = {0:set([1, 4, 5]), 1:set([2, 6]), 2:set([3]),
    3:set([0]), 4:set([1]), 5:set([2]),
    6:set([])}
EX_GRAPH2 = {0:set([1, 4, 5]), 1:set([2, 6]), 2:set([3, 7]),
    3:set([7]), 4:set([1]), 5:set([2]),
    6:set([]), 7:set([3]), 8:set([1, 2]),
    9:set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    """
        Takes the number of nodes and returns a dictionary
        corresponding to a complete directed graph
        with the specified number of nodes.
        """
    graph = {}
    for dummy_node in range(num_nodes):
        graph[dummy_node] = set([dummy_x for dummy_x in range(num_nodes)])
        graph[dummy_node].remove(dummy_node)
    return graph

#Computing degree distributions
def compute_in_degrees(digraph):
    """
        Takes a directed graph digraph
        and computes the in-degrees for the nodes.
        """
    num_degree = {}
    for dummy_node in digraph:
        num_degree[dummy_node] = 0
    for key in digraph:
        for node in digraph[key]:
            num_degree[node] += 1
    return num_degree

def in_degree_distribution(digraph):
    """
        Takes a directed graph digraph
        and computes the unnormalized distribution of the in-degrees.
        """
    degree_distr = {}
    num_degree = compute_in_degrees(digraph)
    for node in num_degree:
        degree_distr[num_degree[node]] = degree_distr.get(num_degree[node],0) + 1
    return  degree_distr