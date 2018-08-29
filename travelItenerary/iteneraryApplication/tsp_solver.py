from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np
from .models import DistanceTime
from decimal import *
import tsp

def create_distance_callback(dist_matrix):
  # Create a callback to calculate distances between cities.

	def distance_callback(from_node, to_node):
		return int(dist_matrix[from_node][to_node])

	return distance_callback

dist_matrix = []

def create_distance_matrix(POI_list):
	no_POI = len(POI_list)+1
	dist_matrix = np.zeros((no_POI,no_POI))
	for i in range(0,no_POI):
		for j in range(0,no_POI):
			if i==0 or j==0:
				dist_matrix[i][j]=0
			elif i==j:
				dist_matrix[i][j] = 0
			else:
				distance_i_to_j_object = DistanceTime.objects.filter(source = POI_list[i-1], dest = POI_list[j-1])
				dist_matrix[i][j] = Decimal(float(distance_i_to_j_object[0].distance))
	print 
	return dist_matrix



def tsp_solver(POI_list):

	tsp_size = len(POI_list)+1
	num_routes = 1
	depot = 0
	dist_matrix = create_distance_matrix(POI_list)
	route = []


	# Create routing model
	if tsp_size > 1:
		routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
		search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
		# Create the distance callback.
		dist_callback = create_distance_callback(dist_matrix)
		routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
		assignment = routing.SolveWithParameters(search_parameters)		# Solve the problem.
		if assignment:
	    	# Solution distance.
			# print "Total time: " + str(assignment.ObjectiveValue()) + " minutes\n"
	    	# Display the solution.
	    	# Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
			route_number = 0
			index = routing.Start(route_number) # Index of the variable for the starting node.
			index = assignment.Value(routing.NextVar(index))
			while not routing.IsEnd(index):
				print routing.IndexToNode(index)

		 		# Convert variable indices to node indices in the displayed route.
		 		
				route.append(POI_list[routing.IndexToNode(index)-1])
				index = assignment.Value(routing.NextVar(index))
			# route.append(POI_list[routing.IndexToNode(index)-1])
	    	# route.append(POI_list[routing.IndexToNode(index)])
			# print "route calculated"
		else:
			print 'No solution found.'
	elif tsp_size == 2:
		route.append(POI_list[0])
	else:
		print 'Specify an instance greater than 0.'
	# print "printing route ABABABABBABABBABBBBABBAB"
	# print route
	return route

# def tsp_solver(POI_list):
# 	tsp_size = len(POI_list)
# 	depot = 0
# 	dist_matrix = create_distance_matrix(POI_list)
# 	route = []

# 	r = range(len(dist_matrix))
# 	# Dictionary of distance
# 	dist = {(i, j): dist_matrix[i][j] for i in r for j in r}
# 	route_index = tsp.tsp(r, dist)[1]
# 	for i in range(1,len(route_index)):
# 		route.append(POI_list[route_index[i]-1])
# 	return route

def calculate_time(path):
	path_len = len(path)
	# print "Printing path length"
	# print path_len
	time=0;
	for i in range(0,path_len-1):
		distance_to_next_object = DistanceTime.objects.filter(source = path[i], dest = path[i+1])
		time+=path[i].average_time_spent
		time+=max(Decimal(0.25), Decimal(distance_to_next_object[0].time/60.0))
	time+=path[path_len-1].average_time_spent
	return float(time)

def calculate_time_upto(POI, path):
	path_len = len(path)
	time=0;
	for i in range(0,path_len-1):
		if path[i] == POI:
			return time

		distance_to_next_object = DistanceTime.objects.filter(source = path[i], dest = path[i+1])
		time+=path[i].average_time_spent
		time+=Decimal(distance_to_next_object[0].time/60.0)

	if path[path_len-1] == POI:
		return time

	return -1