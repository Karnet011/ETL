### Ручной запуск
1. Клонируем репозиторий
2. Создаем виртуальное окружение python -m venv venv
 
Далее выполняем компанды:
- Выполняем команду 
pip install -r requirements.txt
- docker-compose up --build -d db
- venv/bin/python ./sqlite_to_postgres/load_data.py
- docker-compose up --build -d web
- docker-compose up --build nginx  
