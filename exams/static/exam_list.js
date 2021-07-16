/*

Javascript file for the main page

*/

console.log('what in the world');




//the dots [... are added to make modalBtns an array
const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=> {
    const pk = modalBtn.getAttribute('data-pk')
    const name = modalBtn.getAttribute('data-exam')
    const numQuestions = modalBtn.getAttribute('data-questions')
    const time = modalBtn.getAttribute('data-time')

    modalBody.innerHTML = `
      <div class="h5 mb-3">Are you sure you want to begin "<b>${name}</b>"?</div>
      <div class="text-muted">
        <ul>
          <li>Number of Questions: <b>${numQuestions}</b></li>
          <li>Time: <b>${time} minutes</b></li>
        </ul>
      </div>
      `
    startBtn.addEventListener('click', ()=>{

      //window.location.href="../exam-" + pk + "/reading/"
      window.location.href="../exam-" + pk + "/start-exam/"
    })

}))
