function init_question(question, answers, num){
    let current_question_num_element = document.getElementById(`q_num${num}`)

    render_question(question, answers)

    current_question_num_element.classList.add('act')
}

function correct_render_num(){
    let list_question_num_elements = document.querySelectorAll('.q_num')

    for (let i=0; i<list_question_num_elements.length; i++){
        if (list_question_num_elements[i].classList.contains('act')){
            list_question_num_elements[i].classList.remove('act')
            list_question_num_elements[i].classList.add('OK')
        }
    }
}

function del_questions(to_del){
    let answers = document.querySelectorAll('.answer')
    answers[0].parentElement.style.height = `${answers[0].parentElement.clientHeight}px`

    for (let i = 0; i < answers.length; i++){
        console.log(answers[i].querySelector('input').value, to_del)
        if (to_del.indexOf(answers[i].querySelector('input').value) !== -1){
            console.log(answers[i].parentElement.style.height, answers[i].offsetHeight+10)
            answers[i].parentElement.style.height = `calc(${answers[i].parentElement.style.height} - ${answers[i].offsetHeight+10}px)`
            answers[i].remove()
        }
    }
}

function render_question(question, answers){
    let question_field = document.getElementById('question')
    let answers_block = document.querySelector('.game__options')
    let answer_fields = document.querySelectorAll('.answer')

    answers_block.style.height = ''

    question_field.innerText = question

    for (let i=0; i<answer_fields.length; i++){
        answer_fields[i].remove()
    }
    for (let i=0; i<answers.length; i++){
        answers_block.innerHTML += `<label class="answer">
					<input type="radio" name="answer" value="${answers[i]}">
					${answers[i]}
					<span></span>
				</label>`
    }
}

function chance_wrong_question(){
    let inputs = document.getElementsByName('answer');
    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].type === "radio" && inputs[i].checked) {
            inputs[i].disabled = true
            inputs[i].checked = false
            inputs[i].nextSibling.nextSibling.style['backgroundColor'] = 'red'
        }
    }
}