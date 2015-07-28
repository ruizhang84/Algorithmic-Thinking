"""
   comopare hierarchical and k-means clustering
   """
# general import
import random
import urllib2
import matplotlib.pyplot as plt
import time

from clustering import *

# global variable
counter = 0

# Efficiency
def gen_random_clusters(num_clusters):
    """
       creates a list of clusters
       where each cluster in this list corresponds to one randomly generated point
       in the square with corners (+/-1,+/-1).
       """
    fips_codes, population, risk = 0, 0 ,0
    return [ Cluster(fips_codes, random.uniform(-1, 1), random.uniform(-1, 1), population, risk)
                     for dummy_idx in range(num_clusters)]

# Automation
def compute_distortion(cluster_list, data_table):
    """
        takes a list of clusters and uses cluster_error to compute its distortion.
        """
    distortion = []
    for cluster in cluster_list:
        distortion.append(cluster.cluster_error(data_table))
    return sum(distortion)

###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]

##########################################################
# plot function
def plot_clustering_efficiency():
    """
        plot  the running times of the functions slow_closest_pairs 
        and fast_closest_pair for lists of clusters of size 2 to 200.
        """
    global counter
    counter += 1
    
    # slow closest pairs
    slow_closest_pairs_time = []
    slow_closest_pairs_size = []
    for size in range(2, 201):
        cluster_size = gen_random_clusters(size)
        start_time = time.time()
        slow_closest_pair(cluster_size)
        total_time = time.time() - start_time
        # the plot points
        slow_closest_pairs_size.append(size)
        slow_closest_pairs_time.append(total_time)

    # fast closest pairs
    fast_closest_pairs_time = []
    fast_closest_pairs_size = []
    for size in range(2, 201):
        cluster_size = gen_random_clusters(size)
        start_time = time.time()
        fast_closest_pair(cluster_size)
        total_time = time.time() - start_time
        # the plot points
        fast_closest_pairs_size.append(size)
        fast_closest_pairs_time.append(total_time)


    plt.plot(slow_closest_pairs_size, slow_closest_pairs_time, '-b', label= 'slow closest paris')
    plt.plot(fast_closest_pairs_size, fast_closest_pairs_time, '-r', label = 'fast closest pairs')

    plt.legend(loc='upper right')

    plt.title(" plot of efficiency")
    plt.xlabel("number of initial clusters")
    plt.ylabel("running time of the function (s)")
    plt.savefig("efficiency_"+str(counter)+".png", dpi = 72)
    plt.gcf().clear()  # hose-keeping

# Quality
def plot_clustering_quality():
    global counter

    # Data 111 county
    data_table = load_data_table(DATA_111_URL)
    cluster_list = []
    for line in data_table:
        cluster_list.append(Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    
    ## point_h, point_k
    points_h = []
    points_k = []
    cluster_h = cluster_list
    counter += 1
    for output_cluster in range (20, 5, -1):
        cluster_h = hierarchical_clustering(cluster_h, output_cluster)
        cluster_k = kmeans_clustering(cluster_list, output_cluster, 5)
        
        distortion_h = compute_distortion(cluster_h, data_table)
        distortion_k = compute_distortion(cluster_k, data_table)

        points_h.append(distortion_h)
        points_k.append(distortion_k)

    plt.plot(range(20, 5, -1), points_h, '-b', label= 'hierarchical')
    plt.plot(range(20, 5, -1), points_k, '-r', label = 'k-means')
    
    plt.legend(loc='upper right')

    plt.title(" plot of quality for 111 county data")
    plt.xlabel("number of output clusters")
    plt.ylabel("the distortion ")
    plt.savefig("quality_"+str(counter)+".png", dpi = 72)
    plt.gcf().clear()  # hose-keeping



    # Data 290 county
    data_table = load_data_table(DATA_290_URL)
    cluster_list = []
    for line in data_table:
        cluster_list.append(Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    
    ## point_h, point_k
    points_h = []
    points_k = []
    counter += 1
    cluster_h = cluster_list
    for output_cluster in range (20, 5, -1):
        cluster_h = hierarchical_clustering(cluster_h, output_cluster)
        cluster_k = kmeans_clustering(cluster_list, output_cluster, 5)
        
        distortion_h = compute_distortion(cluster_h, data_table)
        distortion_k = compute_distortion(cluster_k, data_table)

        points_h.append(distortion_h)
        points_k.append(distortion_k)

    plt.plot(range(20, 5, -1), points_h, '-b', label= 'hierarchical')
    plt.plot(range(20, 5, -1), points_k, '-r', label = 'k-means')
    
    plt.legend(loc='upper right')

    plt.title(" plot of quality for 290 county data")
    plt.xlabel("number of output clusters")
    plt.ylabel("the distortion ")
    plt.savefig("quality_"+str(counter)+".png", dpi = 72)
    plt.gcf().clear()  # hose-keeping


    # Data 896 county
    data_table = load_data_table(DATA_896_URL)
    cluster_list = []
    counter += 1
    for line in data_table:
        cluster_list.append(Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    
    ## point_h, point_k
    points_h = []
    points_k = []
    cluster_h = cluster_list
    for output_cluster in range (20, 5, -1):
        cluster_h = hierarchical_clustering(cluster_h, output_cluster)
        cluster_k = kmeans_clustering(cluster_list, output_cluster, 5)
        
        distortion_h = compute_distortion(cluster_h, data_table)
        distortion_k = compute_distortion(cluster_k, data_table)

        points_h.append(distortion_h)
        points_k.append(distortion_k)

    plt.plot(range(20, 5, -1), points_h, '-b', label= 'hierarchical')
    plt.plot(range(20, 5, -1), points_k, '-r', label = 'k-means')
    
    plt.legend(loc='upper right')

    plt.title(" plot of quality for 896 county data")
    plt.xlabel("number of output clusters")
    plt.ylabel("the distortion ")
    plt.savefig("quality_"+str(counter)+".png", dpi = 72)
    plt.gcf().clear()  # hose-keeping



#########################
if __name__ == "__main__":
    #plot_clustering_efficiency()
    #data_table = load_data_table(DATA_111_URL)
    #cluster_list = []
    #for line in data_table:
    #    cluster_list.append(Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    #cluster_k = kmeans_clustering(cluster_list, 9, 5)
    #cluster_h = hierarchical_clustering(cluster_list, 9)
    #print compute_distortion(cluster_h, data_table)
    #print compute_distortion(cluster_k, data_table)
    plot_clustering_quality()

