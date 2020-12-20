"use strict"

class Render{
    static show_pay_status_notification(pay_status) {
        switch (pay_status) {
            case true:
                show_modal_notification('Готово!')
                break;
            case 'The user is already player':
                show_modal_notification('Вы уже зарегистрированы.')
                break;
            case 'Time is out':
                show_modal_notification('Игра уже началась!')
                break;
            case 'Not enough money':
                show_modal_notification('Не достаточно денег. Пополните баланс.')
                break;
            case 'Unsuitable currency':
                show_modal_notification('Error: Unsuitable currency')
                break;
        }
    }
}