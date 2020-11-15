"use strict"

let marafon_socket = new WebSocket('wss://' + window.location.host + '/ws/marafon-week/')
marafon_socket.onopen = () => {
    let time_to_response
    let rime_to_choose

    let event_listener = new EventListener()
    let render = new Render()


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

    event_listener.add_listen_question_btns(select_question)

    marafon_socket.onmessage = e => {
        let data = JSON.parse(e.data)
        if (data.type === 'online_watchers') {
            render.update_online('watchers', data.online)
        } else if (data.type === 'online_players') {
            render.update_online('players', data.online)
        } else if (data.type === 'themes_list') {
            render.fill_themes(data.themes)
        } else if (data.type === 'timer') {
            render.time_to_response = data.timer
            start_timer()
        } else if (data.type === 'top_fifteen') {
            render.update_top_fifteen(data.rows)
        } else if (data.type === 'end_game') {
            show_modal_notification('Игра окончена!')
        } else if (data.type === 'selected_question') {
            render.render_question(data.question)
            event_listener.rm_listener_question_btn(select_question)
        } else if (data.type === 'game_history') {
            data.game_history.forEach(i => {
                render.toggle_question_btn(i[0], i[1])
                event_listener.rm_listener_question_btn(select_question)
            })
        }
    }

    function send_start() {
        marafon_socket.send(JSON.stringify({'type': 'event', 'event': 'time_to_start'}))
    }

    let url = window.location.origin + '/marafon-week/?info'
    sendRequest('get', url).then(data => {
        console.log('fetch', data)
        return data
    }).then(marafon_info => {
        let date_start = marafon_info.date_start * 1000
        !marafon_info.is_time_to_start && start_timer(date_start, send_start)
    })


}
