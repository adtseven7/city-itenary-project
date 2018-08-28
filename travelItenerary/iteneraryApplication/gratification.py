from .models import PointOfInterest, Type, Form
import scipy.stats as st
import math

not_matching_score = 100
matching_score = 10000

def p_mean(rating):
	return max(0.0, float(rating)/5.0)

def calc_popularity(POI):
	x = 4.0
	y = 10000
	return ((float(POI.rating) * float(POI.no_people_who_rated) + x * y) / (float(POI.no_people_who_rated) + y))**2


	z_score = st.norm.ppf(0.995)
	p = p_mean(POI.rating)
	n = POI.no_people_who_rated
	lower_bound = p+(z_score*z_score)/(2*n)
	lower_bound -=z_score*math.sqrt((p*(1-p) + z_score*z_score/(4*n))/n)
	lower_bound/=(1+z_score*z_score/n)

	return lower_bound*5.0

def gratification_score(POI,form):
	POI_types = POI.types.all()
	form_types = form['type_tags']

	grat_score = 100
	for type in form_types:
		if type in POI_types:
			grat_score+=matching_score
		else:
			grat_score+=not_matching_score

	grat_score = math.log(grat_score) * calc_popularity(POI)
	return grat_score