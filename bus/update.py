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
        log('warning - website of route ' + routeId + ' is broken or not found.')
        return None
    else:
        return page.text

def update_or_create_route(routeId, routeName):
    try:
        busRoute = BusRoute.objects.get(uid=routeId)
        if busRoute.name != routeName:
            log(' - '.join(['update', 'route', busRoute.uid,
                ' '.join(['name:', busRoute.name, 'to', routeName])]))
                # update - route - uid - name: name to name
            busRoute.name = routeName
            busRoute.save()
    except:
        busRoute = BusRoute(uid=routeId, name=routeName)
        log(' - '.join(['create', 'route', busRoute.uid, busRoute.name]))
        # create - route - uid - name
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
            log(' - '.join(['update', 'stop', busStop.uid,
                ' '.join(['name:', busStop.name, 'to', stopData['name']])]))
                # update - stop - uid - name: name to name
            busStop.name = stopData['name']
            busStop.save()
        if busStop.latitude != stopData['latitude']:
            log(' - '.join(['update', 'stop', busStop.uid, busStop.name, ' '.join(['latitude:',
                str(busStop.latitude), 'to', str(stopData['latitude'])])]))
                # update - stop - uid - name - latitude: latitude to latitude
            busStop.latitude = stopData['latitude']
            busStop.save()
        if busStop.longitude != stopData['longitude']:
            log(' - '.join(['update', 'stop', busStop.uid, busStop.name, ' '.join(['longitude:',
                str(busStop.longitude), 'to', str(stopData['longitude'])])]))
                # update - stop - uid - name - longitude: longitude to longitude
            busStop.longitude = stopData['longitude']
            busStop.save()
    except:
        busStop = BusStop(uid=stopData['uid'], name=stopData['name'],
            latitude=stopData['latitude'], longitude=stopData['longitude'])
        log(' - '.join(['create', 'stop', busStop.uid, busStop.name]))
        # create - stop - uid - name
        busStop.save()
    return busStop

def update_or_create_stops_on_route(route, stop, stopData):
    try:
        stopOnRoute = StopOnRoute.objects.get(route__uid=route.uid, stop__uid=stop.uid,
            direction=stopData['direction'], order=stopData['order'])
    except:
        stopOnRoute = StopOnRoute(route=route, stop=stop,
            direction=stopData['direction'], order=stopData['order'])
        log(' - '.join(['create', 'relationship', str(stopOnRoute)]))
        # create - relationship - StopOnRoute
        stopOnRoute.save()

def update_route(routeId):
    print('start update route ' + routeId)
    page = get_data_from_website(routeId)
    if not page:
        return None
    else:
        page_soap = BeautifulSoup(page, "html.parser")
        routeName = re.search('<span class="stationlist-title">(.+)</span>', page).group(1)
        route = update_or_create_route(routeId, routeName)
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
    print('complete update route ' + routeId + '\n')


def main():
    log('start update route time: ' + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    with open('bus/routeid.txt', encoding='utf8') as sourceFile:
        idSource = sourceFile.read()
    routeIds = re.findall("id: (\S+)", idSource)
    for routeId in routeIds:
        update_route(routeId)
    log('finish update route time: ' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '\n')

main()
