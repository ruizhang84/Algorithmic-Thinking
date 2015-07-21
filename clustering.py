"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster

class Cluster:
    """
    Class for creating and merging clusters of counties
    """
    
    def __init__(self, fips_codes, horiz_pos, vert_pos, population, risk):
        """
        Create a cluster based the models a set of counties' data
        """
        self._fips_codes = fips_codes
        self._horiz_center = horiz_pos
        self._vert_center = vert_pos
        self._total_population = population
        self._averaged_risk = risk
        
        
    def __repr__(self):
        """
        String representation assuming the module is "alg_cluster".
        """
        rep = "alg_cluster.Cluster("
        rep += str(self._fips_codes) + ", "
        rep += str(self._horiz_center) + ", "
        rep += str(self._vert_center) + ", "
        rep += str(self._total_population) + ", "
        rep += str(self._averaged_risk) + ")"
        return rep


    def fips_codes(self):
        """
        Get the cluster's set of FIPS codes
        """
        return self._fips_codes
    
    def horiz_center(self):
        """
        Get the averged horizontal center of cluster
        """
        return self._horiz_center
    
    def vert_center(self):
        """
        Get the averaged vertical center of the cluster
        """
        return self._vert_center
    
    def total_population(self):
        """
        Get the total population for the cluster
        """
        return self._total_population
    
    def averaged_risk(self):
        """
        Get the averaged risk for the cluster
        """
        return self._averaged_risk
   
        
    def copy(self):
        """
        Return a copy of a cluster
        """
        copy_cluster = Cluster(set(self._fips_codes), self._horiz_center, self._vert_center,
                               self._total_population, self._averaged_risk)
        return copy_cluster


    def distance(self, other_cluster):
        """
        Compute the Euclidean distance between two clusters
        """
        vert_dist = self._vert_center - other_cluster.vert_center()
        horiz_dist = self._horiz_center - other_cluster.horiz_center()
        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)
        
    def merge_clusters(self, other_cluster):
        """
        Merge one cluster into another
        The merge uses the relatively populations of each
        cluster in computing a new center and risk
        
        Note that this method mutates self
        """
        if len(other_cluster.fips_codes()) == 0:
            return self
        else:
            self._fips_codes.update(set(other_cluster.fips_codes()))
 
            # compute weights for averaging
            self_weight = float(self._total_population)                        
            other_weight = float(other_cluster.total_population())
            self._total_population = self._total_population + other_cluster.total_population()
            self_weight /= self._total_population
            other_weight /= self._total_population
                    
            # update center and risk using weights
            self._vert_center = self_weight * self._vert_center + other_weight * other_cluster.vert_center()
            self._horiz_center = self_weight * self._horiz_center + other_weight * other_cluster.horiz_center()
            self._averaged_risk = self_weight * self._averaged_risk + other_weight * other_cluster.averaged_risk()
            return self

    def cluster_error(self, data_table):
        """
        Input: data_table is the original table of cancer data used in creating the cluster.
        
        Output: The error as the sum of the square of the distance from each county
        in the cluster to the cluster center (weighted by its population)
        """
        # Build hash table to accelerate error computation
        fips_to_line = {}
        for line_idx in range(len(data_table)):
            line = data_table[line_idx]
            fips_to_line[line[0]] = line_idx
        
        # compute error as weighted squared distance from counties to cluster center
        total_error = 0
        counties = self.fips_codes()
        for county in counties:
            line = data_table[fips_to_line[county]]
            singleton_cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
            singleton_distance = self.distance(singleton_cluster)
            total_error += (singleton_distance ** 2) * singleton_cluster.total_population()
        return total_error

######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    if idx1 == -1 or idx2 == -1:
        return (float('inf'), -1, -1)
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    distance = float('inf')
    idx1, idx2 = -1, -1
    for dummy_idx1 in range(len(cluster_list)):
        for dummy_idx2 in range(dummy_idx1+1, len(cluster_list)):
            if cluster_list[dummy_idx1].distance(cluster_list[dummy_idx2]) < distance:
                distance = cluster_list[dummy_idx1].distance(cluster_list[dummy_idx2])
                idx1 = dummy_idx1
                idx2 = dummy_idx2
    return pair_distance(cluster_list, idx1, idx2)



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    num = len(cluster_list)
    if num  <= 3:
        return slow_closest_pair(cluster_list)
    cluster_list.sort(key = lambda cluster_list: cluster_list.horiz_center())
    cluster_left  = cluster_list[:len(cluster_list)/2]
    cluster_right = cluster_list[len(cluster_list)/2:]
    distance_left,  idxl1, idxl2 = fast_closest_pair(cluster_left)
    distance_right, idxr1, idxr2 = fast_closest_pair(cluster_right)
    distance, idx1, idx2 = min([distance_left,  idxl1, idxl2], [distance_right, len(cluster_list)/2+idxr1, len(cluster_list)/2+idxr2])
    mid = (cluster_list[len(cluster_list)/2-1].horiz_center() + cluster_list[len(cluster_list)/2].horiz_center())/2.0
    return min((distance, idx1, idx2), closest_pair_strip(cluster_list, mid, distance))


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    cluster_s = []
    for cluster_i in range(len(cluster_list)):
        if abs(cluster_list[cluster_i].horiz_center() - horiz_center) < half_width:
            cluster_s.append(cluster_i)
    cluster_s.sort(key = lambda cluster_s: cluster_list[cluster_s].vert_center())
    distance = float('inf')
    idx1, idx2 = -1, -1
    for dummy_u in range(len(cluster_s)-1):
        temp_bound = min(dummy_u+3, len(cluster_s)-1)
        for dummy_v in range(dummy_u+1, temp_bound+1):
            dummy_idx1 = cluster_s[dummy_u]
            dummy_idx2 = cluster_s[dummy_v]
            if cluster_list[dummy_idx1].distance(cluster_list[dummy_idx2]) < distance:
                distance = cluster_list[dummy_idx1].distance(cluster_list[dummy_idx2])
                idx1 = dummy_idx1
                idx2 = dummy_idx2
    return pair_distance(cluster_list, idx1, idx2)
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    cluster = [dummy_cluster.copy() for dummy_cluster in cluster_list]
    while len(cluster) > num_clusters:
        cluster_i, cluster_j = fast_closest_pair(cluster)[1:]
        new_cluster = cluster[cluster_i].merge_clusters(cluster[cluster_j])
        temp_cluster = []
        for dummy_idx in range(len(cluster)):
            if dummy_idx != cluster_i and dummy_idx != cluster_j:
                temp_cluster += [cluster[dummy_idx]]
        temp_cluster += [new_cluster.copy()]
        cluster = temp_cluster
    return cluster


######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    cluster = [dummy_cluster.copy() for dummy_cluster in cluster_list]
    cluster.sort(key = lambda cluster_list: cluster_list.total_population(), reverse = True)
    # position initial clusters at the location of clusters with largest populations
    center = [dummy_cluster for dummy_cluster in cluster[:num_clusters]]
    for dummy_iter in range(num_iterations):
        cluster_k = [[] for dummy_id in range(num_clusters)]
        for dummy_idx in range(len(cluster_list)):
            distance = float('inf')
            for dummy_center in range(num_clusters):
                if cluster_list[dummy_idx].distance(center[dummy_center]) < distance:
                    distance = cluster_list[dummy_idx].distance(center[dummy_center])
                    cluster_sel = dummy_center
            if cluster_k[cluster_sel] == []:
                cluster_k[cluster_sel] = cluster_list[dummy_idx].copy()
            else:
                cluster_k[cluster_sel].merge_clusters(cluster_list[dummy_idx])
        for dummy_center in range(num_clusters):
            center[dummy_center] = cluster_k[dummy_center].copy()

    return cluster_k

