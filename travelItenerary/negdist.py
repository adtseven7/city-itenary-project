import os
import django
import math

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *

DistTime = DistanceTime.objects.all()

for disttimObject in DistTime:
    distance = disttimObject.distance
    if distance < 0:
        [lat1, lon1] = [math.radians(disttimObject.source.latitude), math.radians(disttimObject.source.longitude)]
        [lat2, lon2] = [math.radians(disttimObject.dest.latitude), math.radians(disttimObject.dest.longitude)]
        R = 6373.0
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c * 1000
        #print lat1, lon1, '>', lat2, lon2, '=', distance
        disttimObject.distance = distance
        disttimObject.time = distance / 666
        disttimObject.save()

    time = disttimObject.time
    newtime = time
    if time < 5: 
        newtime = 5
    else:
        newtime = 5*(time/5)
    disttimObject.time = newtime
    disttimObject.save()


