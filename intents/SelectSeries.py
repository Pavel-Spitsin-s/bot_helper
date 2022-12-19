from using_db import *
from random import randint

MAXID_SERIES = 472


def select_series():
    rand_id = randint(0, MAXID_SERIES)
    req = db_sess.query(series.Series).filter(series.Series.id == rand_id).first()
    gen = req.genres
    genres_text = ', '.join([i.genre for i in gen])
    res = f'{req.title}\n\n{genres_text}\n\n{req.description}\n\n\n{req.link}'
    return res
