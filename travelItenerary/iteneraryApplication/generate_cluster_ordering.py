import math
import numpy as np
import itenerary_generator as ig
from gratification import lat_lng_distance
from sklearn.decomposition import PCA


def closest_unvisited_cluster_index(cluster_centroid, cluster_centroids,visited_list):
	minim = 1000000
	output_index = -1
	for i in range(0,len(cluster_centroids)):
		cluster = cluster_centroids[i]
		if lat_lng_distance(cluster_centroid,cluster) < minim and visited_list[i] == 0:
			minim = lat_lng_distance(cluster_centroid,cluster)
			output_index = i
	return output_index

def max_gratification_cluster(cluster):
	grat_score = 0.0

	for POI in cluster:
		grat_score = max(grat_score, ig.gratification_sort(POI))
	return grat_score

def get_first_clusterList(centroid_list):
	cluster_index = 0
	pca = PCA(n_components = 1)
	pca.fit(centroid_list)
	X_pca = pca.transform(centroid_list)

	min_value = 10000

	for i in range(0,len(X_pca)):
		if(X_pca[i][0] < min_value):
			cluster_index = i
			min_value = X_pca[i][0]

	return cluster_index

def generate_order(cluster_list,cluster_centroids, no_clusters):
	current_cluster_index = get_first_clusterList(cluster_centroids)
	first_cluster = cluster_centroids[current_cluster_index]
	visited_list = np.zeros(no_clusters)
	cluster_list_fin = []
	cluster_centroid_fin = []
	cluster_list_fin.append(cluster_list[current_cluster_index])
	cluster_centroid_fin.append(cluster_centroids[current_cluster_index])
	visited_list[current_cluster_index] = 1
	

	for i in range(1,no_clusters):
		index = closest_unvisited_cluster_index(cluster_centroids[current_cluster_index],cluster_centroids,visited_list)
		current_cluster_index = index
		cluster_list_fin.append(cluster_list[index])
		cluster_centroid_fin.append(cluster_centroids[index])
		visited_list[index] = 1

	return (cluster_list_fin, cluster_centroid_fin)


