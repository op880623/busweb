import re
import shelve


dbRoute = 'busInfo/db/route'
dbStop = 'busInfo/db/stop'

class BusRoute(object):


    def __init__(self, uid, name=''):
        self.uid = uid
        self.name = name
        self.routeForward = []
        self.routeBackward = []

    def to_json(self):
        attributes = []
        attributes.append('"uid":"' + self.uid + '"')
        attributes.append('"name":"' + self.name + '"')
        attributes.append('"routeForward":["' + '","'.join(self.routeForward) + '"]')
        attributes.append('"routeBackward":["' + '","'.join(self.routeBackward) + '"]')
        json = '{' + ','.join(attributes) + '}'
        return json

    def stops_after_specific_stop(self, stopId):
        if stopId in self.routeForward:
            return set(self.routeForward[self.routeForward.index(stopId)+1:])
        elif stopId in self.routeBackward:
            return set(self.routeBackward[self.routeBackward.index(stopId)+1:])
        else:
            raise KeyError(stopId + ' is not in route ' + self.uid)

    def stops_before_specific_stop(self, stopId):
        if stopId in self.routeForward:
            return set(self.routeForward[:self.routeForward.index(stopId)])
        elif stopId in self.routeBackward:
            return set(self.routeBackward[:self.routeBackward.index(stopId)])
        else:
            raise KeyError(stopId + ' is not in route ' + self.uid)


class BusStop(object):


    def __init__(self, uid, name=''):
        self.uid = uid
        self.name = name
        self.route = set()
        self.latitude = 0
        self.longitude = 0

    def to_json(self):
        attributes = []
        attributes.append('"uid":"' + self.uid + '"')
        attributes.append('"name":"' + self.name + '"')
        attributes.append('"route":["' + '","'.join(self.route) + '"]')
        attributes.append('"latitude":' + str(self.latitude))
        attributes.append('"longitude":' + str(self.longitude))
        json = '{' + ','.join(attributes) + '}'
        return json

    def connected_stops(self, dbRoute=dbRoute):
        connectedStops = set()
        for route in self.route:
            with shelve.open(dbRoute) as routeData:
                if self.uid in routeData[route].routeForward:
                    connectedStops = connectedStops.union(set(routeData[route].routeForward))
                if self.uid in routeData[route].routeBackward:
                    connectedStops = connectedStops.union(set(routeData[route].routeBackward))
        return connectedStops.difference({self.uid})

    def stops_can_go(self, dbRoute=dbRoute):
        stopsCanGo = {}
        for route in self.route:
            with shelve.open(dbRoute) as routeData:
                try:
                    for stop in routeData[route].stops_after_specific_stop(self.uid):
                        if stop in stopsCanGo.keys():
                            stopsCanGo[stop].append(route)
                        else:
                            stopsCanGo[stop] = [route]
                except:
                    pass
        return stopsCanGo

    def stops_can_come(self, dbRoute=dbRoute):
        stopsCanCome = {}
        for route in self.route:
            with shelve.open(dbRoute) as routeData:
                try:
                    for stop in routeData[route].stops_before_specific_stop(self.uid):
                        if stop in stopsCanCome.keys():
                            stopsCanCome[stop].append(route)
                        else:
                            stopsCanCome[stop] = [route]
                except:
                    pass
        return stopsCanCome
