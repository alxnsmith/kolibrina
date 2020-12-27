"use strict"
let marafon_socket = new WebSocket('wss://' + window.location.host + '/ws/marafon-week/');
marafon_socket.onopen = () => {
    let username;
    let role;
    let timer;

    disable_answers()
    /////////////////////////////////////////////////////////////////////////////////////////////////

    /////////////////////////////////////////////////////////////////////////////////////////////////

    marafon_socket.onmessage = e => {
        let data = JSON.parse(e.data);
        switch (data.type) {
            case 'online_watchers':
                Render.update_online('watchers', data.online);
                break
            case 'online_players':
                Render.update_online('players', data.online);
                break
            case 'correct_answer':
                Render.correct_answer(data.correct_answer)
                break
            case 'themes_list':
                Render.fill_themes(data.themes);
                break
            case 'answer_timer':
                timer = new Timer(data.unix_time_end, 'minutes', Render.timer, select_answer_timer_is_end);
                timer.start();
                break
            case 'static_base_info':
                Render.base_static_render(data.info);
                break
            case 'top_fifteen':
                Render.update_top_fifteen(data.rows);
                break
            case 'end_game':
                EventListener.rm_listen_skip_btn(skip_question)
                show_modal_notification('Игра окончена!');
                Render.state(`Игра окончена! Посмотреть итоги можно <a style="margin-left: .3rem; color: #09f; text-decoration-line: underline" href="${data.summary_url}">здесь</a>`)
                timer.reset()
                break
            case 'selected_question':
                Render.render_question(data.question);
                Render.state('Выбор ответа');
                Render.correct_answer('')
                EventListener.rm_listen_question_btns(select_question);
                if (role === 'player' && data.expected_players.includes(username)) {
                    EventListener.add_listen_answers(select_answer);
                }
                break
            case 'select_question':
                if (data.username === username) {
                    EventListener.add_listen_question_btns(select_question);
                    show_modal_notification('Ваш черёд!');
                    Render.state('Ваш выбор')
                } else {
                    show_modal_notification(`${upFirst(data.username)} выбирает вопрос!`);
                    Render.state(`Выбирает ${upFirst(data.username)}`)
                }
                EventListener.rm_listen_answers()
                timer = new Timer(data.timer, 'minutes', Render.timer, select_question_timer_is_end)
                timer.start()
                EventListener.add_listen_skip_btn(skip_question)
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
                Render.state('Ожидание начала')
                break
            case 'stop_timer':
                if (timer) {
                    timer.stop()
                }
                break
            case 'reset_timer':
                if (timer) {
                    timer.reset()
                }
                break
            case 'redirect':
                window.location = window.location.origin + data.url
                break
            case 'no_events':
                Render.state('Сейчас нет мероприятий.')
                marafon_socket.close()
        }

    }

    function send_start() {
        marafon_socket.send(JSON.stringify({'type': 'event', 'event': 'time_to_start'}));
    }
}
