import tune_the_model as ttm
import os

IDS = {
    "small": "b5458d0c18437bc84d936d49e702690e",  # модель обученная на датасете из 17k анекдотов хорошего качества
    "big": "349d8ee605329c2085df9646268415c5", }  # модель обученная на датасете из 150k анекдотов низкого качества


def init():
    global model
    ttm.set_api_key(os.getenv('JOKE_API_KEY'))
    model = ttm.TuneTheModel.from_id(IDS["small"])


def continue_joke(prefix: str) -> str:
    """
    :param prefix: first part of joke
    :return: string that continued joke in 'prefix'
    """
    if len(prefix) == 0:
        return "Prefix Error"
    model_answer = model.generate(prefix)[0]
    joke = prefix + " " + model_answer
    return joke
