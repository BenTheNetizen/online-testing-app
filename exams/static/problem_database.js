// constants from html document
const sectionBox = document.getElementById('section-box');
const sectionForm = document.getElementById('section-form');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
const url = window.location.href 

function getProblemData(category) {
  $.ajax({
    url: dataUrl,
    type: 'GET',
    data: {
      'csrfmiddlewaretoken': csrf,
      'category': category,
    },
    success: function(response) {
      const data = response.data 
      /*
        shape of data:
        {
          'text': 'text',
          correctAnswer': 'correct_answer',
          choices (could be null): {
            'A': 'choice A',
            'B': 'choice B',
            'C': 'choice C',
            'D': 'choice D',
          }
          materialUrl (could be null): some url
        }
      */
      console.log(data);
      data.forEach((el, index) => {
        // let imgHTML = '<img class="math-material" src="${questionData[3]}"/>'
        sectionBox.innerHTML += `
        <div class='question-container question-container-math' id="${index}-text">
        <div class="mb-2 testing">
          <b class="ca-question-data">${el.text}</b>
        </div>
        <div class="answers-container" id="${index}-answers"></div>
        `;
        
        let answerBox = document.getElementById(`${index}-answers`);

        // if multiple choice question
        if (el.choices) {
          el.choices.forEach(choice => {
            let answer = choice.text
            answerBox.innerHTML += `
            <label for="${el.text}" class="answer-container" onclick="radioChecked(this, ${index})">
              <input type="radio" class="ans" id="${el.text}-${answer}" name="${el.text}" value="${answer}">
              <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
            ${answer}
            </label>
            `;
          })
        } else {
          console.log('WE HAVE A FREE RESPONSE QUESTION');
        }
      })
    },
    error: function(error) {
      console.log(error);
    }
  })
}