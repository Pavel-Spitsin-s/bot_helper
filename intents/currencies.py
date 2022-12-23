import datetime
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import xmltodict
import requests, json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pymorphy2


def make_response(text, photo=None):
    return {
        'text': text,
        'photo': photo
    }


async def currencies_handler(text):
    if 'валют' in text.lower() or 'валюты' in text.lower():
        b = val(datetime.date.today())
        c = valuta(b)
        return make_response(
            c[2] + '\n' + c[9] + '\n' + c[10] + '\n' + c[32] + '\n' + c[33]
        )
    else:
        text = text.split()
        for i in range(len(text)):
            morph = pymorphy2.MorphAnalyzer()
            word = morph.parse(text[i].lower())[0]
            if word.inflect({'nomn'}).word == "доллар" or word.inflect({'nomn'}).word == "доллары":
                s = "доллар сша"
                b = val(datetime.date.today())
                c = valuta(b)
                graphic(s)
                return make_response(
                    c[q[s]],
                    photo=open('graphic-tmp.png', 'rb')
                )
            elif word.inflect({'nomn'}).word == "фунт" or word.inflect({'nomn'}).word == "фунты":
                s = "фунт стерлингов соединенного королевства"
                b = val(datetime.date.today())
                c = valuta(b)
                graphic(s)
                return make_response(
                    c[q[s]],
                    photo=open('graphic-tmp.png', 'rb')
                )
            elif word.inflect({'nomn'}).word == "евро" or word.inflect({'nomn'}).word == "евро":
                s = "евро"
                b = val(datetime.date.today())
                c = valuta(b)
                graphic(s)
                return make_response(
                    c[q[s]],
                    photo=open('graphic-tmp.png', 'rb')
                )
            elif word.inflect({'nomn'}).word == "вон" or word.inflect({'nomn'}).word == "воны":
                s = "вон республики корея"
                b = val(datetime.date.today())
                c = valuta(b)
                graphic(s)
                return make_response(
                    c[q[s]],
                    photo=open('graphic-tmp.png', 'rb')
                )
            elif word.inflect({'nomn'}).word == "иен" or word.inflect({'nomn'}).word == "иены":
                s = "японские иены"
                b = val(datetime.date.today())
                c = valuta(b)
                graphic(s)
                return make_response(
                    c[q[s]],
                    photo=open('graphic-tmp.png', 'rb')
                )
            elif word.inflect({'nomn'}).word == "тенге" or word.inflect({'nomn'}).word == "тенге":
                s = "казахстанские тенге"
                b = val(datetime.date.today())
                c = valuta(b)
                graphic(s)
                return make_response(
                    c[q[s]],
                    photo=open('graphic-tmp.png', 'rb')
                )
        else:
            return make_response(
                "не понимаю"
            )


m = ('австралийский доллар', 'азербайджанский манат', 'фунт стерлингов соединенного королевства',
     'армянские драмы', 'белорусский рубль', 'болгарский лев', 'бразильский реал',
     'венгерские форинты', 'гонконгских доллары', 'датские кроны', 'доллар сша', 'евро',
     'индийские рупии', 'казахстанские тенге', 'канадский доллар', 'киргизские сомы',
     'китайские юани', 'молдавские леи', 'норвежские кроны', 'польский злотый',
     'румынский лей', 'сдр (специальные права заимствования)', 'сингапурский доллар',
     'таджикские сомони', 'турецкие лиры', 'новый туркменский манат', 'узбекские сумы',
     'украинские гривны', 'чешские кроны', 'шведские кроны', 'швейцарские франки',
     'южноафриканские рэнды', 'вон республики корея', 'японские иены')

q = {'австралийский доллар': 0, 'азербайджанский манат': 1, 'фунт стерлингов соединенного королевства': 2,
     'армянские драмы': 3, 'белорусский рубль': 4, 'болгарский лев': 5, 'бразильский реал': 6,
     'венгерские форинты': 7, 'гонконгских доллары': 8, 'датские кроны': 9, 'доллар сша': 10, 'евро': 11,
     'индийские рупии': 12, 'казахстанские тенге': 13, 'канадский доллар': 14, 'киргизские сомы': 15,
     'китайские юани': 16, 'молдавские леи': 17, 'норвежские кроны': 18, 'польский злотый': 19,
     'румынский лей': 20, 'сдр (специальные права заимствования)': 21, 'сингапурский доллар': 22,
     'таджикские сомони': 23, 'турецкие лиры': 24, 'новый туркменский манат': 25, 'узбекские сумы': 26,
     'украинские гривны': 27, 'чешские кроны': 28, 'шведские кроны': 29, 'швейцарские франки': 30,
     'южноафриканские рэнды': 31, 'вон республики корея': 32, 'японские иены': 33}


def graphic(n):
    a = []
    c = []
    # for i in range(32):
    for i in range(7):
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
        word1 = morph.parse(n[0])[0]1
        word2 = morph.parse(n[1])[0]'''
    # x = np.arange(32)
    x = np.arange(7)
    y = np.array(a[::-1])
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # ax1.set_xticklabels(['00.00'] + c[::5])
    ax1.set_xticklabels(['00.00'] + c)
    plt.title("график изменения")
    ax1.plot(x, y, color="red")
    plt.savefig('graphic-tmp.png', dpi=300)
    '''word1.inflect({'gent'}).word+" "+word2.inflect({'gent'}).word'''
    #that


def valuta(p):
    a = []
    for i in range(len(p)):
        d = p[i]['Nominal'] + ' ' + p[i]['Name'] + ': ' + p[i]['Value'] + ' руб'
        a.append(d)
    return a


def val(date):
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    res = requests.get(url,
                       params={"date_req": date.strftime('%d/%m/%Y')})
    p = xmltodict.parse(res.text)
    return p['ValCurs']['Valute']

