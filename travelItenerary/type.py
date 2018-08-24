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
                #print ">>>>>>>>>", json_data
                poi_types = json_data['types']
                for poi_type in poi_types:
                    new_type = Type(type_name = poi_type)
                    new_type.save()





