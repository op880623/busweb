from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.map, name='index'),
    url(r'^departure/(?P<uid>\d+)/$', views.departure_map, name='departure'),
    url(r'^destination/(?P<uid>\d+)/$', views.destination_map, name='destination'),
    url(r'^connected/(?P<uid>\d+)/$', views.connected_map, name='connected'),
    url(r'^info/stop_list/$', views.stop_list, name='stop_list'),
]
