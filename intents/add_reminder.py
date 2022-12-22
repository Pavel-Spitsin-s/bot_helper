from sqlalchemy.orm import Session
from parse.parse_date import get
from data.models.reminder import Reminder
import datetime


async def add_reminder(text, dct, user):
    db_sess = Session.object_session(user)
    cur_date = datetime.datetime.now()

    # пробуем обработать сообщение как напоминание с датой
    response = get(text, dct, cur_date)
    if response is None:
        return "Прошу прощения, не совсем вас поняла, повторите, пожалуйста, ваше напоминание."
    date, action = response[0], response[1]

    # если всё нормально - добавляем напоминание в БД
    reminder = Reminder()
    reminder.user = user
    reminder.target_time = date
    reminder.action = action
    db_sess.add(reminder)
    db_sess.commit()

    return f"""Отлично! Напоминание добавлено.\nВ {date.strftime('%H:%M:%S %d.%m.%Y')} вам придет напоминание в формате: 'Не забудьте {response[1]}!'"""
