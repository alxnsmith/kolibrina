'use strict'

class Render {
    constructor() {

    }

    update_top_fifteen(players) {
        let rating = new rating_top_fifteen()

        players.forEach(player => {
            rating.write_row(player)
        })

        let to_erase = Array.from(rating.rows).slice(players.length)
        to_erase.forEach(row_to_erase => {
            rating.erase_row(row_to_erase)
        })

    }

    update_online(counter, online) {
        if (counter === 'watchers') {
            document.getElementById('online_watchers').innerText = online
        } else if (counter === 'players') {
            document.getElementById('online_players').innerText = online
        }
    }

    fill_themes(themes) {
        let theme_field
        let questions_row
        let questions
        let theme_blocs = document.querySelectorAll('.topic')
        let i = 0
        themes.forEach(theme => {
            theme_field = theme_blocs[i].querySelector('.topic-name')
            questions_row = theme_blocs[i].querySelector('.topic-points')
            questions = theme_blocs[i].querySelectorAll('.topic-point')
            theme_field.innerText = theme[0]
            questions_row.classList.add(`theme_${theme[1]}`)
            questions.forEach(question => {
                question.dataset.block_id = theme[1]
            })
            i++
        })
    }

    start_timer() {
        function render_timer() {
            let time = timerCycle(time_to_response * 1000)
            document.getElementById('timer').innerText = `${String(time.minutes).padStart(2, '0')}:${time.seconds}`
        }

        render_timer()
        let timer = setInterval(() => {
            render_timer()
        }, 1000)
    }

    toggle_question_btn(block_id, pos) {
        let row = document.querySelector(`.topic > .theme_${block_id}`)
        let btn = row.querySelectorAll('.topic-point')[pos - 1]

        let act = document.querySelector('.topic-point.act')
        if (act) {
            act.classList.remove('act')
            act.classList.add('disable')
        }
        btn.classList.add('act')
        btn.style.cursor = 'default'
    }

    render_question(question){
        console.log(question)
        this.toggle_question_btn(question.block_id, question.pos)

        let question_field = document.getElementById('question')
        let answer_fields = document.querySelectorAll('input.answer')

        for (let i = 0; i<answer_fields.length; i++){
            answer_fields[i].parentElement.querySelector('.text').innerText = question.answers[i]
        }
        question_field.innerText = question.question

    }

}