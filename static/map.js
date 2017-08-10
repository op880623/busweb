function set_map() {
  var mapOptions = {
    center: new google.maps.LatLng(25.0180917,121.5386255),
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    scaleControl: true,
  };
  return new google.maps.Map(document.getElementById("map"), mapOptions)
}

function add_marker(stop, map) {
  var marker_position = new google.maps.LatLng(stop.latitude, stop.longitude);
  var marker = new google.maps.Marker({position:marker_position});
  marker.setMap(map);

  stop['marker'] = marker;
}

function add_info_window(stop, map){
  var infoWindow = new google.maps.InfoWindow({
    content: stop.name
  });

  google.maps.event.addListener(stop.marker, 'click', function() {
    if(!stop.open){
      infoWindow.open(map, stop.marker);
      stop.open = true;
      var listener = google.maps.event.addListener(map, 'click', function() {
        infoWindow.close();
        stop.open = false;
        google.maps.event.removeListener(listener);
      });
    }
    else{
      infoWindow.close();
      stop.open = false;
      google.maps.event.removeListener(listener);
    }
  });
}

function add_listener_click_marker(marker){
  google.maps.event.addListener(marker, 'click', function() {
    map.setZoom(15);
    map.setCenter(marker.getPosition());
  });
}

var map = set_map();

var stops = {
  '1059400020': {
    id: '1059400020',
    name: '上塔悠[向東]',
    latitude: 25.07049,
    longitude: 121.56213,
    route: ['0100050500'],
    open: false,
    marker: null
  },
  '2345100320': {
    id: '2345100320',
    name: '秀朗國小[向東]',
    latitude: 24.99988,
    longitude: 121.52104,
    route: ['0100150500', '0100020700', '0100025400', '0400005100', '0100067200', '0100067220', '0400089500', '0415000200'],
    open: false,
    marker: null
  }
};

for (key in stops) {
  add_marker(stops[key], map);
  add_info_window(stops[key], map);
  add_listener_click_marker(stops[key].marker);
}
