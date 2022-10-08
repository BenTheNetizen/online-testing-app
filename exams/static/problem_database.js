// constants from html document
const sectionBox = document.getElementById('section-box');
const sectionForm = document.getElementById('section-form');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
const url = window.location.href 

function getData() {
  $.ajax({
    url: dataUrl,
    type: 'GET',
    data: {
      'csrfmiddlewaretoken': csrf,
      'url': url,
      'potato': 'potato'
    },
    success: function(data) {
      console.log(data);
    },
    error: function(error) {
      console.log(error);
    }
  })
}

getData();