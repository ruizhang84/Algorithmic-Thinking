"""
    Analysis of a computer network.
    """
# general import
# general imports
import urllib2
import random
import time
import math
import matplotlib.pyplot as plt

from connected_components_graph_resilience import *
# global counter that records the number of plots
counter = 0

# make graph
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

def make_random_undirected_graph(num_nodes, probility):
    """
        Takes the number of nodes n and the probility p
        returns a dictionary corresponding to a random undirected graph
        with the specified number of nodes. (Algorithm ER)
        """
    graph = {}
    edges = 0
    for dummy_node in range(num_nodes):
        if dummy_node not in graph:
            graph[dummy_node] = set()
        for dummy_node_pair in range(num_nodes):
            if dummy_node_pair != dummy_node:
                a = random.random() # a real number [0,1)
                if a < probility:
                    print dummy_node, dummy_node_pair
                    graph[dummy_node].add(dummy_node_pair)
                    if dummy_node_pair not in graph:
                        graph[dummy_node_pair] = set([dummy_node])
                    else:
                        graph[dummy_node_pair].add(dummy_node)
        edges += len(graph[dummy_node])
    print "number of edges are ", edges/2

    return graph

def make_synthetic_undirected_graph(num_nodes, num_exist):
    """
        Takes the number of nodes n, the probility p and the number of existing nodes m 
        to which a new node is connected during each iteration,
        returns a dictionary corresponding to a random synthetic directed graph
        with the specified number of nodes. (Algorithm DPA)
        """
    graph = {}
    edges = 0
    graph = make_complete_graph(num_exist)              #creating a complete directed graph on m nodes
    dpa_graph = UPATrial(num_exist)
    for dummy_node in range(num_exist, num_nodes):
        node_neighbors = dpa_graph.run_trial(num_exist)
        graph[dummy_node] = set(node_neighbors)
        for dummy_node_pair in node_neighbors:
            graph[dummy_node_pair] = graph.get(dummy_node_pair,set([]))
            graph[dummy_node_pair].add(dummy_node)
        edges += len(graph[dummy_node])

    print "number of edges are ", edges/2
    return graph

def random_order(graph):
    """
         takes a graph and returns a list of the nodes 
         in the graph in some random order.
         """
    return random.sample(graph, len(graph))


############################################
# Provided code

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


def copy_graph(graph):
    """
        Make a copy of a graph
        """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
        Delete a node from an undirected graph
        """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)

def targeted_order(ugraph):
    """
        Compute a targeted attack order consisting
        of nodes of maximal degree
        
        Returns:
        A list of nodes
        """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)
        
        order.append(max_degree_node)
    return order

##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

def load_graph(graph_url):
    """
        Function that loads a graph given the URL
        for a text representation of the graph
        
        Returns a dictionary that models a graph
        """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    edges = 0 # added count the number of edges
    print "Loaded graph with", len(graph_lines), "nodes" #1239
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))
        edges += len(answer_graph[node])
    print "The number of edges are", edges/2 #3047
    return answer_graph

##########################################################
# plot function
def plot_graphy_resilience_random():
    """
        Computed the resilience for graphs,
        plot with random attack order
        """
    
    global counter
    counter += 1
    random_graph = make_random_undirected_graph(1239, 0.004)
    attack_order = random_order(random_graph)
    random_resilience = compute_resilience(random_graph, attack_order)
    plt.plot(range(len(random_resilience)), random_resilience, '-b', label= 'random, p =0.004')
    
    synthetic_undirected_graph = make_synthetic_undirected_graph(1239, 5)
    attack_order = random_order(synthetic_undirected_graph)
    synthetic_resilience = compute_resilience(synthetic_undirected_graph, attack_order)
    plt.plot(range(len(synthetic_resilience)), synthetic_resilience, '-r', label = 'UPA, m = 5')
    
    network_graph = load_graph(NETWORK_URL)
    attack_order = random_order(network_graph)
    network_resilience = compute_resilience(network_graph, attack_order)
    plt.plot(range(len(network_resilience)), network_resilience, '-g', label = 'Network')
    
    plt.legend(loc='upper right')
    
    plt.title(" plot of graph resilience")
    plt.xlabel("number of nodes removed")
    plt.ylabel("the size of the largest connect component ")
    plt.savefig("graph_resilience_"+str(counter)+".png", dpi = 72)
    plt.gcf().clear()  # hose-keeping

def plot_graphy_resilience_targeted():
    """
        Computed the resilience for graphs,
        plot with a targeted attack order
        """
    
    global counter
    counter += 1
    random_graph = make_random_undirected_graph(1239, 0.004)
    attack_order = fast_targeted_order(random_graph)
    random_resilience = compute_resilience(random_graph, attack_order)
    plt.plot(range(len(random_resilience)), random_resilience, '-b', label= 'random, p =0.004')
    
    synthetic_undirected_graph = make_synthetic_undirected_graph(1239, 5)
    attack_order = fast_targeted_order(synthetic_undirected_graph)
    synthetic_resilience = compute_resilience(synthetic_undirected_graph, attack_order)
    plt.plot(range(len(synthetic_resilience)), synthetic_resilience, '-r', label = 'UPA, m = 5')

    network_graph = load_graph(NETWORK_URL)
    attack_order = fast_targeted_order(network_graph)
    network_resilience = compute_resilience(network_graph, attack_order)
    plt.plot(range(len(network_resilience)), network_resilience, '-g', label = 'Network')
    
    plt.legend(loc='upper right')
    
    plt.title(" plot of graph resilience")
    plt.xlabel("number of nodes removed")
    plt.ylabel("the size of the largest connect component ")
    plt.savefig("graph_resilience_"+str(counter)+".png", dpi = 72)
    plt.gcf().clear()  # hose-keeping

def plot_running_time():
    """
        use the time module to compute the running time of these functions
        plot these running times (vertical axis) as a function of the number of nodes n 
        (horizontal axis) using a standard plot.
        """
    global counter
    counter += 1
    running_time_targeted = []
    running_time_fast_targeted = []
    
    for node_number in range(10, 1000, 10):
        synthetic_undirected_graph = make_synthetic_undirected_graph(node_number, 5)

        start_time = time.time()
        attack_order = targeted_order(synthetic_undirected_graph)
        stop_time = time.time()
        running_time_targeted.append(stop_time - start_time)
        
        start_time = time.time()
        attack_order = fast_targeted_order(synthetic_undirected_graph)
        stop_time = time.time()
        running_time_fast_targeted.append(stop_time - start_time)
    
    plt.plot(range(10, 1000, 10), running_time_targeted, '-b', label = 'targeted_order')
    plt.plot(range(10, 1000, 10), running_time_fast_targeted, '-r', label = 'fast_targeted_order')
    
    plt.legend(loc='upper right')


    plt.title(" plot of running time of desktop Python")
    plt.xlabel("the number of nodes")
    plt.ylabel("running times")
    plt.savefig("running_time_"+str(counter)+".png", dpi = 72)
    plt.gcf().clear()  # hose-keeping

def fast_targeted_order(ugraph):
    """
        creates a list degree_sets whose kth element is the set of nodes of degree k. 
        The method then iterates through the list degree_sets in order of decreasing degree.
        When it encounter a non-empty set, the nodes in this set must be of maximum degree. 
        The method then repeatedly chooses a node from this set, deletes that node from the graph, 
        and updates degree_sets appropriately.
        """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    degree_sets = {}            # degree_set[k] is a set of all nodes whose degree is k
    for k in range(len(new_graph)):
        degree_sets[k] = set([])
    
    for i in new_graph:
        d = len(new_graph[i])
        degree_sets[d].add(i)

    attack_order =[]
    n = len(new_graph)
    for k in reversed(range(n-1)):
        while len(degree_sets[k]):
            u = random.choice(tuple(degree_sets[k]))  # u is an arbitrary element in degree-set[k]
            degree_sets[k].remove(u)
            for v in new_graph[u]:                    # v is the neighbor of u
                d = len(new_graph[v])
                degree_sets[d].remove(v)
                degree_sets[d-1].add(v)

            attack_order.append(u)
            delete_node(new_graph, u)
                
    return attack_order


if __name__ == "__main__":
    start_time = time.time()
    #load_graph(NETWORK_URL)
    #random_graph = make_random_undirected_graph(1239, 0.004) #3092
    #synthetic_undirected_graph =  make_synthetic_undirected_graph(1239, 5)   #3046
    #plot_graphy_resilience_random()
    #fast_targeted_order(synthetic_undirected_graph)
    #plot_running_time()
    plot_graphy_resilience_targeted()
    print("---running time is %s seconds ---" % (time.time() - start_time))