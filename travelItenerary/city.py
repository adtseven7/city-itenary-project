import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *


for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"):
    for name in files:
        file_name = os.path.join(root, name)
        if "description" in file_name:
            with open(file_name) as data:
                city_name =  os.path.dirname(file_name).split('/')[-1]
                description = data.readlines()[0]
                city = City(city_name=city_name, city_description=description)
                city.save()                

                

