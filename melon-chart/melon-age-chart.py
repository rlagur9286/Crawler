import requests
import re
from bs4 import BeautifulSoup

age_url = 'http://www.melon.com/chart/age/list.htm'

params = {
    'idx': 1,
    'chartType': 'YE',
    'chartGenre': 'KPOP',
    'chartDate': 2010,
    'moved': 'Y'
}

html = requests.get(age_url, params=params).text
soup = BeautifulSoup(html, 'html.parser')

for data in soup.select('.tb_list a[href*=playSong]'):
    title = data.text
    mathced = re.search(r"'(\d+)'\)", data.get('href'))
    if mathced:
        song_id = mathced.group(1)
        detail_url = 'http://www.melon.com/song/detail.htm?songId=' + song_id
        print(title, detail_url)