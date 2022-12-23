# -*- coding: utf-8 -*-
import os
import aiohttp

GEOCODER_API_URL = 'https://geocode-maps.yandex.ru/1.x'


async def get_toponym(query):
    apikey = os.getenv('GEOCODER_APIKEY')

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GEOCODER_API_URL, params={
                'geocode': query,
                'apikey': apikey,
                'lang': 'ru_RU',
                'format': 'json'
            }) as response:
                response = await response.json()
                return response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    except Exception as e:
        return


def get_toponym_coords(toponym):  # (долгота, широта)
    if toponym is None:
        return
    return tuple(map(float, toponym['Point']['pos'].split()))


def get_toponym_rect(toponym):
    if toponym is None:
        return
    x1, y1 = map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split())
    x2, y2 = map(float, toponym['boundedBy']['Envelope']['upperCorner'].split())
    return x1, y1, x2, y2


def get_toponym_spn(toponym):
    rect = get_toponym_rect(toponym)
    return (rect[2] - rect[0]) / 2, (rect[3] - rect[1]) / 2


def get_toponym_name(toponym):
    return toponym['name']
