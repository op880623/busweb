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
  if (type == ''){
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

function info_window_content(stop, type){
  var content = '';

  content = content.concat('<div class="card text-center">');

  content = content.concat('<div class="card-header">');
  content = content.concat('<h5 class="card-title">' + stop.name + '</h5>');
  content = content.concat('</div>');


  content = content.concat('<div class="card-body">');
  content = content.concat('<h5 class="card-title">路線:</h5>');
  content = content.concat('</div>');

  content = content.concat('<div class="card-columns">');
  for (index in stop.route)
    content = content.concat('<div class="card">' + stop.route[index] + '</div>');
  content = content.concat('</div>');


  if (type=='departure' || type=='connected'){
    content = content.concat('<div class="card-body">');
    content = content.concat('<h5 class="card-title">從 ' + thisStop.name + ' 來可搭:</h5>');
    content = content.concat('</div>');

    content = content.concat('<div class="card-columns">');
    for (index in stop.departure)
      content = content.concat('<div class="card">' + stop.departure[index] + '</div>');
    content = content.concat('</div>');
  }


  if (type=='destination' || type=='connected'){
    content = content.concat('<div class="card-body">');
    content = content.concat('<h5 class="card-title">去 ' + thisStop.name + ' 可搭:</h5>');
    content = content.concat('</div>');

    content = content.concat('<div class="card-columns">');
    for (index in stop.destination)
      content = content.concat('<div class="card">' + stop.destination[index] + '</div>');
    content = content.concat('</div>');
  }


  content = content.concat('<div class="card-footer text-muted">');
  content = content.concat('<div class="btn-group">');
  content = content.concat(
    '<a type="button" class="btn btn-light" href="/departure/' + stop.uid + '/">能去哪裡</a>');
  content = content.concat(
    '<a type="button" class="btn btn-light" href="/destination/' + stop.uid + '/">如何到這</a>');
  content = content.concat(
    '<a type="button" class="btn btn-light" href="/connected/' + stop.uid + '/">與此相連</a>');
  content = content.concat('</div>');
  content = content.concat('</div>');

  content = content.concat('</div>');

  return content;
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

function create_marker(stop){
  if ('departure' in stop){
    if ('destination' in stop){
      type = 'connected';
    }
    else {
      type = 'departure';
    }
  }
  else {
    if ('destination' in stop){
      type = 'destination';
    }
    else {
      type = '';
    }
  }
  // create a new marker and store it in the stops[key].marker
  add_marker(stop, type);
  // add infoWindow to the marker and listener to close the infoWindow
  var infoWindow = new google.maps.InfoWindow({
    content: info_window_content(stop, type)
  });
  // add a event on click the marker
  add_listener_click_marker(stop, infoWindow);
}


function update_frame(){
  url = "/info/stop_list/"
    + "?e=" + map.getBounds().getNorthEast().lng()
    + "&n=" + map.getBounds().getNorthEast().lat()
    + "&w=" + map.getBounds().getSouthWest().lng()
    + "&s=" + map.getBounds().getSouthWest().lat();
  $.get(url, function(uids) {
    $.each(uids, function(uid, info) {
      if (!(uid in data)) {
        data[uid] = info;
        stop = data[uid];
        if (!('marker' in stop)){
          create_marker(stop);
        }
        else if(stop.marker.getMap() == null){
          create_marker(stop);
        }
      }
    });
  });
}

function get_stops_list(){
  create_marker(thisStop);
  map.setCenter(thisStop.marker.getPosition());
  $.each(stopsList, function(uid, info) {
    create_marker(info);
  });
}


var map;
var data = {};
var type = window.location.pathname.split("/")[1];

async function init() {
  map = set_map();
  await setTimeout(function(){
    if (type == ''){
      update_frame();
      var listener = google.maps.event.addListener(map, 'dragend', function(){
        update_frame();
      });
    }
    else{
      get_stops_list();
    }
  }, 3000);
}

init();
