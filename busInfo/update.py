import re
import shelve
import json
from time import sleep
from datetime import datetime

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
        log('website ' + url + ' is broken or not found.')
        return None
    try:
        jsonTxt = re.search('= JSON\.stringify\((.+)\);', page.text).group(1)
        info = json.loads(jsonTxt)
        return info
    except:
        log('info of ' + url + ' can\'t be extracted.')

def update_route_info(routeUID, name):
    # get data in db or create one
    try:
        busRoute = routeData[routeUID]
        # update name
        if busRoute.name != name:
            log(busRoute.uid + ' - ' + busRoute.name + ' is renamed to ' + name + '.')
            busRoute.name = name
    except KeyError:
        busRoute = BusRoute(uid=routeUID, name=name)
        log(busRoute.uid + ' - ' + busRoute.name + ' is created.')
    return busRoute

def scan_stops(stops, routeUID):
    routeStops = []
    for stop in stops:
        stopUID = stop['UniStopId']
        routeStops.append(stopUID)
        # add new stop into the queue
        if not stopUID in stopDone and not stopUID in stopUndone:
            stopUndone.add(stopUID)
    return routeStops

def update_stops_on_route(route, stopsList, direction):
    if stopsList:
        stops = scan_stops(stopsList, route.uid)
        if direction:
            if route.routeForward != stops:
                log(route.uid + ' - ' + route.name + ' forward route is updated.')
                route.routeForward = stops
        else:
            if route.routeBackward != stops:
                log(route.uid + ' - ' + route.name + ' backward route is updated.')
                route.routeBackward = stops

def update_route(routeUID):
    url = "https://ebus.gov.taipei/Route/StopsOfRoute?routeid=" + routeUID
    info = request_info(url)
    if not info:
        return None
    route = update_route_info(routeUID, info['Name'])
    update_stops_on_route(route, info['GoDirStops'], True)
    update_stops_on_route(route, info['BackDirStops'], False)
    # save date
    routeData[route.uid] = route
    print(route.name + ' is updated.')

def update_stop_info(stopUID, name):
    # get data in db or create one
    try:
        busStop = stopData[stopUID]
        # update name
        if busStop.name != name:
            log(busStop.uid + ' - ' + busStop.name + ' is renamed to ' + name + '.')
            busStop.name = name
    except KeyError:
        busStop = BusStop(uid=stopUID, name=name)
        log(busStop.uid + ' - ' + busStop.name + ' is created.')
    return busStop

def update_latitude(busStop, latitude):
    # update latitude
    if busStop.latitude != latitude:
        busStop.latitude = latitude
        log(busStop.uid + ' - ' + busStop.name + ' latitude is updated.')

def update_longitude(busStop, longitude):
    # update longitude
    if busStop.longitude != longitude:
        busStop.longitude = longitude
        log(busStop.uid + ' - ' + busStop.name + ' longitude is updated.')

def update_route_of_stop(busStop, routeOfStop):
    # update route of stop
    routes = []
    for route in routeOfStop:
        routeUID = route['UniRouteId']
        if re.match('\d{9}0', routeUID):
            routes.append(routeUID)
            # add new route into the queue, ids not end with 0 are not used
            if not routeUID in routeDone and not routeUID in routeUndone:
                    routeUndone.add(routeUID)
    if busStop.route != routes:
        busStop.route = routes
        log(busStop.uid + ' - ' + busStop.name + ' route is updated.')

def update_stop(stopUID):
    url = "https://ebus.gov.taipei/Stop/RoutesOfStop?stopid=" + stopUID
    info = request_info(url)
    if not info:
        return None
    stop = update_stop_info(stopUID, info['Name'])
    update_latitude(stop, info['Latitude'])
    update_longitude(stop, info['Longitude'])
    update_route_of_stop(stop, info['RoutesNumber'])
    # save date
    stopData[stop.uid] = stop
    print(stop.name + ' is updated.')


log('start update route time: ' + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
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
