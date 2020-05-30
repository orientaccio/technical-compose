from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin
from model.heuristic import run_generation_heuristic as heuristic

import logging
import numpy as np

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
number_suggestions = 3

@app.route("/api/predict/", methods=['POST'])
@cross_origin()
def make_predict():
	# Get input and predict
	data = request.get_json()['input']
	preds_all = heuristic.predict(data)[:number_suggestions] 

	# Prepare JSON
	response = jsonify({'preds': preds_all})

	logging.info('Request:\t %s', data)
	logging.info('Answer:\t %s', preds_all)
	
	return response, 201

@app.route("/test/api/", methods=['POST'])
def hello():
	return jsonify({'preds': "test "}), 201

if __name__=='__main__':
	logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
	logging.info('Starting server...')
	app.run(host='127.0.0.1', port=5000)