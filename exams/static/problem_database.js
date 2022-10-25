// constants from html document
const questionBox = document.getElementById("section-box");
const sectionForm = document.getElementById("problem-database-form");
const buttonContainer = document.getElementById("button-container");
const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const url = window.location.href;

var examType = "SAT";
var questionType = "MATH";

// this function handles both the selection options due to how the dropdown works in dropdown-list.js (see bottom of file)
function filterExamType(selection) {
  // clear questions
  questionBox.innerHTML = "";

  let optionSelection = $(selection).text();
  if (optionSelection == "SAT Exam Questions") {
    console.log(`selected ${optionSelection}`);
    examType = "SAT";
    getButtonData();
  } else if (optionSelection == "ACT Exam Questions") {
    console.log(`selected ${optionSelection}`);
    examType = "ACT";
    getButtonData();
  } else if (optionSelection == "Math") {
    console.log(`selected ${optionSelection}`);
    questionType = "MATH";
    getButtonData();
  } else if (optionSelection == "Grammar") {
    console.log(`selected ${optionSelection}`);
    questionType = "GRAMMAR";
    getButtonData();
  } else {
    console.log("dwajioDAWJDAWJIO");
  }
}

function getButtonData() {
  $.ajax({
    url: buttonDataUrl,
    type: "GET",
    data: {
      csrfmiddlewaretoken: csrf,
      question_type: questionType
    },
    success: function(response) {
      const data = response.data;
      console.log('response: ', data);
      /*
       shape of data: 
       {
          'key': key,
          'value': english_category_map[key],
       }
      */
      // clear the button container
      buttonContainer.innerHTML = "";
      
      data.forEach((el) => {
        buttonContainer.innerHTML += `
          <button
            class="problem-categories-button"
            name="problem-categories-button"
            data-category="${el.key}"
            onclick="getProblemData('${el.key}')"
          >
            ${el.value}
          </button>
        `;
      });

    },
    error: function(error) {
      console.log(error);
    }
  });
}

function getProblemData(category) {
  console.log('category: ', category);
  $.ajax({
    url: dataUrl,
    type: "GET",
    data: {
      csrfmiddlewaretoken: csrf,
      exam_type: examType,
      question_type: questionType,
      category: category,
    },
    success: function (response) {
      const data = response.data;
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
      questionBox.innerHTML = "";
      if (!data.length) {
        console.log("no data");
        questionBox.innerHTML = "No questions found for this category";
      }
      data.forEach((el, index) => {
        // let imgHTML = '<img class="math-material" src="${questionData[3]}"/>'
        // questionBox.innerHTML += `
        // <div class='question-container question-container-math' id="${index}-text">
        // `;
        if (el.materialUrl) {
          questionBox.innerHTML += `
          <div class='problem-database-question-container'>
            <img class="math-material" src="${el.materialUrl}">
            <div class="mb-2 testing">  
              <b class="ca-question-data">
                <p class="question-tag">
                  From question ${el.questionNumber} in ${el.exam} - ${
            el.section
          } 
                </p>
                ${index + 1}. ${el.text}
                <img class='question-hide-show-img' src=${hideAnswerUrl} data-index=${index} data-correct-answer=${
            el.correctAnswer
          } alt="eye-icon" onclick="showCorrectAnswer(this)" />
              </b>
            </div>
            <div class="answers-container" id="${index}-answers"></div>
          </div>
          `;
        } else {
          questionBox.innerHTML += `
          <div class='problem-database-question-container'>
            <div class="mb-2 testing">  
              <b class="ca-question-data">
                <p class="question-tag">
                  From question ${el.questionNumber} in ${el.exam} - ${
            el.section
          } 
                </p>
                ${index + 1}. ${el.text}
                <img class='question-hide-show-img' src=${hideAnswerUrl} data-index=${index} data-correct-answer=${
            el.correctAnswer
          } alt="eye-icon" onclick="showCorrectAnswer(this)" />
              </b>
            </div>
            <div class="answers-container" id="${index}-answers"></div>
          </div>
          `;
        }
        let answerBox = document.getElementById(`${index}-answers`);

        // if multiple choice question
        if (el.choices) {
          el.choices.forEach((choice) => {
            let answer = choice.text;
            let letter = choice.letter;
            answerBox.innerHTML += `
            <label for="${el.text}" class="answer-container" onclick="radioChecked(this, ${index})">
              <input type="radio" class="ans" id="${index}-${letter}" name="${el.text}" value="${answer}">
              <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
            ${answer}
            </label>
            `;
          });
        } else {
          console.log("WE HAVE A FREE RESPONSE QUESTION");
        }
      });

      questionBox.innerHTML += `
      </div>
      </div>
      `;
      // $('.answers-container').css('width', '50%')
      // needed statement for mathjax to render
      MathJax.typesetPromise();

      // set styling for the button
      // first set all buttons to grey
      let buttons = document.getElementsByName("problem-categories-button");
      buttons.forEach((button) => {
        button.className = "problem-categories-button";
      });
      // now set styling on selected button
      let selectedButton = document.querySelector(
        `[data-category=${CSS.escape(category)}]`
      );
      selectedButton.className = "problem-categories-button-selected";
    },
    error: function (error) {
      console.log(error);
    },
  });
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
