import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

Films_Genre = sqlalchemy.Table(

    'genre_to_film',

    SqlAlchemyBase.metadata,

    sqlalchemy.Column('film', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('films.id')),

    sqlalchemy.Column('genre', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('genres.id'))
)

Series_Genre = sqlalchemy.Table(

    'genre_to_series',

    SqlAlchemyBase.metadata,

    sqlalchemy.Column('film', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('series.id')),

    sqlalchemy.Column('genre', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('genres.id'))
)


class Genres(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'genres'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    genre = sqlalchemy.Column(sqlalchemy.String, unique=True)
