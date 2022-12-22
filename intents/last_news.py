import aiohttp
import requests
from bs4 import BeautifulSoup as bs


async def last_news():
    link = 'https://ria.ru/'
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as res:
            soup = bs(await res.text(), 'html.parser')
            url = soup.find('a', class_='cell-main-photo__link').get('href')

        async with session.get(url) as res:
            soup = bs(await res.text(), 'html.parser')

            title = soup.find('div', class_='article__title').text
            texts = soup.find_all('div', class_='article__text')
            text = '\n'.join([i.text for i in texts])
            return f'{title}\n\n{text}'
