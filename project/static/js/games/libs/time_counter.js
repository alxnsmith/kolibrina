class TimeCounter {
    constructor(end_time) {
        this.end_time = end_time
    }

    delta_time() {
        let now = Date.parse(Date())
        return Math.floor((this.end_time - now) / 1000)
    }

    left_time() {
        let delta = this.delta_time(this.end_time)

        let days = Math.floor(delta / 86400)
        let hours = Math.floor(delta / 360 % 24)
        let minutes = Math.floor(delta / 60 % 60)
        let seconds = Math.ceil(delta % 60)
        return {'days': days, 'hours': hours, 'minutes': minutes, 'seconds': seconds, 'delta': delta}
    }
}
