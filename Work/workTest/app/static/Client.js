function delInterest(elem){
  var xhr = new XMLHttpRequest();
  var newURL = window.location.protocol
  var metas = document.getElementsByTagName('meta');
  for (var i=0; i<metas.length; i++) {
      if (metas[i].getAttribute("name") == "csrf-token") {
         var csrftoken = metas[i].getAttribute("content");
         break;
      }
   }
  var infoStr = elem.parentNode
  xhr.open('POST', newURL, true);
  xhr.setRequestHeader("X-CSRFToken", csrftoken)
  var s = infoStr.textContent;
  var a = s.split('X')[0]
  s = a.trim();
  var data = {
    interest: s,
    action: "delete"
  };
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
      delInterests(infoStr);
    }
  };
  xhr.send(JSON.stringify(data));
}
function delInterests(node){
  node.parentNode.removeChild(node);
}
function interestSubmit(){
  var infoStr = document.getElementById("interestInput");
  if(infoStr.value != ""){
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
      interest: infoStr.value,
      action: "new item"
    };
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && xhr.status == 200) {
        updateListInterests(infoStr.value);
        infoStr.value = '';
      }
    };
    xhr.send(JSON.stringify(data));
  }

}
function updateListInterests(str){
  var list = document.getElementById("interests");
  var div = document.createElement('div')
  div.className = "stack-horz";
  div.innerHTML = str+" <button class='del' onclick='delInterest(this)'>X</button>"
  list.appendChild(div);
}
function interestChange(infoStr){
  var options = document.getElementById("interestsList");
  resetOptions(options);
  if (infoStr.length > 0){
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
      interest: infoStr,
      action: "get list"
    };
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && xhr.status == 200) {
        var fixedResponse = xhr.responseText.replace(/\'/g, "'");
        updateDatalistInterests(JSON.parse(fixedResponse));
      }
    };
    xhr.send(JSON.stringify(data));
  }
}
function updateDatalistInterests(res){
  var options = document.getElementById("interestsList");
  resetOptions(options);
  for(var i = 0; i < res.length; i++){
    var op = document.createElement('option')
    op.innerHTML = res[i][1]
    options.appendChild(op)
  }
}
function resetOptions(options) {
  while (options.firstChild) {
    options.removeChild(options.firstChild);
  }
}
