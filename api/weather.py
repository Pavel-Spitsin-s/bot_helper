import os
import aiohttp
import datetime

WEATHER_API_URL = "https://api.weather.yandex.ru/v2/forecast"

conditions = {
    'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
    'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
    'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
    'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
    'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
    'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
    'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
}
wind_dirs = {
    'nw': 'СЗ', 'n': 'С', 'ne': 'СВ', 'e': 'В',
    'se': 'ЮВ', 's': 'Ю', 'sw': 'ЮЗ', 'w': 'З', 'c': 'штиль'
}
type_prec = {
    '0': 'без осадков', '1': 'дождь', '2': 'дождь со снегом', '3': 'снег', '4': 'град'
}
clowness = {
    '0': 'ясно', '0.25': 'малооблачно', '0.5': 'облачно с прояснениями', '0.75': 'облачно с прояснениями',
    '1': 'пасмурно'
}
CONDITION_TO_EMOJI = {
    'clear': '☀️', 'partly-cloudy': '⛅', 'cloudy': '⛅',
    'overcast': '☁️', 'drizzle': '🌧', 'light-rain': '🌧', 'rain': '🌧',
    'moderate-rain': '🌧', 'heavy-rain': '🌧', 'continuous-heavy-rain': '🌧',
    'showers': '🌧', 'wet-snow': '❄️', 'light-snow': '❄️', 'snow': '❄️',
    'snow-showers': '❄️', 'hail': '🌧', 'thunderstorm': '⚡',
    'thunderstorm-with-rain': '⛈', 'thunderstorm-with-hail': '⛈'
}


def common(res, a):
    b = {}
    A = []
    for i in range(len(res)):
        if a == 1:
            dan = res['fact']
            b['date'] = datetime.datetime.fromtimestamp(res['now'])
            b['temperature'] = dan['temp']
        else:
            dan = res[i]['parts']['day_short']
            b['date'] = datetime.datetime.fromtimestamp(res[i]['date_ts'])
            b['temperature'] = dan['feels_like']
        s = dan['condition']
        b['condition'] = conditions[s]
        b['wind_speed'] = dan['wind_speed']
        s = dan['wind_dir']
        b['wind_dir'] = wind_dirs[s]
        b['humidity'] = dan['humidity']
        s = dan['prec_type']
        b['type_prec'] = type_prec[str(s)]
        s = dan['cloudness']
        b['cloudness'] = str(clowness[str(s)])
        b['pressure'] = dan['pressure_mm']
        b['emoji'] = CONDITION_TO_EMOJI[dan['condition']]
        A.append(b)
    return A


async def get_weather(longitude, latitude, dayf):
    token = os.getenv('WEATHER_APIKEY')
    if dayf == 1:
        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_API_URL,
                                   params={'lat': latitude, 'lon': longitude, 'lang': 'ru_RU'},
                                   headers={'X-Yandex-API-Key': token}) as response:
                response = await response.json()
                return common(response, 1)
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_API_URL,
                                   params={'lat': latitude, 'lon': longitude, 'lang': 'ru_RU', 'limit': dayf},
                                   headers={'X-Yandex-API-Key': token}) as response:
                response = await response.json()
                return common(response['forecasts'], 2)
