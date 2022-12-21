import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Reminder(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reminder'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    target_time = sqlalchemy.Column(sqlalchemy.DateTime)
    action = sqlalchemy.Column(sqlalchemy.Text)

    user = orm.relation('User')
