class Render{
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
        let questions
        let theme_blocs = document.querySelectorAll('.topic')
        let i = 0
        themes.forEach(theme => {
            theme_field = theme_blocs[i].querySelector('.topic-name')
            questions = theme_blocs[i].querySelectorAll('.topic-point')
            theme_field.innerText = theme[0]
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
}