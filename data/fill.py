from data.models.__all_models import *
from data.models import db_session
from using_db import db_sess
import csv
from data.models.series import Series
from data.models.joke import Joke
from data.models.films import Films
from data.models.genres import Genres


def fillJokes():
    file = csv.reader(open('data/not using data/jokes.csv'))
    jid = 0
    for i in file:
        item = Joke()
        item.text = i[0].strip()
        item.id = jid
        item.src = 1
        item.is_banned = 0
        db_sess.add(item)
        jid += 1


def fillFilms():
    file = csv.reader(open('data/not using data/films.csv'))
    jid = 0
    for i in file:
        item = Films()
        item.id = jid
        item.title = i[0].strip()
        # item.genres_str = i[1].strip()
        for j in i[1].strip().split(", "):
            j = j.strip()
            g = db_sess.query(Genres).filter(Genres.genre == j).one_or_none()
            if g is None:
                g = Genres()
                g.genre = j

            item.genres.append(g)

        item.description = i[2].strip()
        item.link = i[3].strip()
        db_sess.add(item)
        jid += 1


def fillSeries():
    file = csv.reader(open('data/not using data/series.csv'))
    jid = 0
    for i in file:
        item = Series()
        item.id = jid
        item.title = i[0].strip()
        # item.genres_str = i[1].strip()
        for j in i[1].strip().split(", "):
            j = j.strip()
            g = db_sess.query(Genres).filter(Genres.genre == j).one_or_none()
            if g is None:
                g = Genres()
                g.genre = j.strip()
            item.genres.append(g)
        item.description = i[2].strip()
        item.link = i[3].strip()
        db_sess.add(item)
        jid += 1


fillJokes()
fillFilms()
fillSeries()
db_sess.commit()
