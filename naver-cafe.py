import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import mechanicalsoup
"""
base_url = 'https://m.cafe.naver.com'
list_url = 'https://m.cafe.naver.com/ArticleList.nhn?search.clubid=25158488&search.menuid=3515&search.boardtype=L'
html = requests.get(list_url).text
soup = BeautifulSoup(html, 'html.parser')

for data in soup.select('.list_area .board_box '):
    title = data.find('a').find('strong').text.strip()
    detail_url = urljoin(base_url, data.find('a').get('href'))
    detail_html = requests.get(detail_url).text
    print(detail_html)
    detail_soup = BeautifulSoup(detail_html, 'html.parser')
    # for text in detail_soup.select('.NHN_Writeform_Main'):
        # print(text)

"""
"""
base_url = 'https://m.cafe.naver.com'
ajax_url = 'https://m.cafe.naver.com/ArticleList.nhn'
params = {
    "search.clubid": 25158488,
    "search.menuid": 3515,
    "search.page": 2,
}

html = requests.get(ajax_url).text
soup = BeautifulSoup(html, 'html.parser')

for data in soup.select('li'):
    title = data.find('a').find('strong').text.strip()
    detail_url = urljoin(base_url, data.find('a').get('href'))
    detail_html = requests.get(detail_url).text
    print(detail_html)
    detail_soup = BeautifulSoup(detail_html, 'html.parser')
    for text in detail_soup.select('.NHN_Writeform_Main'):
    print(text)
"""

# ---------------------------------------------------------------------------------------------
# mechanicalSoup을 통한 로그인

base_url = 'https://m.cafe.naver.com'
LOGIN_URL = 'https://nid.naver.com/nidlogin.login?mode=number'
browser = mechanicalsoup.StatefulBrowser()
browser.open(LOGIN_URL)

browser.select_form('#frmNIDLogin')
browser['key'] = '96088929'
browser.submit_selected()
browser.launch_browser()

ajax_url = 'https://m.cafe.naver.com/ArticleList.nhn'
params = {
    "search.clubid": 25158488,
    "search.menuid": 3515,
    "search.page": 2,
}
soup = browser.open(ajax_url, params=params).soup

for data in soup.select('li'):
    title = data.find('a').find('strong').text.strip()
    detail_url = urljoin(base_url, data.find('a').get('href'))

    detail_soup = browser.open(detail_url).soup
    for text in detail_soup.select('.NHN_Writeform_Main'):
        print(text)