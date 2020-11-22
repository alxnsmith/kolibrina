'use strict'

function upFirst(str){  // upperCase the first character
    return str[0].toUpperCase() + str.slice(1)
}

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
    marafon_socket.send(JSON.stringify({
        'type': 'event',
        'event': 'select_answer',
        'answer': event.target.value,
    }))
}