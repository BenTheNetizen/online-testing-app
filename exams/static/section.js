/*

Javascript file for taking the exam sections

*/

const url = window.location.href

const sectionBox = document.getElementById('section-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')

$.ajax({
  type: 'GET',
  url: `${url}data`,
  success: function(response) {
    //console.log(response)
    const data = response.data

    //el is the dictionary index that represents a single question, answer pair
    data.forEach(el => {
      for (const [question, answers] of Object.entries(el)) {
        sectionBox.innerHTML += `
          <hr>
          <div class="mb-2">
            <b>${question}</b>
          </div>
        `
        answers.forEach(answer=>{
          sectionBox.innerHTML += `
            <div>
              <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
              <label for="${question}">${answer}</label>
            </div>
          `
        })
      }
    })
  },
  error: function(error) {
    console.log(error)
  }
})

const sectionForm = document.getElementById('section-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const sendData = () => {
  const elements = [...document.getElementsByClassName('ans')]
  const data = {}
  data['csrfmiddlewaretoken'] = csrf[0].value
  elements.forEach(el=>{
    if (el.checked) {
      data[el.name] = el.value
    } else {
      //this checks if the question has been answered
      if (!data[el.name]) {
        data[el.name] = null
      }
    }
  })

  $.ajax({
      type: 'POST',
      url: `${url}save/`,
      data: data,
      success: function(response) {
        //console.log(response)
        const results = response.results
        sectionForm.classList.add('not-visible')

        scoreBox.innerHTML = `Your result is ${response.score.toFixed(2)}%`

        results.forEach(res=>{
          const resultDiv = document.createElement("div")
          for (const [question, resp] of Object.entries(res)) {
            console.log(question)
            console.log(resp)

            resultDiv.innerHTML += question
            const cls = ['container', 'p-3', 'text-light', 'h3']
            resultDiv.classList.add(...cls)

            if (resp=='not answered') {
              resultDiv.innerHTML += '- not answered'
              resultDiv.classList.add('bg-danger')
            }
            else {
              const answer = resp['answered']
              const correct = resp['correct_answer']

              if (answer == correct) {
                resultDiv.classList.add('bg-success')
                resultDiv.innerHTML += ` answered: ${answer}`

              } else {
                resultDiv.classList.add('bg-danger')
                resultDiv.innerHTML += ` | correct answer: ${correct}`
                resultDiv.innerHTML == ` | answered: ${answer}`
              }
            }
          }
          resultBox.append(resultDiv)
        })
      },
      error: function(error) {
        console.log(error)
      }
  })

}

sectionForm.addEventListener('submit', e=>{
  e.preventDefault()

  sendData()
})
