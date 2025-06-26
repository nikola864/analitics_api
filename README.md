# analitics_api
Analytics API Service
Простой API-сервис для загрузки и анализа данных с использованием Flask, Pandas и PostgreSQL.

📌 Функционал
Загрузка файлов (CSV, Excel) через API

Анализ данных (среднее, медиана, корреляция)

Очистка данных (удаление дубликатов, заполнение пропусков)

Хранение файлов и результатов анализа в PostgreSQL

Получение статистики через API endpoints

🚀 Быстрый старт
Требования
Python 3.8+
PostgreSQL 12+
pip

УСТАНОВКА
1. Клонируйте репозиторий:
git clone https://github.com/nikola864/analitics_api.git
cd analytics_api
2. Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
3. Установите зависимости:
pip install -r requirements.txt
4. Настройте базу данных:
Создайте БД в PostgreSQL
Обновите настройки в config.py
5. Запустите приложение:
python app.py

API Endpoints
Загрузка файла

POST /upload
Content-Type: multipart/form-data
file: <ваш_файл.csv>


Анализ данных

GET /analyze/<file_id>

Очистка данных

POST /clean/<file_id>
Content-Type: application/json

{
    "remove_duplicates": true,
    "missing_values": "fill",
    "fill_value": 0
}

Получение статистики

GET /stats/<analysis_id>

 Технологии
Backend: Flask
Анализ данных: Pandas
База данных: PostgreSQL (SQLAlchemy)
Хранение файлов: Локальная файловая система

СТРУКТУРА ПРОЕКТА:

analytics_api/
├── app.py              # Основное приложение
├── config.py           # Конфигурация
├── requirements.txt    # Зависимости
├── services/           # Бизнес-логика
│   ├── data_service.py     # Анализ данных
│   └── storage_service.py  # Работа с хранилищем
├── models/             # Модели БД
│   └── data_models.py
└── utils/              # Вспомогательные функции
    └── file_utils.py








