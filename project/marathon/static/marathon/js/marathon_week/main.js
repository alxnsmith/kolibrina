"use strict"

let marafon_socket = new WebSocket('wss://' + window.location.host + '/ws/marafon-week/')
marafon_socket.onopen = () => {
    let time_to_response
    let rime_to_choose


    EventListener.add_listen_question_btns(select_question)

    marafon_socket.onmessage = e => {
        let data = JSON.parse(e.data)
        if (data.type === 'online_watchers') {
            Render.update_online('watchers', data.online)
        } else if (data.type === 'online_players') {
            Render.update_online('players', data.online)
        } else if (data.type === 'themes_list') {
            Render.fill_themes(data.themes)
        } else if (data.type === 'timer') {
            Render.time_to_response = data.timer
            start_timer()
        } else if (data.type === 'static_base_info') {
            Render.base_static_render(data.info)
        } else if (data.type === 'top_fifteen') {
            Render.update_top_fifteen(data.rows)
        } else if (data.type === 'end_game') {
            show_modal_notification('Игра окончена!')
        } else if (data.type === 'selected_question') {
            Render.render_question(data.question)
            EventListener.add_listen_answers(select_answer)
            EventListener.rm_listener_question_btn(select_question)
        } else if (data.type === 'game_history') {
            data.game_history.forEach(i => {
                Render.toggle_question_btn(i[0], i[1])
                EventListener.rm_listener_question_btn(select_question)
            })
        } else if (data.type === 'date_time_start'){
            let timer = new Timer(
                data.date_time_start,
                'minutes',
                Render.timer
            )

            timer.start()
        }
    }

    function send_start() {
        marafon_socket.send(JSON.stringify({'type': 'event', 'event': 'time_to_start'}))
    }

}
