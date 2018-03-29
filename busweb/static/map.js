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
  content = content.concat(
    '<a href="/departure/' + stop.uid + '/"><button>能去哪裡</button></a>');
  content = content.concat(
    '<a href="/destination/' + stop.uid + '/"><button>如何到這</button></a>');
  content = content.concat(
    '<a href="/connected/' + stop.uid + '/"><button>與此相連</button></a>');
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
  add_marker(stop, type);
  // add infoWindow to the marker and listener to close the infoWindow
  var infoWindow = new google.maps.InfoWindow({
    content: info_window_content(stop, type)
  });
  // add a event on click the marker
  add_listener_click_marker(stop, infoWindow);
}



function get_stop(uid, type){
  if (!(uid in data)) {
    $.get("/info/stop/" + uid + "/", function(result) {
      data[uid] = result;
      stop = data[uid];
      if (!('marker' in stop)){
        create_marker(stop, type);
      }
      else if(stop.marker.getMap() == null){
        create_marker(stop, type);
      }
    });
  }
}

function update_frame(){
  url = "/info/stop_list/"
    + "?e=" + map.getBounds().getNorthEast().lng()
    + "&n=" + map.getBounds().getNorthEast().lat()
    + "&w=" + map.getBounds().getSouthWest().lng()
    + "&s=" + map.getBounds().getSouthWest().lat();
  $.get(url, function(uids) {
    $.each(uids, function(uid) {
      get_stop(uid, type);
    });
  });
}

function get_stops_list(){
  create_marker(thisStop, '');
  map.setCenter(thisStop.marker.getPosition());
  $.each(stopsList, function(type, list){
    $.each(list, function(uid, info) {
      create_marker(info, type);
    });
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
