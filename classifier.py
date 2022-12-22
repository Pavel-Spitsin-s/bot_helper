from intents.jokes_gen import *
from intents.select_film import *
from intents.select_series import *
from intents.last_news import *
from intents.talking import *
from intents.add_reminder import *


async def classify(text, user):
    if any(w in text for w in ('анекдот', 'шутк')):
        return ['анекдот', await get_joke()]
    elif any(w in text for w in ('фильм', 'кино')):
        return ['фильм', await select_film()]
    elif any(w in text for w in ('сериал',)):
        return ['сериал', await select_series()]
    elif any(w in text for w in ('заметка',)):
        text = text.replace('заметка', 'Заметка:')
        return ['заметка', text]
    elif any(w in text for w in ('новост',  'ново')):
        return ['новость', await last_news()]
    elif any(w in text for w in ('напомн', 'напомин')):
        return ['напоминание', await add_reminder(text, user)]
    else:
        return ['болталка', await get_next_sequence(text, user, 0)]
