import datetime
from using_db import db_sess
from data.models.reminder import Reminder
import asyncio


async def update_reminders(bot):
    while True:
        current = datetime.datetime.now()

        # получение всех напоминаний, время которых пришло
        reminders = db_sess.query(Reminder).filter(Reminder.target_time <= current).order_by(Reminder.target_time)
        for rem in reminders:
            await bot.send_message(chat_id=f"{rem.user.tg_id}", text=f"Не забудьте {rem.action}!")
            db_sess.delete(rem)
            db_sess.commit()
        await asyncio.sleep(5)
