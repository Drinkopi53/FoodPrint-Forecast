"""
Flask web application for FoodPrint Forecast
"""
import sys
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.coordinator import FoodPrintForecast

app = Flask(__name__)
system = FoodPrintForecast()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Handle image upload
    if 'fridge_image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image = request.files['fridge_image']
    if image.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Save image temporarily
    image_path = os.path.join('data', 'uploads', image.filename)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    image.save(image_path)
    
    # Analyze image
    try:
        results = system.analyze_fridge_image(image_path)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/leaderboard')
def leaderboard():
    top_users = system.get_leaderboard()
    return jsonify(top_users)

@app.route('/add_contribution', methods=['POST'])
def add_contribution():
    data = request.get_json()
    username = data.get('username')
    emission_results = data.get('emission_results')
    
    if not username or not emission_results:
        return jsonify({'error': 'Missing username or emission results'}), 400
    
    system.add_user_contribution(username, emission_results)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)