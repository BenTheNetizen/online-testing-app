/*
Javascript file for taking the exam sections
*/


const url = window.location.href
const sectionBox = document.getElementById('section-box')
const sectionMaterial = document.getElementById('section-material')

//used to gather the section name so that we can redirect to the correct following break or section
var sectionName
const sectionForm = document.getElementById('section-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

// grabs the data for the first passage
getPassage()

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
                  <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true onclick="radioChecked(this)" checked>
                  <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label">${answer}</label>
                </div>
              `
            } else {
              sectionBox.innerHTML += `
                <div>
                  <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true onclick="radioChecked(this)">
                  <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label">${answer}</label>
                </div>
              `
            }
          })
          // STYLE THE CORRECT ANSWER BELOW HERE
          let question_text = questionData[0].replaceAll('&quot;', '"')
          console.log(`Question ${questionNum}: ${question_text}-${correctAnswers[questionNum-1]}-label`)
          document.getElementById(`${question_text}-${correctAnswers[questionNum-1]}-label`).style.color = "green";
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
