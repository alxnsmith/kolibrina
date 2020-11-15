'use strict'

class EventListener {
    constructor() {
        this.question_buttons = document.querySelectorAll('.topic-point')
    }

    add_listen_question_btns(func) {
        this.question_buttons.forEach(btn => {
            btn.addEventListener('click', func)
        })
    }

    rm_listener_question_btn(func) {
        let act = document.querySelector('.topic-point.act')
        act.removeEventListener('click', func)
    }
}