function validate_password_inputs(querySelector1, querySelector2) {
    let input1 = document.querySelector(querySelector1);
    let input2 = document.querySelector(querySelector2);
    let equals;

    function input_handler() {
        input1 = document.querySelector(querySelector1);
        input2 = document.querySelector(querySelector2);
        if (input1.value === '') return;
        if (input1.value.length >= input2.value.length) {
            equals = input1.value.slice(0, input2.value.length) === input2.value;
        } else equals = false;
        let left_block1 = input1.parentElement.querySelector('.input-group-text');
        let left_block2 = input2.parentElement.querySelector('.input-group-text');
        let inp1 = input1.parentElement.querySelector('.string');
        let inp2 = input2.parentElement.querySelector('.string');
        if (!equals) {
            let border_style = 'red 1px solid';
            left_block1.style.borderTop = left_block2.style.borderTop = border_style;
            left_block1.style.borderLeft = left_block2.style.borderLeft = border_style;
            left_block1.style.borderBottom = left_block2.style.borderBottom = border_style;
            inp1.style.borderTop = inp2.style.borderTop = border_style;
            inp1.style.borderRight = inp2.style.borderRight = border_style;
            inp1.style.borderBottom = inp2.style.borderBottom = border_style;
        } else {
            left_block1.style.border = left_block2.style.border = '';
            inp1.style.border = inp2.style.border = '';
        }
    }

    input2.addEventListener('input', input_handler);
    input1.addEventListener('input', input_handler);
}
