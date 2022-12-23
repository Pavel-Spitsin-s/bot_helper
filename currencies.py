import datetime
import random
import aiogram
import dateutils
import dateutil.parser as dparser
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import xmltodict
import requests, json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pymorphy2

BOT_TOKEN = ''

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def message_handler(message: types.Message):
    if 'валют' in message.text.lower():
        b = val(datetime.date.today())
        c = valuta(b)
        await message.answer(c[2]+'\n'+c[9]+'\n'+c[10]+'\n'+c[32]+'\n'+c[33])
    else:
        s = message.text
        b = val(datetime.date.today())
        c = valuta(b)
        graphic(s)
        await message.answer_photo(open('/project/graphic.png', 'rb'), c[q[s]])


m = ('Австралийский доллар', 'Азербайджанский манат', 'Фунт стерлингов Соединенного королевства',
     'Армянские драмы', 'Белорусский рубль', 'Болгарский лев', 'Бразильский реал',
     'Венгерские форинты', 'Гонконгских доллары', 'Датские кроны', 'Доллар США', 'Евро',
     'Индийские рупии', 'Казахстанские тенге', 'Канадский доллар', 'Киргизские сомы',
     'Китайские юани', 'Молдавские леи', 'Норвежские кроны', 'Польский злотый',
     'Румынский лей', 'СДР (специальные права заимствования)', 'Сингапурский доллар',
     'Таджикские сомони', 'Турецкие лиры', 'Новый туркменский манат', 'Узбекские сумы',
     'Украинские гривны', 'Чешские кроны', 'Шведские кроны', 'Швейцарские франки',
     'Южноафриканские рэнды', 'Вон Республики Корея', 'Японские иены')

q = {'Австралийский доллар': 0, 'Азербайджанский манат': 1, 'Фунт стерлингов Соединенного королевства': 2,
     'Армянские драмы': 3, 'Белорусский рубль': 4, 'Болгарский лев': 5, 'Бразильский реал': 6,
     'Венгерские форинты': 7, 'Гонконгских доллары': 8, 'Датские кроны': 9, 'Доллар США': 10, 'Евро': 11,
     'Индийские рупии': 12, 'Казахстанские тенге': 13, 'Канадский доллар': 14, 'Киргизские сомы': 15,
     'Китайские юани': 16, 'Молдавские леи': 17, 'Норвежские кроны': 18, 'Польский злотый': 19,
     'Румынский лей': 20, 'СДР (специальные права заимствования)': 21, 'Сингапурский доллар': 22,
     'Таджикские сомони': 23, 'Турецкие лиры': 24, 'Новый туркменский манат': 25, 'Узбекские сумы': 26,
     'Украинские гривны': 27, 'Чешские кроны': 28, 'Шведские кроны': 29, 'Швейцарские франки': 30,
     'Южноафриканские рэнды': 31, 'Вон Республики Корея': 32, 'Японские иены': 33}




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
    save_results_to = '/project/'
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