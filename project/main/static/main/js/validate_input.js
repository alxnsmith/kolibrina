function validate_password_inputs(querySelector1, querySelector2) {
    let input1 = document.querySelector(querySelector1)
    let input2 = document.querySelector(querySelector2)
    let equals
    function input_handler(e) {
        input1 = document.querySelector(querySelector1)
        input2 = document.querySelector(querySelector2)
        if (input1.value === '') {return;}
        if (input1.value.length >= input2.value.length) {
            equals = input1.value.slice(0, input2.value.length) === input2.value
        } else {
            equals = false
        }
        let left_block1 = input1.parentElement.querySelector('.input-group-text')
        let left_block2 = input2.parentElement.querySelector('.input-group-text')
        let inp1 = input1.parentElement.querySelector('.string')
        let inp2 = input2.parentElement.querySelector('.string')
        if (!equals){
            left_block1.style.borderTop = left_block2.style.borderTop = 'red 1px solid'
            left_block1.style.borderLeft = left_block2.style.borderLeft = 'red 1px solid'
            left_block1.style.borderBottom = left_block2.style.borderBottom = 'red 1px solid'
            inp1.style.borderTop = inp2.style.borderTop = 'red 1px solid'
            inp1.style.borderRight = inp2.style.borderRight = 'red 1px solid'
            inp1.style.borderBottom = inp2.style.borderBottom = 'red 1px solid'
        }else{
            left_block1.style.border = left_block2.style.border = ''
            inp1.style.border = inp2.style.border = ''
        }
    }
    input2.addEventListener('input', input_handler)
    input1.addEventListener('input', input_handler)
}
function validate_input(querySelector) {
    let input = document.querySelector(querySelector)
    let last_value = ''
    let showing_alert = false

    function reset_input_value_to(input, str) {
        input.value = str
        showing_alert = false
    }

    function input_handler(e) {
        input = document.querySelector(querySelector)
        if (input.value === '') {
            last_value = input.value;
            return;
        }
        if (!input.reportValidity() && !showing_alert) {
            setTimeout(() => reset_input_value_to(input, last_value.toString()), 6000);
            showing_alert = true;
            return;
        }
        if (input.checkValidity() && showing_alert) clearTimeout(reset_input_value_to);
        showing_alert = false;
        if (input.reportValidity() && !showing_alert) last_value = input.value;
    }

    input.addEventListener('input', input_handler)
}