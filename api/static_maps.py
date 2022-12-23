# -*- coding: utf-8 -*-
import urllib.parse

from api.geocoder import get_toponym_rect, get_toponym_coords, get_toponym_spn

STATIC_MAPS_URL = 'https://static-maps.yandex.ru/1.x/'


def get_toponym_map_url(toponym):
    spn = get_toponym_spn(toponym)
    coords = get_toponym_coords(toponym)

    return STATIC_MAPS_URL + '?' + urllib.parse.urlencode({
        'l': 'map',
        'lang': 'ru_RU',
        'size': '400,300',
        'll': f'{coords[0]},{coords[1]}',
        'spn': f'{spn[0]},{spn[1]}'
    })
