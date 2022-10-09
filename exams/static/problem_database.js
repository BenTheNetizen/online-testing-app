// constants from html document
const questionBox = document.getElementById('section-box');
const sectionForm = document.getElementById('problem-database-form');
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

      // reset the section box and answer box
      questionBox.innerHTML = '';
      if (!data.length) {
        console.log('no data');
        questionBox.innerHTML = 'No questions found for this category';
      }
      data.forEach((el, index) => {
        // let imgHTML = '<img class="math-material" src="${questionData[3]}"/>'
        // questionBox.innerHTML += `
        // <div class='question-container question-container-math' id="${index}-text">
        // `;
        if (el.materialUrl) {
          questionBox.innerHTML += `
          <img class="math-material" src="${el.materialUrl}">
          `;
        }
        questionBox.innerHTML += `
        <div class="mb-2 testing">  
          <b class="ca-question-data">
            ${el.text}
            <img class='question-hide-show-img' src=${hideAnswerUrl} data-index=${index} data-correct-answer=${el.correctAnswer} alt="eye-icon" onclick="showCorrectAnswer(this)" />
          </b>
        </div>
        <div class="answers-container" id="${index}-answers"></div>
        `;
        
        let answerBox = document.getElementById(`${index}-answers`);

        // if multiple choice question
        if (el.choices) {
          el.choices.forEach(choice => {
            let answer = choice.text
            let letter = choice.letter
            answerBox.innerHTML += `
            <label for="${el.text}" class="answer-container" onclick="radioChecked(this, ${index})">
              <input type="radio" class="ans" id="${index}-${letter}" name="${el.text}" value="${answer}">
              <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
            ${answer}
            </label>
            `;
          })
        } else {
          console.log('WE HAVE A FREE RESPONSE QUESTION');
        }
      })

      questionBox.innerHTML += `
      </div>
      </div>
      `
      // $('.answers-container').css('width', '50%')
      // needed statement for mathjax to render
      MathJax.typesetPromise();

      // set styling for the button
      // first set all buttons to grey
      let buttons = document.getElementsByName('problem-categories-button');
      buttons.forEach(button => {
        button.className = 'problem-categories-button';
      })
      // now set styling on selected button
      let selectedButton = document.querySelector(`[data-category=${CSS.escape(category)}]`);
      selectedButton.className = 'problem-categories-button-selected';
    },
    error: function(error) {
      console.log(error);
    }
  })
}

function showCorrectAnswer(el) {
  let index = el.dataset.index;
  let correctAnswer = el.dataset.correctAnswer;
  if (el.src.includes(hideAnswerUrl)) {
    el.src = showAnswerUrl;
    // get's the input element of the correct answer and checks it
    document.getElementById(`${index}-${correctAnswer}`).checked = true;
  } else {
    el.src = hideAnswerUrl;
    document.getElementById(`${index}-${correctAnswer}`).checked = false;
  }
  
  // write functionality for showing the correct answer
}