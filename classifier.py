from intents import JokesGen, SelectFilm, SelectSeries, LastNews, add_reminder, talking


def classify(text, user):
    if any(w in text for w in ('анекдот', 'шутк')):
        return ['анекдот', JokesGen.get_joke()]
    elif any(w in text for w in ('фильм', 'кино')):
        return ['фильм', SelectFilm.select_film()]
    elif any(w in text for w in ('сериал',)):
        return ['сериал', SelectSeries.select_series()]
    elif any(w in text for w in ('заметка',)):
        text = text.replace('заметка', 'Заметка:')
        return ['заметка', text]
    elif any(w in text for w in ('новост',  'ново')):
        return ['новость', LastNews.last_news()]
    elif any(w in text for w in ('напомн', 'напомин')):
        return ['напоминание', add_reminder.add_reminder(text, user)]
    else:
        return ['болталка', talking.get_next_sequence(text, user)]
