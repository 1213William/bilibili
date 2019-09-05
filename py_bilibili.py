import requests
import pymongo
from bs4 import BeautifulSoup
from threading import Thread
from bilibili.config import *


client = pymongo.MongoClient('localhost', connect=False)
db = client[MONGO_D]


def get_html(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(e)


def get_page_html(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    return soup.select('li.video-item')


def get_content(user_list):
    for data in user_list:
        # 利用contents挨个往下面找，直到到自己想要的那一层标签
        link_all = data.contents[0]['href']
        link = 'https:' + link_all
        title = data.contents[0]['title']
        num = data.contents[1].contents[2].contents[0].text
        info = {
            'title': title,
            'link': link,
            'num': num.strip()
        }
        yield info


def main(keyword, offset):
    url = 'https://search.bilibili.com/all?keyword=%s&from_source=banner_search&page=%s' % (keyword, offset)
    html = get_html(url)
    res = get_page_html(html)
    for i in get_content(res):
        # db[MONGO_T].insert(i)
        print(i)
        # print('Successfully insert!!!')


if __name__ == '__main__':
    lst = []
    for i in range(START, END):
        t = Thread(target=main, args=(KEYWORD, i,))
        t.start()
        lst.append(t)
    for i in lst:
        i.join()
