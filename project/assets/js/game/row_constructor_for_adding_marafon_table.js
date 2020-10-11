class row_constructor_for_marafon_table {
    constructor() {
        this.table_row_count = 0
        this.table = document.getElementById('add_marafon_table')
    }

    add_row(theme_id, theme, category_id) {
        if (parseInt(theme_id) > -1 && this.table_row_count < 4) {
            this.table_row_count++
            let bg_color_class = 'tm_row'
            if (this.table_row_count % 2 === 1) {
                bg_color_class = 'sv_row'
            }
            this.table.innerHTML += `<tr class="${bg_color_class} theme_row" data-row-num="${this.table_row_count}" data-theme-id='${theme_id}' data-category-id='${category_id}' data-category-id='${category_id}'>\n            <td class="fc"><span><span class="close_btn"></span> ${theme}</span></td>\n            <td>\n                <table>\n                    <tr>\n                        <td>\n                            <div class="circle_btn" data-row-num="${this.table_row_count}" data-theme-id='${theme_id}' data-category-id='${category_id}' data-difficulty="10"><span>01</span></div>\n                        </td>\n                        <td>\n                            <div class="circle_btn" data-row-num="${this.table_row_count}" data-theme-id='${theme_id}' data-category-id='${category_id}' data-difficulty="10"><span>02</span></div>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n            <td class="vntr">\n                <table>\n                    <tr>\n                        <td>\n                            <div class="circle_btn" data-row-num="${this.table_row_count}" data-theme-id='${theme_id}' data-category-id='${category_id}' data-difficulty="20"><span>03</span></div>\n                        </td>\n                        <td>\n                            <div class="circle_btn" data-row-num="${this.table_row_count}" data-theme-id='${theme_id}' data-category-id='${category_id}' data-difficulty="20"><span>04</span></div>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n            <td class="vntr">\n                <table>\n                    <tr>\n                        <td>\n                            <div class="circle_btn" data-row-num="${this.table_row_count}" data-theme-id='${theme_id}' data-category-id='${category_id}' data-difficulty="30"><span>05</span></div>\n                        </td>\n                        <td>\n                            <div class="circle_btn" data-row-num="${this.table_row_count}" data-theme-id='${theme_id}' data-category-id='${category_id}' data-difficulty="30"><span>06</span></div>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n            <td class="vntr">\n                <table>\n                    <tr>\n                        <td>\n                            <div class="circle_btn" data-row-num="${this.table_row_count}" data-theme-id='${theme_id}' data-category-id='${category_id}' data-difficulty="40"><span>07</span></div>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n            <td class="vntr">\n                <table>\n                    <tr>\n                        <td>\n                            <div class="circle_btn" data-row-num="${this.table_row_count}" data-theme-id='${theme_id}' data-category-id='${category_id}' data-difficulty="50"><span>08</span></div>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n        </tr>`
            let all_rows = this.table.querySelectorAll('.theme_row')
            setTimeout(()=>{all_rows[all_rows.length - 1].style.transform = 'scaleY(1)'}, 100)
            setTimeout(()=>{all_rows[all_rows.length - 1].style.opacity = '1'}, 100)
        } else {
            return {'status': 'error', 'error': 'Выберите категорию, затем выберите тему, для добавления ее в таблицу.'}
        }
    }
    get_table_row_count(){
        return this.table_row_count
    }
}