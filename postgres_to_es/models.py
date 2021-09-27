import dataclasses
import typing
import uuid


@dataclasses.dataclass
class Person:
    id: uuid
    name: str

    @classmethod
    def from_dict(cls, dict_: dict[str, typing.Any]):
        if dict_:
            return cls(
                id=dict_['id'],
                name=dict_['name']
            )
        return None

    @classmethod
    def from_dict_list(cls, iterable: typing.Iterable[dict]) -> list['Person']:
        if iterable:
            return [cls.from_dict(it) for it in iterable]
        return []


@dataclasses.dataclass
class Movie:
    id: uuid
    title: str
    description: str
    imdb_rating: float
    genre: list[str]
    writers: list[Person]
    actors: list[Person]
    director: list[Person]
    actors_names: list[str]
    writers_names: list[str]
    # updated_at: datetime

    @classmethod
    def from_dict(cls, dict_: dict[str, typing.Any]) -> 'Movie':
        data = cls(
            id=dict_['id'],
            title=str(dict_['title']),
            description=str(dict_['description']),
            imdb_rating=float(dict_['imdb_rating']),
            genre=list(map(str, dict_['genre'])),
            actors_names=list(map(str, dict_['actors_names'])),
            writers_names=list(map(str, dict_['writers_names'])),
            writers=Person.from_dict_list(dict_['writers']),
            actors=Person.from_dict_list(dict_['actors']),
            director=Person.from_dict_list(dict_['director']),
        )
        return data
