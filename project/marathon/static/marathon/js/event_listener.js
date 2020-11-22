'use strict'

class EventListener {
    constructor() {

    }

    static rm_listen_question_btns(func) {
        let question_buttons = document.querySelectorAll('.topic-point')
        question_buttons.forEach(btn => {
            btn.removeEventListener('click', func)
            btn.style.cursor = 'default'
        })
    }

    static add_listen_question_btns(func) {
        let question_buttons = document.querySelectorAll('.topic-point')
        this.rm_listen_question_btns(func)
        question_buttons.forEach(btn => {
            if (!btn.classList.contains('act') && !btn.classList.contains('disable')) {
                btn.addEventListener('click', func)
                btn.style.cursor = 'pointer'
            }
        })
    }

    static add_listen_answers(func) {
        function rm_listen_answers(func){
            answer_fields.forEach(answer => {
                answer.removeEventListener('click', func)
                if (!answer.checked) {
                    answer.disabled = true
                    answer.parentElement.style.cursor = 'default'
                }
            })
        }

        let answer_fields = document.querySelectorAll('.game__options label input')
        function answer_listener(event){
            func(event)
            rm_listen_answers(answer_listener)
        }

        rm_listen_answers(answer_listener)
        answer_fields.forEach(answer => {
            answer.checked = false
            answer.disabled = false
            answer.parentElement.style.cursor = 'pointer'
            answer.addEventListener('click', answer_listener)
        })
    }
}