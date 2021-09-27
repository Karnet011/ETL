import logging
import os
import environ

env = environ.Env()
environ.Env.read_env()

# Logging settings
logging.basicConfig(filename='etl.log', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ELASTIC_HOSTS = os.environ.get('ELASTIC_HOSTS', 'http://localhost:9200').split(',')
FILE_STORAGE = os.environ.get('FILE_STORAGE') or 'state.txt'

# Postgres settings
PAGE = 100
dsn = {'dbname': os.environ.get('POSTGRES_DB'),
       'user': os.environ.get('POSTGRES_USER'),
       'password': os.environ.get('POSTGRES_PASSWORD'),
       'host': os.environ.get('POSTGRES_HOST'),
       'port': os.environ.get('POSTGRES_PORT')
       }

OLD_DATE = os.environ.get('OLD_DATE') or '2019-01-01 00:00:00'
