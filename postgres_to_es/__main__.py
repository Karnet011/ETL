import logging

from postgres_to_es.postgres_model.film_model import FilmWork


from postgres_to_es.es_loader import ESLoader
from postgres_to_es.postgres_load import PgProducer
from postgres_to_es.config import dsn, ELASTIC_HOSTS, FILE_STORAGE
from postgres_to_es.postgres_model.base_table import FILMWORK_ETL
from postgres_to_es.state_etl import JsonFileStorage, State

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('root')


if __name__ == '__main__':
    logger.info('Start ETL application with %s mode', FILMWORK_ETL.value)
    jsf = JsonFileStorage(FILE_STORAGE)
    state = State(jsf)
    db_adapter = PgProducer(dsn)
    es_loader = ESLoader(ELASTIC_HOSTS)
    filmwork = FilmWork(state, db_adapter, es_loader)
    filmwork.etl_process()
