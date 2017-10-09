import requests
from bs4 import BeautifulSoup
from itertools import count
from urllib.parse import urljoin
from time import sleep


POTBBANG_URL = 'http://www.podbbang.com'


def get_mp3(pid):
    for page in count(1):

        potbbang_episode_url = 'http://www.podbbang.com/podbbangchnew/episode_list'
        params = {
            'id': pid,
            'page': page,
        }
        res = requests.get(potbbang_episode_url, params=params)
        res.encoding = 'utf-8'
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        for data in soup.select('.epi_repeat li'):
            try:
                title = data.find('dt').text
                mp3_url = urljoin(POTBBANG_URL, data.find('a').get('href'))
            except AttributeError:
                return
            else:
                print(title, mp3_url)
                headers = {
                    'Referer': 'http://www.podbbang.com/ch/{}'.format(pid)
                }
                mp3_bin = requests.get(mp3_url, headers=headers).content
                filename = '{}.mp3'.format(title)
                if len(mp3_bin) == 0:
                    print('download fail...')
                    continue
                print('size : ', len(mp3_bin), filename)
                with open(filename, 'wb') as f:
                    f.write(mp3_bin)
            sleep(1)
        return

get_mp3(pid=13942)