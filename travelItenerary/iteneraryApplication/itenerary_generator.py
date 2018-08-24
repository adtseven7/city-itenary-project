from .models import City, Type, PointOfInterest, OpenCloseTime, Photo, Form
from sklearn.cluster import KMeans
import numpy as np
from tsp_solver import tsp_solver, calculate_time, calculate_time_upto
from .gratification import gratification_score
import json, copy
from django.core.serializers.json import DjangoJSONEncoder

half_day_time = 12

grat_score_dict = dict()

def generate_gratification_score_all(POI_list,form):
	global grat_score_dict
	for POI in POI_list:
		grat_score_dict[POI]=gratification_score(POI,form)

def gratification_sort(POI):
	return grat_score_dict[POI]

def generate_itenerary(form):
	city = form['city']
	start_date = form['start_date']
	end_date = form['end_date']

	no_days = (end_date - start_date).days + 1
	POI_list = PointOfInterest.objects.filter(POI_city = city)
	generate_gratification_score_all(POI_list,form)
	kmeans = kMeanClustering(POI_list,no_days)
	
	cluster_list = []

	for i in range(0,no_days):
		cluster_list.append([])

	for i in range(0,len(POI_list)):
		cluster_list[kmeans.labels_[i]].append(POI_list[i])
	
	

	cluster_list = tsp_POI_delegation(cluster_list)
	# print(cluster_list[0])
	output = itenerary_json(cluster_list,form)
	#print(output)
	return output

def kMeanClustering(POI_list,no_days):
	coord_matrix = []
	for POI in POI_list:
		latitude = POI.latitude
		longitude = POI.longitude
		coord_matrix.append([latitude,longitude])
	kmeans = KMeans(n_clusters=no_days, random_state=0).fit(coord_matrix)
	return kmeans

def redistribute(cluster_list):
	extra_time_list = []
	for tour in cluster_list:
		add = (float(half_day_time) - float(calculate_time(tour))) / float(len(tour))
		extra_time_list.append(add)
	return extra_time_list

def tsp_POI_delegation(cluster_list):
	no_days = len(cluster_list)
	cluster_list_tsp = copy.deepcopy(cluster_list)
	for i in range(0,no_days-1):
		cluster_list[i].sort(key=gratification_sort, reverse=True)
		# extra >>>>>>>
		threshold = 15
		#print ">>>>>>>>>>>", i, len(cluster_list[i])
		for j in range(15, max(threshold, len(cluster_list[i]))):
			extra_poi = cluster_list[i].pop(-1)
			cluster_list[i+1].append(extra_poi)

		#print ">>>>>>>>>>>", i, len(cluster_list[i])
		
		# end >>>>>>>>>>
		cluster_list_tsp[i] = tsp_solver(cluster_list[i])
		time = calculate_time(cluster_list_tsp[i])
		while(time>half_day_time):
			POI_to_delegate = cluster_list[i].pop(-1)				#removing the last element to fit the time inside half a day
			cluster_list[i+1].append(POI_to_delegate)
			cluster_list_tsp[i] = tsp_solver(cluster_list[i])
			time = calculate_time(cluster_list_tsp[i])

	i = no_days-1
	cluster_list[i].sort(key=gratification_sort, reverse=True)

	# extra >>>>>>>
	threshold = 15
	#print ">>>>>>>>>>>", i, len(cluster_list[i])
	for j in range(15, max(threshold, len(cluster_list[i]))):
		extra_poi = cluster_list[i].pop(-1)

	#print ">>>>>>>>>>>", i, len(cluster_list[i])

	# end >>>>>>>>>>


	cluster_list_tsp[i] = tsp_solver(cluster_list[i])
	time = calculate_time(cluster_list_tsp[i])
	while(time>half_day_time):
			print "++++++++++++++++++++++", cluster_list[i][-1].POI_name
			del cluster_list[i][-1]			#removing the last element to fit the time inside half a day
			cluster_list_tsp[i] = tsp_solver(cluster_list[i])
			time = calculate_time(cluster_list_tsp[i])
	
	return cluster_list_tsp


def itenerary_json(cluster_list,form):
	extra_time_list = redistribute(cluster_list)
	json_output={}
	city = form['city']
	start_date = form['start_date']
	end_date = form['end_date']
	no_days = (end_date - start_date).days+1
	tour=[]

	ct = 0
	for path in cluster_list:
		#print "*******", extra_time_list[ct]
		path_json = []
		multiply = 0
		for POI in path:
			POI_json = dict()
			POI_json['lat'] = POI.latitude
			POI_json['lng'] = POI.longitude
			POI_json['name'] = POI.POI_name
			POI_json['place_id'] = POI.POI_id
			POI_json['rating'] = POI.rating
			POI_json['description'] = POI.description
			POI_json['time'] = float(calculate_time_upto(POI,path)) + (multiply * extra_time_list[ct])
			POI_json['time_spent'] = float(PointOfInterest.objects.get(POI_id = POI.POI_id).average_time_spent) + float(extra_time_list[ct])
			POI_json['cost'] = 10
			path_json.append(POI_json)
			multiply += 1
		tour.append(path_json)
		ct += 1
		# print(path)

	json_output['city'] = city.city_name
	json_output['start_date'] = start_date
	json_output['no_days'] = no_days
	json_output['tour'] = tour
	# print(json_output)
	return json.dumps(json_output,cls=DjangoJSONEncoder)
