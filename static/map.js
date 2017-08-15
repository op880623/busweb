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
  content = [stop.name, stop.uid, 'route:'].concat(stop.route)
  content = content.concat('<button onclick="request_data(uid=\''+ stop.uid + '\', type=\'' + 'departure\')">see stops can go</button>')
  content = content.concat('<button onclick="request_data(uid=\''+ stop.uid + '\', type=\'' + 'destination\')">see stops can come</button>')
  var infoWindow = new google.maps.InfoWindow({
    content: content.join('<br>')
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

function create_marker(stopObject) {
  add_marker(stopObject, map);  // create a new marker and store it in the stops[key].marker
  add_info_window(stopObject, map);  // add infoWindow to the marker and listener to close the infoWindow
  add_listener_click_marker(stopObject.marker);  // add a event on click the marker
}


function request_data(uid='', type='') {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      data = JSON.parse(this.responseText);

      // update thisStop data if exists
      if (uid != '' && (type == 'departure' || type == 'destination')) {
        if (thisStop.marker !== null) {
          thisStop.marker.setMap(null);
        }
        thisStop = data.thisStop;
        create_marker(thisStop);
      }

      // clear old data and create new merker with new data
      for (key in stops) {
        stops[key].marker.setMap(null);
      }
      stops = data.stops;
      for (key in stops) {
        create_marker(stops[key]);
      }
    }
  };

  // decide request type
  var url = "info_request/";
  if (uid != '' && (type == 'departure' || type == 'destination')) {
    url = "info_request/" + type + "/" + uid;
  }

  xhttp.open("GET", url, true);
  xhttp.send();
}


var map = set_map();

var data, stops;
var thisStop = {marker: null};

request_data();
