function render_question(question, answers, old_answers, num){
    let question_field = document.getElementById('question')
    let list_question_num_elements = document.querySelectorAll('.q_num')
    let current_question_num_element = document.getElementById(`q_num${num}`)
    let answer_fields = document.querySelectorAll('.answer')

    for (let i=0; i<list_question_num_elements.length; i++){
        if (list_question_num_elements[i].classList.contains('act')){
            list_question_num_elements[i].classList.remove('act')
        }
    }
    for (let i=0; i<answers.length; i++){
        answer_fields[i].innerHTML = answer_fields[i].innerHTML.replaceAll(old_answers[i], answers[i])
    }
    question_field.innerText = question
    current_question_num_element.classList.add('act')
}