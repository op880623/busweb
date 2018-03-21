function set_map(){
  var mapOptions = {
    center: new google.maps.LatLng(25.0180917,121.5386255),
    zoom: 15,
    minZoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    scaleControl: true,
  };
  return new google.maps.Map(document.getElementById("map"), mapOptions)
}


function add_marker(stop, type){
  var marker_position = new google.maps.LatLng(stop.latitude, stop.longitude);
  if (type == 'all'){
    icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';
    opacity = 0.4;
  } else {
    icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
    opacity = 1;
  }
  var marker = new google.maps.Marker({
    position: marker_position,
    icon: icon,
    opacity: opacity
  });
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
    '\'departure\', \'' + stop.uid + '\')">能去哪裡</button>');
  content = content.concat('<button onclick="render_this_stop(' +
    '\'destination\', \'' + stop.uid + '\')">如何到這</button>');
  content = content.concat('<button onclick="render_this_stop(' +
    '\'connected\', \'' + stop.uid + '\')">與此相連</button>');
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

function create_marker(uid, type){
  if (!(uid in data)) {
    $.get("info/stop/" + uid + "/", function(stop) {
      data[uid] = stop;
      stop = data[uid]
      // create a new marker and store it in the stops[key].marker
      add_marker(stop, type);
      // add infoWindow to the marker and listener to close the infoWindow
      var infoWindow = new google.maps.InfoWindow({
        content: info_window_content(stop, type)
      });
      // add a event on click the marker
      add_listener_click_marker(stop, infoWindow);
    });
  }
  else if (data[uid] == null) {
    $.get("info/stop/" + uid + "/", function(stop) {
      data[uid] = stop;
      stop = data[uid]
      // create a new marker and store it in the stops[key].marker
      add_marker(stop, type);
      // add infoWindow to the marker and listener to close the infoWindow
      var infoWindow = new google.maps.InfoWindow({
        content: info_window_content(stop, type)
      });
      // add a event on click the marker
      add_listener_click_marker(stop, infoWindow);
    });
  }
  else if (data[uid].marker.getMap() == null){
    stop = data[uid]
    // create a new marker and store it in the stops[key].marker
    add_marker(stop, type);
    // add infoWindow to the marker and listener to close the infoWindow
    var infoWindow = new google.maps.InfoWindow({
      content: info_window_content(stop, type)
    });
    // add a event on click the marker
    add_listener_click_marker(stop, infoWindow);
  }
}


function render_this_stop(type, uid){
  url = 'info/' + type + '/' + uid + '/'
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200){
      // turn old related stops back to normal stops
      if (thisStop.marker !== null)
        update_markers('to_normal');
      // update thisStop and related data
      thisStop = data[uid];
      stopsList = JSON.parse(this.responseText);
      // turn new related stops to marked stops
      update_markers('to_related');
      thisStop.marker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png');
      thisStop.marker.setOpacity(1);
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}

function update_markers(marker_type){
  // clear old markers of related stops
  all_related_stops_do(function(){
    if (stopsList[key][index] in data)
      data[stopsList[key][index]].marker.setMap(null);
  });
  // clear old marker of thisStop
  if (thisStop.marker.getMap() !== null)
    thisStop.marker.setMap(null);

  // set markers of related stops
  all_related_stops_do(function(){
    if (marker_type == 'to_related')
      create_marker(stopsList[key][index], key);
    else
      create_marker(stopsList[key][index], 'all');
  });
  // set marker of thisStop
  if (thisStop.marker.getMap() !== null)
    //  this if judgement prevents stop having two markers
    // due to route pass through the same stop as thisStop
    thisStop.marker.setMap(null);
  create_marker(thisStop.uid, 'all');
}


function all_related_stops_do(behavior){
  // method to go through all related stops
  for (key in stopsList)
    for (index in stopsList[key])
      behavior();
}

function update_stops(){
  url = "info/stop_list/"
    + "?e=" + map.getBounds().getNorthEast().lng()
    + "&n=" + map.getBounds().getNorthEast().lat()
    + "&w=" + map.getBounds().getSouthWest().lng()
    + "&s=" + map.getBounds().getSouthWest().lat();
  $.get(url, function(uids) {
    $.each(uids, function(uid) {
      create_marker(uid, "all");
    //   if (!(uid in data)) {
    //     $.get("info/stop/" + uid + "/", function(stop) {
    //       data[uid] = stop;
    //       create_marker(data[uid], "all");
    //     });
    //   }
    //   else if (data[uid] == null) {
    //     $.get("info/stop/" + uid + "/", function(stop) {
    //       data[uid] = stop;
    //       create_marker(data[uid], "all");
    //     });
    //   }
    });
  });
}

var map = set_map();

var data = {};
var busName = {};
var thisStop = {marker: null};
var stopsList;

$(document).ready(function() {
  $.getJSON("info/bus_list/", function(result) {
    $.each(result, function(uid, name) {
      busName[uid] = name;
    });
    update_stops();
  });
  var listener = google.maps.event.addListener(map, 'dragend', function(){
    update_stops();
  });
});

//
// all:
//   canvas move: get stops all range
//   too big :don't update stops
// thisStop not null
// show related stops
