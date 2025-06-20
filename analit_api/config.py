import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'postgresql://postgres:kolya2468@localhost/analytics_db'
#   QLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads') # путь к файлу "uploads"
    ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

    @staticmethod
    def init_app(app):
        # создание папки для загрузок, если нет
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)



#2. Настраивает подключение к базе данных
#3. Определяет параметры для работы с файлами
#4. Создание папки для загрузок, если её нет


