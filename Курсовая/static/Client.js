
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



// Adds a marker to the map.
function addMarker(location, map) {
  // Add the marker at the clicked location, and add the next-available label
  // from the array of alphabetical characters.

  var marker = new google.maps.Marker({
    position: location,
    //label: labels[labelIndex++ % labels.length],
    map: map
  });
  var xhr = new XMLHttpRequest();
  var newURL = window.location.protocol
  // 2. Конфигурируем его: GET-запрос на URL 'phones.json'
  xhr.open('POST', newURL, true);

  // 3. Отсылаем запрос
  xhr.send(location);
  if (xhr.responseText == 'Ok') {
    // обработать ошибку
    alert( "ne ok"); // пример вывода: 404: Not Found
  } else {
    // вывести результат
    alert( xhr.responseText ); // responseText -- текст ответа.
  }
}


// 4. Если код ответа сервера не 200, то это ошибка


google.maps.event.addDomListener(window, 'load', initialize);
