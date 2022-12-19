import datetime
from data import db_session
from data.reminder import Reminder
import asyncio


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
