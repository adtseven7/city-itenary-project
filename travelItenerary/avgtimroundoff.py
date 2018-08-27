import os
import django
import math
from decimal import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *

POI_objects = PointOfInterest.objects.all()

for POI in POI_objects:
    if POI.average_time_spent != Decimal(1.0):
        print POI.average_time_spent

