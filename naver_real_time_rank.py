import requests
from bs4 import BeautifulSoup

"""
# ------------------------------------------------------------------
# 네이버 실시간 검색 순위 크롤링

html = requests.get('https://www.naver.com/').text
soup = BeautifulSoup(html, 'html.parser')
tag_list = soup.select('.PM_CL_realtimeKeyword_rolling_base .ah_item .ah_k')
for idx, tag in enumerate(tag_list, 1):
    print(idx, tag.text)

"""

"""
# ------------------------------------------------------------------
# 네이버 실시간 검색 순위 크롤링
from fake_useragent import UserAgent
from collections import OrderedDict
from itertools import count
ua = UserAgent()

def naver_search(q, max_page=None):
    headers = {
        'User-Agent': ua.ie
    }
    url = 'https://search.naver.com/search.naver'

    post_dict = OrderedDict()

    for idx in count(0):
        params = {
            'where': 'post',
            'query': q,
            'start': (idx*10) + 1,
        }
        html = requests.get(url, params=params, headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')

        tag_list = soup.select('#elThumbnailResultArea .sh_blog_title ')
        for tag in tag_list:
            if tag.get('href') in post_dict:
                return post_dict
            else:
                post_dict[tag.get('href')] = tag.text

        if max_page and max_page <= idx:
            break
    return post_dict

post_dict = naver_search(q='AskDjango')
print(post_dict)
"""