from bs4 import BeautifulSoup
import requests
"""
# ---------------------------------------------------------------------------------------------
# 직접 html 계층 구조 파악해서 find로 찾아서 가져오기

html = requests.get('http://www.melon.com/chart/index.htm').text
soup = BeautifulSoup(html, 'html.parser')
# soup = BeautifulSoup(html, 'lxml')  # html.parser보다 유연한 처리 가능
tag_list = []

for tr_tag in soup.find(id='tb_list').find_all('tr'):
    tag = tr_tag.find(class_='wrap_song_info')
    if tag:
        tag_sub_list = tag.find_all(href=lambda value: (value and 'playSong' in value))
        tag_list.extend(tag_sub_list)

for (idx, tag) in enumerate(tag_list, 1):
    print(idx, tag)
"""

"""
# ---------------------------------------------------------------------------------------------
# css selector 문법을 사용해서 가져오기
# selector 지정할 때는 최대한 rough 하게
html = requests.get('http://www.melon.com/chart/index.htm').text
soup = BeautifulSoup(html, 'html.parser')

tag_list = soup.select('#tb_list tr .wrap_song_info a[href*=playSong]')  # 아이디가 tb_list 이고 직계인줄은 모르겠지만 자식중에 tr
for idx, tag in enumerate(tag_list, 1):                                 #을 찾아서 class가 wrap_song_info이고 a속성의 href tag에 playSong이 포함된 리스트를 가져옴
    print(idx, tag.text)

"""

"""
# ---------------------------------------------------------------------------------------------
# 구글 finance 페이지 가져오기
params = {
 'q': 'EPA:BRNTB',
 'startdate': 'Jan 01, 2016',
 'enddate': 'Jun 02, 2016',
}

response = requests.get('https://www.google.com/finance/historical', params=params)
html = response.text
print(response.request.url)
soup = BeautifulSoup(html, 'lxml') #'html.parser')
for tr_tag in soup.select('#prices > table > tr'):
    row = [td_tag.text.strip() for td_tag in tr_tag.select('th, td')]
    print(row)
"""

# ---------------------------------------------------------------------------------------------
# reddit 가져오기 user-agent 조작
from fake_useragent import UserAgent
ua = UserAgent()

print(ua.ie)
response = requests.get("https://www.reddit.com/", headers={'User-Agent': ua.ie})
html = response.text
soup = BeautifulSoup(html, 'html.parser')

for tag in soup.select('#siteTable .thing'):
    score = tag.select('.score.unvoted')[0].get('title', None)
    name = tag.find('a', class_='title').text
    print(score, name)
