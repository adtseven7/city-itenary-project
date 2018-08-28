import os
import django
import math
from decimal import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *

POI_objects = PointOfInterest.objects.all()

for POI in POI_objects:
    time_in_min = int(float(POI.average_time_spent) * 60.0)
    if time_in_min%5 != 0:
        print "haha"
        POI.average_time_spent = Decimal((5*(time_in_min/5)/60.0))
        POI.save()

