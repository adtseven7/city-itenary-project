import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *


for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"):
    for name in files:
        file_name = os.path.join(root, name)
        if "rating" in file_name:
            with open(file_name) as data:
                count = int(data.readlines()[0])
                poi_name = os.path.dirname(file_name).split('/')[-1]
                try: 
                	poi = PointOfInterest.objects.get(POI_name=poi_name)
                	poi.no_people_who_rated = count
                	poi.save()
                except:
                    pass

