import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelItenerary.settings")

django.setup()
from iteneraryApplication.models import *


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from bs4 import BeautifulSoup as bs
from time import sleep


driver = webdriver.Chrome()
driver.get("http://www.google.com")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def find_mean(arr):
    sum = 0.0
    for el in arr:
        if el >= 15:
            el = float(el)/60
        sum += el
    return sum/len(arr)

def getAvgTime(site , city):
    try:
        times = []
        driver.get("http://www.google.com")    
        inputElement = driver.find_element_by_name("q")
        inputElement.clear()
        inputElement.send_keys(site+' '+city)
        inputElement.submit()
        WebDriverWait(driver, 15).until(EC.title_contains(site))
        soup = bs(driver.page_source , 'html.parser')
        try:
            times = [float(s) for s in soup.select('div[class*="UYKlhc"]')[0].b.text.replace('-',' ').split(' ') if is_number(s)]
            print times
        except:
            times = []

        #UYKlhc

        inputElement = driver.find_element_by_name("q")
        inputElement.clear()
        inputElement.send_keys(site+' '+city+' tripadvisor 2018 what to know')
        inputElement.submit()
        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        WebDriverWait(driver, 10).until(EC.title_contains(site))
        soup = bs(driver.page_source , 'html.parser')
        tripAdvisorLink = soup.find_all('h3',{'class':'r'})[0].a['href']
        driver.get(tripAdvisorLink)
        WebDriverWait(driver, 15).until(EC.title_contains('TripAdvisor'))
        soup = bs(driver.page_source , 'html.parser')
        durationSpan = soup.select('span[class*="ui_icon duration"]')[0]
        print(durationSpan)
        durationText = durationSpan.parent.text
        print(durationText)
        durationText = durationText.replace('-',' ')
        for s in durationText.split(' '):
             if is_number(s):
                print 'appended {}'.format(s)
                times.append(float(s))
        
    except Exception as e:
        print 'line 66'
        print e
    finally:
        if len(times) > 0:
            print 'returned {}'.format(find_mean(times))
            return find_mean(times)
        else:
            print 'returned 1'
            return 1



poiList = PointOfInterest.objects.filter(average_time_spent__gt=4)
for poi in poiList:
    poi.average_time_spent = getAvgTime(poi.POI_name , poi.POI_city_id)
    print poi.average_time_spent
    try:
        poi.save()
        # print 'updated {} , {} to {}'.format(poi.POI_name, poi.POI_city_id , poi.average_time_spent)
    except Exception as e:
        print 'error saving'
        print e
        raw_input('press enter to continue')


driver.quit();