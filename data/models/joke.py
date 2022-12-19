import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Joke(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'joke'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    src = sqlalchemy.Column(sqlalchemy.Integer)
    is_banned = sqlalchemy.Column(sqlalchemy.Boolean)
    text = sqlalchemy.Column(sqlalchemy.Text)