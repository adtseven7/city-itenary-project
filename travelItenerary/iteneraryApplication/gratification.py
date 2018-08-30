from .models import PointOfInterest, Type, Form
import scipy.stats as st
import math
from math import sin, cos, sqrt, atan2, radians
from heapq import nsmallest

R = 6373.0
matching_score = 8000

def p_mean(rating):
	return max(0.0, float(rating)/5.0)

def calc_popularity(POI):
	x = 3.5
	y = 20000
	multiplier = 1
	if(POI.google_rank <=10):
		multiplier*= 5.0/(POI.google_rank) + 0.5
	a = (float(POI.rating) * float(POI.no_people_who_rated) + x * y) / (float(POI.no_people_who_rated) + y)
	a = a* math.log(POI.no_people_who_rated)
	return math.exp(a/2)*(multiplier/2 + 0.5)


	# z_score = st.norm.ppf(0.995)
	# p = p_mean(POI.rating)
	# n = POI.no_people_who_rated
	# lower_bound = p+(z_score*z_score)/(2*n)
	# lower_bound -=z_score*math.sqrt((p*(1-p) + z_score*z_score/(4*n))/n)
	# lower_bound/=(1+z_score*z_score/n)

	# return lower_bound*5.0

def gratification_score(POI,form):
	POI_types = POI.types.all()
	form_types = form['type_tags']

	pref_score = 100
	for type in form_types:
		if type in POI_types:
			pref_score+=matching_score

	grat_score = math.log(pref_score)*calc_popularity(POI)*3
	return float(grat_score)

def lat_lng_distance(point1,point2):
	lat1 = radians(point1[0])
	lon1 = radians(point1[1])
	lat2 = radians(point2[0])
	lon2 = radians(point2[1])

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance

def dist_gratification(grat_score, POI, cluster_centroid, no_days):
	lat = POI.latitude
	lng = POI.longitude
	distance = lat_lng_distance((lat,lng),cluster_centroid)
	return grat_score*math.exp(-0.1*(no_days-1)*distance)


def dist_gratification_k_closest(grat_score,POI,cluster,k):
	ksmallest = nsmallest(k, cluster, lambda p : lat_lng_distance((p.latitude,p.longitude), (POI.latitude, POI.longitude)))
	mean = 0
	for point in ksmallest:
		mean+=lat_lng_distance((point.latitude,point.longitude), (POI.latitude, POI.longitude))
	mean = mean/k
	return grat_score*math.exp(-5*mean)

def calculate_cluster_center(cluster_list):
	centroid = [0,0]
	n = len(cluster_list)
	for POI in cluster_list:
		centroid[0]+=POI.latitude
		centroid[1]+=POI.longitude

	centroid[0]/n
	centroid[1]/n
	return tuple(centroid)
	
