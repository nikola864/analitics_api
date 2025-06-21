from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
from data_service import DataService
from storage_service import StorageService
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация SQLAlchemy
db = SQLAlchemy(app)
# Инициализация папки для загрузок
Config.init_app(app)

storage_service = StorageService()
data_service = DataService(storage_service)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == "":
        return jsonify({'error':'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_id = storage_service.save_file(file, filename)
        return jsonify({'file_id': file_id}), 201
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/analyze/<file_id>', methods=['GET'])
def analyze_data(file_id):
    try:
        df = storage_service.get_file_data(file_id)
        stats = data_service.calculate_basic_stats(file_id)
        correlation = data_service.calculate_correlation(df)

        analysis_id = storage_service.save_analysis(file_id, {
            'basic_stats': stats,
            'correlation': correlation
        })
        return jsonify({
            'analysis_id': analysis_id,
            'basic_stats': stats,
            'correlation': correlation
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/clean/<file_id>', methods=['POST'])
def clean_data(file_id):
    try:
        df = storage_service.get_file_data(file_id)
        clean_params = request.json or {}

        cleaned_df = data_service.clean_data(df, clean_params)
        new_file_id = storage_service.save_dataframe(cleaned_df, f"cleaned_{file_id}")
        return jsonify({
            'file_id': new_file_id,
            'message': 'Data cleaned successfully'
        }), 200
    except Exception as e:
        return jsonify({'error':str(e)}), 400


@app.route('/stats/<analysis_id>', methods=['GET'])
def get_stats(analysis_id):
    try:
        stats = storage_service.get_analysis(analysis_id)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



















