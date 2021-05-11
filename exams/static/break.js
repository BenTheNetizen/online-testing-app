/*

  JavaScript for the break page

*/

const breakForm = document.getElementById('break-form')
const nextSection = document.getElementById('next-section').innerHTML

//count-down timer
var distance = 3000

var x = setInterval(function() {

  var now = new Date().getTime();

  distance -= 1000

  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="demo"
  document.getElementById("demo").innerHTML = minutes + "m " + seconds + "s ";

  if (distance < 0) {
    clearInterval(x);
    document.getElementById("demo").innerHTML = "EXPIRED";
  }
}, 1000);



breakForm.addEventListener('submit', e=>{
  e.preventDefault()

  if (nextSection == "writing") {
    window.location.href="./writing"
  }
  else if (nextSection == "math2") {
    window.location.href="./math2"
  }

})
