'use strict'

function select_question(event) {
    EventListener.rm_listen_question_btns(select_question)
    let target = event.target
    let block = target.dataset.block
    let pos = target.dataset.pos
    marafon_socket.send(JSON.stringify({
        'type': 'event',
        'event': 'select_question',
        'block': block,
        'pos': pos
    }))
}
function select_answer(event) {
    EventListener.rm_listen_skip_btn(skip_question)
    EventListener.rm_listen_answers(select_answer)
    marafon_socket.send(JSON.stringify({
        'type': 'event',
        'event': 'select_answer',
        'answer': event.target.value,
    }))
}
function select_answer_timer_is_end() {
    EventListener.rm_listen_skip_btn(skip_question)
    marafon_socket.send(JSON.stringify({
        'type': 'event',
        'event': 'select_answer_timer_is_end'
    }))
}
function select_question_timer_is_end() {
    marafon_socket.send(JSON.stringify({
        'type': 'event',
        'event': 'select_question_timer_is_end'
    }))
}

function disable_answers(){
    EventListener.rm_listen_skip_btn(skip_question)
    EventListener.answer_fields.forEach(answer => {
        EventListener.toggle_answer(answer, 'disable')
    })
}

function skip_question(){
    marafon_socket.send(JSON.stringify({
        'type': 'event',
        'event': 'skip_question'
    }))
    console.log('Skip_question')
    EventListener.rm_listen_skip_btn(skip_question)
}