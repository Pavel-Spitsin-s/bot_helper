# -*- coding: utf-8 -*-
import os
import requests

GEOCODER_API_URL = 'https://geocode-maps.yandex.ru/1.x'


def get_toponym(query):
    apikey = os.getenv('geocoder_apikey')

    try:
        response = requests.get(GEOCODER_API_URL, params={
            'geocode': query,
            'apikey': apikey,
            'lang': 'ru_RU',
            'format': 'json'
        }).json()
        return response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    except Exception as e:
        return


def get_toponym_coords(toponym):  # (долгота, широта)
    if toponym is None:
        return 0, 0
    return tuple(map(float, toponym['Point']['pos'].split()))
