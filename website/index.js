window.onload = function() { 
    input = document.getElementById("input");
	input.onkeyup = function(e) {
		if (e.key === " ") {
			predict();
		}
	}
};

function predict() {
	input = document.getElementById("input").innerHTML;
	send_request(input);
}

function send_request(input) {
	$.ajax({
		type: "POST",
		url: "http://127.0.0.1:5000/test/api",
		datatype: 'json',
		data: {
			'input': input
		},
		success: function(response) {
			// primitives only pass by value in js
			// message = input.textContent + '<span class="unselectable">' + response.value + '</span>';
			// document.getElementById("input").innerHTML = message;
			document.getElementById("sugg0").innerHTML = response.value;
			document.getElementById("sugg1").innerHTML = response.value;
			document.getElementById("sugg2").innerHTML = response.value;
			console.log(response);
		},
		error: function(response) {
			console.log(response);
		}
	})
}