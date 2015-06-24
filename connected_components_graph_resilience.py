"""
    Connected components and graph resilience.
    """
# general import
import time
from collections import deque

def bfs_visited(ugraph, start_node):
    """
        Takes the undirected graph ugraph and the node start_node 
        and returns the set consisting of all nodes that are visited 
        by a breadth-first search that starts at start_node.
        """
    # maintain a queue of visiting nodes
    queue = deque()
    visited = set([start_node])
    
    queue.append(start_node)                # push the start node into the queue
    while queue:                            # while queue is not empty
        node = queue.popleft()              # expand the node
        for neighbor in ugraph[node]:       # get the neighbor of node
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited

# connected component
def cc_visited(ugraph):
    """
        Takes the undirected graph ugraph and returns a list of sets, 
        where each set consists of all the nodes in a connected component.
        """
    connected_component = []
    visited = set()
    for start_node in ugraph:
        if start_node not in visited:
            visited_temp = bfs_visited(ugraph, start_node)
            connected_component.append(visited_temp)
            visited.update(visited_temp)
    return connected_component

def largest_cc_size(ugraph):
    """
        Takes the undirected graph ugraph 
        and returns the size (an integer) of the largest connected component in ugraph.
        """
    largest_cc = 0
    for start_node in ugraph:
        visited = bfs_visited(ugraph, start_node)
        temp_size = len(visited)
        if largest_cc < temp_size:
            largest_cc = temp_size
    return largest_cc


# graph resilience
def compute_resilience(ugraph, attack_order):
    """
        Takes the undirected graph ugraph, a list of nodes attack_order
        For each node in the list, the function removes the given node and its edges from the graph 
        and then computes the size of the largest connected component for the resulting graph.
        return a list whose k+1th entry is the size of the largest connected component in the graph 
        after the removal of the first k nodes in attack_order.
        """
    # make a subset of graph exclude node in attack_order
    sub_graph = make_subgraph(ugraph, attack_order)

    # make clusters of subset graph
    root = {}                                       # path compression
    root_cc = {}                                    # connected component
    max_cc = 0
    resilience = deque()                            # largest connected components
    for node in sub_graph:
        if node not in root:
            visited = bfs_visited(sub_graph, node)
            for connected_node in visited:
                root[connected_node] = node
            root_cc[node] = len(visited)
            if root_cc[node] > max_cc:
                max_cc = root_cc[node]
    resilience.appendleft(max_cc)

    for dummy_idx in range(len(attack_order)):
        attacker = attack_order[-dummy_idx-1]
        union_node = set([])
        for dummy_id in ugraph[attacker]:
            if dummy_id not in attack_order[:-dummy_idx-1]:
                union_node.add(root[dummy_id])              # nodes to union

        # union-find
        root_cc[attacker] = 1
        root[attacker] = attacker

        for node in union_node:
            root_cc[attacker] += root_cc[node]
            del root_cc[node]
            
            for key in root:
                if root[key] == node:
                    root[key] = attacker

        # update largest cc
        if max_cc < root_cc[attacker]:
            max_cc = root_cc[attacker]
        resilience.appendleft(max_cc)

    return list(resilience)

def make_subgraph(ugraph, attack_order):
    """
        split compte_resilience function
        make a subset of graph exclude node in attack_order
        """
    sub_graph = {}
    for node in ugraph:
        if node not in attack_order:
            sub_graph[node] = set([])
            for neighbor in ugraph[node]:
                if neighbor not in attack_order:
                    sub_graph[node].add(neighbor)
    return sub_graph

if __name__ == "__main__":
    start_time = time.time()
    GRAPH1 = {0: set([1, 2, 3, 4]),
          1: set([0, 2, 3, 4]),
          2: set([0, 1, 3, 4]),
          3: set([0, 1, 2, 4]),
          4: set([0, 1, 2, 3])}
    
    print compute_resilience(GRAPH1, [2, 4, 3, 1])
    print("---running time is %s seconds ---" % (time.time() - start_time))