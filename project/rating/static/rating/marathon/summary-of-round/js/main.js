'use strict'

let ratings_data
let opened_table_name

function init() {
    let url = window.location.href
    sendRequest('get', url, 'get_data').then(data=>{
        ratings_data = data.marathon
        Render.init(ratings_data)
        EventListener.init()
        Render.tables(ratings_data)
    })
}

init()