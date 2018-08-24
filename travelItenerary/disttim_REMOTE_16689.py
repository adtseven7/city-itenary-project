import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *

data_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"

done = {}

for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"):
    for name in files:
        file_name = os.path.join(root, name)
        if "dist" in file_name:
            with open(file_name) as data:
                for line in data.readlines():
                    json_data = json.loads(line)
                    if (json_data['source'], json_data['dest']) in done.keys():
                        continue
                    done[(json_data['source'], json_data['dest'])] = 1
                    try:
                        source_object = PointOfInterest.objects.get(POI_id=json_data['source'])
                        dest_object = PointOfInterest.objects.get(POI_id=json_data['dest'])
                        disttime_object = DistanceTime(source = source_object, dest = dest_object, distance = json_data['dist'], time = json_data['time'])
                        disttime_object.save()
                    except:
                        print "++++"
                        pass
