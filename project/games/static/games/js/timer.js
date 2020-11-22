'use strict'
// time counter required

class Timer {
    constructor(unix_time_end, bit, renderer, task, argument) {
        this.counter = new TimeCounter(unix_time_end)
        this.bit = bit
        this.renderer = renderer
        this.task = task
        this.argument = argument
    }

    render_time(time) {
        if (this.bit === 'seconds') {
            time = time === undefined ? this.counter.delta : time
            this.renderer(time)
        } else if (this.bit === 'minutes') {
            time = time === undefined ? this.counter.left_minutes_time() : time
            this.renderer(time.minutes, time.seconds)
        } else if (this.bit === 'hours') {
            time = time === undefined ? this.counter.left_hours_time() : time
            this.renderer(time.hours, time.minutes, time.seconds)
        } else {
            time = time === undefined ? this.counter.left_days_time() : time
            this.renderer(time.days, time.minutes, time.seconds)
        }
        return time.delta
    }

    start() {
        this.render_time()
        this.timer = setInterval(()=>{
            let delta = this.render_time()
            if (delta < 1) {
                this.stop()
                if (this.task !== undefined) {
                    this.task(this.argument !== undefined ? this.argument : void(0) )
                }
            }
        }, 1000)
    }

    stop(){
        clearInterval(this.timer)
    }
    reset(){
        this.stop()
        this.render_time({'minutes': 0, 'seconds': 0})
    }
}