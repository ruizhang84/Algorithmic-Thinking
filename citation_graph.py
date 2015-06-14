"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
import math
import random
import matplotlib.pyplot as plt
import time

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)

# global counter that records the number of plots
counter = 0

###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set()
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

#citation_graph = load_graph(CITATION_URL)

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

def compute_sum_in_degrees(digraph):
    """
        Takes a directed graph digraph
        and computes the sum of in-degrees for the nodes.
        return the total of in-degree and 
        a dictionary of in-degree
        """
    num_degree = compute_in_degrees(digraph)
    totindeg = 0
    for dummy_node in num_degree:
        totindeg += num_degree[dummy_node]
    return (totindeg, num_degree)

def compute_out_degrees_ave(digraph):
    """
        Takes a directed graph digraph
        and computes the average out-degrees for the nodes.
        """
    num_degree = []
    for node in digraph:
        num_degree.append(len(digraph[node]))
    return sum(num_degree)/float(len(digraph))

def in_degree_distribution(digraph):
    """
        Takes a directed graph digraph
        and computes the normalized distribution of the in-degrees.
        """
    degree_distr = {}
    num_degree = compute_in_degrees(digraph)
    for node in num_degree:
        degree_distr[num_degree[node]] = degree_distr.get(num_degree[node],0) + 1
    for degree in degree_distr:
        degree_distr[degree] = degree_distr[degree]/float(len(num_degree))
    return  degree_distr

#Representing directed graphs
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

def make_random_directed_graph(num_nodes, probility):
    """
        Takes the number of nodes n and the probility p
        returns a dictionary corresponding to a random directed graph
        with the specified number of nodes. (Algorithm ER)
        """
    graph = {}
    for dummy_node in range(num_nodes):
        graph[dummy_node] = set()
        for dummy_node_pair in range(num_nodes):
            if dummy_node_pair != dummy_node:
                a = random.random() # a real number [0,1)
                if a < probility:
                    graph[dummy_node].add(dummy_node_pair)
    return graph

def make_synthetic_directed_graph(num_nodes, num_exist):
    """
        Takes the number of nodes n, the probility p and the number of existing nodes m 
        to which a new node is connected during each iteration,
        returns a dictionary corresponding to a random synthetic directed graph
        with the specified number of nodes. (Algorithm DPA)
        """
    graph = {}
    graph = make_complete_graph(num_exist)              #creating a complete directed graph on m nodes
    dpa_graph = DPATrial(num_exist)
    for dummy_node in range(num_exist, num_nodes):
        node_neighbors = dpa_graph.run_trial(num_exist)
        graph[dummy_node] = set(node_neighbors)
    return graph


def plot_graphy(degree_distr):
    """
        log/log plot of the in degree distribution
        """
        
    global counter
    counter += 1
    for degree in degree_distr:
        if degree != 0:
            plt.plot(math.log(degree,10), math.log(degree_distr[degree],10), 'bo')
    plt.title("log/log plot of in-degree distribution")
    plt.xlabel(r'$log_{10}^{degree}$')
    plt.ylabel(r'$log_{10}^{in-degree\,distribution}$')
    plt.savefig("graph_in_degree_"+str(counter)+".png", dpi = 72)
    plt.gcf().clear()  # hose-keeping


def plot_graphy_simple(degree_distr):
    """
        simple plot of the in degree distribution
        """
    global counter
    counter += 1
    for degree in degree_distr:
            plt.plot(degree, degree_distr[degree], 'bo')
    plt.title("plot of in degree distribution")
    plt.xlabel(r'$degree$')
    plt.ylabel(r'$in-degree\,distribution$')
    plt.savefig("graph_in_degree_"+str(counter)+".png", dpi = 72)
    plt.gcf().clear()  # hose-keeping

#Helper class for implementing efficient version of DPA algorithm
#Provided code
class DPATrial:
    """
        Simple class to encapsulate optimized trials for DPA algorithm
        
        Maintains a list of node numbers with multiple instances of each number.
        The number of instances of each node number are
        in the same proportion as the desired probabilities
        
        Uses random.choice() to select a node number from this list for each trial.
        """
    
    def __init__(self, num_nodes):
        """
            Initialize a DPATrial object corresponding to a
            complete graph with num_nodes nodes
            
            Note the initial list of node numbers has num_nodes copies of
            each node number
            """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]
    
    def run_trial(self, num_nodes):
        """
            Conduct num_node trials using by applying random.choice()
            to the list of node numbers
            
            Updates the list of node numbers so that the number of instances of
            each node number is in the same ratio as the desired probabilities
            
            Returns:
            Set of nodes
            """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

if __name__ == "__main__":
    start_time = time.time()
    citation_graph = load_graph(CITATION_URL)
    citation_degree_distr = in_degree_distribution(citation_graph)
    compute_out_degrees_ave(citation_graph)
    random_directed_graph = make_random_directed_graph(10000, 0.5)
    random_directed_distr = in_degree_distribution(random_directed_graph)
    synthetic_directed_graph = make_synthetic_directed_graph(27770, 12)
    synthetic_directed_distr = in_degree_distribution(synthetic_directed_graph)
    plot_graphy(citation_degree_distr)
    plot_graphy(random_directed_distr)
    plot_graphy(synthetic_directed_distr)
    plot_graphy_simple(random_directed_distr)
    print("---running time is %s seconds ---" % (time.time() - start_time))


