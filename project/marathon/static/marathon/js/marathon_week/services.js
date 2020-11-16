'use strict'

function select_question(event) {
    let target = event.target
    let block_id = target.dataset.block_id
    let pos = target.dataset.pos
    marafon_socket.send(JSON.stringify({
        'type': 'event',
        'event': 'select_question',
        'block_id': block_id,
        'pos': pos
    }))
}
function select_answer(event) {
    EventListener.rm_listen_answers(select_answer)
    marafon_socket.send(JSON.stringify({
        'type': 'event',
        'event': 'select_answer',
        'answer': event.target.value,
    }))
}