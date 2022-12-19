import asyncio
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import nest_asyncio
import datetime
from data.reminder import Reminder
from data import db_session
from data.user import User
from parse.parse_date import get_date
import sqlalchemy.exc
import os

nest_asyncio.apply()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
db_session.global_init("db/base.db")


def add_reminder(text, user_id):
    db_sess = db_session.create_session()
    cur_date = datetime.datetime.now()
    # пробуем обработать сообщение как напоминание с датой
    response = get_date(text, cur_date)
    if response is None:
        return "Прошу прощения, не совсем вас понял, повторите, пожалуйста."
    date, action = response[0], response[1]
    # если всё нормально - добавляем напоминание в БД
    reminder = Reminder()
    reminder.user_id = user_id
    reminder.target_time = date
    reminder.action = action
    db_sess.add(reminder)
    db_sess.commit()
    return f"""Отлично! Напоминание добавлено.\nВ {date.strftime('%H:%M:%S %d.%m.%Y')} \
    вам придет напоминание в формате: 'Не забудьте {response[1]}!'"""


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    db_sess = db_session.create_session()
    # создаём нового пользователя
    user = User()
    user.tg_id = message.chat.id
    try:
        db_sess.add(user)
        db_sess.commit()
        await message.answer(
            "Привет! Я бот-напоминалка\nНапиши мне в свободной форме, что надо запомнить и когда напомнить, и я это сделаю!")
    except sqlalchemy.exc.IntegrityError:
        await message.answer("Вы уже есть в моей базе.")


@dp.message_handler()
async def get_reminder(message: types.Message):
    # рассматриваем полученное сообщение как напоминание с датой
    response = add_reminder(message.text, message.chat.id)
    await message.answer(response)


async def update_reminders():
    while 1:
        current = datetime.datetime.now()
        db_sess = db_session.create_session()
        # получение всех напоминаний, время которых пришло
        reminders = db_sess.query(Reminder).filter(Reminder.target_time <= current).order_by(Reminder.target_time)
        for rem in reminders:
            await bot.send_message(chat_id=f"{rem.user_id}", text=f"Не забудьте {rem.action}!")
            db_sess.delete(rem)
            db_sess.commit()
        await asyncio.sleep(5)


async def on_startup(x):
    asyncio.create_task(update_reminders())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
