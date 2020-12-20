"use strict"

class Services {
    static reg_btn_click(e) {
        let target = e.target;
        function check_status_exist() {
            if (target.classList.contains('is_player')) target.dataset.cached_pay_status = 'The user is already player';
            let cached_pay_status = target.dataset.cached_pay_status;
            if (cached_pay_status) {
                Render.show_pay_status_notification(cached_pay_status);
                return false
            }
            return true
        }

        if (!check_status_exist()){return}


        let request_url = window.location.origin + target.dataset.url;
        let csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        let header_addition = {"X-CSRFToken": csrftoken};
        let body = {
            'codename': target.dataset.codename,
            'pk': target.dataset.pk
        };
        sendRequest('post', request_url, body, header_addition).then(e => {
            target.dataset.cached_pay_status = e.pay_status;
            Render.show_pay_status_notification(e.pay_status);
            if (e.pay_status === true){
                target.classList.add('is_player')
                update_balance()
            }
        });

    }
}
