from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin
from model.gpt2.generation import run_generation_gpt2 as gpt2

import logging
import numpy as np
import torch

from transformers import (
    CTRLLMHeadModel,
    CTRLTokenizer,
    GPT2LMHeadModel,
    GPT2Tokenizer,
    OpenAIGPTLMHeadModel,
    OpenAIGPTTokenizer,
    TransfoXLLMHeadModel,
    TransfoXLTokenizer,
    XLMTokenizer,
    XLMWithLMHeadModel,
    XLNetLMHeadModel,
    XLNetTokenizer,
)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
number_suggestions = 3

@app.route("/api/predict/", methods=['POST'])
@cross_origin()
def make_predict():
	# Get input and predict
	data = request.get_json()['input'].replace('&nbsp;', ' ')
	preds_all = gpt2.generate(data)

	# Prepare JSON
	response = jsonify({'preds': preds_all[:number_suggestions]})

	logging.info('Request:\t %s', data)
	logging.info('Answer:\t %s', preds_all[:number_suggestions])
	
	return response, 201

@app.route("/test/api/", methods=['POST'])
def hello():
	return jsonify({'preds': "test "}), 201

if __name__=='__main__':
	logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
	logging.info('Starting server...')
	app.run(host='127.0.0.1', port=5000)