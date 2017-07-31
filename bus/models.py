from django.db import models


class BusStop(models.Model):
    uid = models.CharField(max_length=15)# id used in target website
    name = models.CharField(max_length=100)
    route = models.ManyToManyField('BusRoute', through='StopOnRoute')
    latitude = models.FloatField(max_length=10, blank=True, null=True)
    longitude = models.FloatField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class BusRoute(models.Model):
    uid = models.CharField(max_length=15)# id used in target website
    name = models.CharField(max_length=100)
    stops = models.ManyToManyField(BusStop, through='StopOnRoute')

    def __str__(self):
        return self.name

    def stops_after_specific_stop(self, stop):
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
        return self.stops.filter(stoponroute__direction=stopInfo.direction, stoponroute__order__gt=stopInfo.order).order_by('stoponroute__order')

    def stops_before_specific_stop(self, stop):
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
        return self.stops.filter(stoponroute__direction=stopInfo.direction, stoponroute__order__lt=stopInfo.order).order_by('stoponroute__order')


class StopOnRoute(models.Model):
    route = models.ForeignKey(BusRoute, blank=True, null=True)
    stop = models.ForeignKey(BusStop, blank=True, null=True)
    direction = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.route.name + '-' + self.stop.name
