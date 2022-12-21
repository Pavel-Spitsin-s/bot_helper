from data.models.__all_models import *
from data.models import db_session
from aiogram import types

db_session.global_init("data/database.db")
db_sess = db_session.create_session()


def add_user(message: types.Message):
    tgid = message.chat.id
    user = db_sess.query(User).filter(User.tg_id == tgid).one_or_none()
    if user is None:
        user = User()
        user.tg_id = tgid
        db_sess.add(user)
    return user


def add_to_data(message: types.Message, answer, intent):
    msg = Message()
    msg.text = message.text
    msg.datetime = message.date
    msg.intent = intent
    ans_text = ''
    for i in answer:
        if i.isalpha() or i in '.,)(:;"[]-_=+ ':
            ans_text += i
    msg.answer = ans_text
    user = add_user(message)
    msg.user = user
    db_sess.add(msg)
    db_sess.commit()
