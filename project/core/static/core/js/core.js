'use strict'

function first_init() {
    function init_backgrounds() {
        let elements = document.querySelectorAll('[data-bg]')
        elements.forEach(e => {
            if (!e.getAttribute('data-bg-webp') || !canUseWebp()) {
                e.style.backgroundImage = `url(${e.getAttribute('data-bg')})`
                console.warn('Your browser is not supported WEBP images, loaded JPEG.\n', e)
            }
        })
    }
    function init_online_counter(){
        const onlineSocket = new WebSocket(
            `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://`+ window.location.host + '/ws/online/'
        );
        onlineSocket.onmessage = e => {
            let data = JSON.parse(e.data)
            if (data.type === 'online') {
                document.querySelector('#online span').textContent = data.online
            }
        }
        onlineSocket.onclose = e => {
            console.error('Online socket closed unexpectedly.', e);
        };
    }

    init_backgrounds()
    init_online_counter()
}

window.addEventListener('load', e => {
    first_init()
})

function show_modal_notification(value, classes = undefined, mode = 'text') {
    let notification = document.getElementById('modal_notification')
    if (classes) {
        notification.classList.add(...classes)
    }
    if (!value) {
        value = 'Что-то пошло не так...'
    }
    if (mode === 'text') {
        notification.innerText = value
    } else if (mode === 'html') {
        notification.innerHTML = value
    }
    notification.style.opacity = '1'
    notification.style.top = '1vh'
    setTimeout(() => {
        notification.style.opacity = ''
        notification.style.top = ''
        notification.className = ''
    }, 5000)
}

function show_error(text, mode) {
    show_modal_notification(text, ['border-danger', 'alert-danger'], mode)
}

function show_success(text, mode) {
    show_modal_notification(text, ['border-success', 'alert-success'], mode)
}

function canUseWebp() {
    let elem = document.createElement('canvas');
    let is_firefox = window.navigator.userAgent.match(/Firefox\/([0-9]+)\./);
    let firefox_ver = is_firefox ? parseInt(is_firefox[1]) : 0;
    if (!!(elem.getContext && elem.getContext('2d'))) {
        return elem.toDataURL('image/webp').indexOf('data:image/webp') === 0 || firefox_ver >= 65;
    }
    return false;
}

