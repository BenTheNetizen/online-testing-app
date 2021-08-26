/*
Javascript file for the exam list page
*/

//the dots [... are added to make modalBtns an array

//function to show the correct exam's details when button is clicked on the exam list
var prevElement = null
var allSectionsCompleted = true
var hasSelectedRecentExam = false
const guideMsg = document.getElementById("guide-msg");
const examDropdown = document.getElementById('select-exam');
const examButtons = document.getElementsByClassName('choose-exam-btn');


//run this function to filter by default and select first exam (SAT)
if (recentExamType != null) {
  if (recentExamType == 'SAT') {
    filterExamType('<li>SAT Mock Exams</li>')
  }
  else if (recentExamType == 'ACT') {
    filterExamType('<li>ACT Mock Exams</li>')
  }
  else {
    console.log('RECENT EXAM HAS NO EXAM TYPE!??!')
  }
} else {
  filterExamType('<li>SAT Mock Exams</li>')
}


//run this function to open the first exam by default

// gets exam details (also shows recent exam if possible)
function getExamDetails(btnId) {
  const btn = document.getElementById(btnId)
  const examName = btn.getAttribute("data-exam-name")
  const examPk = btn.getAttribute("data-exam-pk")
  const examDetailsDiv = document.getElementById(examName + "-details")

  // highlight clicked button
  $(btn).parent().find('button').css('backgroundColor', 'transparent')
  $(btn).css('backgroundColor', 'rgb(234,237,237)')
  // hide arrow of clicked button
  $(btn).parent().find('button .arrow').css('display', 'inline-block')
  $(btn).find('.arrow').css('display', 'none')

  if (examDetailsDiv.style.display == "none")
  {
    if (prevElement === null)
    {
      prevElement = examDetailsDiv;
    }
    else
    {
      prevElement.style.display = "none";
      prevElement = examDetailsDiv;
    }
    examDetailsDiv.style.display = "block";
    guideMsg.style.display = "none";
  }
  else
  {
    if (prevElement == examDetailsDiv) {
      //guideMsg.style.display = "block";
    } else {
      examDetailsDiv.style.display = "none";
    }
  }

//ajax request to grab the Results (raw score) info from database
  $.ajax({
    type: 'GET',
    url: `${url}exam-${examPk}/data`,
    success: function(response) {
      data = response.data

      //reset the boolean for if all sections are done (if any are not finished, set this to false)
      allSectionsCompleted = true
      data.forEach(el => {
        for (const [section, section_data] of Object.entries(el)) {
          //NOTE THAT 'section_data' IS AN ARRAY
          //'section' is the string of the section type
          //section_data[0] is the raw score (if it exists)
          //section_data[1] are the minutes left (if it exists)
          //section_data[2] are the seconds left (if it exists)
          if (section_data[0] != null) {
            // Implies that the section has been finished
            document.getElementById(`exam${examPk}-${section}-raw-score`).innerHTML = `Raw Score: ${section_data[0]}`
            document.getElementById(`exam${examPk}-${section}-start`).style.display = 'none'
            document.getElementById(`exam${examPk}-${section}-time-remaining`).style.display = 'none'

            if (section_data[1] != null) {
              //implies that there is a scaled_score
              document.getElementById(`exam${examPk}-${section}-scaled-score`).innerHTML = `Estimated Section Score: ${section_data[1]}`
            }
          }
          else if (section_data[2] != null) {
            // Implies that the section is in progress

            allSectionsCompleted = false
            var secondsLeft = section_data[3]
            if (secondsLeft <= 9) {
              secondsLeft = '0' + secondsLeft
            }
            document.getElementById(`exam${examPk}-${section}-time-remaining`).innerHTML = `${section_data[2]}:` + secondsLeft + ` minutes remaining`
            // THIS IS NOW HANDLEd IN exam_list.htl
            document.getElementById(`exam${examPk}-${section}-start`).innerHTML = '<span class="material-icons material-icons-round">play_arrow</span>Resume this section'
            document.getElementById(`exam${examPk}-${section}-start`).href = section_data[5]
            document.getElementById(`exam${examPk}-${section}-review`).style.display = 'none'
            document.getElementById(`exam${examPk}-${section}-reset`).style.display = 'none'
          }
          else {
            ('section never started')
            // Implies that the section has not ever been started
            allSectionsCompleted = false
            startBtn = document.getElementById(`exam${examPk}-${section}-start`)
            startBtn.innerHTML = 'Begin this section'
            startBtn.href = section_data[4]
            startBtn.style.display = 'block'

            document.getElementById(`exam${examPk}-${section}-raw-score`).innerHTML = 'Raw Score: N/A'
            document.getElementById(`exam${examPk}-${section}-scaled-score`).innerHTML = 'Estimated Section Score: N/A'
            document.getElementById(`exam${examPk}-${section}-reset`).style.display = 'none'
            document.getElementById(`exam${examPk}-${section}-review`).style.display = 'none'
            document.getElementById(`exam${examPk}-${section}-time-remaining`).style.display = 'none'
          }
        }
      })

      // Set the regular/extended time buttons to the correct state
      let isExtendedTime = response.is_extended_time
      let regularTimeBtn = document.getElementById(`${examPk}-regular-time-btn`)
      let extendedTimeBtn = document.getElementById(`${examPk}-extended-time-btn`)
      if (isExtendedTime) {
        changeSectionTime('extended', examPk, extendedTimeBtn)
      } else {
        changeSectionTime('regular', examPk, regularTimeBtn)
      }
    },
    error: function(error) {
      console.log(error)
    }
  })
}

function filterExamType(selection) {
  let examType = $(selection).text()

  if (examType == 'SAT Mock Exams') {
    //hide all exam buttons
    [...examButtons].forEach(element => {
      element.style.display = "none";
    })

    //show the queried exam buttons
    let query = document.querySelectorAll("[data-exam-type='SAT']")
    query.forEach(element => {
      element.style.display = "block";
    })

    // select the most recent exam if it exists
    if (recentExam != null && !hasSelectedRecentExam) {
      getExamDetails(`${recentExam}-btn`)
      hasSelectedRecentExam = true
    } else {
      // select the first SAT exam
      getExamDetails('SAT Mock Test 1-btn')
    }


  } else if (examType == 'ACT Mock Exams') {
    //hide all exam buttons
    [...examButtons].forEach(element => {
      element.style.display = "none";
    })

    //show the queried exam buttons
    let query = document.querySelectorAll("[data-exam-type='ACT']")
    query.forEach(element => {
      element.style.display = "block";
    })

    // select the most recent exam if it exists
    if (recentExam != null && !hasSelectedRecentExam) {
      getExamDetails(`${recentExam}-btn`)
      hasSelectedRecentExam = true
    } else {
      // select the first ACT exam
      getExamDetails('ACT Mock Test 1-btn')
    }
  }
}

function changeSectionTime(value, examPk, elt) {
  // change button colors when clicked
  $(elt).parent().find('button').css('backgroundColor', 'white')
  $(elt).parent().find('button').css('color', 'black')
  $(elt).css('backgroundColor', '#66A1A5')
  $(elt).css('color', 'white')

  let isExtendedTime
  if (value === 'regular') {
    isExtendedTime = false
  }
  else if (value === 'extended') {
    isExtendedTime = true
  }

  $.ajax({
    type: 'POST',
    url: `${url}exam-${examPk}/change-time`,
    data: {
      csrfmiddlewaretoken: csrf,
      is_extended_time: isExtendedTime,
    },
    success: function(response) {

    },
    error: function(error) {
      console.log(error)
    }
  })

}

//function checks if all results have been completed
function openBreakdown(elt) {
  modalId = elt.dataset.modalId
  resultsUrl = elt.dataset.url
  if (allSectionsCompleted) {
    window.open(resultsUrl);
  } else {
    //display modal stating that the exam is not yet completed
    $(modalId).modal()
  }
}

function resetExam(examPk, targetBtnId) {

  $.ajax({
    type: 'POST',
    url: `${url}exam-${examPk}/reset`,
    data: {
      csrfmiddlewaretoken: csrf
    },
    success: function(response) {
      getExamDetails(targetBtnId)

    },
    error: function(error) {
      console.log(error)
    }
  })
}
