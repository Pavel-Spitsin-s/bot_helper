from intents.jokes_gen import get_joke
from intents.select_film import select_film
from intents.select_series import select_series
from intents.last_news import last_news
from intents.talking import get_next_sequence
from intents.add_reminder import add_reminder
from intents.weather import weather_handler
from intents.currencies import currencies_handler
from generate.slot_detection_tune import message_to_tag


async def classify(text, user):
    tags = {}

    if ('anek' in tags.keys()) or ('анек' in text):
        return ['анекдот', await get_joke()]
    elif ('film' in tags.keys()) or ('фильм' in text):
        return ['фильм', await select_film()]
    elif ('serial' in tags.keys()) or ('сериал' in text):
        return ['сериал', await select_series()]
    elif (any(w in tags.keys() for w in ('news', 'last_news'))) or ('новост' in text):
        return ['новость', await last_news()]
    elif any(w in tags.keys() for w in ['currency', 'currency_name']) or any(w in text for w in ['курс', 'доллар сша']):
        return ['валюты', await currencies_handler(text)]
    elif ('reminder' in tags.keys()) or any(w in text for w in ['напомн', 'напомин']):
        return ['напоминание', await add_reminder(text, user)]
    elif 'weather_descriptor' in tags.keys() or 'погода' in text:
        return ['погода', await weather_handler(text, user)]
    else:
        return ['болталка', await get_next_sequence(text, user, 0)]
