import re
import shelve
import json
from time import sleep
from datetime import datetime, timedelta

import requests

from busInfo.models import BusRoute, BusStop


logFileDir = 'busInfo/update.log'
dbRoute = 'busInfo/db/route'
dbStop = 'busInfo/db/stop'

logFile = open(logFileDir, 'a', encoding='utf8')
routeData = shelve.open(dbRoute)
stopData = shelve.open(dbStop)

def log(text):
    logFile.write(text + '\n')
    print(text)

def get_route_uid():
    with open('busInfo/routeid.txt', encoding='utf8') as sourceFile:
        idSource = sourceFile.read()
    return re.findall("id: (\S+)", idSource)

def request_info(url):
    page = requests.get(url)
    sleep(0.5)
    if page.status_code != 200:
        # it's usually 404 page
        log('warning - website ' + url + ' is broken or not found.')
        return None
    try:
        jsonTxt = re.search('= JSON\.stringify\((.+)\);', page.text).group(1)
        info = json.loads(jsonTxt)
        return info
    except:
        # a url redirect to other page cause this
        log('warning - info of ' + url + ' can\'t be extracted.')

def add_stop_to_queue(stopUID):
    # add into update queue if stop has not be updated
    if not stopUID in stopDone and not stopUID in stopUndone:
        stopUndone.add(stopUID)

def get_route_object(routeUID):
    # get data in db or create one
    try:
        busRoute = routeData[routeUID]
        if busRoute.updateTime > datetime.now() + timedelta(days=-1):
            for stopUID in busRoute.routeForward + busRoute.routeBackward:
                add_stop_to_queue(stopUID)
            return None
    except KeyError:
        busRoute = BusRoute(uid=routeUID)
        log('created - route - ' + busRoute.uid)
    return busRoute

def update_route_name(busRoute, name):
    if busRoute.name != name:
        # use str(name) to prevent name is None
        busRoute.name = str(name)
        log('update - ' + busRoute.uid + ' - name - ' + busRoute.name + ' to ' + str(name))

def scan_stops(stopsList):
    routeStops = []
    for stop in stopsList:
        stopUID = stop['UniStopId']
        routeStops.append(stopUID)
        # add new stop into the queue
        add_stop_to_queue(stopUID)
    return routeStops

def update_stops_on_route(busRoute, stopsList, direction):
    if stopsList:
        stops = scan_stops(stopsList)
        if direction:
            if busRoute.routeForward != stops:
                log('update - ' + busRoute.uid + ' ' + busRoute.name + ' - forward route')
                busRoute.routeForward = stops
        else:
            if busRoute.routeBackward != stops:
                log('update - ' + busRoute.uid + ' ' + busRoute.name + ' - backward route')
                busRoute.routeBackward = stops

def update_route(routeUID):
    # get route object from db, break if been updated in one day
    route = get_route_object(routeUID)
    if not route:
        return None
    # get data from web, break if fail
    url = "https://ebus.gov.taipei/Route/StopsOfRoute?routeid=" + routeUID
    info = request_info(url)
    if not info:
        return None
    # update data
    update_route_name(route, info['Name'])
    update_stops_on_route(route, info['GoDirStops'], True)
    update_stops_on_route(route, info['BackDirStops'], False)
    # save date
    route.updateTime = datetime.now()
    routeData[route.uid] = route
    print(route.name + ' is updated.')


def add_route_to_queue(routeUID):
    # add into update queue if route has not be updated
    if not routeUID in routeDone and not routeUID in routeUndone:
        routeUndone.add(routeUID)

def get_stop_object(stopUID):
    # get data in db or create one
    try:
        busStop = stopData[stopUID]
        if busStop.updateTime > datetime.now() + timedelta(days=-1):
            for routeUID in busStop.route:
                add_route_to_queue(routeUID)
            return None
    except KeyError:
        busStop = BusStop(uid=stopUID)
        log('create - stop - ' + busStop.uid)
    return busStop

def update_stop_name(busStop, name):
    if busStop.name != name:
        # use str(name) to prevent name is None
        busStop.name = str(name)
        log('update - ' + busStop.uid + ' - name ' + busStop.name + ' to ' + str(name))

def update_latitude(busStop, latitude):
    if busStop.latitude != latitude:
        busStop.latitude = latitude
        log('update - ' + busStop.uid + ' ' + busStop.name + ' - latitude')

def update_longitude(busStop, longitude):
    if busStop.longitude != longitude:
        busStop.longitude = longitude
        log('update - ' + busStop.uid + ' ' + busStop.name + ' - longitude')

def update_route_of_stop(busStop, routeOfStop):
    routes = []
    for route in routeOfStop:
        routeUID = route['UniRouteId']
        if re.match('\d{9}0', routeUID):
            routes.append(routeUID)
            # add new route into the queue, ids not end with 0 are not used
            add_route_to_queue(routeUID)
    if busStop.route != routes:
        busStop.route = routes
        log('update - ' + busStop.uid + ' ' + busStop.name + ' - route')

def update_stop(stopUID):
    # get stop object from db, break if been updated in one day
    stop = get_stop_object(stopUID)
    if not stop:
        return None
    # get data from web, break if fail
    url = "https://ebus.gov.taipei/Stop/RoutesOfStop?stopid=" + stopUID
    info = request_info(url)
    if not info:
        return None
    # update data
    update_stop_name(stop, info['Name'])
    update_latitude(stop, info['Latitude'])
    update_longitude(stop, info['Longitude'])
    update_route_of_stop(stop, info['RoutesNumber'])
    # save date
    stop.updateTime = datetime.now()
    stopData[stop.uid] = stop
    print(stop.name + ' is updated.')


log('start update route time: ' + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
# sets to record each object is updated or not
# program start with ids got from get_route_uid()
routeUndone = set(get_route_uid())
routeDone = set()
stopUndone = set()
stopDone = set()

while(len(routeUndone) + len(stopUndone)):
    while(len(routeUndone)):
        routeUID = routeUndone.pop()
        routeDone.add(routeUID)
        update_route(routeUID)
    while(len(stopUndone)):
        stopUID = stopUndone.pop()
        stopDone.add(stopUID)
        update_stop(stopUID)

log(str(len(routeDone)) + ' routes and ' + str(len(stopDone)) + ' stops are updated.')
log('finish update route time: ' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '\n')


routeData.close()
stopData.close()
logFile.close()
