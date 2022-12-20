import os
import aiohttp
import datetime

conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
              'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
              'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
              'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
              'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
              'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
              'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
              }
wind_dirs = {'nw': 'СЗ', 'n': 'С', 'ne': 'СВ', 'e': 'В',
             'se': 'ЮВ', 's': 'Ю', 'sw': 'ЮЗ', 'w': 'З', 'с': 'штиль'}
type_prec = {'0': 'без осадков', '1': 'дождь', '2': 'дождь со снегом', '3': 'снег', '4': 'град'}
clowness = {'0': 'ясно', '0.25': 'малооблачно', '0.5': 'облачно с прояснениями', '0.75': 'облачно с прояснениями',
            '1': 'пасмурно'}
CONDITION_TO_SMILE = {
    'clear': '☀️', 'partly-cloudy': '⛅', 'cloudy': '⛅',
    'overcast': '☁️', 'drizzle': '🌧', 'light-rain': '🌧', 'rain': '🌧',
    'moderate-rain': '🌧', 'heavy-rain': '🌧', 'continuous-heavy-rain': '🌧',
    'showers': '🌧', 'wet-snow': '❄️', 'light-snow': '❄️', 'snow': '❄️',
    'snow-showers': '❄️', 'hail': '🌧', 'thunderstorm': '⚡',
    'thunderstorm-with-rain': '⛈', 'thunderstorm-with-hail': '⛈'
}

WEATHER_API_URL = "https://api.weather.yandex.ru/v2/forecast"


def get_today_weather(res):
    dan = res['fact']
    b = {}
    b['date'] = datetime.datetime.fromtimestamp(res['now'])
    b['tempreture'] = dan['temp']
    s = dan['conditions']
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
    b['smile'] = CONDITION_TO_SMILE[dan['condition']]
    return b


def obr_forecasts(dan):
    A = []
    for i in range(len(dan)):
        b = {}
        b['date'] = datetime.datetime.fromtimestamp(dan[i]['date_ts'])
        b['tempreture'] = dan[i]['parts']['day_short']['feels_like']
        s = dan[i]['parts']['day_short']['condition']
        b['smile'] = CONDITION_TO_SMILE[s]
        b['conditions'] = conditions[s]
        b['wind_speed'] = dan[i]['parts']['day_short']['wind_speed']
        s = dan[i]['parts']['day_short']['wind_dir']
        b['wind_deer'] = wind_dirs[s]
        b['humidity'] = dan[i]['parts']['day_short']['humidity']
        s = dan[i]['parts']['day_short']['prec_type']
        b['type_prec'] = type_prec[str(s)]
        s = dan[i]['parts']['day_short']['cloudness']
        b['cloudness'] = str(clowness[str(s)])
        b['pressure'] = dan[i]['parts']['day_short']['pressure_mm']
        A.append(b)
    return A


async def get_weather(latitude, longitude, dayf):
    token = os.getenv('WEATHER_APIKEY')
    if dayf == 1:
        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_API_URL,
                                   params={'lat': latitude, 'lon': longitude, 'lang': 'ru_RU'},
                                   headers={'X-Yandex-API-Key': token}) as response:
                response = await response.json()
                return get_today_weather(response)
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_API_URL,
                                   params={'lat': latitude, 'lon': longitude, 'lang': 'ru_RU', 'limit': dayf},
                                   headers={'X-Yandex-API-Key': token}) as response:
                response = await response.json()
                return obr_forecasts(response['forecasts'])

