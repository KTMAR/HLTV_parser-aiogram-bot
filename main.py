import json

import requests
from bs4 import BeautifulSoup


def get_first_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }
    url = 'https://www.hltv.org/'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_card = soup.find_all('a', class_='newsline article')

    news_dict = {}
    for article in articles_card:
        article_title = article.find('div', class_='newstext').text.strip()
        article_url = f'https://www.hltv.org{article.get("href")}'
        article_date = article.find('div', class_='newsrecent').text.strip()

        article_id = article_url.split('/', 4)[-1]

        # print(f'{article_title} | {article_url} | {article_date}')
        news_dict[article_id] = {
            'article_date': article_date,
            'article_title': article_title,
            'article_url': article_url
        }
    with open('news_dict.json', 'w') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open('news_dict.json') as file:
        news_dict = json.load(file)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }
    url = 'https://www.hltv.org/'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_card = soup.find_all('a', class_='newsline article')

    fresh_news = {}

    for article in articles_card:
        article_url = f'https://www.hltv.org{article.get("href")}'
        article_id = article_url.split('/', 4)[-1]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find('div', class_='newstext').text.strip()
            article_date = article.find('div', class_='newsrecent').text.strip()

            news_dict[article_id] = {
                'article_date': article_date,
                'article_title': article_title,
                'article_url': article_url
            }

            fresh_news[article_id] = {
                'article_date': article_date,
                'article_title': article_title,
                'article_url': article_url
            }

    with open('news_dict.json', 'w') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    # get_first_news()
    print(check_news_update())


if __name__ == '__main__':
    main()
