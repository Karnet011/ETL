from typing import Generator

from postgres_to_es.models import Movie, Person
from postgres_to_es.utils import coroutine
from postgres_to_es.postgres_model.base_table import BaseTable

LAST_FW_QUERY = "SELECT id FROM filmwork WHERE modified > %s ORDER BY modified;"


class FilmWork(BaseTable):

    @coroutine
    def transform(self, target: Generator) -> Generator:
        while result := (yield):
            transformed = []
            for row in result:
                movie = Movie.from_dict({**row})
                transformed.append(movie)
            target.send(transformed)

    def etl_process(self):
        es_target = self.es_loader_coro(self.index)
        transform_target = self.transform(es_target)
        enrich_target = self.enrich('''
                                    SELECT fw.id, fw.title, fw.description, fw.rating as imdb_rating,
                            ARRAY_AGG(DISTINCT g.name) AS genre,
                            JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'director') AS director,
                            JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
                            JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers,
                            ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
                            ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names
                            FROM content.film_work fw
                            LEFT OUTER JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
                            LEFT OUTER JOIN content.genre g ON (gfw.genre_id = g.id)
                            LEFT OUTER JOIN content.person_film_work pfw ON (fw.id = pfw.film_work_id)
                            LEFT OUTER JOIN content.person p ON (pfw.person_id = p.id)
                            WHERE fw.id IN ( SELECT
                                id
                                FROM content.film_work
                                LIMIT 100)
                            GROUP BY fw.id, fw.title, fw.description, fw.rating; 
                                    ''', transform_target)

        updated_fw_target = self.collect_updated_ids(
            '''SELECT id FROM content.film_work WHERE updated_at > %s ORDER BY updated_at;''', enrich_target)

        self.event_loop([updated_fw_target])
