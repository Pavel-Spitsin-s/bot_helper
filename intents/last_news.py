import requests
from bs4 import BeautifulSoup as bs


def last_news():
    link = 'https://ria.ru/'
    req = requests.get(link)

    soup = bs(req.text, 'html.parser')
    url = soup.find('a', class_='cell-main-photo__link').get('href')

    newr = requests.get(url)
    newsoup = bs(newr.text, 'html.parser')

    title = newsoup.find('div', class_='article__title').text
    texts = newsoup.find_all('div', class_='article__text')
    text = '\n'.join([i.text for i in texts])
    return f'{title}\n\n{text}'
