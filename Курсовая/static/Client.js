
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

function filter(){
  var msg   = $('#formx').serialize();
        $.ajax({
          type: 'POST',
          url:  window.location.protocol,
          data: msg,
          success: function(data) {
            $('#results').html(data);
          },
          error:  function(xhr, str){
	    alert('Возникла ошибка: ' + xhr.responseCode);
          }
        });
}
//google.maps.event.addDomListener(window, 'load', initialize);
