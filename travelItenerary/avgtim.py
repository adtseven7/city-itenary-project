import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *


for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"):
    for name in files:
        file_name = os.path.join(root, name)
        if "avg_time" in file_name:
            with open(file_name) as data:
                time = float(data.readlines()[0])
                print time
                '''
                poi_name = os.path.dirname(file_name).split('/')[-1]
                try:
                	poi = PointOfInterest.objects.get(POI_name=poi_name)
                	poi.average_time_spent = time
                	poi.save()
                except:
                    pass

                '''

