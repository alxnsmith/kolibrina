let team_info
let current_user_info

function init(){
    get_team_info().then(r  =>{
        if (r){
            team_info = r
            current_user_info = get_info_about_current_user()
            select_number_in_the_team()
            init_invite_list()
        }
    })
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

function select_number_in_the_team() {
    let num = current_user_info.number_in_the_team
    let id = 'num' + num
    document.getElementById(id).checked = true
}

function get_team_info(){
    let request_url = window.location.origin + '/api/team/'
    request_url+= `?event=get_team_info&team=${get_team()}`
    return sendRequest('get', request_url)
}

function del_teammate (teammate) {
    alert(teammate)
}

function get_team(){
    return  document.getElementById('team').defaultValue
}

function get_current_user(){
    return document.getElementById('username').defaultValue
}

function get_info_about_current_user(){
    function f(player) {
        if (get_current_user() === player.username){
            return player
        }}
    return team_info.players.filter(f)[0]
}
function add_teammate(teammate){
    let value = teammate.parentElement.querySelector('input').value
    alert(_get_userID_from_datalist_option_value(value))
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
    datalist_container = datalist[0].parentElement
    datalist_container.innerHTML = ''
    for (let i = 0; i < new_datalist.length; i++) {
        datalist_container.innerHTML += `<option value="${new_datalist[i]}"></option>`
    }
}

init()