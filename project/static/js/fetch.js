function sendRequest(method, requestURL, body=null) {
    const headers = {
        'Content-Type': 'application/json'
    }
    if (body){ body = JSON.stringify(body)}
    return fetch(requestURL, {
        method: method,
        body: body,
        headers: headers
    }).then(response => {
        if (response.ok){
            return response.json()
        }
        return response.json().then(error => {
            const err = new Error('Что-то пошло не так...')
            err.data = error
            throw err
        })
    })
}
