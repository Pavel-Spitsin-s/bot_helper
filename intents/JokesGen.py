import sqlite3
from random import randint
from using_db import *


joke_list = []


def get_joke():
    if len(joke_list):
        res = joke_list[-1]
        joke_list.pop()
        return res
    else:
        for i in range(100):
            ID = randint(1, 17078)  # range id
            text = db_sess.query(joke.Joke).filter(joke.Joke.id == ID).first().text
            joke_list.append(text)
        return get_joke()
