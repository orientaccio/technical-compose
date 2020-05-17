from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin
from model.heuristic import heuristic

import logging
import numpy as np

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/api/predict/", methods=['POST'])
@cross_origin()
def make_predict():
	n = 3
	response = ""
	data = request.get_json()['input']
	preds_all = heuristic.predict(data)

	if (not preds_all):
		response = jsonify({'preds': preds_all})
	else:
		preds_send = np.array(preds_all[:n])
		preds_send = np.squeeze(np.delete(preds_send, 1, axis=1))
		response = jsonify({'preds': preds_send.tolist()})

	logging.info('Request:\t %s', data)
	logging.info('Answer:\t %s', response)
	
	return response, 201

@app.route("/test/api/", methods=['POST'])
def hello():
	return jsonify({'value': "test "}), 201

if __name__=='__main__':
	logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
	logging.info('Starting server...')
	app.run(host='127.0.0.1', port=5000)