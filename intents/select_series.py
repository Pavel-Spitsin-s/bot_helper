from using_db import *
from random import randint
from sqlalchemy.sql.expression import func


async def select_series():
    rand_id = randint(0, db_sess.query(func.max(Series.id)).scalar())
    req = db_sess.query(Series).filter(Series.id == rand_id).first()
    genres_text = ', '.join([i.genre for i in req.genres])
    res = f'{req.title}\n\n{genres_text}\n\n{req.description}\n\n\n{req.link}'
    return res
