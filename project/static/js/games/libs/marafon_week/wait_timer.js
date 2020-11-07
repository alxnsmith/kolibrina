function start_timer(date_start, func) {
    let days_block = document.getElementById('days')
    let hours_block = document.getElementById('hours')
    let minutes_block = document.getElementById('minutes')
    let seconds_block = document.getElementById('seconds')

    let time_counter = new TimeCounter(date_start)

    function render_timer() {
        let time = time_counter.left_time()

        days_block.innerText = time.days
        hours_block.innerText = time.hours
        minutes_block.innerText = time.minutes
        seconds_block.innerText = time.seconds
    }

    render_timer()
    let waitToStart = setInterval(() => {
        render_timer()
        if (time_counter.delta_time() < 1) {
            clearInterval(waitToStart)
            let wait_block = document.querySelector('.wait_block')
            wait_block.style.opacity = '0'
            setTimeout(() => {
                wait_block.remove()
            }, 400)
            func()
        }
    }, 1000)
}
