'use strict'

class EventListener{
    static init(){
        this._add_listen_show_all_btn()
        this._add_listen_close_full_table()
        this._add_listen_window_btn_full_table()
        this._add_listen_print_btn_full_table()
    }
    static _add_listen_show_all_btn(){
        let btn_list = document.querySelectorAll('.show-all-btn')
        btn_list.forEach(btn=>{
            btn.addEventListener('click', Services.show_all_btn_click_event)
        })
    }
    static _add_listen_close_full_table(){
        let btn = document.querySelector('.full-table-container .close')
        btn.addEventListener('click', Services.hide_full_table_event)
    }
    static _add_listen_window_btn_full_table(){
        let btn = document.querySelector('.full-table-container .window')
        btn.addEventListener('click', Services.open_table_in_new_window)
    }
    static _add_listen_print_btn_full_table(){
        let btn = document.querySelector('.full-table-container .print')
        btn.addEventListener('click', Services.print_table)
    }
}
