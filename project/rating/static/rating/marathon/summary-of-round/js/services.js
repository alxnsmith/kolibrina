'use strict'
class Services{
    static show_all_btn_click_event(e){
        let table_name = e.target.parentElement.id
            .replace('_league', '')
            .replace('_rating', '')
        let table_title = e.target.parentElement.querySelector('strong').innerText
        let table_html = Render.get_table(ratings_data, table_name)
        if (table_html.row_length > 0) {
            Render.full_table(table_name, table_html.html, table_title)
        } else {
            show_modal_notification('Таблица пуста!')
        }
    }

    static hide_full_table_event(e){
        Render.hide_full_table()
    }

    static open_table_in_new_window(e){
        let width = 1000
        let height = 500
        let win = window.open(
            "",
            "Title",
            `toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=${width},height=${height},left=${(screen.width / 2) - (width / 2)},top=${(screen.height / 2) - (height / 2)}`
        )
        let html = ''
        let table_html = e.target.parentElement.querySelector('table').outerHTML
        let style = `table{display:block;max-width:fit-content;min-width:max-content;overflow:auto;margin:auto;border-collapse: collapse;}caption{margin: 10px 0;min-width: max-content;}table td, th{border: black dashed 1px;padding: 5px 10px}`

        html += `<style>${style}</style>` + table_html
        win.document.body.innerHTML = html
        return win
    }
    static print_table(e){
        let win = Services.open_table_in_new_window(e)
        win.print()
        win.close()
    }
}