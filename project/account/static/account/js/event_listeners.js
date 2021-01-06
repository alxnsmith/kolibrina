"use strict"

class EventListener{
    static rm_listener_reg_btn(target){
        target.removeEventListener('click', Services.reg_btn_click)
    }
    static listen_reg_btn(){
        let btns = document.querySelectorAll('.reg_btn')
        btns.forEach(btn=>{btn.addEventListener('click', Services.reg_btn_click)})
    }
}