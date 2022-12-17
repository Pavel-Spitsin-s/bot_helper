import os
import aiohttp

conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
              'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
              'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
              'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
              'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
              'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
              'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
              }
wind_dirs = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
             'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль'}
type_prec = {'0': 'без осадков', '1': 'дождь', '2': 'дождь со снегом', '3': 'снег', '4': 'град'}
clowness = {'0': 'ясно', '0.25': 'малооблачно', '0.5': 'облачно с прояснениями', '0.75': 'облачно с прояснениями',
            '1': 'пасмурно'}

WEATHER_API_URL = "https://api.weather.yandex.ru/v2/forecast?"
def get_today_weather(dan):
    s = ''
    b = {}
    b['температура'] = dan['fact']['temp']
    s = dan['fact']['condition']
    b['осадки'] = conditions[s]
    b['скорость ветра'] = dan['fact']['wind_speed']
    s = dan['fact']['wind_dir']
    b['направление ветра'] = wind_dirs[s]
    b['влажность'] = dan['fact']['humidity']
    s = dan['fact']['prec_type']
    b['тип осадков'] = type_prec[str(s)]
    s = dan['facts']['cloudness']
    b['ясность'] = str(clowness[str(s)])
    b['давление'] = dan['fact']['pressure_mm']
    return b


def obr_forecasts(dan):
    s = ''
    A = []
    for i in range(len(dan)):
        b = {}
        b['дата'] = dan[i]['date']
        b['температура'] = dan[i]['parts']['day_short']['feels_like']
        s = dan[i]['parts']['day_short']['condition']
        b['осадки'] = conditions[s]
        b['скорость ветра'] = dan[i]['parts']['day_short']['wind_speed']
        s = dan[i]['parts']['day_short']['wind_dir']
        b['направление ветра'] = wind_dirs[s]
        b['влажность'] = dan[i]['parts']['day_short']['humidity']
        s = dan[i]['parts']['day_short']['prec_type']
        b['тип осадков'] = type_prec[str(s)]
        s = dan[i]['parts']['day_short']['cloudness']
        b['ясность'] = str(clowness[str(s)])
        b['давление'] = dan[i]['parts']['day_short']['pressure_mm']
        A.append(b)
    return A


async def get_weather(latitude, longitude, dayf):
    token = os.getenv('WEATHER_APIKEY')
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_API_URL,
                               params={'lat': latitude, 'lon': longitude, 'lang': 'ru_RU', 'limit': dayf},
                               headers={'X-Yandex-API-Key': token}) as response:
            response = await response.json()
            return obr_forecasts(response['forecasts'])
