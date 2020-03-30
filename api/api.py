import os
import config
import db
from flask import Blueprint, Flask, request, jsonify
from ludwig.api import LudwigModel
import pandas as pd
import psycopg2 as ps
from datetime import datetime

# Define API
app = Flask(__name__)
api = Blueprint('api', __name__)

# Load the model
model = LudwigModel.load('model')

@app.route('/predict', methods = ['POST'])
def predict():    
	'''Predict sentiment category from text input'''

	if request.method == 'POST':

		# Get data from POST request
		data = request.form['text']
		
		# Load POST request data into DataFrame
		pred = pd.DataFrame([str(data)], columns = ['text'])

		# Use model to make prediction
		pred_df = model.predict(data_df=pred)

		# Return probability score of positive sentiment
		return jsonify(float(pred_df['category_probabilities_2'][0]))

@app.route('/review', methods = ['POST'])
def insert_review():
	'''Insert review into database'''

	if request.method == 'POST':

		# Define fields expected to be present in POST request
		expected_fields = ['review_label','text']

		# Throw error if missing fields
		if any(field not in request.form for field in expected_fields):
			return jsonify({'error': 'Missing field in body'}), 400

		# Get data from POST request
		review_label = int(request.form['review_label'])
		description = str(request.form['text'])
		date = datetime.strftime(datetime.today(), '%Y-%m-%d')
		
		# Update database
		return db.add_record(review_label, description, date)

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
	app.run(debug = config.DEBUG, host = config.HOST, port = config.API_PORT)
