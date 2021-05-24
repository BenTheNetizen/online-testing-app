/*

Javascript file for the sign-up modal

*/

console.log('djwaidawjoi');

const url = window.location.href

//the dots [... are added to make modalBtns an array
const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

const sendData = () => {
  const username = document.getElementById('username').value
  const password = document.getElementById('password').value

  const data = {}
  data['csrfmiddlewaretoken'] = csrf[0].value
  data['username'] = username
  data['password'] = password

  console.log(data)

  $.ajax({
    type: 'POST',
    url: `${url}`,
    data: data,
    success: function(response) {
      console.log(response)
    }
  })
}

modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=> {

    modalBody.innerHTML = `
      <div class="h5 mb-3">Please fill out the information below</div>
      <div class="text-muted">
        <ul>

          <label>Enter a username</label>
          {% csrf_token %}
          <input id="username"/>
          <label>Enter a password</label>
          {% csrf_token %}
          <input id="password"/>
        </ul>
      </div>
      `
    startBtn.addEventListener('click', ()=>{

      console.log("TEST")
      sendData()
    })

}))
