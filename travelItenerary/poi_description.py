import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *


for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"):
    for name in files:
        file_name = os.path.join(root, name)
        if "sites.json" in file_name:
            with open(file_name) as data:
                json_data = json.load(data)
                for place in json_data:
                    name = place['name']
                    des = place['description']
                    try:
                        POI = PointOfInterest.objects.get(POI_name = name)
                        POI.description = des
                        POI.save()
                    except:
                        #print name, des, "<<<<<<<<<<<<<"
                        pass

                

