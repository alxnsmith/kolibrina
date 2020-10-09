class row_constructor_for_marafon_table {
    constructor() {
        self.table_row_count = 0
        self.table = document.getElementById('add_marafon_table')
    }

    add_row(theme_id, theme) {
        if (theme_id && self.table_row_count < 4) {
            self.table_row_count++
            let bg_color_class = 'tm_row'
            if (self.table_row_count % 2 === 1) {
                bg_color_class = 'sv_row'
            }
            self.table.innerHTML += `<tr class="${bg_color_class} theme_row" data-theme-id='${theme_id}'>\n            <td class="fc"><span><span class="close_btn"></span> ${theme}</span></td>\n            <td>\n                <table>\n                    <tr>\n                        <td>\n                            <div class="circle_btn"><span>01</span></div>\n                        </td>\n                        <td>\n                            <div class="circle_btn"><span>02</span></div>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n            <td class="vntr">\n                <table>\n                    <tr>\n                        <td>\n                            <div class="circle_btn"><span>03</span></div>\n                        </td>\n                        <td>\n                            <div class="circle_btn"><span>04</span></div>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n            <td class="vntr">\n                <table>\n                    <tr>\n                        <td>\n                            <div class="circle_btn"><span>05</span></div>\n                        </td>\n                        <td>\n                            <div class="circle_btn"><span>06</span></div>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n            <td class="vntr">\n                <table>\n                    <tr>\n                        <td>\n                            <div class="circle_btn"><span>07</span></div>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n            <td class="vntr">\n                <table>\n                    <tr>\n                        <td>\n                            <div class="circle_btn"><span>08</span></div>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n        </tr>`
            let all_rows = self.table.querySelectorAll('.theme_row')
            setTimeout(()=>{all_rows[all_rows.length - 1].style.transform = 'scaleY(1)'}, 100)
            setTimeout(()=>{all_rows[all_rows.length - 1].style.opacity = '1'}, 100)
        } else {
            return {'status': 'error', 'error': 'Выберите категорию, затем выберите тему, для добавления ее в таблицу.'}
        }
    }
    get_table_row_count(){
        return self.table_row_count
    }
}