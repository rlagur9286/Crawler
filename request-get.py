import requests
from bs4 import BeautifulSoup

# get_params = (('k1', 'v1'), ('k1', 'v3'), ('k2', 'v2'))   # 튜플의 튜플 형태로
get_params = [('k1', 'v1'), ('k1', 'v3'), ('k2', 'v2')]  # 튜플의 List 형태로
response = requests.get('http://httpbin.org/get', params=get_params)
print(response.text)
print(response.json().get('args'))
# print(response.ok) # => 응답 상태
# print(response.status_code) # => 상태 코드

print(response.headers['content-type']) # header는 CaseInsensitiveDict 타입 대소문자 구별 x

bytes_data = response.content  # 응답 Raw 데이터(bytes)
str_data = response.text  # response.encoding 으로 디코딩하여 유니코드 변환

# 이미지 데이터일 경우에는 .content 만 사용
with open('flower.jpg', 'wb') as f:
    f.write(response.content)

# 문자열 데이터일 경우에는 .text를 사용
html = response.text

# 문자열이 깨지는 경우 encoding 문제!!!
response.encoding = 'euc-kr'
response.text

# 또는
response.text.decode('euc-kr')

"""
request_headers = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'),
    'Referer': 'http://news.naver.com/main/home.nhn',
}

response = requests.get('http://news.naver.com/main/home.nhn', headers=request_headers)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

for tag in soup.select('a[href*=sectionList.nhn]'):
    print(tag.text.strip())
"""