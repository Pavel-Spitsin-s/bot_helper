from aiogram import Bot
from aiogram.types import ContentType
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import soundfile as sf
import librosa
from speech2text import speech_to_text, rate
from text2speech import text_to_speech
from classifier import classify
from using_db import *
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)


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
        await message.answer("Извините, не поняла вас, повторите, пожалуйста, еще раз.")


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
        await message.answer("Извините, не поняла вас, повторите, пожалуйста еще раз.")


@dp.message_handler(content_types=['location'])
async def location_handler(message: types.Message):
    user = add_user(message)
    user.lat = message.location.latitude
    user.long = message.location.longitude
    db_sess.commit()

    await message.answer(
        'Ваша геолокация сохранена и '
        'теперь будет использоваться для получения погоды.'
    )


executor.start_polling(dp, skip_updates=True)
