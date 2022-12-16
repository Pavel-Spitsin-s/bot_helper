# -*- coding: utf-8 -*-
from api.geocoder import get_toponym_rect

STATIC_MAPS_URL = 'https://static-maps.yandex.ru/1.x/'


def get_toponym_map_url(toponym):
    rect = get_toponym_rect(toponym)

    return STATIC_MAPS_URL + \
        f'?l=map' \
        f'&lang=ru_RU' \
        f'&size=400,300' \
        f'&bbox={rect[0]},{rect[1]}~{rect[2]},{rect[3]}'
