/*
	@brief: set up listener for key events
			" " -> updates the suggestions
			"1" -> choose 1st suggestion
			"2" -> choose 2nd suggestion
			"3" -> choose 3rd suggestion
*/
window.onload = function() { 
    input = document.getElementById("input");
	input.onkeydown = function(event) 
	{	
		// update suggestions	
		if (event.key === " ")
		{
			update_suggestions();
		}

		// choose suggestion CTRL + key_number
		if (event.altKey && (event.key === "1" ||
							 event.key === "2" ||
							 event.key === "3")) 
		{
			append_suggestion(event.key);

			// move to the end of text
			document.execCommand('selectAll', false, null);
			document.getSelection().collapseToEnd();
		}
	}
};

// @brief: add the suggestion to the input area
function append_suggestion(number) {
	suggestion = "sugg" + (number-1);
	document.getElementById("input").innerHTML += document.getElementById(suggestion).innerHTML;
}

// @brief: update the suggestion bar
function update_suggestions() {
	input = document.getElementById("input").innerHTML;
	send_request(input);
}

/* 
	@brief: send request = input_sequence to the flask server
			response updates suggestion
*/
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