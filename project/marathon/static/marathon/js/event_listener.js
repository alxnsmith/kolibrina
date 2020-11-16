'use strict'

class EventListener {
    constructor() {

    }

    static add_listen_question_btns(func) {
        let question_buttons = document.querySelectorAll('.topic-point')
        question_buttons.forEach(btn => {
            btn.addEventListener('click', func)
        })
    }

    static rm_listener_question_btn(func) {
        let act = document.querySelector('.topic-point.act')
        act.removeEventListener('click', func)
    }

    static add_listen_answers(func) {
        let answer_fields = document.querySelectorAll('.game__options label input')
        answer_fields.forEach(answer => {
            answer.checked = false
            answer.disabled = false
            answer.parentElement.style.cursor = 'pointer'
            answer.addEventListener('click', func)
        })
    }

    static rm_listen_answers(func){
        let answer_fields = document.querySelectorAll('.game__options label')
        answer_fields.forEach(answer => {
            let answer_input = answer.querySelector('input')
            answer_input.removeEventListener('click', func)
            if (!answer_input.checked) {
                answer_input.disabled = true
                answer.style.cursor = 'default'
            }
        })
    }
}