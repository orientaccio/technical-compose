<?php
	$sl = $_POST['sl'];
	console.log("Message here");
	$headers = array('Content-Type: application/json', 'Access-Control-Allow-Headers: *');
	$fields = array('sl'=>$sl);
	$payload = json_encode($fields);

	$curl_session = curl_init();
	curl_setopt($curl_session, CURLOPT_URL, 'http://127.0.0.1:5000/test/api');
	curl_setopt($curl_session, CURLOPT_POST, true);
	curl_setopt($curl_session, CURLOPT_HTTPHEADER, $headers);
	curl_setopt($curl_session, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($curl_session, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($curl_session, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4);
	curl_setopt($curl_session, CURLOPT_POSTFIELDS, $payload);
				
	$result = curl_exec($curl_session);

	curl_close($curl_session);
				
	echo $result;
?>