import math
import numpy as np

def Euclidean(a,b):
	dist = math.pow(a[0]-b[0],2) + math.pow(a[1]-b[1],2)
	return math.sqrt(dist*1.0)

def closest_unvisited_cluster_index(cluster_centroid, cluster_centroids,visited_list):
	minim = 1000000
	output_index = -1
	for i in range(0,len(cluster_centroids)):
		cluster = cluster_centroids[i]
		if Euclidean(cluster_centroid,cluster) < minim and visited_list[i] == 0:
			minim = Euclidean(cluster_centroid,cluster)
			output_index = i
	return output_index


def generate_order(cluster_list,cluster_centroids, no_clusters):
	first_cluster = cluster_centroids[0]
	visited_list = np.zeros(no_clusters)
	cluster_list_fin = []
	cluster_list_fin.append(cluster_list[0])
	visited_list[0] = 1
	current_cluster_index = 0

	for i in range(1,no_clusters):
		index = closest_unvisited_cluster_index(cluster_centroids[current_cluster_index],cluster_centroids,visited_list)
		current_cluster_index = index
		cluster_list_fin.append(cluster_list[index])
		visited_list[index] = 1

	return cluster_list_fin


