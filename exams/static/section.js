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
var nextSection
var hasCompletedExam
// grabs the data for the first passage
getPassage()

// sends the section data to the backend and redirects to different section or back to the hub
function sendData(goToHub) {
  const data = {}
  data['csrfmiddlewaretoken'] = csrf[0].value
  /*
  const elements = [...document.getElementsByClassName('ans')]

  elements.forEach(el=>{
    if (el.type == 'text') {
      data[el.name] = el.value
    } else {
      if (el.checked) {
        data[el.name] = el.value
      } else {
        //this checks if the question has been answered
        if (!data[el.name]) {
          data[el.name] = 'N'
        }
      }
    }

  })
  console.log(data)
  */
  $.ajax({
      type: 'POST',
      url: `${url}save`,
      data: data,
      success: function(response) {
        console.log(`completedExam: ${hasCompletedExam}`)
        //GO TO HUB IF EXAM IS COMPLETED OR USER SELECTS TO GO BACK TO HUB
        if (hasCompletedExam || goToHub) {
          window.location.href= window.location.origin + '/exam-list'
        }
        //NEW WAY OF ROUTING THE EXAMS (BREAKS ARE ONLY FOR THE SAT AND ACT EXAMS)
        else if (examType == 'SAT') {
          if (nextSection == 'writing') {
            window.location.href="../break1/writing"
          }
          else if (nextSection == 'math1') {
            window.location.href="../break2/math1"
          }
          else {
            window.location.href=`../${nextSection}/section-directions`
          }
        } else if (examType == 'ACT') {
          if (nextSection == 'math') {
            window.location.href="../break1/reading"
          }
          else {
            window.location.href=`../${nextSection}/section-directions`
          }
        } else {
          window.location.href=`../${nextSection}/section-directions`
        }

        // OLD WAY OF ROUTING FOR THE SAT EXAM
        /*
        //THIS IS A HORRIBLE WAY TO REDIRECT THE URLs
        sectionName = response.section_name
        if (isNextSection && examType == 'SAT') {
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
        // ROUTING FOR THE ACT EXAM
        } else if (isNextSection && examType =='ACT') {
          if (sectionName == "english") {
            window.location.href="../math/section-directions"
          }
          else if (sectionName == "math") {
            window.location.href="../break1/reading"
          }
          else if (sectionName == "reading") {
            window.location.href="../science/section-directions"
          }
          else if (sectionName =="science") {
            window.location.href="../results"
          }
        }
        else {
          window.location.href= window.location.origin + '/exam-list'
        }
        */
      },
      error: function(error) {
        console.log(error)
      }
  })
}

// makes ajax request to save the progress of the student each time they select an answer
function radioChecked(elt, questionNum) {
  /*
  console.log('radio checked!')
  console.log(`Name: ${elt.name}, Value: ${elt.value}`)
  let question = elt.name
  let answer = elt.value
  */

  //handles the question tracker column on the right
  $(`#question${questionNum}`).parent().find('.material-icons').addClass('answered')

  // if input with type textbox is passed as arg
  var question
  var answer
  if ( $(elt).hasClass('ca-textbox') ) {
    $(elt).css('backgroundColor', '#f5f5f5')

    question = elt.name
    answer = elt.value
  }
  // else, when label containing input with type radio is passed as arg, do this
  else {
    console.log('radio checked!')
    console.log($(elt).find('input').attr('name'))
    $(elt).parent().find('label').css('backgroundColor', 'white')
    $(elt).css('backgroundColor', '#f5f5f5')
    $(elt).find('input').prop("checked", true)

    question = $(elt).find('input').attr('name')
    answer = $(elt).find('input').attr('value')
  }
  console.log(`questionNum: ${questionNum}`)
  $.ajax({
      type: 'POST',
      url: `${url}save-question`,
      data: {
        csrfmiddlewaretoken: csrf[0].value,
        question: question,
        question_number: questionNum,
        answer: answer,
      },
      success: function(response) {

      },
      error: function(error) {
        console.log(error)
      }
  })
}

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

  //display the passage num
  if (!isMathSection) {
    document.getElementById('passage-num').innerHTML = `Passage ${passageNum} of ${maxPassages}`
  }

  let ajax_url = isMathSection ? `${url}data` : `${url}passage-` + passageNum + `/data`
  $.ajax({
    type: 'GET',
    url: ajax_url,
    success: function(response) {
      console.log(response)

      const data = response.data
      console.log(data)

      //handling for math section only
      if (isMathSection) {
        // make math section form wider than in reading section
        $('#section-form').css('flex-basis', '84%')

        data.forEach(el => {
          for (const [questionNum, questionData] of Object.entries(el)) {
            //NOTE THAT 'questionData' IS AN ARRAY
            //questionData[0] are the question texts
            //questionData[1] are the answers
            //questionData[2] is either '' or contains the answer that was previously selected
            //questionData[3] is the image URL
            var sectionBoxString = ''
            if (questionData[3] != null) {
              //implies that there is an image to add to the question
                sectionBox.innerHTML += `
                <div class='question-container question-container-math'>
                <img class="math-material" src="${questionData[3]}">
                <div class="mb-2 testing">
                  <b class="ca-question-num">Question ${questionNum}</b>
                  <br>
                  <b class="ca-question-data">${questionData[0]}</b>
                </div>
                <div class="answers-container">
              `
            } else {
                sectionBox.innerHTML += `
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
              sectionBox.innerHTML += `
                <div>
                  <input type="text" class="ans ca-textbox" id="${questionNum}-textbox" name="${questionData[0]}" onfocusout="radioChecked(this, ${questionNum})">
                </div>
              `
              if (questionData[2] != null) {
                // CONDITION FOR FREE RESPONSE BEING PREVIOUSLY ANSWERED
                document.getElementById(`${questionNum}-textbox`).setAttribute('value', questionData[2])
                document.getElementById(`${questionNum}-textbox`).style.backgroundColor = '#f5f5f5'
                $(`#question${questionNum}`).parent().find('.material-icons').addClass('answered')
              }
            } else {
              questionData[1].forEach(answer=>{
                // CONDITION FOR QUESTION BEING PREVIOUSLY ANSWERED
                if (answer == questionData[2] && questionData[2] != null) {
                  // SETS QUESTION TRACKER ON THE RIGHT TO GREEN
                  $(`#question${questionNum}`).parent().find('.material-icons').addClass('answered')
                  sectionBox.innerHTML += `
                    <!--
                    <div>
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" onclick="radioChecked(this, ${questionNum})" checked>
                      <label for="${questionData[0]}">${answer}</label>
                    </div>
                    -->

                    <label for="${questionData[0]}" class="answer-container" style="background-color: #f5f5f5" onclick="radioChecked(this, ${questionNum})">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" checked>
                      <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
                    ${answer}
                    </label>
                  `
                } else {

                  sectionBox.innerHTML += `
                    <!--
                    <div>
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" onclick="radioChecked(this, ${questionNum})">
                      <label for="${questionData[0]}">${answer}</label>
                    </div>
                    -->
                    <label for="${questionData[0]}" class="answer-container" onclick="radioChecked(this, ${questionNum})">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}">
                      <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
                    ${answer}
                    </label>
                  `
                }
              })
            }
            sectionBox.innerHTML += `
            </div>
            </div>
            `
            //sectionBox.innerHTML += sectionBoxString
            $('.answers-container').css('width', '50%')
          }
        })
      } else {

        //handling for non math sections
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
                  <b id="question-${questionNum}" class="ca-question-num">Question ${questionNum}</b>
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
                  <b id="question-${questionNum}" class="ca-question-num">Question ${questionNum}</b>
                  <br>
                  <b class="ca-question-data">${questionData[0]}</b>
                </div>
                <div class="answers-container">
              `
            }
            // Handle the answer displaying
            questionData[1].forEach(answer=>{
              answer = answer.replaceAll('\"', '&quot;')

              // CONDITION FOR QUESTION BEING PREVIOUSLY ANSWERED
              if (answer == questionData[2] && questionData[2] != null) {
                // SETS THE PREVIOUSLY ANSWERED TO GREEN
                $(`#question${questionNum}`).parent().find('.material-icons').addClass('answered')
                sectionBoxString += `
                <!--
                  <div>
                    <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" onclick="radioChecked(this, ${questionNum})" checked>
                    <label for="${questionData[0]}">${answer}</label>
                  </div>
                -->
                <label for="${questionData[0]}" class="answer-container" style="background-color: #f5f5f5" onclick="radioChecked(this, ${questionNum})">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" checked>
                      <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
                    ${answer}
                </label>
                `
              } else {
                sectionBoxString += `
                  <!--
                  <div>
                    <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}" onclick="radioChecked(this, ${questionNum})">
                    <label for="${questionData[0]}">${answer}</label>
                  </div>
                  -->
                  <label for="${questionData[0]}" class="answer-container" onclick="radioChecked(this, ${questionNum})">
                      <input type="radio" class="ans" id="${questionData[0]}-${answer}" name="${questionData[0]}" value="${answer}">
                      <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
                    ${answer}
                  </label>
                `
              }

            })
            sectionBoxString += `
            </div>
            </div>
            `
            sectionBox.innerHTML += sectionBoxString
          }
        })

        // return to top of the page after passage change
        document.getElementById('section-form').scrollTop = 0
      }

      // needed statement for MathJax functionality
      MathJax.typesetPromise();


    },
    error: function(error) {
      console.log(error)
    }
  })

}

function getNextSection() {
  const data = {}
  data['csrfmiddlewaretoken'] = csrf[0].value

  $.ajax({
      type: 'POST',
      url: `${url}get-next-section`,
      data: data,
      success: function(response) {
        console.log(response)

        hasCompletedExam = response.has_completed_exam
        // Exam completed, display completed exam modal
        if (hasCompletedExam) {
          // display modal
          $('#finishSectionModal').modal('hide')
          $('#completedExamModal').modal()
        }
        else {
          // display finish section confirmation modal
          nextSection = response.next_section
          $('#finishSectionModal').modal('hide')
          $('#finishSectionConfirmationModal').modal()
        }

      },
      error: function(error) {
        console.log(error)
      }
  })
}
