import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *

# data_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"

# done = {}

# for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + "/new_data"):
#     for name in files:
#         file_name = os.path.join(root, name)
#         if "dist" in file_name:
#             with open(file_name) as data:
#                 for line in data.readlines():
#                     json_data = json.loads(line)
#                     if (json_data['source'], json_data['dest']) in done.keys():
#                         continue
#                     done[(json_data['source'], json_data['dest'])] = 1
#                     try:
#                         source_object = PointOfInterest.objects.get(POI_id=json_data['source'])
#                         dest_object = PointOfInterest.objects.get(POI_id=json_data['dest'])
#                         disttime_object = DistanceTime(source = source_object, dest = dest_object, distance = json_data['dist'], time = json_data['time'])
#                         disttime_object.save()
#                     except:
#                         print "++++"
#                         pass

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from bs4 import BeautifulSoup as bs
from time import sleep
import json
import os

driver = webdriver.Chrome()
driver.get("http://www.google.com")

def search_on_tripadvisor(tripadvisorQueryString):
    try:
        print(tripadvisorQueryString)
        driver.get("http://www.google.com")    
        inputElement = driver.find_element_by_name("q")
        inputElement.send_keys(tripadvisorQueryString)
        inputElement.submit()

        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        WebDriverWait(driver, 10).until(EC.title_contains(tripadvisorQueryString))
        soup = bs(driver.page_source , 'html.parser')
        tripAdvisorLink = soup.find_all('h3',{'class':'r'})[0].a['href']
        driver.get(tripAdvisorLink)
        WebDriverWait(driver, 15).until(EC.title_contains('TripAdvisor'))
        soup = bs(driver.page_source , 'html.parser')
        rating = soup.select('span[class*="overallRating"]')[0].text
        print rating
        rating_n = int(soup.select('a[class*="seeAllReviews"]')[0].text.split(' ')[0].replace(',',''))
        print rating_n
        return (rating,rating_n)
    except:
        return (0,1)



#search_on_tripadvisor('Latin Quarters paris tripadvisor rating')
poiList = PointOfInterest.objects.filter(rating=0)
for poi in poiList:
    poi.rating , poi.no_people_who_rated = search_on_tripadvisor(u'{} {} tripadvisor rating'.format(poi.POI_name , poi.POI_city_id))
    try:
        poi.save()
    except:
        print 'error'



driver.quit();