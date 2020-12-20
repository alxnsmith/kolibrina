'use strict'
// String.prototype.repeat = function( num )
// {
//     return new Array( num + 1 ).join( this );
// }

class Render {
    static init(data) {
        let title = document.querySelector('.title > h2 > strong'),
            marathon_id = document.querySelector('.marafon-number'),
            page = document.querySelector('header nav a:nth-child(2) > span'),
            author_firstname = document.querySelector('.marafon_author-name .firstname'),
            author_lastname = document.querySelector('.marafon_author-name .lastname'),
            author_city = document.querySelector('.marafon_author-name .city')

        page.classList.add('select')
        title.innerText = `Марафон недели №${data.id}`
        marathon_id.innerText = data.id
        author_firstname.innerText = data.author.firstname
        author_lastname.innerText = data.author.lastname
        author_city.innerText = data.author.city
    }

    static tables(data) {
        let tables = {
            'common': {'data': data.ratings.common, 'html_id': '#common_rating'},
            'super': {'data': data.ratings.super, 'html_id': '#super_league'},
            'premier': {'data': data.ratings.premier, 'html_id': '#premier_league'},
            'highest': {'data': data.ratings.highest, 'html_id': '#highest_league'},
            'student': {'data': data.ratings.student, 'html_id': '#student_league'},
            'college': {'data': data.ratings.college, 'html_id': '#college_league'},
            'school': {'data': data.ratings.school, 'html_id': '#school_league'}
        }

        for (let table_name in tables) {
            let table = document.querySelector(tables[table_name].html_id + ' table')
            let table_html = this.get_table(data, table_name, [0, data.num_of_rounds-1], [0, 2]).html
            if (table_html.length > 0) {
                table.innerHTML = table_html
            }
        }
    }

    static purge_full_table(){
        let full_table = document.querySelector('.full-table')
        let content = full_table.querySelector('.full-table-container .content')
        content.innerHTML = ''
    }
    static hide_full_table(){
        let full_table = document.querySelector('.full-table')
        this.purge_full_table()
        full_table.classList.remove('show')
        setTimeout(()=>{full_table.style.display = 'none'}, 300)
    }
    static full_table(table_name, table_html, title){
        let full_table = document.querySelector('.full-table')
        let content = full_table.querySelector('.full-table-container .content')
        content.innerHTML+=`<table data-name="${table_name}"><caption><strong>${title}</strong></caption>${table_html}</table.>`
        full_table.style.display = 'block'
        setTimeout(()=>{full_table.classList.add('show')}, 0)
    }

    static get_table(data, table_name, rounds, range) {
        let table_html = ''
        let row_length = 0
        let row_html
        let empty_row;
        if (range) {
            empty_row = `<tr><td>_.</td><td>______ ____</td><td>_________</td>${Array(rounds[1]+2+1).join('<td>____</td>')}</tr>`;
        }
        let tables = {
            'common': data.ratings.common, 'super': data.ratings.super,
            'premier': data.ratings.premier, 'highest': data.ratings.highest,
            'student': data.ratings.student, 'college': data.ratings.college,
            'school': data.ratings.school
        }

        let header = this._rating_table_header(data.num_of_rounds)
        table_html += header

        tables[table_name].map((row, i) => {
            row_html = this._rating_table_row(i + 1, row.username, row.hide_name, row.lastname, row.firstname, row.city, row.score_rounds, row.sum)
            if (range) {
                table_html += range[0] <= i && i <= range[1] ? row_html : ''
                if (i < 2 && i + 1 === tables[table_name].length) {
                    table_html += Array(range[1]+1-i).join(empty_row)
                }
            } else {
                table_html += row_html
            }
            row_length++
        })
        if (!row_html && range){
            table_html+=Array(range[1]+2).join(empty_row)
        }
        return {html: table_html, row_length: row_length}
    }

    static _rating_table_header(num_of_rounds) {
        function get_rounds() {
            let rounds = ''
            for (let i = 0; i < num_of_rounds; i++) {
                rounds += `<th>${i + 1} Тур</th>`
            }
            return rounds
        }

        return `<tr><th>п/п</th><th>ФИО</th><th>Город</th>${get_rounds()}<th>&#8721;</th></tr>`
    }

    static _rating_table_row(num, username, hide_name, lastname, firstname, city, scores, sum) {
        let new_scores = [...scores]
        new_scores.push(sum)
        new_scores = new_scores.map(score => {
            return `<td>${score ? score : 0}</td>`
        }).join('')
        return `<tr><td>${num}.</td><td>${upFirst(username)} ${!hide_name ? upFirst(lastname) : ''}` +
            ` ${!hide_name ? upFirst(firstname) : ''}</td><td>${!hide_name ? 'г. ' + city : '_________'}</td>${new_scores}</tr>`
    }


}