import sqlite3
import psycopg2
import os
import environ
import model
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dataclasses import astuple, fields

env = environ.Env()
environ.Env.read_env()


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def load_table(self, table: str) -> list:
        """Выгрузка данных из SQLite и преобразования строки в dict"""
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT * FROM {table}""")
        return cursor


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.pg_conn = pg_conn

    def save_all_data(self, data: list[object], table: str, rows_name: str):
        cursor = self.pg_conn.cursor()
        query = f"""INSERT INTO {table} ({rows_name})
                    VALUES %s 
                    ON CONFLICT (id) DO NOTHING; """

        psycopg2.extras.execute_values(cur=cursor, sql=query, argslist=data, page_size=len(data))
        self.pg_conn.commit()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_loader = SQLiteLoader(connection)
    postgres_saver = PostgresSaver(pg_conn)

    models = {'person': model.Person,
              'genre': model.Genre,
              'film_work': model.FilmWork,
              'genre_film_work': model.GenreFilmWork,
              'person_film_work': model.PersonFilmWork,
              }

    for table_name, model_dataclass in models.items():
        data = [model_dataclass(**row) for row in sqlite_loader.load_table(table=table_name)]
        postgres_saver.save_all_data([astuple(obj) for obj in data], table=f"content.{table_name}",
                                     rows_name=','.join(data[-1].__dataclass_fields__.keys()))


if __name__ == '__main__':
    dsl = {'dbname': os.environ.get('POSTGRES_DB'),
           'user': os.environ.get('POSTGRES_USER'),
           'password': os.environ.get('POSTGRES_PASSWORD'),
           'host': os.environ.get('POSTGRES_HOST'),
           'port': os.environ.get('POSTGRES_PORT')
           }
    with sqlite3.connect('sqlite_to_postgres/db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
    pg_conn.close()
