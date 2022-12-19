from data.models.__all_models import *
from data.models import db_session
from aiogram import types

db_session.global_init("data/database.db")
db_sess = db_session.create_session()


def add_to_data(message_: types.Message, intent):
    msg = message.Message()
    msg.text = message_.text
    msg.datetime = message_.date
    msg.intent = intent
    tgid = message_.chat.id
    user_ = db_sess.query(user.User).filter(user.User.tg_id == tgid).one_or_none()
    if user_ is None:
        user_ = user.User()
        user_.tg_id = tgid
    msg.user = user_
    db_sess.add(msg)
    db_sess.commit()