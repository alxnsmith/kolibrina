document.addEventListener('load', ()=>{
	document.querySelector("a.open-modal").click((e)=>{
		let idModal = e.target.getAttribute("href");
		document.querySelector(idModal).style.display = "block";
	});
	document.querySelector("a.close").click(function() {
		document.querySelector(".modal").style.display = 'none';
	});
});