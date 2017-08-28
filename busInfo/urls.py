from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.all_stops, name='all_stops'),
    url(r'^departure/(?P<uid>\d+)/$', views.departure, name='departure'),
    url(r'^destination/(?P<uid>\d+)/$', views.destination, name='destination'),
    url(r'^connected/(?P<uid>\d+)/$', views.connected, name='connected'),
]
