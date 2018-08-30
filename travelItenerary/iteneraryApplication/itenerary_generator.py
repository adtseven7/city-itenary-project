from .models import City, Type, PointOfInterest, OpenCloseTime, Photo, Form, DistanceTime
from sklearn.cluster import KMeans
import numpy as np
from tsp_solver import tsp_solver, calculate_time, calculate_time_upto
from .gratification import *
import json, datetime, copy
from django.core.serializers.json import DjangoJSONEncoder
import math
from .get_POI import get_POI_object
from .generate_cluster_ordering import generate_order
from decimal import *

half_day_time = 10.0
trip_time_start = 10.0
threshold = 12

grat_score_dict = dict()
grat_score_dist_dict = dict()

def generate_POI_dict(POI):
	POI_json = dict()
	POI_json['lat'] = float(POI.latitude)
	POI_json['lng'] = float(POI.longitude)
	POI_json['name'] = POI.POI_name
	POI_json['place_id'] = POI.POI_id
	POI_json['rating'] = float(POI.rating)
	POI_json['description'] = POI.description
	POI_json['cost'] = 10
	
	return POI_json

def generate_gratification_score_all(POI_list,form):
	global grat_score_dict
	for POI in POI_list:
		grat_score_dict[POI]=gratification_score(POI,form)
		grat_score_dist_dict[POI] = grat_score_dict[POI]

def gratification_sort(POI):
	return grat_score_dict[POI]

def dist_gratification_sort(POI):
	return grat_score_dist_dict[POI]

def cluster_gratification(cluster_list):
	avg_grat = 0.0
	for POI in cluster_list:
		avg_grat+=grat_score_dict[POI]
	if(len(cluster_list)==0):
		return 0.0
	avg_grat/=len(cluster_list)
	return avg_grat


def get_lat(POI):
	return POI.latitude

def get_lng(POI):
	return POI.longitude

def tour_sort_key(POI):
	return float(POI['time'])

def modify_time_to_spend(POI,no_days):
	if no_days==1:
		a = float(POI.average_time_spent)
		if(a<0.75):
			POI.average_time_spent = 0.75
		elif a>1.5:
			POI.average_time_spent = 1.5
		else:
			POI.average_time_spent = a

	elif no_days == 2:
		# print "NO OF DAYS are", no_days
		a = float(POI.average_time_spent)
		if(a<1.0):
			POI.average_time_spent = 1.0
		elif a>1.5:
			POI.average_time_spent = 1.5
		else:
			POI.average_time_spent = a

	elif no_days == 3:
		a = float(POI.average_time_spent)
		if(a<1.0):
			POI.average_time_spent = 1.0
		elif a>2.0:
			POI.average_time_spent = 2.0
		else:
			POI.average_time_spent = a
	POI.average_time_spent = Decimal(POI.average_time_spent)

	return POI


def generate_itenerary(form):
	city = form['city']
	start_date = form['start_date']
	end_date = form['end_date']

	no_days = (end_date - start_date).days + 1
	POI_list = []
	POI_querySet = PointOfInterest.objects.filter(POI_city = city)
	for POI in POI_querySet:
		if POI.google_rank > 20 and POI.no_people_who_rated <100:
			continue
		POI_list.append(POI)

	# print POI_list[1].average_time_spent
	# for i in range(0,len(POI_list)):
	# 	modify_time_to_spend(POI_list[i],no_days)

	# print POI_list[1].average_time_spent

	generate_gratification_score_all(POI_list,form)
	POI_list.sort(key=gratification_sort, reverse=True)
	for POI in POI_list:
		print ">>>>>>>>>>>>>>>>>>>>>>>>>...................", POI.POI_name, grat_score_dict[POI]

	while(len(POI_list) >= threshold*no_days):
		# print POI_list[-1]
		del POI_list[-1]
	kmeans = kMeanClustering(POI_list,no_days)
	
	cluster_list = []

	for i in range(0,no_days):
		cluster_list.append([])

	for i in range(0,len(POI_list)):
		cluster_list[kmeans.labels_[i]].append(POI_list[i])

	cluster_centroids = []
	(cluster_list,cluster_centroids) = generate_order(cluster_list,kmeans.cluster_centers_, no_days)
	# print ">>>>>>>>>>><<<<<<<<<<<<>>>>>>>>><<<<<<<<<<<<"
	# print cluster_centroids
	cluster_list = tsp_POI_delegation(cluster_list,cluster_centroids,no_days)
	
	cluster_list.sort(key = cluster_gratification, reverse = True)

	output = itenerary_json(cluster_list,form)
	
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
		minute_add = int(add * 60)
		minute_add = 5*(minute_add/5)
		add = float(minute_add/60.0)
		extra_time_list.append(0)
		# print ">>>>>>>>>>>>>***********", add
	return extra_time_list

# def new_find_route(cluster_list):
# 	no_days = len(cluster_list)
# 	sites_to_visit_list = [[]] * no_days
	
# 	for i in range(no_days):
# 		cluster_list[i].sort(key=gratification_sort, reverse=True)
# 		threshold = 11
# 		while len(cluster_list[i]) > threshold:
# 			extra_poi = cluster_list[i].pop(-1)
# 			if i < no_days-1:
# 				cluster_list[i+1].append(extra_poi)

# 		sites_to_visit_list[i] = reorder(cluster_list[i])
# 		time = calculate_time(sites_to_visit_list[i])
# 		while(time>half_day_time):
# 			POI_to_delegate = remove_site(sites_to_visit_list[i])				#removing the last element to fit the time inside half a day
# 			if i < no_days-1 :
# 				cluster_list[i+1].append(POI_to_delegate)
# 			sites_to_visit_list[i] = reorder(sites_to_visit_list[i])
# 			time = calculate_time(sites_to_visit_list[i])
	
# 	return sites_to_visit_list

# def remove_site(sites_list):
# 	grat_scores = [grat_score_dict[x] for x in sites_list]
# 	min_val = min(grat_scores)
# 	index_min = grat_scores.index(min_val)
# 	return sites_list.pop(index_min)

# def reorder(cluster):
# 	print '		reorder'
# 	bylat = copy.deepcopy(cluster)
# 	bylatRev = copy.deepcopy(cluster)
# 	bylng = copy.deepcopy(cluster)
# 	bylngRev = copy.deepcopy(cluster)

# 	bylat.sort(key=get_lat)
# 	bylatRev.sort(key=get_lat,reverse=True)
# 	bylng.sort(key=get_lng)
# 	bylngRev.sort(key=get_lng,reverse=True)

# 	times = [
# 		calculate_time(bylat),
# 		calculate_time(bylatRev),
# 		calculate_time(bylng),
# 		calculate_time(bylngRev)
# 	]
# 	sortedArrays = [
# 		bylat,
# 		bylatRev,
# 		bylng,
# 		bylngRev
# 	]

# 	sorted_times = sorted(times)
	
# 	for i in range(4):
# 		if sorted_times[0] == times[i]:
# 			return sortedArrays[i]

	


def tsp_POI_delegation(cluster_list,cluster_list_centroids, no_days):
	no_days = len(cluster_list)
	cluster_list_tsp = copy.deepcopy(cluster_list)
	for i in range(0,no_days-1):

		for POI in cluster_list[i]:
			grat_score_dist_dict[POI] = dist_gratification(grat_score_dict[POI],POI,cluster_list_centroids[i],no_days)

		cluster_list[i].sort(key=dist_gratification_sort, reverse=True)

		
		
		while(len(cluster_list[i]) >= threshold):
			extra_poi = cluster_list[i].pop(-1)
			cluster_list[i+1].append(extra_poi)

		
		cluster_list_tsp[i] = tsp_solver(cluster_list[i])
		time = calculate_time(cluster_list_tsp[i])
		while(time>half_day_time):
			for POI in cluster_list[i]:
				grat_score_dist_dict[POI] = dist_gratification(grat_score_dict[POI],POI,cluster_list_centroids[i],no_days)
				# grat_score_dict[POI] = dist_gratification_k_closest(grat_score_dict[POI],POI,cluster_list[i],2)
				# print POI, " gratification ", grat_score_dict[POI]
			cluster_list[i].sort(key=dist_gratification_sort, reverse=True)					
			POI_to_delegate = cluster_list[i].pop(-1)				#removing the last element to fit the time inside half a day

			cluster_list[i+1].append(POI_to_delegate)
			cluster_list_tsp[i] = tsp_solver(cluster_list[i])
			time = calculate_time(cluster_list_tsp[i])
			cluster_list_centroids[i] = calculate_cluster_center(cluster_list[i])

	i = no_days-1
	
	# for elem in cluster_list[0]:
	# 	print "----------", elem.POI_name, grat_score_dict[elem]

	for POI in cluster_list[i]:
		grat_score_dist_dict[POI] = dist_gratification(grat_score_dict[POI],POI,cluster_list_centroids[i],no_days)

	cluster_list[i].sort(key=dist_gratification_sort, reverse=True)

	while(len(cluster_list[i]) >= threshold):
		# print cluster_list[i][-1]
		cluster_list[i].pop(-1)

	cluster_list_tsp[i] = tsp_solver(cluster_list[i])
	time = calculate_time(cluster_list_tsp[i])

	extra_poi = []
	while(time>half_day_time):
		for POI in cluster_list[i]:
			grat_score_dist_dict[POI] = dist_gratification(grat_score_dict[POI],POI,cluster_list_centroids[i],no_days)
			# print POI, " gratification ", grat_score_dict[POI]	
			# grat_score_dict[POI] = dist_gratification_k_closest(grat_score_dict[POI],POI,cluster_list[i],2)
			# print "++++++++++++++++++++++", cluster_list[i][-1].POI_name
		# print cluster_list[i][-1]
		cluster_list[i].sort(key=dist_gratification_sort, reverse=True)
		extra_poi.append(cluster_list[i].pop(-1))			#removing the last element to fit the time inside half a day
		cluster_list_tsp[i] = tsp_solver(cluster_list[i])
		time = calculate_time(cluster_list_tsp[i])
		cluster_list_centroids[i] = calculate_cluster_center(cluster_list[i])
	
	reassign_sites(extra_poi, cluster_list_tsp)


	return cluster_list_tsp

def reassign_sites(extra_poi , cluster_list):
	extra_poi.sort(key = gratification_sort)
	print extra_poi
	print ">ADSDSADSADSADSAD"
	for poi in extra_poi:
		print u'considering excluded point {}'.format(poi.POI_name)
		#sort the clusters in increasing order of distance from this point
		dist_sorted_cluster_indices = sort_by_distance(poi, cluster_list)
		print cluster_list[dist_sorted_cluster_indices[0]]
		print "............."
		print "............."
		for cluster_index in dist_sorted_cluster_indices:
			print '		cluster {} is closest.'.format(cluster_index)
			if (half_day_time -  (calculate_time(cluster_list[cluster_index]) + float(poi.average_time_spent))) >= 0.75 :
				cluster_list[cluster_index].append(poi)
				print u'reassigned {} to cluster {}'.format(poi.POI_name , cluster_index)
				break
		
	for i in range(len(cluster_list)):
		print cluster_list[i]
		cluster_list[i] = tsp_solver(cluster_list[i])
		print "after tsp"
		print cluster_list[i]


def sort_by_distance(point, cluster_list_arg):
	cluster_list = copy.deepcopy(cluster_list_arg)
	return sorted(range(len(cluster_list)),
		key= lambda i : 
		lat_lng_distance(calculate_cluster_center(cluster_list[i]), (point.latitude , point.longitude))
	)

def itenerary_json(cluster_list,form):
	# extra_time_list = redistribute(cluster_list)
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
			POI_json['time'] = float(calculate_time_upto(POI,path))
			POI_json['time_spent'] = POI.average_time_spent
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

def time_difference(start_time,end_time):
	output=0;
	output+=(end_time.hour - start_time.hour)
	output+=(end_time.minute - start_time.minute)/60.0
	return output

def POI_time(time):
	output = 0;
	output+=(time.hour - trip_time_start)
	output+=time.minute/60.0
	return float(output)


def modify_itenerary(tour,event_name,event_start,event_end):
	start_day = tour['start_date'].split("T")[0];
	start_day = datetime.datetime.strptime(start_day, "%Y-%m-%d").date()
	# print tour
	if not check_itenerary_consistency(tour,event_name,event_start,event_end):
		return -1

	print "check itenerary passed"

	POI_is_present = False
	for i in range(0, len(tour['tour'])):
		path = tour['tour'][i]
		for POI in path:
			if POI['name']==event_name:
				
				POI_is_present = True
				start_time = event_start.split("T")[1]
				start_time = start_time.split("+")[0]
				start_time = datetime.datetime.strptime(start_time, '%H:%M:%S').time()
				date_travel = event_start.split("T")[0]
				date_travel = datetime.datetime.strptime(date_travel, "%Y-%m-%d").date()
				end_time = event_end.split("T")[1]
				end_time = end_time.split("+")[0]
				end_time = datetime.datetime.strptime(end_time, '%H:%M:%S').time()
				time_diff = time_difference(start_time,end_time)
				# print time_diff
				POI['time_spent'] = time_diff
				# print POI['time']
				POI['time'] = POI_time(start_time)
				# print POI['time']

				if (date_travel - start_day).days != i:
					path.remove(POI)
					tour['tour'][(date_travel - start_day).days].append(POI)

	if not POI_is_present:
		POI_object = get_POI_object(event_name, tour['city'])
		POI_obj_json = generate_POI_dict(POI_object)
		start_time = event_start.split("T")[1]
		start_time = start_time.split("+")[0]
		start_time = datetime.datetime.strptime(start_time, '%H:%M:%S').time()
		date_travel = event_start.split("T")[0]
		date_travel = datetime.datetime.strptime(date_travel, "%Y-%m-%d").date()
		end_time = event_end.split("T")[1]
		end_time = end_time.split("+")[0]
		end_time = datetime.datetime.strptime(end_time, '%H:%M:%S').time()
		time_diff = time_difference(start_time,end_time)
		# print time_diff
		POI_obj_json['time_spent'] = time_diff
		# print POI['time']
		POI_obj_json['time'] = float(start_time.hour + start_time.minute/60.0 - trip_time_start)
		# print POI['time']
		tour['tour'][(date_travel - start_day).days].append(POI_obj_json)

	for path in tour['tour']:
		path.sort(key=tour_sort_key)

	for path in tour['tour']:
		for i in range(0, len(path)):
			if i==0:
				path[i]['travel_time'] = 0;
			else:
				timeDiff = float(path[i]['time']) - float(path[i-1]['time']) - float(path[i-1]['time_spent'])
				path[i]['travel_time'] = math.floor(timeDiff*60)

	return tour


def get_actual_time_difference(POI_first, POI_second, city_name):
	POI_source = PointOfInterest.objects.filter(POI_city = city_name, POI_name = POI_first)
	POI_dest = PointOfInterest.objects.filter(POI_city = city_name, POI_name = POI_second)
	# print "ASDASDASDASD<>><><><<><><<><><><><><><><"
	Distance_time_object = DistanceTime.objects.filter(source = POI_source[0], dest = POI_dest[0])
	time_diff = Distance_time_object[0].time
	return float(time_diff)/60.0
	# return 0


def check_itenerary_consistency(tour,event_name,event_start,event_end):
	start_day = tour['start_date'].split("T")[0];
	start_day = datetime.datetime.strptime(start_day, "%Y-%m-%d").date()

	# POI = get_POI_object(event_name,tour['city'])

	for path_index in range(0,len(tour['tour'])):
		path = tour['tour'][path_index]
		for POI in path:
			if POI['name'] == event_name:
				continue;
			date_travel = event_start.split("T")[0]
			date_travel = datetime.datetime.strptime(date_travel, "%Y-%m-%d").date()
			if((date_travel - start_day).days > path_index):
				break;
			if((date_travel - start_day).days < path_index):
				return True


			start_time_event = event_start.split("T")[1]
			start_time_event = start_time_event.split("+")[0]
			start_time_event = datetime.datetime.strptime(start_time_event, '%H:%M:%S').time()
			end_time_event= event_end.split("T")[1]
			end_time_event = end_time_event.split("+")[0]
			end_time_event = datetime.datetime.strptime(end_time_event, '%H:%M:%S').time()

			POI_event_start_time = POI_time(start_time_event)
			POI_event_end_time = POI_time(end_time_event)
			POI_end_time = float(POI['time']) + float(POI['time_spent'])
			POI_start_time = float(POI['time'])
			if POI_event_start_time == POI_start_time or POI_event_end_time == POI_end_time:
				return False
			if POI_event_start_time < POI_start_time:
				if POI_event_end_time > POI_start_time:
					return False
				travel_time = POI_start_time - POI_event_end_time
				travel_time_actual = get_actual_time_difference(event_name,POI['name'],tour['city'])
				if travel_time >= travel_time_actual:
					return True
				return False

			print POI_start_time, " ", POI_end_time
			print POI_event_start_time, " ", POI_event_end_time

			if POI_start_time < POI_event_start_time:
				if POI_end_time > POI_event_start_time:
					return False
				travel_time = POI_event_start_time - POI_end_time
				print travel_time
				travel_time_actual = get_actual_time_difference(POI['name'],event_name,tour['city'])
				print travel_time_actual
				if round(travel_time,5) >= round(travel_time_actual,5):
					print POI["name"]
					print ".........................................."
					return True
				return False

	return True		


def value_function(grat_score, distance, no_days):
	#print ";;;;;;;;;;", grat_score, distance
	grat_score = float(grat_score)
	distance = float(distance)/10000.0
	return (grat_score**2) * math.exp(max(0, (no_days-1)) * (-distance))
	'''grat_score = float(grat_score)
	distance = float(distance)/1000.0
	divide = max(1, 500.0 / (no_days**3))
	return (grat_score**2) * math.exp(-distance/divide)
	'''


def generate_itenerary_greedy(POI_list, form):
	city = form['city']
	start_date = form['start_date']
	end_date = form['end_date']

	no_days = (end_date - start_date).days + 1
	POI_query_list = PointOfInterest.objects.filter(POI_city = city)
	generate_gratification_score_all(POI_list,form)
	POI_list = []
	for i in range(0, len(POI_query_list)):
		if POI_query_list[i].no_people_who_rated > 100:
			POI_list.append(POI_query_list[i])
	POI_list.sort(key=gratification_sort, reverse=True)
	# for i in range(10*no_days, len(POI_query_list)):
	# 	POI_list.pop()
	for elem in POI_list:
		print elem.POI_name, grat_score_dict[elem]
	visited = {}

	cluster_list = []
	no_days = (end_date - start_date).days + 1
	cur = 0
	final_path = []
	for day in range(1, no_days + 1):
		start = cur
		path = []
		time = 9.0 * 60.0
		while True:
			if POI_list[start] not in visited.keys():
				break
			start += 1
		path.append(POI_list[start])
		visited[POI_list[start]] = 1
		time += float(POI_list[start].average_time_spent) * 60.0
		pretime = time
		start_time = 9.0 * 60.0
		total_time = 9.0 * 60.0
		while True:
			if time - start_time > total_time:
				break
			value = -1000000000.0
			next_start = start + 1
			for i in range(0, len(POI_list)):
				if i == start:
					continue
				other_poi = POI_list[i]
				if other_poi in visited.keys():
					continue
				other_value = value_function(grat_score_dict[other_poi], DistanceTime.objects.get(source = POI_list[start], dest = other_poi).distance, no_days)

				if other_value > value:
					time = pretime + DistanceTime.objects.get(source = POI_list[start], dest = other_poi).time + (float(other_poi.average_time_spent) * 60.0)
					if time - start_time > total_time:
						time = pretime
						continue
					next_poi = other_poi
					value = other_value
					next_start = i

			if(value == -1000000000.0):
				break
			# print ":::::::::::", next_poi.POI_name, time

			path.append(next_poi)
			visited[next_poi] = 1
			pretime = time
			start = next_start

		final_path.append(path)
		for j in range(cur+1, len(POI_list)):
			if POI_list[j] not in visited.keys():
				cur = j
				break

	if no_days == 1:
		final_path[0] = tsp_solver(final_path[0])
	return final_path