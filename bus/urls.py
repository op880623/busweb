from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^bus_list/$', views.bus_list, name='bus_list'),
    url(r'^stop_list/$', views.stop_list, name='stop_list'),
    url(r'^stop/(?P<uid>\d+)/$', views.stop, name='stop'),
    url(r'^departure/(?P<uid>\d+)/$', views.departure, name='departure'),
    url(r'^destination/(?P<uid>\d+)/$', views.destination, name='destination'),
    url(r'^connected/(?P<uid>\d+)/$', views.connected, name='connected'),
]
