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
  var content = [stop.name];
  if (type=='departure'){
    content = content.concat('從 ' + thisStop.name + ' 來可搭:');
    for (index in stop.route)
      if (thisStop.route.indexOf(stop.route[index]) !== -1)
        content = content.concat(busName[stop.route[index]]);
  }
  else if (type=='destination'){
    content = content.concat('去 ' + thisStop.name + ' 可搭:');
    for (index in stop.route)
      if (thisStop.route.indexOf(stop.route[index]) !== -1)
        content = content.concat(busName[stop.route[index]]);
  }
  else{
    content = content.concat('路線:');
    for (index in stop.route)
      content = content.concat(busName[stop.route[index]]);
  }
  // render_this_stop('departure' or 'destination', 'uid')
  content = content.concat('<button onclick="render_this_stop(' +
    '\'departure\', \'' + stop.uid + '\')">能去哪裡</button>')
  content = content.concat('<button onclick="render_this_stop(' +
    '\'destination\', \'' + stop.uid + '\')">如何到這</button>')
  content = content.concat('<button onclick="render_this_stop(' +
    '\'connected\', \'' + stop.uid + '\')">與此相連</button>')
  return content.join('<br>');
}

function add_listener_click_marker(stop, infoWindow){
  google.maps.event.addListener(stop.marker, 'click', function(){
    map.setZoom(17);
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


function render_data(){
  // create new merker with new data
  for (key in data) {
    create_marker(data[key], "all");
  }
}

function render_this_stop(type, uid){
  url = 'info/' + type + '/' + uid + '/'
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200){
      var stopsList = JSON.parse(this.responseText);
      // update thisStop data
      clear_map();
      // render thisStop
      if (thisStop.marker !== null){
        thisStop.marker.setMap(null);
      }
      thisStop = data[uid];
      create_marker(thisStop, 'all');
      // render related stops
      for (key in stopsList)
        // if judgement to prevent stop with two markers
        // due to route pass through the same stop as thisStop
        for (index in stopsList[key])
          if (data[stopsList[key][index]].marker.getMap() == null)
            create_marker(data[stopsList[key][index]], key);
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}

function clear_map(){
  // clear old data
  for (key in data) {
    data[key].marker.setMap(null);
  }
}

function request_data(){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200){
      data = JSON.parse(this.responseText).stop;
      busName = JSON.parse(this.responseText).route;
      render_data();
    }
  };
  xhttp.open("GET", "info/", true);
  xhttp.send();
}

document.getElementById("title").addEventListener("click", function(){
  clear_map();
  render_data();
});

var map = set_map();

var data;
var thisStop = {marker: null};

request_data();
