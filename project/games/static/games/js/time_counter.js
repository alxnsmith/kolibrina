class TimeCounter {
    constructor(end_time) {
        this.end_time = Date.parse(end_time)/1000
    }

    delta_time() {
        let now = Date.parse(Date()) / 1000
        return Math.floor(this.end_time - now)
    }

    get delta(){
        return this.delta_time(this.end_time)
    }

    left_days_time() {
        let days = Math.floor(this.delta / 86400)
        let hours = Math.floor(this.delta / 360 % 24)
        let minutes = Math.floor(this.delta / 60 % 60)
        let seconds = Math.ceil(this.delta % 60)
        return {'days': days, 'hours': hours, 'minutes': minutes, 'seconds': seconds, 'delta': this.delta}
    }

    left_hours_time() {
        let hours = Math.floor(this.delta / 360)
        let minutes = Math.floor(this.delta / 60 % 60)
        let seconds = Math.ceil(this.delta % 60)
        return {'hours': hours, 'minutes': minutes, 'seconds': seconds, 'delta': this.delta}
    }

    left_minutes_time() {
        let minutes = Math.floor(this.delta / 60)
        let seconds = Math.ceil(this.delta % 60)
        return {'minutes': minutes, 'seconds': seconds, 'delta': this.delta}
    }
}
