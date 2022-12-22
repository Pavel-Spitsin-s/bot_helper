from aiogram import Bot, types
from aiogram.types import ContentType
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import soundfile as sf
import librosa
from speech2text import speech_to_text, rate
from text2speech import text_to_speech
from classifier import classify
from using_db import *
import os
import tune_the_model as ttm
import asyncio
from generate import slot_detection_tune
from intents import talking
from update_reminders import update_reminders

talking.run()
slot_detection_tune.run()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def on_startup(x):
    asyncio.create_task(update_reminders(bot))


async def download_file(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    path = file.file_path
    await bot.download_file(path, 'audio/voice.wav')
    x, _ = librosa.load('audio/voice.wav', sr=rate)
    sf.write('audio/voice.wav', x, rate)


@dp.message_handler(content_types=[ContentType.TEXT])
async def text_message(message: types.Message):
    text = message.text.lower()
    if text:
        res = await classify(text, add_user(message))
        add_to_data(message, res[1], res[0])
        await message.answer(res[1])

    else:
        await message.answer("Извините, не поняла вас, повторите, пожалуйста, еще раз.", parse_mode='markdown')


@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message(message: types.Message):
    await download_file(message)
    text = await speech_to_text(message)
    message.text = text
    if text:
        res = await classify(text, add_user(message))
        add_to_data(message, res[1], res[0])
        if len(res[1]) < 1000:
            await message.answer_voice(open(text_to_speech(res[1]), 'rb'), res[1])
        else:
            await message.answer(res[1])
    else:
        await message.answer("Извините, не поняла вас, повторите, пожалуйста еще раз.", parse_mode='markdown')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
