from intents import JokesGen, SelectFilm, SelectSeries, LastNews


def classify(text):
    if 'анекдот' in text or 'шутк' in text:
        return ['анекдот', JokesGen.get_joke()]
    elif 'фильм' in text or 'кино' in text:
        return ['фильм', SelectFilm.select_film()]
    elif 'сериал' in text:
        return ['сериал', SelectSeries.select_series()]
    elif 'заметка' in text:
        text = text.replace('заметка', 'Заметка:')
        return ['заметка', text]
    elif 'новост' in text or 'ново' in text:
        return ['новость', LastNews.last_news()]
    else:
        return ['болталка', 'Извините, не поняла вас']
