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
                for site in json_data:
                    google_rank = site['rank']
                    try:
                        poi = PointOfInterest.objects.get(POI_name=site['name'])
                        poi.google_rank = google_rank
                        poi.save()
                    except:
                        print site['name'], "<<<<<<<<<<"


