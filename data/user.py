import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    lat = sqlalchemy.Column(sqlalchemy.String)
    long = sqlalchemy.CHAR(sqlalchemy.String)
    name = sqlalchemy.CHAR(sqlalchemy.String)
