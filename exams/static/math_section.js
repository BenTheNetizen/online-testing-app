/*
Javascript file for taking the exam sections
*/


const url = window.location.href
const sectionBox = document.getElementById('section-box')
const sectionMaterial = document.getElementById('section-material')
var passage_num = 1

//used to gather the section name so that we can redirect to the correct following break or section
var section_name
const sectionForm = document.getElementById('section-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

// grabs the data for the first passage
getPassage()

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
        data[el.name] = 'N'
      }
    }
  })
  console.log(data)

  $.ajax({
      type: 'POST',
      url: `${url}save`,
      data: data,
      success: function(response) {
        console.log(response)
        //THIS IS A HORRIBLE WAY TO REDIRECT THE URL
        section_name = response.section_name

        if (section_name == "reading") {
          window.location.href="../break1"
        }
        else if (section_name == "writing") {
          window.location.href="../math1/section-directions"
        }
        else if (section_name == "math1") {
          window.location.href="../break2"
        }
        else if (section_name =="math2") {
          window.location.href="../results"
        }
      },
      error: function(error) {
        console.log(error)
      }
  })

}

function radioChecked(elt) {
  console.log('radio checked!')
  console.log(elt.name)
  let question = elt.name
  let answer = elt.value

  $.ajax({
      type: 'POST',
      url: `${url}save-question`,
      data: {
        csrfmiddlewaretoken: csrf[0].value,
        question: question,
        answer: answer,
      },
      success: function(response) {

      },
      error: function(error) {
        console.log(error)
      }
  })
}

function getPassage() {
  $.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response) {
      console.log(response)
      const data = response.data
      console.log(data)
      //el is the dictionary index that represents a single question, answer pair
      var question_number = 1
      data.forEach(el => {
        for (const [question, question_data] of Object.entries(el)) {
          //NOTE THAT 'question_data' IS AN ARRAY
          //question_data[0] are the answers
          //question_data[1] is either '' or contains the answer that was previously selected\
          //question_data[2] is the image URL
          if (question_data[2] != null) {
            sectionBox.innerHTML += `
              <hr>
              <img class="math-material" src="${question_data[2]}">
              <div class="mb-2">
                <b>Question ${question_number}</b>
                <br>
                <b>${question}</b>
              </div>
            `
          } else {
            sectionBox.innerHTML += `
              <hr>
              <div id=""
              <div class="mb-2">
                <b>Question ${question_number}</b>
                <br>
                <b>${question}</b>
              </div>
            `
          }

          question_data[0].forEach(answer=>{
            if (answer == question_data[1] && question_data[1] != null) {
              sectionBox.innerHTML += `
                <div>
                  <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}" onclick="radioChecked(this)" checked>
                  <label for="${question}">${answer}</label>
                </div>
              `
            } else {
              sectionBox.innerHTML += `
                <div>
                  <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}" onclick="radioChecked(this)">
                  <label for="${question}">${answer}</label>
                </div>
              `
            }
          })

          question_number += 1

        }
      })


      MathJax.typesetPromise();
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
