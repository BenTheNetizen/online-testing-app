/*
Javascript file for the exam list page
*/

//the dots [... are added to make modalBtns an array

//function to show the correct exam's details when button is clicked on the exam list
var prevElement = null
var allSectionsCompleted = true
const guideMsg = document.getElementById("guide-msg");
const url = window.location.href
const examDropdown = document.getElementById('select-exam');
const examButtons = document.getElementsByClassName('choose-exam-btn');

//run this function to filter by default (SAT)
filterExamType()

function getExamDetails(btnId, examPk, elt) {
  const btn = document.getElementById(btnId)
  const examName = btn.getAttribute("data-exam")
  const examDetailsDiv = document.getElementById(examName + "-details")

  // highlight clicked button
  $(elt).parent().find('button').css('backgroundColor', 'transparent')
  $(elt).css('backgroundColor', 'rgb(234,237,237)')
  // hide arrow of clicked button
  $(elt).parent().find('button .arrow').css('display', 'inline-block')
  $(elt).find('.arrow').css('display', 'none')

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
    examDetailsDiv.style.display = "none";
    if (prevElement == examDetailsDiv) {
      guideMsg.style.display = "block";
    }
  }

//ajax request to grab the Results (raw score) info from database
  $.ajax({
    type: 'GET',
    url: `${url}exam-${examPk}/data`,
    success: function(response) {
      console.log(response.data)
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
            document.getElementById(`exam${examPk}-${section}-score`).innerHTML = `Raw Score: ${section_data[0]}`
            document.getElementById(`exam${examPk}-${section}-start`).style.display = 'none'
            document.getElementById(`exam${examPk}-${section}-time-remaining`).style.display = 'none'
          }
          else if (section_data[1] != null) {
            // Implies that the section is in progress
            allSectionsCompleted = false
            document.getElementById(`exam${examPk}-${section}-time-remaining`).innerHTML = `${section_data[1]}:${section_data[2]} minutes remaining`
            document.getElementById(`exam${examPk}-${section}-start`).innerHTML = '<span class="material-icons material-icons-round">play_arrow</span>Resume this section'
            document.getElementById(`exam${examPk}-${section}-review`).style.display = 'none'
          }
          else {
            // Implies that the section has not ever been started
            allSectionsCompleted = false
            document.getElementById(`exam${examPk}-${section}-reset`).style.display = 'none'
            document.getElementById(`exam${examPk}-${section}-review`).style.display = 'none'
            document.getElementById(`exam${examPk}-${section}-time-remaining`).style.display = 'none'
          }
        }
      })
    },
    error: function(error) {
      console.log(error)
    }
  })
}

function filterExamType() {
  let examType = examDropdown.value

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
  }

}
function changeSectionTime(value, examPk, elt) {
  // change button colors when clicked
  $(elt).parent().find('button').css('backgroundColor', 'white')
  $(elt).parent().find('button').css('color', 'black')
  $(elt).css('backgroundColor', '#66A1A5')
  $(elt).css('color', 'white')

  console.log('change time')
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
      console.log(response)
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

function resetExam(examPk) {
  console.log(examPk)

  $.ajax({
    type: 'POST',
    url: `${url}exam-${examPk}/reset`,
    data: {
      csrfmiddlewaretoken: csrf
    },
    success: function(response) {
      console.log('reset ajax received response')
    },
    error: function(error) {
      console.log(error)
    }
  })
}
