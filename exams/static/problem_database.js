// constants from html document
const questionBox = document.getElementById("section-box");
const sectionForm = document.getElementById("problem-database-form");
const sectionMaterial = document.getElementById('section-material');
const buttonContainer = document.getElementById("button-container");
const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const url = window.location.href;

var examType = "SAT";
var questionType = "MATH";
var passageNum = 1;
var passageData;
var maxPassages;

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
      question_type: questionType,
      exam_type: examType,
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

function test() {
  console.log('how the fuck si this possible');
}

function getPassageData(value) {
  // assumes that passageData is already defined
  if (passageData === undefined) {
    console.log('passageData is undefined');
    return;
  }

  if (value == "init") {
    passageNum = 1;
  } else if (value == "next") {
    passageNum += 1;
  } else if (value == "prev") {
    passageNum -= 1;
  }

  document.getElementById('passage-num').innerHTML = `Passage ${passageNum} of ${maxPassages}`;

  questionBox.innerHTML = ''
  sectionMaterial.innerHTML = `
    <img src=${passageData[passageNum - 1].materialUrl} />
  `;

  passageData[passageNum-1].questions.forEach((question, index) => {
    var questionBoxString = '';

    if (question.text.includes('no question')) {
      questionBoxString += `
        <div class='question-container' id="${index+1}-text">
        <div class="mb-2 testing">
          <b id="question-${index+1}" class="ca-question-num">Question ${index+1}</b>
          <br>
        </div>
        <div class="answers-container">
      `;
    } else {
      questionBoxString += `
        <div class='question-container' id="${index+1}-text">
        <div class="mb-2 testing">
          <b id="question-${index+1}" class="ca-question-num">Question ${index+1}</b>
          <br>
          <b class="ca-question-data">${question.text}</b>
        </div>
        <div class="answers-container">
      `;
    }

    question.choices.forEach((answer) => {
      answer = answer.text.replaceAll('\"', '&quot;');
      questionBoxString += `
        <!--
        <div>
          <input type="radio" class="ans" id="${question.text}-${answer}" name="${question.text}" value="${answer}" onclick="radioChecked(this, ${index+1})">
          <label for="${question.text}">${answer}</label>
        </div>
        -->
        <label for="${question.text}" class="answer-container" onclick="radioChecked(this, ${index+1})">
            <input type="radio" class="ans" id="${question.text}-${answer}" name="${question.text}" value="${answer}">
            <span class="checkmark-con"><span class="material-icons checkmark">done</span></span>
          ${answer}
        </label>
        </div>
        </div>
      `;
    });

    questionBox.innerHTML += questionBoxString;
  })
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
      passageData = response.questions_groupby_passage;
      maxPassages = passageData.length;
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
      console.log('passage data: ', passageData);

      /*
        shape of passageData:
        {
          'material_url',
          'questions': [question (see shape above)]
        }
      */
      // reset the section box and answer box
      questionBox.innerHTML = "";
      if (!data.length) {
        console.log("no data");
        questionBox.innerHTML = "No questions found for this category";
      }

      if (questionType == 'MATH') {
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
          if (el.choices[0].text != null) {
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
            answerBox.innerHTML += `
            <p>This is a free response question.</p>
            `
          }
        });
  
        questionBox.innerHTML += `
        </div>
        </div>
        `;

      } else {
        getPassageData('init');

      }
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
  let answerBox = document.getElementById(`${index}-answers`);
  let correctAnswer = el.dataset.correctAnswer;
  if (el.src.includes(hideAnswerUrl)) {
    el.src = showAnswerUrl;
    // check if the correct answer is multiple choice or free response
    if(correctAnswer[0].toUpperCase() != correctAnswer[0].toLowerCase()) {
      document.getElementById(`${index}-${correctAnswer}`).checked = true;
    } else {
      answerBox.innerHTML = `<p>Correct answer: ${correctAnswer}</p>`;
    }
  } else {
    el.src = hideAnswerUrl;
    if (correctAnswer[0].toUpperCase() != correctAnswer[0].toLowerCase()) {
      document.getElementById(`${index}-${correctAnswer}`).checked = false;
    } else {
      answerBox.innerHTML = "<p>This is a free response question.</p>";
    }
  }

  // write functionality for showing the correct answer
}
