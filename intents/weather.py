# -*- coding: utf-8 -*-
from api.geocoder import *
from api.static_maps import get_toponym_map_url
from api.weather import get_weather

from utils.utils import get_loc_from_doc, text2doc, get_date_diff_from_message


def make_response(text, markdown=False, photo_url=None):
    return {
        'text': text,
        'markdown': markdown,
        'photo_url': photo_url
    }


async def weather_handler(text, user):
    text = text.title()
    doc = text2doc(text)
    loc = get_loc_from_doc(doc)
    diff = get_date_diff_from_message(text)

    if not loc:
        if user.lat is not None and user.long is not None:
            loc = f'{user.long},{user.lat}'
        else:
            return make_response(
                'Вы можете отправить мне Ваши координаты, чтобы запрашивать погоду в своём городе.'
                'Или Вы можете назвать конкретный город, чтобы узнать погоду в нём.'
            )

    if diff < 0:
        return make_response(
            'Некорректная дата. Нельзя запрашивать погоду в прошлом, '
            'а также погоду через 7 дней и более.'
        )

    toponym = await get_toponym(loc)

    if toponym is not None:
        weather = (await get_weather(*get_toponym_coords(toponym), diff))[diff - 1]

        date_str = weather['date'].strftime('%d.%m.%Y')
        return make_response(
            f'*{weather["emoji"]} | Погода | {get_toponym_name(toponym)} | {date_str}*\n'
            f'*{weather["condition"].capitalize()}*\n'
            f'*Температура*: {weather["temperature"]} °C\n'
            f'*Атмосферное давление*: {weather["pressure"]} мм рт. ст.\n'
            f'*Влажность*: {weather["humidity"]}%.\n'
            f'*Скорость ветра*: {weather["wind_speed"]} м/с, {weather["wind_dir"]}.\n',
            markdown=True,
            photo_url=get_toponym_map_url(toponym)
        )
    else:
        return make_response(
            'К сожалению, не удалось найти координаты указанной локации.'
        )
