import requests
from bs4 import BeautifulSoup
import json

"""
# ------------------------------------------------------------------
# [level 1] 단순 HTML 크롤링

lv1_url = 'https://askdjango.github.io/lv1/'

html = requests.get(lv1_url).text
soup = BeautifulSoup(html, 'html.parser')

course_list = soup.select('#course_list .course a')

for tag in course_list:
    print(tag.text, tag.get('href'))
"""

"""
# ------------------------------------------------------------------
# [level 2] Ajax 렌더링 크롤링

lv2_data_json_url = 'https://askdjango.github.io/lv2/data.json'
json_string = requests.get(lv2_data_json_url).text

course_list = json.loads(json_string)

for json in course_list:
    # print(json.get('name'), json.get('url'))
    print('{name} {url}'.format(**json))    # 오 신기방기...
"""

# ------------------------------------------------------------------
# [level 3] 자바스크립트 렌더링 크롤링

import re

lv3_url = 'https://askdjango.github.io/lv3/'

html = requests.get(lv3_url).text

# result = re.search(r'var courses = (.+);', html, re.S)  # 만족하는 모든 매칭 중 가장 크게 잡는 방법
result = re.search(r'var courses = (.+?);', html, re.S)  # 만족하는 모든 매칭 중 최소 매칭

course_list = json.loads(result.group(1))

for json in course_list:
    # print(json.get('name'), json.get('url'))
    print('{name} {url}'.format(**json))    # 오 신기방기...