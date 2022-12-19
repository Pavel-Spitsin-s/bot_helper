import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'message'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('user.id'))
    datetime = sqlalchemy.Column(sqlalchemy.DATETIME)
    status = sqlalchemy.Column(sqlalchemy.String)
    intent = sqlalchemy.Column(sqlalchemy.String)
    user = orm.relation('User', back_populates='msg')