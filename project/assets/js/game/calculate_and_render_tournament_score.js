function init_points_in_total() {
    document.getElementById('points_in_total').innerText =
        parseFloat(document.querySelector('#points_per_game span').innerText) + parseFloat(document.getElementById('points_per_month').innerText)}
init_points_in_total()