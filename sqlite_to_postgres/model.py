import uuid
import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Person:
    id: uuid.UUID
    full_name: str
    birth_date: datetime
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class FilmWork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime
    certificate: str
    rating: float
    file_path: str
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class GenreFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime


@dataclass(frozen=True)
class PersonFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime
