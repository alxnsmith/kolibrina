class timer {
    constructor(time, element, socket) {
        self.duration = time
        self.elem_timer = element
        self.socket = socket
        this.rearm_timer()
    }
    minutes() {
        return `${Math.floor(self.time / 60)}`.padStart(2, '0')
    }
    seconds() {
        return `${self.time % 60}`.padStart(2, '0')
    }
    timer_value() {
        return `${this.minutes()}:${this.seconds()}`
    }
    rearm_timer() {
        self.time = self.duration
        self.elem_timer.innerText = this.timer_value()
    }
    stop() {
        clearInterval(self.timer)
    }
    start() {
        self.timer = setInterval(() => {
            if (self.time > 0) {
                self.time--
                self.elem_timer.innerText = this.timer_value()
            } else {
                clearInterval(self.timer)
                self.socket.send(JSON.stringify({
                    'event': 'respond',
                    'answer': null
                }))
            }
        }, 1000)
    }
}