/*
Javascript file for taking the exam sections
*/

const url = window.location.href
const sectionBox = document.getElementById('section-box')
const sectionMaterial = document.getElementById('section-material')
var passageNum = 1
//used to gather the section name so that we can redirect to the correct following break or section
var sectionName
const sectionForm = document.getElementById('section-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

// grabs the data for the first passage
getPassage()

function sendData(isNextSection) {
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
        //THIS IS A HORRIBLE WAY TO REDIRECT THE URLs
        sectionName = response.section_name

        if (isNextSection) {
          if (sectionName == "reading") {
            window.location.href="../break1/writing"
          }
          else if (sectionName == "writing") {
            window.location.href="../math1/section-directions"
          }
          else if (sectionName == "math1") {
            window.location.href="../break2/math2"
          }
          else if (sectionName =="math2") {
            window.location.href="../results"
          }
        }
        else {
          window.location.href= window.location.origin + '/exam-list'
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

      data.forEach(el => {
        for (const [questionNum, questionData] of Object.entries(el)) {
          //NOTE THAT 'questionData' IS AN ARRAY
          //questionData[0] are the question texts
          //questionData[1] are the answers
          //questionData[2] is either '' or contains the answer that was previously selected\
          //questionData[3] is the image URL
          if (questionData[3] != null) {
            sectionBox.innerHTML += `
              <hr>
              <img class="math-material" src="${questionData[3]}">
              <div class="mb-2">
                <b>Question ${questionNum}</b>
                <br>
                <b>${questionData[0]}</b>
              </div>
            `
          } else {
            sectionBox.innerHTML += `
              <hr>
              <div id=""
              <div class="mb-2">
                <b>Question ${questionNum}</b>
                <br>
                <b>${questionData[0]}</b>
              </div>
            `
          }

          questionData[1].forEach(answer=>{
            if (answer == questionData[2] && questionData[2] != null) {
              sectionBox.innerHTML += `
                <div>
                  <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" onclick="radioChecked(this)" checked>
                  <label for="${questionData[0]}">${answer}</label>
                </div>
              `
            } else {
              sectionBox.innerHTML += `
                <div>
                  <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" onclick="radioChecked(this)">
                  <label for="${questionData[0]}">${answer}</label>
                </div>
              `
            }
          })
        }
      })

      // needed statement for MathJax functionality
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
