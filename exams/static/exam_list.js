/*
Javascript file for the exam list page
*/

//the dots [... are added to make modalBtns an array

//function to show the correct exam's details when button is clicked on the exam list
var prevElement = null
const guideMsg = document.getElementById("guide-msg");
const url = window.location.href

function getExamDetails(btnId, examPk) {
  const btn = document.getElementById(btnId);
  const examName = btn.getAttribute("data-exam");
  const examDetailsDiv = document.getElementById(examName + "-details");

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
      //debugger;
      data = response.data

      data.forEach(el => {
        for (const [section, section_data] of Object.entries(el)) {
          //NOTE THAT 'section_data' IS AN ARRAY
          //'section' is the string of the section type
          //section_data[0] is the raw score (if it exists)
          //section_data[1] are the minutes left (if it exists)
          //section_data[2] are the seconds left (if it exists)
          if (section_data[0] != null) {
            // Implies that the section has been finished
            document.getElementById(section + '-score').innerHTML = `Raw Score: ${section_data[0]}`

            document.getElementById(section + '-start').style.display = 'none'
            document.getElementById(section + '-time-remaining').style.display = 'none'
          }
          else if (section_data[1] != null) {
            // Implies that the section is in progress
            document.getElementById(section + '-time-remaining').innerHTML = `${section_data[1]} minutes ${section_data[2]} seconds remaining`
            document.getElementById(section + '-start').innerHTML = 'Resume this section'
            document.getElementById(section + '-review').style.display = 'none'
          }
          else {
            // Implies that the section has not ever been started
            document.getElementById(section + '-reset').style.display = 'none'
            document.getElementById(section + '-review').style.display = 'none'
            document.getElementById(section + '-time-remaining').style.display = 'none'
          }
        }
      })
    },
    error: function(error) {
      console.log(error)
    }
  })
}

function changeSectionTime(value, examPk) {
  console.log('change time')
  let timeMultiplier
  if (value === 'regular') {
    timeMultiplier = 1.0
  }
  else if (value === 'extended') {
    timeMultiplier = 1.5
  }

  $.ajax({
    type: 'POST',
    url: `${url}exam-${examPk}/change-time`,
    data: {
      csrfmiddlewaretoken: csrf,
      multiplier: timeMultiplier,
    },
    success: function(response) {
      console.log(response)
    },
    error: function(error) {
      console.log(error)
    }
  })

}

function resetExam(examPk) {
  console.log(examPk)

  $.ajax({
    type: 'POST',
    url: `${url}exam-${examPk}/reset`,
    success: function(response) {
      console.log('reset ajax received response')
    },
    error: function(error) {
      console.log(error)
    }
  })
}
