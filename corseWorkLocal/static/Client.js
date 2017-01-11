function initMapg(){
  var bangalore = { lat: 49.97, lng: 32.59 };
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: bangalore
  });
  posts = document.getElementById("posts")
  if(posts){
    jPosts = JSON.parse(posts.innerHTML);
    for(var i = 0; i < jPosts.length; i ++ ){
      addPosts({lat: jPosts[i][4], lng: jPosts[i][3]}, map, jPosts[i][2])
    }
  }

}
function initMap() {
  var bangalore = { lat: 49.97, lng: 32.59 };
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: bangalore
  });
  // This event listener calls addMarker() when the map is clicked.
  google.maps.event.addListener(map, 'click', function(event) {
    new_post(event.latLng, map);
  });
  posts = document.getElementById("posts")
  if(posts){
    jPosts = JSON.parse(posts.innerHTML);
    for(var i = 0; i < jPosts.length; i ++ ){
      addPosts({lat: jPosts[i][4], lng: jPosts[i][3]}, map, jPosts[i][2])
    }
  }

}
function addPosts(location, map, text){
  var infowindow = new google.maps.InfoWindow({
    content: text
  });
  var marker = new google.maps.Marker({
    position: location,
    map: map
  });
  marker.addListener('click', function() {
    infowindow.open(map, marker);
  });
}
function new_post(location, map){
  var div = document.createElement('div');
  div.className = "modal_box";
  div.innerHTML = "<br><br><form  class='forma'>"+
  "<h1>New post</h1>"+
  "<textarea class='textbox' id='textpost' name='comment'></textarea><br>"+
  "<input type='button' value='Ok' id='postbutton'>"+
  "<input type='button' value='Close' onclick=remove_modalBox()>"+
  "</form>";
  document.body.appendChild(div)
  document.getElementById('postbutton').onclick = function(){
    addMarker(location, map);
    remove_modalBox();
  };
}
function addMarker(location, map) {
  var textPost = document.getElementById("textpost").value
  var infowindow = new google.maps.InfoWindow({
    content: textPost
  });
  var marker = new google.maps.Marker({
    position: location,
    //label: labels[labelIndex++ % labels.length],
    map: map
  });
  marker.addListener('click', function() {
    infowindow.open(map, marker);
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
  var data = {
    location: location,
    text: textPost
  };
  xhr.send(JSON.stringify(data));
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


/*function filter(){
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

}*/

var $ = jQuery;

jQuery(document).ready(function($){
  var $result = $('#result');
  var $name = $('#name');
  var metas = document.getElementsByTagName('meta');
  for (var i=0; i<metas.length; i++) {
      if (metas[i].getAttribute("name") == "csrf-token") {
         var csrftoken = metas[i].getAttribute("content");
         break;
      }
   }
  $('#find').on('click', function(){
    $.ajax({
      type: "POST",
      url: document.location.pathname,
      headers: {
        "X-CSRFToken": csrftoken
      },
      data: {
        name: $name.val()
      },
      seccess: function(data){
        alert('OK')
      },
      error: function(){
        alert('error')
      }
    })
  });
});

function remove_modalBox(){
  document.body.removeChild(document.body.lastChild)
}
