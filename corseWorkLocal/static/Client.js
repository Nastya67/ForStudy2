function initMapg(){
  var bangalore = { lat: 49.97, lng: 32.59 };
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: bangalore
  });
  map.setOptions({disableDoubleClickZoom: true });
  posts = document.getElementById("posts")
  if(posts){
    jPosts = JSON.parse(posts.innerHTML);
    for(var i = 0; i < jPosts.length; i ++ ){
      addPostsg({lat: jPosts[i]['latitude'], lng: jPosts[i]['longitude']}, map,
      jPosts[i]['text'], jPosts[i]['title'])
    }
  }
  googleMAP = map;
}
var markers={};
var googleMAP;
function initMap() {
  var bangalore = { lat: 49.97, lng: 32.59 };
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: bangalore
  });
  map.setOptions({disableDoubleClickZoom: true });
  google.maps.event.addListener(map, 'dblclick', function(event) {
    new_post(event.latLng, map);
  });
  posts = document.getElementById("posts")
  if(posts){
    jPosts = JSON.parse(posts.innerHTML);
    for(var i = 0; i < jPosts.length; i ++ ){
      addPosts(jPosts[i]['idpost'], {lat: jPosts[i]['latitude'], lng: jPosts[i]['longitude']}, map,
      jPosts[i]['text'], jPosts[i]['title'])
    }
  }
  googleMAP = map;
}
function addPosts(id, location, map, text, title){
  var marker = new google.maps.Marker({
    position: location,
    map: map
  });
  markers[id] = {"mark":marker,'title':title};
  if(title || text){
    var infowindow = new google.maps.InfoWindow({
      content: "<b>"+ecran(title)+"</b><br>"+ecran(text)+
      "<form><input type='button' value='delete'"+
      "onclick=del_post('"+id+"')><spam hidden></spam></form>"
    });
    marker.addListener('click', function() {
      infowindow.open(map, marker);
    });
  }
}

function del_post(id){
  markers[id]['mark'].setMap(null)
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
    id:id,
    action:"delete"
  };
  xhr.send(JSON.stringify(data));
}

function addPostsg(id, location, map, text, title){
  var marker = new google.maps.Marker({
    position: location,
    map: map
  });
  markers[id] = marker;
  if(title || text){
    var infowindow = new google.maps.InfoWindow({
      content: "<b>"+ecran(title)+"</b><br>"+ecran(text)
    });
    marker.addListener('click', function() {
      infowindow.open(map, marker);
    });
  }
}
function new_post(location, map){
  var div = document.createElement('div');
  div.className = "modal_box";
  div.innerHTML = "<br><br><form class='forma' enctype='multipart/form-data'>"+
  "<h1>New post</h1>"+
  "<div align='left'>Title</div>"+
  "<input class='textbox' id='titlepost'><br>"+
  "<div align='left'>Your comment</div>"+
  "<textarea class='textarea' id='textpost' name='comment'></textarea><br>"+
  "<input type='button' class='okey' value='Ok' id='postbutton'>&nbsp;&nbsp;"+
  "<input type='button' value='Close' class='okey' onclick=remove_modalBox()>"+
  "</form>";
  document.body.appendChild(div)
  document.getElementById('postbutton').onclick = function(){
    addMarker(location, map);
    remove_modalBox();
  };
}

function find_post(){
  alert("find")
  var str = document.getElementById('findstr').value;
  alert("")
  for(var key in markers){
    if(markers[key]['title'].search(str))
      alert(markers[key]['title']);
  }
}

function ecran(text){
  if(text){
    var res = text.replace(/</g, "&lt;");
    res = text.replace(/>/g, "&gt;");
    return res;
  }
  return "";
}


function addMarker(location, map) {
  var textPost = document.getElementById("textpost").value;
  var titlePost = document.getElementById("titlepost").value;
  addPosts("id", location, map, textPost, titlePost);
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
    text: textPost,
    title: titlePost
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

}

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
});*/

function remove_modalBox(){
  document.body.removeChild(document.body.lastChild)
}
