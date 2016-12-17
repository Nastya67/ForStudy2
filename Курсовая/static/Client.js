
function initMap() {
  var bangalore = { lat: 49.97, lng: 32.59 };
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: bangalore
  });
  // This event listener calls addMarker() when the map is clicked.
  google.maps.event.addListener(map, 'click', function(event) {
    addMarker(event.latLng, map);
  });
  posts = document.getElementById("posts")
  if(posts){
    jPosts = JSON.parse(posts.innerHTML);
    for(var i = 0; i < jPosts.length; i ++ ){
      addPosts({lat: jPosts[i][4], lng: jPosts[i][3]}, map)
    }
  }

}
function addPosts(location, map){
  var marker = new google.maps.Marker({
    position: location,
    map: map
  });
}

function addMarker(location, map) {
  var marker = new google.maps.Marker({
    position: location,
    //label: labels[labelIndex++ % labels.length],
    map: map
  });
  var xhr = new XMLHttpRequest();
  var newURL = window.location.protocol
  var metas = document.getElementsByTagName('meta');
  for (var i=0; i<metas.length; i++) {
      if (metas[i].getAttribute("name") == "csrf-token") {
         var csrftoken = metas[i].getAttribute("content");
         break;
      }
   }
  xhr.open('POST', newURL, true);
  xhr.setRequestHeader("X-CSRFToken", csrftoken)
  xhr.send(location);
}

function getXmlHttp(){
  var xmlhttp;
  try {
    xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
  } catch (e) {
    try {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    } catch (E) {
      xmlhttp = false;
    }
  }
  if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
    xmlhttp = new XMLHttpRequest();
  }
  return xmlhttp;
}


function filter(){
  var msg   = $('#formx').serialize();
  var xhr = new XMLHttpRequest();
  var newURL = window.location.protocol
  var metas = document.getElementsByTagName('meta');
  for (var i=0; i<metas.length; i++) {
      if (metas[i].getAttribute("name") == "csrf-token") {
         var csrftoken = metas[i].getAttribute("content");
         break;
      }
   }
  xhr.open('POST', newURL, true);
  xhr.setRequestHeader("X-CSRFToken", csrftoken)
  xhr.send(msg);

  list_user = getElementById("result")
  var elem = list_user.getElementsByTagName("*");
  for(var i = 0; i < elem.length; i++){
    list_user.removeChild(elem[i])
  }
  var li = document.createElement('li')
  li.innerHTML = xhr.responseText
  list_user.appendChild(li)

}
//google.maps.event.addDomListener(window, 'load', initialize);
