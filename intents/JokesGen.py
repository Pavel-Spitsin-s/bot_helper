from random import randint
from using_db import *
from sqlalchemy.sql.expression import func


joke_list = []


def get_joke():
    global joke_list
    if not joke_list:
        max_id = db_sess.query(func.max(Joke.id)).scalar()
        ids = [randint(1, max_id) for _ in range(100)]
        joke_list = [i.text for i in db_sess.query(Joke).filter(Joke.id.in_(ids)).all()]
    res = joke_list[-1]
    joke_list.pop()
    return res
