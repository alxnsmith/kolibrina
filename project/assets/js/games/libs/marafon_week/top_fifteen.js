class rating_top_fifteen {
    constructor() {
        this.rows = document.querySelectorAll('.rating-place')
    }

    write_username(username) {
        this.row.querySelector('.username').innerHTML = username;
    }

    write_score(score) {
        this.row.querySelector('.rt-points .score').innerHTML = score
    }

    write_score_delta(score_delta) {
        this.row.querySelector('.rt-points .score_delta').innerHTML = score_delta
    }

    write_first_name(first_name) {
        this.row.querySelector('.first_name').innerHTML = first_name
    }

    write_last_name(last_name) {
        this.row.querySelector('.last_name').innerHTML = last_name
    }

    write_city(city) {
        this.row.querySelector('.city').innerHTML = city
    }

    score_display(display) {
        this.row.querySelector('.rt-points').style.display = display
    }

    write_row(user_dict) {
        this.row = this.rows[user_dict.pos]
        this.write_score(user_dict.score)
        this.write_score_delta(user_dict.score_delta)
        this.score_display('block')

        if (user_dict.hide_name) {
            this.write_username(user_dict.username)
        } else {
            this.write_first_name(user_dict.first_name)
            this.write_last_name(user_dict.last_name)
            this.write_city(user_dict.city)
        }
    }

    erase_row(row) {
        this.row = row
        this.write_score('0')
        this.write_score_delta('0')
        this.score_display('none')
        this.write_username('')
        this.write_first_name('')
        this.write_last_name('')
        this.write_city('')
    }
}
