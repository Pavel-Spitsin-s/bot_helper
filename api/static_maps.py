# -*- coding: utf-8 -*-
import urllib.parse

from api.geocoder import get_toponym_rect

STATIC_MAPS_URL = 'https://static-maps.yandex.ru/1.x/'


def get_toponym_map_url(toponym):
    rect = get_toponym_rect(toponym)

    return STATIC_MAPS_URL + '?' + urllib.parse.urlencode({
        'l': 'map',
        'lang': 'ru_RU',
        'size': '400,300',
        'bbox': f'{rect[0]},{rect[1]}~{rect[2]},{rect[3]}'
    })
