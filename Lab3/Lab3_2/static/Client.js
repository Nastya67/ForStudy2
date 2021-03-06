function showError(container, errorMessage) {
  container.className = 'error';
  var msgElem = document.createElement('span');
  msgElem.className = "error-message";
  msgElem.innerHTML = errorMessage;
  container.appendChild(msgElem);
}

function resetError(container) {
  container.className = '';
  if (container.lastChild.className == "error-message") {
    container.removeChild(container.lastChild);
  }
}

function valid(form){
  var validate = 1;
  var elems = form.elements;

    resetError(elems.name.parentNode);
    if (!elems.name.value) {
      validate = 0;
      showError(elems.name.parentNode, '  enter the name');
    }

    resetError(elems.author.parentNode);
    if (!elems.author.value) {
      validate = 0;
      showError(elems.author.parentNode, '  specify author');
    }

    resetError(elems.size.parentNode);
    if (!elems.size.value) {
      validate = 0;
      showError(elems.size.parentNode, '  specify size');
    }

    resetError(elems.edition.parentNode);
    if (!elems.edition.value) {
      validate = 0;
      showError(elems.edition.parentNode, '  specify edition');
    }

    resetError(elems.date.parentNode);
    if (!elems.date.value) {
      validate = 0;
      showError(elems.date.parentNode, '  specify date');
    }

    if(validate){
      form.submit()
    }
}

function ask_del(){
  var div = document.createElement('div');
  div.className = "modal_box";
  div.innerHTML = "<form method='post' id='forma'>Are you sure?<br>"+
  "<input type='button' value='No' onclick=remove_modalBox()>&nbsp"+
  "<input type='submit' name='delete' value='Delete'></form>";
  document.body.appendChild(div)
}

function remove_modalBox(){
  document.body.removeChild(document.body.lastChild)
}

function filter_books(){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
      var data = this.responseText;
      alert(data);
      JSON.parse(data);
      var template = document.getElementById("filter").innerHTML;
      var renderHTML = Mustache.render(template, {listd:data});
      document.getElementById('my-list').innerHTML = renderHTML;
      //var del = document.getElementById('without_filter')
      //document.body.removeChild(del)
    }
  };
  var val = document.getElementById("searchBox");
  xhttp.open('GET', '/list?field_find='+val.value+'&find=Find', true);
  xhttp.send();
}
