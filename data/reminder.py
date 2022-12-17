import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Reminder(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reminders'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    target_time = sqlalchemy.Column(sqlalchemy.DateTime)
    action = sqlalchemy.Column(sqlalchemy.Text)
