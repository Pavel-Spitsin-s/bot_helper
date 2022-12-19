from using_db import *
from random import randint

MAXID_FILM = 998


def select_film():
    rand_id = randint(0, MAXID_FILM)
    req = db_sess.query(films.Films).filter(films.Films.id == rand_id).first()
    gen = req.genres
    genres_text = ', '.join([i.genre for i in gen])
    res = f'{req.title}\n\n{genres_text}\n\n{req.description}\n\n\n{req.link}'
    return res
