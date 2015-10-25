from flask import Flask, request, jsonify, make_response
from model import db, Data
from datetime import datetime
import sys
import os

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello, world!"

@app.route("/hackumass/api", methods=['POST'])
def api():
	try:
		jsonData = request.get_json()
		print jsonData
		for elem in jsonData['data']:
			data = Data(elem['acc_x'], elem['acc_y'], elem['acc_z'], elem['lat'], elem['lng'], elem['time'])
			db.session.add(data)
			db.session.commit()

		os.system("calculate.py")

		return make_response(jsonify({'Successful!' : 'Data added.'}), 200)

	except:
		return make_response(jsonify({'Uh oh!' : 'Something went wrong.'}), 400)

@app.route("/hackumass/bumps", methods=['GET'])
def bumps():
	data = Data.query.filter(Data.bump != 0).all()
	response = []

	for elem in data:
		dictData = {
			"acc_x" : elem.acc_x,
			"acc_y" : elem.acc_y,
			"acc_z" : elem.acc_z,
			"lat" : elem.lat,
			"lng" : elem.lng,
			"bump" : elem.bump
		}
		response.append(dictData)

	return make_response(jsonify({"result" : response}),  200)

@app.route("/api/v0.1/public")
def public():
	data = Data.query.all()
	response = []

	for elem in data:
		dictData = {
			"acc_x" : elem.acc_x,
			"acc_y" : elem.acc_y,
			"acc_z" : elem.acc_z,
			"lat" : elem.lat,
			"lng" : elem.lng,
			"bump" : elem.bump
		}
		response.append(dictData)

	return make_response(jsonify({"result" : response}), 200)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
