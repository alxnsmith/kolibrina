'use strict'

class EventListener {
    constructor() {

    }
    static get answer_fields(){
        return document.querySelectorAll('.game__options label input');
    }
    static get question_buttons(){
        return document.querySelectorAll('.topic-point');
    }
    static get skip_btn(){
        return document.querySelector('#skip_btn')
    }

    static rm_listen_question_btns(func) {
        this.question_buttons.forEach(btn => {
            btn.removeEventListener('click', func);
            btn.style.cursor = 'default';
        })
    }

    static add_listen_question_btns(func) {
        this.rm_listen_question_btns(func);
        this.question_buttons.forEach(btn => {
            if (!btn.classList.contains('act') && !btn.classList.contains('disable')) {
                btn.addEventListener('click', func);
                btn.style.cursor = 'pointer';
            }
        })
    }

    static toggle_answer(answer, event){
        if (event === 'disable') {
            answer.disabled = true;
            answer.checked = false;
            answer.parentElement.style.cursor = 'default';
        } else if (event === 'enable') {
            answer.checked = false;
            answer.disabled = false;
            answer.parentElement.style.cursor = 'pointer';
        }
    }

    static rm_listen_answers(func){
        this.answer_fields.forEach(answer => {
            answer.removeEventListener('click', func);
            if (!answer.checked) {
                this.toggle_answer(answer, 'disable')
            }
        })
    }

    static add_listen_answers(func) {
        this.rm_listen_answers(func);
        this.answer_fields.forEach(answer => {
            this.toggle_answer(answer, 'enable')
            answer.addEventListener('click', func);
        })
    }

    static add_listen_skip_btn(func){
        this.skip_btn.addEventListener('click', func)
    }

    static rm_listen_skip_btn(func){
        this.skip_btn.removeEventListener('click', func)
    }
}