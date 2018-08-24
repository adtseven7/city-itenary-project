import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *

<<<<<<< HEAD
data_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/data"

for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/data"):
=======
data_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"

done = {}

for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"):
>>>>>>> 34bfe6199204acbdafdf2998b566f26b82ccf926
    for name in files:
        file_name = os.path.join(root, name)
        if "dist" in file_name:
            with open(file_name) as data:
                for line in data.readlines():
                    json_data = json.loads(line)
<<<<<<< HEAD
=======
                    if (json_data['source'], json_data['dest']) in done.keys():
                        continue
                    done[(json_data['source'], json_data['dest'])] = 1
>>>>>>> 34bfe6199204acbdafdf2998b566f26b82ccf926
                    try:
                        source_object = PointOfInterest.objects.get(POI_id=json_data['source'])
                        dest_object = PointOfInterest.objects.get(POI_id=json_data['dest'])
                        disttime_object = DistanceTime(source = source_object, dest = dest_object, distance = json_data['dist'], time = json_data['time'])
                        disttime_object.save()
                    except:
<<<<<<< HEAD
                        print json_data['source'], json_data['dest'], "<<<<<<<<"
=======
                        print "++++"
                        pass
>>>>>>> 34bfe6199204acbdafdf2998b566f26b82ccf926
