import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *



for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"):
    for name in files:
        file_name = os.path.join(root, name)
        if "info" in file_name:
            with open(file_name) as data:
                json_data = json.load(data)
               # print ">>>>>>>>", json_data

                new_poi = PointOfInterest()
                #print "+++++++++", os.path.dirname(file_name)
                try:
                    new_poi.POI_city = City.objects.get(city_name = os.path.dirname(file_name).split('/')[-3])
                except:
                    print os.path.dirname(file_name).split('/')[-3]
                new_poi.POI_name = os.path.dirname(file_name).split('/')[-1]
                new_poi.latitude = json_data['lat']
                new_poi.longitude = json_data['lng']
                new_poi.POI_id = json_data['place_id']
                try: new_poi.rating = json_data['rating']
                except: new_poi.rating = 2.5
                
                new_poi.save()
                #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", new_poi.POI_name
                    
                poi_types = json_data['types']
                for poi_type in poi_types:
                        new_poi.types.add(poi_type)

