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
  console.log($(elt).find('input').attr('name'))
  $(elt).parent().find('label').css('backgroundColor', 'white')
  $(elt).css('backgroundColor', '#f5f5f5')
  $(elt).find('input').prop("checked", true);

  let question = $(elt).find('input').attr('name')
  let answer = $(elt).find('input').attr('value')

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

function getPassage(value) {
  if (value == 'prev')
  {
    console.log('CHANGE PASSAGE TO PREV')
    if (passage_num > 1) {
      passage_num -= 1
    }
  }
  if (value == 'next')
  {
    console.log('CHANGE PASSAGE TO NEXT')
    passage_num += 1
  }

  $.ajax({
    type: 'GET',
    url: `${url}passage-` + passage_num + `/data`,
    success: function(response) {
      console.log(response)

      const data = response.data
      console.log(data)
      //el is the dictionary index that represents a single question, answer pair

      //clearing the images and questions
      sectionBox.innerHTML = ''
      sectionMaterial.innerHTML = ''

      //handling the passage displaying
      console.log(response.img_urls)
      for (i in response.img_urls) {
        console.log(response.img_urls[i])
        sectionMaterial.innerHTML += `
          <img src="${response.img_urls[i]}">
          `
      }
      //handling the questions displaying
      data.forEach(el => {
        for (const [question_number, question_data] of Object.entries(el)) {
          //NOTE THAT 'question_data' IS AN ARRAY
          //question_data[0] is question text; question_data[1] are the answers;
          //question_data[2] is either '' or contains the answer that was previously selected
          var sectionBoxString = ''
          sectionBoxString += `
            <div class="mb-2 testing">
              <div class="ca-question-num">Question ${question_number}</div>
              <div class="ca-question-data">${question_data[0]}</div>
            </div>
            <div class="answers-container">
          `
          question_data[1].forEach(answer=>{
            if (answer == question_data[2] && question_data[2] != null) {
              sectionBoxString += `
                
                  <!--<input type="radio" class="ans" id="${question_data[0]}-${answer}" name="${question_data[0]}" value="${answer}" onclick="radioChecked(this)" checked> -->
                  <!--<label for="${question_data[0]}">${answer}</label> -->
                  <label for="${question_data[0]}" class="answer-container" onclick="radioChecked(this)">
                    <input type="radio" class="ans" id="${question_data[0]}-${answer}" name="${question_data[0]}" value="${answer}" checked>
                    <span class="checkmark-con"><span class="material-icons checkmark">done</span>
                    </span>
                    ${answer}
                  </label>
                
              `
            } else {
              sectionBoxString += `
                
                  <!-- <input type="radio" class="ans" id="${question_data[0]}-${answer}" name="${question_data[0]}" value="${answer}" onclick="radioChecked(this)"> -->
                  <!-- <label for="${question_data[0]}">${answer}</label> -->
                  <label for="${question_data[0]}" class="answer-container" onclick="radioChecked(this)">
                    <input type="radio" class="ans" id="${question_data[0]}-${answer}" name="${question_data[0]}" value="${answer}">
                    <span class="checkmark-con"><span class="material-icons checkmark">done</span>
                    </span>
                    ${answer}
                  </label>
                
              `
            }
            
          })
          sectionBoxString += `
            </div>
            `
          sectionBox.innerHTML += sectionBoxString
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
