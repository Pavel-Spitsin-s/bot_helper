import datetime
import random
import aiogram
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import xmltodict
import requests, json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pymorphy2

BOT_TOKEN = '5954009166:AAHHfPlaoQmEA9eHAdgSSssdJ7fNGoviMLQ'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def message_handler(message: types.Message):
    if 'валют' in message.text.lower():
        b = val(datetime.date.today())
        c = valuta(b)
        await message.answer(c[2]+'\n'+c[9]+'\n'+c[10]+'\n'+c[32]+'\n'+c[33])
    else:
        graphic('Евро')
        await message.answer_photo(open('graphic.png', 'rb'))



q = {'Австралийский доллар': '0', 'Азербайджанский манат': '1', 'Фунт стерлингов Соединенного королевства': '2',
     'Армянских драмов': '3', 'Белорусский рубль': '4', 'Болгарский лев': '5', 'Бразильский реал': '6',
     'Венгерских форинтов': '7', 'Гонконгских долларов': '8', 'Датских крон': '9', 'Доллар США': '10', 'Евро': '11',
     'Индийских рупий': '12', 'Казахстанских тенге': '13', 'Канадский доллар': '14', 'Киргизских сомов': '15',
     'Китайских юаней': '16', 'Молдавских леев': '17', 'Норвежских крон': '18', 'Польский злотый': '19',
     'Румынский лей': '20', 'СДР (специальные права заимствования)': '21', 'Сингапурский доллар': '22',
     'Таджикских сомони': '23', 'Турецких лир': '24', 'Новый туркменский манат': '25', 'Узбекских сумов': '26',
     'Украинских гривен': '27', 'Чешских крон': '28', 'Шведских крон': '29', 'Швейцарский франк': '30',
     'Южноафриканских рэндов': '31', 'Вон Республики Корея': '32', 'Японские иены': '33'}


def graphic(n):
    a = []
    c = []
    for i in range(32):
        s = datetime.datetime.now() - datetime.timedelta(days=i)
        c.append(str(s.day) + '.' + str(s.month))
        f = val(s)
        b = f[int(q[n])]['Value']
        b = b.split(',')
        b = b[0] + '.' + b[1]
        b = float(b)
        a.append(b)
    c = c[::-1]
    '''morph = pymorphy2.MorphAnalyzer()
    if n!='Евро':
        n = n.split()
        word1 = morph.parse(n[0])[0]
        word2 = morph.parse(n[1])[0]'''
    save_results_to = '/Users/Dmitry/Desktop/place'
    x = np.arange(32)
    y = np.array(a[::-1])
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_xticklabels(['00.00'] + c[::5])
    plt.title("Курс изменения "+"за месяц")
    ax1.plot(x, y, color="red")
    plt.savefig(save_results_to+'graphic.png', dpi=300)
    '''word1.inflect({'gent'}).word+" "+word2.inflect({'gent'}).word'''


def valuta(p):
    a = []
    for i in range(len(p)):
        d = p[i]['Nominal'] + ' ' + p[i]['Name'] + ': ' + p[i]['Value']+' руб'
        a.append(d)
    return a

def val(date):
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    res = requests.get(url,
                       params={"date_req": date.strftime('%d/%m/%Y')})
    p = xmltodict.parse(res.text)
    return p['ValCurs']['Valute']


# graphic('Доллар США')
executor.start_polling(
    dp,
    skip_updates=True,
)