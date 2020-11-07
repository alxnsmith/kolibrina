$(document).ready(function() {
	$("a.open-modal").click(function() {
		var idModal = $(this).attr("href");
		$(idModal).css("display", "block");
	});
	$("a.close").click(function() {
		$(".modal").css("display", "none");
	});
});