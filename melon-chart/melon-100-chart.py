import requests
import re
from bs4 import BeautifulSoup

melon_url = 'http://www.melon.com/chart/index.htm'

html = requests.get(melon_url).text
soup = BeautifulSoup(html, 'html.parser')

for data in soup.select('#tb_list .wrap_song_info a'):
    title = data.text
    mathced = re.search(r",(\d+)\)", data.get('href'))
    if mathced:
        song_id = mathced.group(1)
        detail_url = 'http://www.melon.com/song/detail.htm?songId=' + song_id
        print(title, detail_url)