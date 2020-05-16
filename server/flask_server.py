from keras.models import load_model
from flask import Flask, abort, jsonify, request
from model.heuristic import heuristic
import numpy as np

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route("/api/predict", methods=['POST'])
# def make_predict():
# 	data = request.get_json(force=True)
# 	predict_request = [data['sl'],data['sw'],data['pl'],data['pw']]
# 	predict_request = np.array([predict_request])
# 	y_pred = irisModel.predict(predict_request)
# 	return jsonify({'setosa': str(y_pred[0][0]),
# 		'versicolor': str(y_pred[0][1]),
# 		'virginica': str(y_pred[0][2])}), 201

@app.route("/api/predict/", methods=['POST'])
@cross_origin()
def make_predict():
	data = request.get_json()
	print(data)
	return jsonify({'value': "test "}), 201

@app.route("/test/api/", methods=['POST'])
def hello():
	return jsonify({'value': "test "}), 201

if __name__=='__main__':
	print("Starting server...")
	app.run(host='127.0.0.1', port=5000)
	# preds = heuristic.predict("view for")
	# print(preds)