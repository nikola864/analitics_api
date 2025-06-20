import os
import pandas as pd
from data_models import db, FileMetadata, AnalysisResult
from datetime import datetime, timezone
from config import Config

class StorageService:
    def __init__(self):
        self.db = db

    def save_file(self, file, filename):
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename) # os.path.join() - чтобы путь к файлу склеился правильно
        file.save(filepath)

        file_meta = FileMetadata(
            filename = filename,
            filepath = filepath,
            upload_date = datetime.now(timezone.utc),
            file_size = os.path.getsize(filepath)
        )
        self.db.session.add(file_meta)
        self.db.session.commit()
        return file_meta.id

    def get_file_data(self, file_id):
        file_meta = FileMetadata.query.get_or_404(file_id)

        # читаем файлы
        if file_meta.filename.endswith('.csv'):
            df = pd.read_csv(file_meta.filepath)
        elif file_meta.filename.endswith('.xls', '.xlsx'):
            df = pd.read_excel(file_meta.filepath)
        else:
            raise ValueError('Unsupported file format')

        return df

    def save_dataframe(self, df, base_filename):
        filename = f'{base_filename}.csv'
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        df.to_csv(filepath, index=False)

        file_meta = FileMetadata(
            filename=filename,
            filepath=filepath,
            upload_date=datetime.now(timezone.utc),
            file_size=os.path.getsize(filepath)
        )
        self.db.session.add(file_meta)
        self.db.session.commit()
        return file_meta.id

    def save_analysis(self, file_id, results):
        analysis = AnalysisResult(
            file_id=file_id,
            analysis_date = datetime.now(timezone.utc),
            basic_stats=results.get('basic_stats'),
            correlation_matrix=results.get('correlation')
        )
        self.db.session.add(analysis)
        self.db.session.commit()
        return analysis.id

    def get_analysis(self, analysis_id):
        analysis = AnalysisResult.query.get_or_404(analysis_id)
        return {
            'basic_stats': analysis.basic_stats,
            'correlation_matrix': analysis.correlation_matrix,
            'analysis_date': analysis.analysis_date.isoformat()
        }





