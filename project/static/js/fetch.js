function sendRequest(method, requestURL, body=null, headers_addition=null) {
    let headers = {
        'Content-Type': 'application/json',
        ...headers_addition
    }

    if (body){
        if (method.toLowerCase() === 'get') {
            let query = '?'
            if (typeof body === 'object') {
                let i = 0
                for (let item in body) {
                    query += (i > 0 ? '&' : '') + item + '=' + body[item]
                    i++
                }
            } else if (typeof body === 'string'){
                query+=body
            }

            body = null
            requestURL+=query
        } else if (!(body instanceof FormData)){
            body = JSON.stringify(body)
        }
    }
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
