from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FileMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    filepath = db.Column(db.String(512), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)

    analyses = db.relationship('AnalysisResult', backref='file', lazy=True)

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file_metadata.id'), nullable=False)
    analysis_date = db.Column(db.DateTime, nullable=False)
    basic_stats = db.Column(db.JSON)
   #correlation_matrix = db.Column(db.JSON)



# FileMetadata класс с помощью которого будет храниться инф-ция о файле
# AnalysisResult класс с помощью которого будет храниться инф-ция об анализе файла
