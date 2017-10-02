import requests
import time
from PIL import Image as PILImage
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()

headers = {
    'Referer': 'http://comic.naver.com/webtoon/detail.nhn?titleId=119874&no=1015&weekday=tue',
    'User-Agent': ua.ie
}

URL = 'http://comic.naver.com/webtoon/weekdayList.nhn?week=mon'
BASE_URL = 'http://comic.naver.com'

while True:
    html = requests.get(URL, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')

    webtoon_list = soup.select('.img_list li dt')

    for webtoon in webtoon_list:
        # 해당 요일의 모든 웹툰의 제목과 URL GET
        title = webtoon.find('a').get('title')
        href = webtoon.find('a').get('href')

        # title 이름으로 파일 생성
        with open(title, 'a', encoding='utf-8') as f:
            while True:
                try:
                    html = requests.get(BASE_URL + href, headers=headers, timeout=5.0).text
                    soup = BeautifulSoup(html, 'html.parser')

                    viewList = soup.select('.viewList .title')
                    for idx, view in enumerate(viewList, 1):
                        title = view.find('a').text
                        href = BASE_URL + view.find('a').get('href')
                        f.write('{},{}\n'.format(title, href))

                    if soup.select('#content > div.paginate > div > a.next'):
                        URL = BASE_URL + soup.select('#content > div.paginate > div > a.next')[0].get('href')
                    else:
                        break
                except Exception as e:
                    print(e)

