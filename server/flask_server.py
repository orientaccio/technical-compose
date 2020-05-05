from keras.models import load_model
from flask import Flask, abort, jsonify, request
import numpy as np
import rnn_ngram_sentences as ngram

app = Flask(__name__)
irisModel = None

# @app.route("/iris/api", methods=['POST'])
# def make_predict():
# 	data = request.get_json(force=True)
# 	predict_request = [data['sl'],data['sw'],data['pl'],data['pw']]
# 	predict_request = np.array([predict_request])
# 	y_pred = irisModel.predict(predict_request)
# 	return jsonify({'setosa': str(y_pred[0][0]),
# 		'versicolor': str(y_pred[0][1]),
# 		'virginica': str(y_pred[0][2])}), 201

@app.route("/test/api/", methods=['POST'])
def hello():
	# y_pred = ngram.predict(["contribute to", "inform on", "lead by british"])
	# print(y_pred)
	return jsonify({'value': "test "}), 201
	# data = request.get_json(force=True)
	# print(data['input'])
	# y_pred = ngram.predict(["contribute to", "inform on"])
	# print(y_pred)
	# return jsonify({'value': y_pred[0]}), 201

if __name__=='__main__':
	print("Starting server...")
	app.run(host='127.0.0.1', port=5000)