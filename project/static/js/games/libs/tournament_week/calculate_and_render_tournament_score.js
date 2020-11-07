function init_points_in_total() {
    document.getElementById('points_in_total').innerText =
        `${Math.round((
            parseFloat(document.querySelector('#points_per_game span').innerText.replace(',', '.'))
                + parseFloat(document.getElementById('points_per_month').innerText.replace(',', '.')
            )
        )*1000)/1000}`.replace('.', ',')
}

init_points_in_total()