import re
import shelve
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from bus.models import BusRoute, BusStop, StopOnRoute

def log(text):
    print(text)
    with open('update.log', 'a', encoding='utf8') as logFile:
        logFile.write(text + '\n')

def get_data_from_website(routeId):
    page = requests.get("https://ebus.gov.taipei/Route/StopsOfRoute?routeid=" + routeId)
    if page.status_code != 200:
        log('website of route ' + routeId + ' is broken or not found.')
        return None
    else:
        return page.text

def update_or_create_route(routeId, routeName):
    # check id and name
    try:
        busRoute = BusRoute.objects.get(uid=routeId)
        if busRoute.name != routeName:
            log(busRoute.name + ' is renamed to ' + routeName + '.')
            busRoute.name = routeName
            busRoute.save()
    except:
        busRoute = BusRoute(uid=routeId, name=routeName)
        log(busRoute.name + ' is created.')
        busRoute.save()
    return busRoute

def get_data_from_raw(stopsRawData, direction):
    stopsData = []
    for stopRawData in stopsRawData:
        order = int(stopRawData.find(class_='auto-list-stationlist-number').string)
        name = str(stopRawData.find(class_='auto-list-stationlist-place').string)
        uid = stopRawData.find(id='item_UniStopId')['value']
        latitude = float(stopRawData.find(id='item_Latitude')['value'])
        longitude = float(stopRawData.find(id='item_Longitude')['value'])
        stop = {'order': order, 'name': name, 'uid': uid,
            'latitude': latitude, 'longitude': longitude, 'direction':direction}
        stopsData.append(stop)
    return stopsData

def update_or_create_stop(stopData):
    try:
        busStop = BusStop.objects.get(uid=stopData['uid'])
        if busStop.name != stopData['name']:
            log(busStop.name + ' is renamed to ' + stopData['name'] + '.')
            busStop.name = stopData['name']
            busStop.save()
        if busStop.latitude != stopData['latitude']:
            log(busStop.name + '\'s latitude is changed from ' +
                str(busStop.latitude) + ' to ' + str(stopData['latitude']) + '.')
            busStop.latitude = stopData['latitude']
            busStop.save()
        if busStop.longitude != stopData['longitude']:
            log(busStop.name + '\'s longitude is changed from ' +
                str(busStop.longitude) + ' to ' + str(stopData['longitude']) + '.')
            busStop.longitude = stopData['longitude']
            busStop.save()
    except:
        busStop = BusStop(uid=stopData['uid'], name=stopData['name'],
            latitude=stopData['latitude'], longitude=stopData['longitude'])
        log(busStop.name + ' is created.')
        busStop.save()
    return busStop

def update_or_create_stops_on_route(route, stop, stopData):
    try:
        stopOnRoute = StopOnRoute.objects.get(route__uid=route.uid, stop__uid=stop.uid)
        if stopOnRoute.direction != stopData['direction']:
            log('direction is changed from ' + str(stopOnRoute.direction) +
                ' to ' + str(stopData['direction']) + '.')
            stopOnRoute.direction = stopData['direction']
            stopOnRoute.save()
        if stopOnRoute.order != stopData['order']:
            log('order is changed from ' + str(stopOnRoute.order) +
                ' to ' + str(stopData['order']) + '.')
            stopOnRoute.order = stopData['order']
            stopOnRoute.save()
    except:
        stopOnRoute = StopOnRoute(route=route, stop=stop,
            direction=stopData['direction'], order=stopData['order'])
        log('relationship between ' + str(stopOnRoute) + ' is created.')
        stopOnRoute.save()

def update_route(routeId):
    log('start update route ' + routeId)
    page = get_data_from_website(routeId)
    if not page:
        return None
    else:
        page_soap = BeautifulSoup(page, "html.parser")
        routeName = re.search('<span class="stationlist-title">(.+)</span>', page).group(1)
        route = update_or_create_route(routeId, routeName)

    # check stops on route
    stopsData = []
    stopsRawData = page_soap.find(id='GoDirectionRoute').find_all('span',
        class_='auto-list auto-list-stationlist')
    stopsData += get_data_from_raw(stopsRawData, direction=True)
    stopsRawData = page_soap.find(id='BackDirectionRoute').find_all('span',
        class_='auto-list auto-list-stationlist')
    stopsData += get_data_from_raw(stopsRawData, direction=False)

    for stopData in stopsData:
        stop = update_or_create_stop(stopData)
        update_or_create_stops_on_route(route, stop, stopData)

    log('complete update route ' + routeId)
