from django.db import models


class BusStop(models.Model):
    uid = models.CharField(max_length=15)# id used in target website
    name = models.CharField(max_length=100)
    route = models.ManyToManyField('BusRoute', through='StopOnRoute')
    latitude = models.FloatField(max_length=10, blank=True, null=True)
    longitude = models.FloatField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def to_json(self):
        uid = '"uid":"' + self.uid + '"'
        name = '"name":"' + self.name + '"'
        if self.latitude is None:
            latitude = '"latitude":null'
        else:
            latitude = '"latitude":' + str(self.latitude)
        if self.longitude is None:
            longitude = '"longitude":null'
        else:
            longitude = '"longitude":' + str(self.longitude)
        route = '"route":[' + ','.join(['"' + route.uid + '"' for route in self.route.all()]) + ']'
        json = '{' + ','.join([uid, name, latitude, longitude, route]) + '}'
        return json

    def stops_can_go(self):
        # return array of dicts that contain stop which self can go and routes from self to stop
        # one stop and a set of route in a dict
        # a series of dicts in a array
        # ruturn format [{'stop': BusStop, 'route': <QuerySet of BusRoute>}*n]
        stopsCanGo = BusStop.objects.none()
        for route in self.route.all():
            stopsCanGo = stopsCanGo.union(route.stops_after_specific_stop(self, order=False))
        stopsHowToGo = []
        for stop in stopsCanGo:
            stopsHowToGo.append({'stop': stop,'route': self.route.all().intersection(stop.route.all())})
        return stopsHowToGo

    def stops_can_come(self):
        # return array of dicts that contain stop which can come to self and routes from stop to self
        # one stop and a set of route in a dict
        # a series of dicts in a array
        # ruturn format [{'stop': BusStop, 'route': <QuerySet of BusRoute>}*n]
        stopsCanCome = BusStop.objects.none()
        for route in self.route.all():
            stopsCanCome = stopsCanCome.union(route.stops_before_specific_stop(self, order=False))
        stopsHowToCome = []
        for stop in stopsCanCome:
            stopsHowToCome.append({'stop': stop,'route': self.route.all().intersection(stop.route.all())})
        return stopsHowToCome


class BusRoute(models.Model):
    uid = models.CharField(max_length=15)# id used in target website
    name = models.CharField(max_length=100)
    stops = models.ManyToManyField(BusStop, through='StopOnRoute')

    def __str__(self):
        return self.name

    def stops_after_specific_stop(self, stop, order=True):
        # input stop can be BusStop, BusStop.id(str) or BusStop.name(str)
        # ruturn a QuerySet containing BusStops after given BusStop on this BusRoute
        # result is sorted by order on this BusRoute by default
        # set order to False to get result which is not sorted
        if isinstance(stop, BusStop):
            pass
        elif isinstance(stop, str):
            try:
                stop = BusStop.objects.get(uid=stop)
            except:
                try:
                    stop = BusStop.objects.get(name=stop)
                except:
                    raise ValueError("BusStop matching this uid or name does not exist.")
        else:
            raise TypeError('must be a BusStop object or string of BusStop.uid but ' + str(type(stop)))
        try:
            stopInfo = StopOnRoute.objects.get(route=self, stop=stop)
        except:
            raise ValueError('StopOnRoute matching this uid or name does not exist.')
        if order is True:
            return self.stops.filter(stoponroute__direction=stopInfo.direction, stoponroute__order__gt=stopInfo.order).order_by('stoponroute__order')
        else:
            return self.stops.filter(stoponroute__direction=stopInfo.direction, stoponroute__order__gt=stopInfo.order)

    def stops_before_specific_stop(self, stop, order=True):
        # input stop can be BusStop, BusStop.id(str) or BusStop.name(str)
        # ruturn a QuerySet containing BusStops before given BusStop on this BusRoute
        # result is sorted by order on this BusRoute by default
        # set order to False to get result which is not sorted
        if isinstance(stop, BusStop):
            pass
        elif isinstance(stop, str):
            try:
                stop = BusStop.objects.get(uid=stop)
            except:
                try:
                    stop = BusStop.objects.get(name=stop)
                except:
                    raise ValueError("BusStop matching this uid or name does not exist.")
        else:
            raise TypeError('must be a BusStop object or string of BusStop.uid but ' + str(type(stop)))
        try:
            stopInfo = StopOnRoute.objects.get(route=self, stop=stop)
        except:
            raise ValueError('StopOnRoute matching this uid or name does not exist.')
        if order is True:
            return self.stops.filter(stoponroute__direction=stopInfo.direction, stoponroute__order__lt=stopInfo.order).order_by('stoponroute__order')
        else:
            return self.stops.filter(stoponroute__direction=stopInfo.direction, stoponroute__order__lt=stopInfo.order)


class StopOnRoute(models.Model):
    route = models.ForeignKey(BusRoute, blank=True, null=True)
    stop = models.ForeignKey(BusStop, blank=True, null=True)
    direction = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.route.name + '-' + self.stop.name
