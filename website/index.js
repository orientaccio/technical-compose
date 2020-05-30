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

// @brief: update the suggestion bar sending the last n words typed
function update_suggestions() {
	input = document.getElementById("input").innerHTML;
	input = input.split(" ");
	
	n = 5;
	input_sent = []
	if (input.length > n)
	{
		for (i = input.length-n; i < input.length; i++) 
			input_sent.push(input[i]);
	}
	else
		input_sent = input;
	input_sent = input_sent.join(" ");

	send_request(input_sent);
}

/* 
	@brief: send request = input_sequence to the flask server
			response updates suggestion
*/
function send_request(input) {
	input = input.replace(/&nbsp;/g, " ")
	console.log("message sent: " + input);

	$.ajax({
		type: "POST",
		url: "http://127.0.0.1:5000/api/predict/",
		contentType: "application/json; charset=utf-8",
    	dataType: "json",
		data: JSON.stringify({
			"input": input
		}),
		success: function(response) {
			// primitives only pass by value in js
			console.log(typeof response);
			if (response['preds'].length > 0 && response['preds'][0] != '') {
				document.getElementById("sugg0").innerHTML = response['preds'][0];
				document.getElementById("sugg1").innerHTML = response['preds'][1];
				document.getElementById("sugg2").innerHTML = response['preds'][2];
			}
			else {
				document.getElementById("sugg1").innerHTML = "-";
				document.getElementById("sugg2").innerHTML = "-";
				document.getElementById("sugg0").innerHTML = "-";
			}

			console.log(response);
		},
		error: function(response) {
			console.log(response);
		}
	})
}