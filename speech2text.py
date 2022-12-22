from aiogram import types
import json, wave
from vosk import Model, KaldiRecognizer

# speech to text
rate = 44100  # 44100 / 8000
speech_model = Model('models/small_model')  # small_model / model
rec = KaldiRecognizer(speech_model, rate)


async def speech_to_text(message: types.Message):
    wf = wave.open('audio/voice.wav', 'rb')
    text = ""
    while True:
        data = wf.readframes(rate)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            text += f" {res['text']}"
    res = json.loads(rec.FinalResult())
    text += res['text']
    return text
