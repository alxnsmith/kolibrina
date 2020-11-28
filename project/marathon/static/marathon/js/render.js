'use strict'

class Render {
    constructor() {

    }

    static base_static_render(info){
        let marathon_number = document.querySelector('.marafon-number')
        let firstname = document.querySelector('.marafon_author-name .firstname')
        let lastname = document.querySelector('.marafon_author-name .lastname')
        let city = document.querySelector('.marafon_author-name .city')
        marathon_number.innerText = info.marathon_id
        firstname.innerText = info.firstname
        lastname.innerText = info.lastname
        city.innerText = info.city
    }

    static timer(minutes, seconds) {
        let timer_html = document.querySelector('.marafon-timer')
        minutes = String(minutes).padStart(2, '0')
        seconds = String(seconds).padStart(2, '0')
        timer_html.innerText = `${minutes}:${seconds}`
    }

    static correct_answer(answer) {
        let elem = document.querySelector('.correct_answer span')
        elem.innerText = answer
    }

    static update_top_fifteen(players) {
        let rating = new rating_top_fifteen()

        players.forEach(player => {
            if (player.score_delta > 0){player.score_delta = '+' + String(player.score_delta)}
            rating.write_row(player)
        })

        let to_erase = Array.from(rating.rows).slice(players.length)
        to_erase.forEach(row_to_erase => {
            rating.erase_row(row_to_erase)
        })

    }

    static update_online(counter, online) {
        if (counter === 'watchers') {
            document.getElementById('online_watchers').innerText = online
        } else if (counter === 'players') {
            document.getElementById('online_players').innerText = online
        }
    }

    static fill_themes(themes) {
        let theme_field
        let theme_blocks = document.querySelectorAll('.topic')
        let i = 0
        themes.forEach(theme => {
            theme_field = theme_blocks[i].querySelector('.topic-name')
            theme_field.innerText = theme[0]
            i++
        })
    }

    static toggle_question_btn(block, pos) {
        let row = document.querySelectorAll('.topic')[block]
        let btn = row.querySelectorAll('.topic-point')[pos]

        let act = document.querySelector('.topic-point.act')
        if (act) {
            act.classList.remove('act')
            act.classList.add('disable')
        }
        btn.classList.add('act')
        btn.style.cursor = 'default'
    }

    static render_question(question){
        this.toggle_question_btn(question.block, question.pos)

        let question_field = document.getElementById('question')
        let answer_fields = document.querySelectorAll('.game__options label')
        for (let i = 0; i<answer_fields.length; i++){
            answer_fields[i].querySelector('.text').innerText = question.answers[i]
            answer_fields[i].querySelector('.answer').value = question.answers[i]
        }
        question_field.innerText = question.question
    }

    static state(state){
        let elem = document.querySelector('.btn_choose');
        elem.innerText = state
    }
}