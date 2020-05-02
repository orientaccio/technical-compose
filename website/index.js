function predict() {
	//text input boxes
	sl = document.getElementById("sl").value;
	setosa_fn = document.getElementById("setosa");

	$.ajax({
		type: "POST",
		url: "./predict.php",
		// async: false,
		datatype: 'json',
		data: {
			sl: sl
		},
		success: function(response) {
			var obj = JSON.parse(response);
			setosa_fn.innerHTML = obj.value;
		},
		error: function(response) {
			console.log(response);
			setosa_fn.innerHTML = "Error";
		}
	})
}

function proceed() {
	sl = document.getElementById("sl").value;
	setosa_fn = document.getElementById("setosa");

    var form = document.createElement('form');
    form.setAttribute('method', 'post');
    form.setAttribute('action', 'http://127.0.0.1:5000/test/api');
    form.style.display = 'hidden';
    document.body.appendChild(form)
    form.submit();
}