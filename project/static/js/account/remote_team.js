let team_info
let current_user_info

function init_team(){
    let team = get_team()
    if (team !== '') {
        get_team_info(team).then(r => {
            if (r) {
                _get_num_from_select()
                _get_role_from_select()
                team_info = r
                current_user_info = get_info_about_current_user()
                set_checked_number_in_the_team()
                init_invite_list()
                _init_nums(team_info)
                if (current_user_info.team_role){
                    _show_nums()
                }

            }
        })
    }else {
        _check_invite_list_and_set_button()
    }
}

function init_invite_list(){
    let players = team_info.players
    let players_id = []
    let datalist = document.getElementById('users').querySelectorAll('option')
    let invite_list_user_id = []
    let invite_list_user_object_name = []
    for (let i=0; i<datalist.length; i++){
        invite_list_user_id.push(Number(_get_userID_from_datalist_option_value(datalist[i].value)))
        invite_list_user_object_name.push(datalist[i].value)
    }
    for (let i=0; i<players.length; i++) {
        players_id.push(Number(players[i].id))
    }
    let subtract = subtract_filter(invite_list_user_id, players_id);
    let new_datalist = invite_list_user_object_name.filter(item => endswith_filter(item, subtract))
    replace_datalist(datalist, new_datalist)
}


function set_checked_number_in_the_team() {
    let num = current_user_info['number_in_the_team']
    if (num) {
        let id = 'num' + num
        document.getElementById(id).checked = true
    }
}


function _get_num_from_select(){
    let nums = document.querySelectorAll('.nums')[1]
    nums.onclick = event => {
        let target = event.target
        if (target.classList.contains('num')){
            set_number_in_the_team(target)
        }
    }
}


function set_number_in_the_team(element) {
    let number = element.value
    let popup_notification = element.parentElement.querySelector('span')
    let notification_style = popup_notification.style
    notification_style.display = 'block'
    let request_url = window.location.origin + '/api/team/'
    let data = {
        'event': 'set_number_in_the_team',
        'number': number,
    }
    sendRequest('put', request_url, data).then(r =>{
        if (r.status === 'Error! Need "number"'){
            _error_red_and_text_popup('Номер занят', popup_notification, '-60%')
            setTimeout(()=>{window.location.reload()}, 1400)
        }
    _smooth_show_and_hide_popup(popup_notification)
    }).catch(()=> {
        _error_red_and_text_popup('Ошибка соединения', popup_notification)
        _smooth_show_and_hide_popup(popup_notification)
    })

}


function _get_role_from_select(){
    let user_roles = document.querySelector('.roles')
    let teammate_roles = document.querySelectorAll('.teammate_roles')
    user_roles.onclick = event=>_call_select_team_role(event)
    for (let i=0; i<teammate_roles.length; i++) {
        teammate_roles[i].onclick = event => _call_select_team_role(event)
    }
    function _call_select_team_role(event){
        let target = event.target
        let input = target.querySelector('input')
        if (target.classList.contains('role') && !input.disabled && !input.checked){
            select_team_role(input.value, target)
        }
        if (target.classList.contains('teammate_role') && !input.disabled && !input.checked){
            let teammate_username = event.target.parentElement.parentElement.parentElement.querySelector('.teammate_username').value
            select_team_role(input.value, target, teammate_username)
        }
    }
}


function select_team_role(role, element, username=null){
    let popup_notification = element.parentElement.querySelector('span')
    let element_style = popup_notification.style
    element_style.display = 'block'
    let request_url = window.location.origin + '/api/team/'
    let data
    if (!username){
        data = {
            'event': 'set_team_role',
            'role': role,
        }
    }   else {
        data = {
            'event': 'set_team_role',
            'role': role,
            'username': username
            }
    }
    sendRequest('put', request_url, data).then(r =>{
        if (r.status === 'error'){
            let error_text
            if (r.error === 'There many to Legionaries'){
                error_text = 'Слишком много Легионеров!'
                _error_red_and_text_popup(error_text, popup_notification, '0%', '120px', '80%')
            }else if (r.error === 'There many to Basics'){
                error_text = 'Слишком много Базовых!'
                _error_red_and_text_popup(error_text, popup_notification, '0', '120px', '80%')
            }else if (r.error === 'Commander place is not empty!'){
                error_text = 'Это место занято!'
                _error_red_and_text_popup(error_text, popup_notification, '0', '120px', '80%')
            }

        setTimeout(()=>{window.location.reload()}, 1400)
        } else {_show_nums()}

        _smooth_show_and_hide_popup(popup_notification, '30%')


    }).catch(()=> {
        _error_red_and_text_popup('Ошибка соединения', popup_notification)
        _smooth_show_and_hide_popup(popup_notification)
    })

}


function get_team_info(team){
    let request_url = window.location.origin + '/api/team/'
    request_url+= `?event=get_team_info&team=${team}`
    return sendRequest('get', request_url)
}

function del_teammate (teammate, elem) {
    let teammate_block = elem.parentElement
    let request_url = window.location.origin + '/api/team/'
    let data = {
        'event': 'delete_player_from_team',
        'player': teammate
    }
    return sendRequest('delete', request_url, data).then(r=>{
        if (r.status === 'OK'){
            teammate_block.remove()
        }else if (r.status === 'error') {
            console.error(r.error)
            show_modal_notification()
        }
    })
}

function del_team (){
    let request_url = window.location.origin + '/api/team/'
    let data = {
        'event': 'delete_team',
    }
    return sendRequest('delete', request_url, data).then(r=>{
        if (r.status === 'OK'){
            window.location.reload()
        } else {
            console.error(r.error)
        }
    })
}

function get_team(){
    let input = document.getElementById('team')
    input.defaultValue = input.defaultValue.trim()
    return input.defaultValue
}

function get_current_user(){
    return document.getElementById('username').defaultValue
}

function get_info_about_current_user(){
    function f(player) {
        if (get_current_user() === player.username){
            return player
        }
    }
    return team_info.players.filter(f)[0]
}

function add_player_to_invite_list(add_player_button){
    let input = add_player_button.parentElement.querySelector('input')
    if (input.value) {
        let player_id = _get_userID_from_datalist_option_value(input.value)
        let request_url = window.location.origin + '/api/team/'
        let data = {
            'event': 'add_player_to_invite_list',
            'player_id': player_id,
        }
        sendRequest('post', request_url, data).then(r => {

            if (r.status === 'OK') {
                input.style.backgroundColor = '#5f5'
            } else {
                input.style.backgroundColor = '#f55'
                alert('Игрок уже приглашен!')
            }
            setTimeout(() => {
                input.style.backgroundColor = '#fff'
            }, 2000)
            let length = input.value.length
            let cleaner = setInterval(() => {
                input.value = input.value.slice(0, length--)
                if (length < 0) {
                    clearInterval(cleaner)
                }
            }, 10)
        })
    }
}

function _get_userID_from_datalist_option_value(value){
    let count = 0
    let id
    if (value.includes(' | ')) {
        id = value.split(' | ')[1]
    }
    for (let i = 0; i <= 7; i++) {
        if (id[i] === '0'){
            count++
        }else{break}
    }
    return id.slice(count-7)
}

function subtract_filter(array1, array2){
    return array1.filter(x => !array2.includes(Number(x)))
}

function endswith_filter(value, ends){
    for (let i=0; i<ends.length; i++){
        if (value.endsWith(ends[i])){
            return value
        }
    }
}

function replace_datalist(datalist, new_datalist){
    let datalist_container = datalist[0].parentElement
    datalist_container.innerHTML = ''
    for (let i = 0; i < new_datalist.length; i++) {
        datalist_container.innerHTML += `<option value="${new_datalist[i]}"></option>`
    }
}

function _check_invite_list_and_set_button(){
    let invites = []
    let input = document.getElementById('team')
    let btn = document.getElementById('add_team')
        options = input.parentElement.querySelectorAll('option')
    if (options.length > 0) {
        for (let i=0; i<options.length; i++){
            invites.push(options[i].value)
        }
    }
    input.oninput = () => {
        if (invites.indexOf(input.value) !== -1) {
            btn.innerText = "Вступить в команду"
            btn.onclick = ()=>{
                join_to_team(input.value)
            }
        }else{
            btn.innerText = "Добавить команду"
            btn.onclick = ()=>{
                create_team(input.value)
            }
        }
    }
}

function join_to_team(team){
    let request_url = window.location.origin + '/api/team/'
    let data = {
        'event': 'join_to_team',
        'name': team
    }
    return sendRequest('put', request_url, data).then(r=> {
        if (r.status === 'OK') {
            window.location.reload()
        }else {console.error(r.error)}
    })
}

function create_team(team){
    let request_url = window.location.origin + '/api/team/'
    let data = {
        'event': 'create_team',
        'name': team
    }
    return sendRequest('post', request_url, data).then(r=> {
        if (r.status === 'OK') {
            window.location.reload()
        }else {
            console.error(r.error)
            if (r.error === 'This name of command exists!'){
                show_modal_notification('Название команды уже занято, попробуйте другое.')
            } else {
                show_modal_notification()
            }
        }
    })
}

function leave_from_team(){
    let request_url = window.location.origin + '/api/team/'
    let data = {
        'event': 'leave_from_team',
    }
    return sendRequest('put', request_url, data).then(r=> {
        window.location.reload()
    })
}

function _error_red_and_text_popup(text,
                                   element,
                                   left='-50%',
                                   min_width='100px',
                                   triangle_top = '70%',
                                   triangle_left = '45%',){
    let triangle_color = 'rgba(255, 0, 0, 0.8) transparent transparent transparent'
    element.innerHTML = `${text}<span></span>`
    let triangle = element.querySelector('span')
    let triangle_style = triangle.style
    let element_style = element.style
    element_style['backgroundColor'] = 'rgba(255, 0, 0, 0.8)'
    element_style['min-width'] = min_width
    element_style['left'] = left
    triangle_style.borderColor = triangle_color
    triangle_style.left = triangle_left
    triangle_style.top = triangle_top
    setTimeout(()=>{
        element_style['backgroundColor'] = ''
        element_style['min-width'] = ''
        element_style['left'] = ''
        element.innerHTML = 'Готово<span></span>'
    },2000)

}

function _smooth_show_and_hide_popup(element, left){
    let element_style = element.style
    element_style['opacity'] = '1'
    if (!element_style['left']) {
        element_style['left'] = left
    }
        setTimeout(()=>{element_style['opacity'] = ''},1000)
        setTimeout(()=>{element_style.display = ''},2000)
}

function _init_nums(team_info){
    for (let i=0; i<team_info.players.length; i++) {
        let num = team_info.players[i].number_in_the_team
        if (num) {
            let elem = document.querySelector(`#num${num}`)
            if (!elem.checked) {
                elem.disabled = true
            }
        }
    }
}

function _show_nums(){
    let nums = document.querySelectorAll('.nums')
    for (let i=0; i<nums.length; i++){
        nums[i].style.display = ''
        setTimeout(()=>{nums[i].style.opacity = '1'}, 100)
    }
}
init_team()