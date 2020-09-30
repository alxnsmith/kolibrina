function init_points_in_total() {
    document.getElementById('points_in_total').innerText =
        parseInt(document.getElementById('points_per_game').innerText) + parseInt(document.getElementById('points_per_month').innerText)}
init_points_in_total()