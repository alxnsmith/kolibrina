"use strict"

let marafon_socket = new WebSocket('wss://' + window.location.host + '/ws/marafon-week/');
marafon_socket.onopen = () => {
    let username;
    let role;
    let timer;

/////////////////////////////////////////////////////////////////////////////////////////////////

    // send_start()

/////////////////////////////////////////////////////////////////////////////////////////////////

    marafon_socket.onmessage = e => {
        let data = JSON.parse(e.data);
        console.log(data.type)
        switch (data.type) {
            case 'online_watchers':
                Render.update_online('watchers', data.online);
                break
            case 'online_players':
                Render.update_online('players', data.online);
                break
            case 'themes_list':
                Render.fill_themes(data.themes);
                break
            case 'respond_timer':
                timer = new Timer(data.unix_time_end, 'minutes', Render.timer, show_modal_notification, 'Time is out');
                timer.start();
                break
            case 'static_base_info':
                Render.base_static_render(data.info);
                break
            case 'top_fifteen':
                Render.update_top_fifteen(data.rows);
                break
            case 'end_game':
                show_modal_notification('Игра окончена!');
                break
            case 'selected_question':
                Render.render_question(data.question);
                console.log(data)
                if (role === 'player' && data.expected_players.includes(username)){
                    EventListener.add_listen_answers(select_answer);
                }
                break
            case 'select_question':
                if (data.username === username) {
                    EventListener.add_listen_question_btns(select_question);
                    show_modal_notification('Ваш черёд!');
                } else {
                    show_modal_notification(`${upFirst(data.username)} выбирает вопрос!`);
                }
                timer = new Timer(data.timer, 'minutes', Render.timer) // добавить функцию для отправки ивента о том, что время на выбор вопроса вышло и пора выбрать рандомный
                timer.start()
                break
            case 'game_history':
                data.game_history.forEach(btn => {
                    Render.toggle_question_btn(btn[0], btn[1]);
                })
                break
            case 'username':
                username = data.username;
                break
            case 'role':
                role = data.role;
                break
            case 'date_time_start':
                timer = new Timer(data.date_time_start, 'minutes', Render.timer, send_start);
                timer.start();
                break
            case 'stop_timer':
                if (timer) {timer.stop()}
                break
            case 'reset_timer':
                if (timer) {timer.reset()}
                break
            }
    }

    function send_start() {
        marafon_socket.send(JSON.stringify({'type': 'event', 'event': 'time_to_start'}));
    }
}
