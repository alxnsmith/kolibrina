class rating_top_fifteen {
    constructor() {
        this.rows = document.querySelectorAll('.rating-place')
    }

    write_row(user_dict) {
        this.row = this.rows[user_dict.pos]
        this._write_score(user_dict.score)
        this._write_score_delta(user_dict.score_delta)
        this._score_display('block')

        if (user_dict.hide_name) {
            this._write_username(user_dict.username)
        } else {
            this._write_first_name(user_dict.first_name)
            this._write_last_name(user_dict.last_name)
            this._write_city(user_dict.city)
        }
    }

    erase_row(row) {
        this.row = row
        this._write_score('0')
        this._write_score_delta('0')
        this._score_display('none')
        this._write_username('')
        this._write_first_name('')
        this._write_last_name('')
        this._write_city('')
    }

    _write_username(username) {
        this.row.querySelector('.username').innerHTML = username;
    }

    _write_score(score) {
        this.row.querySelector('.rt-points .score').innerHTML = score
    }

    _write_score_delta(score_delta) {
        this.row.querySelector('.rt-points .score_delta').innerHTML = score_delta
    }

    _write_first_name(first_name) {
        this.row.querySelector('.first_name').innerHTML = first_name
    }

    _write_last_name(last_name) {
        this.row.querySelector('.last_name').innerHTML = last_name
    }

    _write_city(city) {
        this.row.querySelector('.city').innerHTML = city
    }

    _score_display(display) {
        this.row.querySelector('.rt-points').style.display = display
    }
}
