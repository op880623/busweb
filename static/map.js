function set_map(){
  var mapOptions = {
    center: new google.maps.LatLng(25.0180917,121.5386255),
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    scaleControl: true,
  };
  return new google.maps.Map(document.getElementById("map"), mapOptions)
}


function add_marker(stop){
  var marker_position = new google.maps.LatLng(stop.latitude, stop.longitude);
  var marker = new google.maps.Marker({position:marker_position});
  marker.setMap(map);
  stop.marker = marker;
}

function info_window_content(stop, type='all'){
  var content = [stop.name, stop.uid];
  if (type=='departure'){
    content = content.concat('route from ' + thisStop.name + ' to here:');
    content = content.concat(stop.route.filter(function(n){
      return thisStop.route.indexOf(n) !== -1}));
  }
  else if (type=='destination'){
    content = content.concat('route from here to ' + thisStop.name + ':');
    content = content.concat(stop.route.filter(function(n){
      return thisStop.route.indexOf(n) !== -1}));
  }
  else{
    content = content.concat('route:').concat(stop.route)
  }
  // request_data('info/departure/stopUid/', type='departure'or'destination', render_this_stop)
  content = content.concat('<button onclick="request_data(' +
    '\'info/departure/' + stop.uid + '/\', ' +
    '\'departure\', ' + 'render_this_stop)">see stops can go</button>')
  content = content.concat('<button onclick="request_data(' +
    '\'info/destination/' + stop.uid + '/\', ' +
    '\'destination\', ' + 'render_this_stop)">see stops can come</button>')
  return content.join('<br>');
}

function add_listener_click_marker(stop, infoWindow){
  google.maps.event.addListener(stop.marker, 'click', function(){
    map.setZoom(15);
    map.setCenter(stop.marker.getPosition());
    if(!stop.open){
      infoWindow.open(map, stop.marker);
      stop.open = true;
      var listener = google.maps.event.addListener(map, 'click', function(){
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

function create_marker(stop, type){
  // create a new marker and store it in the stops[key].marker
  add_marker(stop);
  // add infoWindow to the marker and listener to close the infoWindow
  var infoWindow = new google.maps.InfoWindow({
    content: info_window_content(stop, type)
  });
  // add a event on click the marker
  add_listener_click_marker(stop, infoWindow);
}


function render_data(type){
  // clear old data and create new merker with new data
  for (key in stops) {
    stops[key].marker.setMap(null);
  }
  stops = data.stops;
  for (key in stops) {
    create_marker(stops[key], type);
  }
}

function render_this_stop(type){
  // update thisStop data
  if (thisStop.marker !== null){
    thisStop.marker.setMap(null);
  }
  thisStop = data.thisStop;
  create_marker(thisStop, 'all');
  render_data(type);
}

function request_data(url, type, renderFunc){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200){
      data = JSON.parse(this.responseText);
      renderFunc(type);
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}


document.getElementById("title").addEventListener("click", function(){
  request_data("info/", "all", render_data);
});

var map = set_map();

var data, stops;
var thisStop = {marker: null};

request_data("info/", "all", render_data);
