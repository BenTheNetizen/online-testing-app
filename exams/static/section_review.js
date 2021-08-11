/*
Javascript file for taking the exam sections
*/
const url = window.location.href
const sectionBox = document.getElementById('section-box')
const sectionMaterial = document.getElementById('section-material')
var passageNum = 1

//used to gather the section name so that we can redirect to the correct following break or section
const sectionForm = document.getElementById('section-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

// grabs the data for the first passage
getPassage()

// gets the passage (images) information and questions
function getPassage(value) {
  if (value == 'prev' && passageNum > 1)
  {
    console.log('CHANGE PASSAGE TO PREV')
    passageNum -= 1
  }
  if (value == 'next' && passageNum < maxPassages)
  {
    console.log('CHANGE PASSAGE TO NEXT')
    passageNum += 1
  }
  let ajax_url = isMathSection ? `${url}data` : `${url}passage-` + passageNum + `/data`
  $.ajax({
    type: 'GET',
    url: ajax_url,
    success: function(response) {
      console.log(response)

      const data = response.data
      console.log(data)

      if (isMathSection) {
        // make math section form wider than in reading section
        $('#section-form').css('flex-basis', '84%')
        
        data.forEach(el => {
          for (const [questionNum, questionData] of Object.entries(el)) {
            //NOTE THAT 'questionData' IS AN ARRAY
            //questionData[0] are the question texts
            //questionData[1] are the answers
            //questionData[2] is either '' or contains the answer that was previously selected\
            //questionData[3] is the image URL
            var sectionBoxString = ''
            if (questionData[3] != null) {
              sectionBoxString += `              
                <!--
                <div class="mb-2 testing">
                  <b class="ca-question-num">Question ${questionNum}</b>
                  <br>
                  <b class="ca-question-data">${questionData[0]}</b>
                </div>
                <div class="answers-container">
                -->
                <div class='question-container question-container-math'>
                <img class="math-material" src="${questionData[3]}">
                <div class="mb-2 testing">
                  <b class="ca-question-num">Question ${questionNum}</b>
                  <br>
                </div>
                <div class="answers-container">
              `
            } else {
              sectionBoxString += `
              <!--
                <div class="mb-2 testing">
                  <b class="ca-question-num">Question ${questionNum}</b>
                  <br>
                  <b class="ca-question-data">${questionData[0]}</b>
                </div>
                <div class="answers-container">
              -->
              <div class='question-container question-container-math'>
                <div class="mb-2 testing">
                  <b class="ca-question-num">Question ${questionNum}</b>
                  <br>
                  <b class="ca-question-data">${questionData[0]}</b>
                </div>
                <div class="answers-container">
              `
            }

            //checks if one of the answers are null, implies math fill in the answer box
            if (questionData[1][0] == null) {
              if (questionData[2] == `${correctAnswers[questionNum-1]}` ) {
                $('#question'+questionNum).parent().find('.material-icons').addClass('answered')
                $('#question'+questionNum).parent().show()

                sectionBoxString += `
                  <div>
                    <input type="text" class="ans ca-textbox" id="${questionNum}-textbox" name="${questionData[0]}" value="${questionData[2]}" disabled=true">
                    <p>Correct Answer(s): ${correctAnswers[questionNum-1]}</p>
                  </div>
                `
                // CONDITION FOR FREE RESPONSE BEING PREVIOUSLY ANSWERED
                //document.getElementById(`${questionNum}-textbox`).setAttribute('value', questionData[2])
                //document.getElementById(`${questionNum}-textbox`).style.backgroundColor = '#f5f5f5'
              }
              else {
                $('#question'+questionNum).parent().find('.material-icons').addClass('answered')
                $('#question'+questionNum).parent().find('.material-icons').text('close')
                $('#question'+questionNum).parent().find('.material-icons').css('backgroundColor', '#7d120b')
                $('#question'+questionNum).parent().show()
                if (questionData[2] != null) {
                  sectionBoxString += `
                    <div>
                      <input type="text" class="ans ca-textbox missed-correct-answer" id="${questionNum}-textbox" name="${questionData[0]}" value="${questionData[2]}" disabled=true">
                      <p>Correct Answer(s): ${correctAnswers[questionNum-1]}</p>
                    </div>
                  `
                }
                else {
                  sectionBoxString += `
                    <div>
                      <input type="text" class="ans ca-textbox missed-correct-answer" id="${questionNum}-textbox" name="${questionData[0]}" disabled=true">
                      <p>Correct Answer(s): ${correctAnswers[questionNum-1]}</p>
                    </div>
                  `
                }
              }
            } else {
              questionData[1].forEach(answer=>{
                if (answer == questionData[2] && questionData[2] != null) {
                  if ( `${answer}` ==  `${correctAnswers[questionNum-1]}`) {
                    console.log('correct!!!' + questionNum)
                    $('#question'+questionNum).parent().find('.material-icons').addClass('answered')
                    $('#question'+questionNum).parent().show()  

                    sectionBoxString += `
                    <!--
                    <div>
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true onclick="radioChecked(this)" checked>
                      <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label">${answer}</label>
                    </div>
                    -->
                    <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label" class="answer-container" style="background-color: #f5f5f5" onclick="radioChecked(this)">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true checked>
                      <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
                    ${answer}
                    </label>
                  `
                  }
                  else {
                    sectionBoxString += `
                    <!--
                    <div>
                    <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true onclick="radioChecked(this)" checked>
                    <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label">${answer}</label>
                    </div>
                    -->
                    <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label" class="answer-container" onclick="radioChecked(this)">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true checked>
                      <span class="checkmark-con"><span class="material-icons checkmark" style="background-color: #7d120b; color: white; opacity: 1">close</span></span>
                    ${answer}
                    </label>
                  `
                  }
                } else {
                  if ( `${answer}` ==  `${correctAnswers[questionNum-1]}`) {
                    $('#question'+questionNum).parent().find('.material-icons').addClass('answered')
                    $('#question'+questionNum).parent().find('.material-icons').text('close')
                    $('#question'+questionNum).parent().find('.material-icons').css('backgroundColor', '#7d120b')
                    $('#question'+questionNum).parent().show()

                    sectionBoxString += `
                    <!--
                    <div>
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" onclick="radioChecked(this)">
                      <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label">${answer}</label>
                    </div>
                    -->
                    <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label" class="answer-container missed-correct-answer" onclick="radioChecked(this)">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true>
                      <span class="checkmark-con" style="border-width:0px;"><span class="material-icons checkmark" style="opacity:1; background-color: #66a1a5">done</span></span>
                    ${answer}
                    </label>
                  `
                  }
                  else {
                    sectionBoxString += `
                    <!--
                    <div>
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true onclick="radioChecked(this)">
                      <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label">${answer}</label>
                    </div>
                    -->
                    <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label" class="answer-container" onclick="radioChecked(this)">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true>
                      <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
                    ${answer}
                    </label>
                  `
                  }
                }
              })
              // STYLE THE CORRECT ANSWER BELOW HERE
              let question_text = questionData[0]
              //document.getElementById(`${question_text}-${correctAnswers[questionNum-1]}-label`).style.color = "green";
            }
            sectionBoxString += `
              </div>
              </div>
            `
            sectionBox.innerHTML += sectionBoxString
            $('.missed-correct-answer').parents('.question-container').addClass('question-container-wrong')
            $('.answers-container').css('width', '50%')
          }
        })
      } else {
        //clearing the images and questions
        sectionBox.innerHTML = ''
        sectionMaterial.innerHTML = ''
        $('.question-tracker > div').hide();

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
          for (const [questionNum, questionData] of Object.entries(el)) {
            //NOTE THAT 'questionData' IS AN ARRAY
            //questionData[0] is question text; questionData[1] are the answers;
            //questionData[2] is either '' or contains the answer that was previously selected
            var sectionBoxString = ''
            if (questionData[0].includes('no question')) {
              sectionBoxString += `
                <!--
                <div class="mb-2">
                  <b>Question ${questionNum}</b>
                  <br>
                </div>
                -->
                <div class='question-container'>
                <div class="mb-2 testing">
                  <b class="ca-question-num">Question ${questionNum}</b>
                  <br>
                </div>
                <div class="answers-container">
              `
            } else {
              sectionBoxString += `
                <!--
                <div class="mb-2">
                  <b>Question ${questionNum}</b>
                  <br>
                  <b>${questionData[0]}</b>
                </div>
                -->
                <div class='question-container'>
                <div class="mb-2 testing">
                  <b class="ca-question-num">Question ${questionNum}</b>
                  <br>
                  <b class="ca-question-data">${questionData[0]}</b>
                </div>
                <div class="answers-container">
              `
            }
            questionData[1].forEach(answer=>{
              var answerWithQuotes = answer
              answer = answer.replaceAll('"', '&quot;')
              if (answer == questionData[2] && questionData[2] != null) {
                if ( `${answerWithQuotes}` ==  `${correctAnswers[questionNum-1]}`) {
                  console.log('correct!!!' + questionNum)
                  $('#question'+questionNum).parent().find('.material-icons').addClass('answered')
                  $('#question'+questionNum).parent().show()

                  sectionBoxString += `
                <!--
                  <div>
                  <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true onclick="radioChecked(this)" checked>
                  <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label">${answer}</label>
                  </div>
                -->
                <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label" class="answer-container" style="background-color: #f5f5f5" onclick="radioChecked(this)">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true checked>
                      <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
                    ${answer}
                </label>
                `
                }
                else {
                  sectionBoxString += `
                <!--
                  <div>
                  <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true onclick="radioChecked(this)" checked>
                  <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label">${answer}</label>
                  </div>
                -->
                <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label" class="answer-container" onclick="radioChecked(this)">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true checked>
                      <span class="checkmark-con"><span class="material-icons checkmark" style="background-color: #7d120b; color: white; opacity: 1">close</span></span>
                    ${answer}
                </label>
                `
                }                
              } else {
                if ( `${answerWithQuotes}` ==  `${correctAnswers[questionNum-1]}`) {
                  console.log('wrong!!!' + questionNum)
                  $('#question'+questionNum).parent().find('.material-icons').addClass('answered')
                  $('#question'+questionNum).parent().find('.material-icons').text('close')
                  $('#question'+questionNum).parent().find('.material-icons').css('backgroundColor', '#7d120b')
                  $('#question'+questionNum).parent().show()

                  sectionBoxString += `
                  <!--
                  <div>
                    <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true onclick="radioChecked(this)">
                    <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label">${answer}</label>
                  </div>
                  -->
                  <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label" class="answer-container missed-correct-answer" onclick="radioChecked(this)">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true>
                      <span class="checkmark-con" style="border-width:0px;"><span class="material-icons checkmark" style="opacity:1; background-color: #66a1a5">done</span></span>
                    ${answer}
                  </label>
                  `
                }
                else {
                  sectionBoxString += `
                  <!--
                  <div>
                    <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true onclick="radioChecked(this)">
                    <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label">${answer}</label>
                  </div>
                  -->
                  <label for="${questionData[0]}" id="${questionData[0]}-${answer}-label" class="answer-container" onclick="radioChecked(this)">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" disabled=true>
                      <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
                    ${answer}
                  </label>
                `
                }
              }
            })
            sectionBoxString += `
            </div>
            </div>
            `
            sectionBox.innerHTML += sectionBoxString
            $('.missed-correct-answer').parents('.question-container').addClass('question-container-wrong')

            // STYLE THE CORRECT ANSWER BELOW HERE
            let question_text = questionData[0].replaceAll('&quot;', '"')
            console.log(`Question ${questionNum}: ${question_text}-${correctAnswers[questionNum-1]}-label`)

            //document.getElementById(`${question_text}-${correctAnswers[questionNum-1]}-label`).style.color = "green";
          }
        })
      }

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
