import requests
import json
from bs4 import BeautifulSoup

request_url = 'https://www.bigkinds.or.kr/news/newsResult.do'
raw_data = """pageInfo:main
login_chk:null
LOGIN_SN:null
LOGIN_NAME:null
indexName:news
keyword:문재인
byLine:
searchScope:1
searchFtr:1
startDate:2017-07-04
endDate:2017-10-04
sortMethod:date
contentLength:100
providerCode:
categoryCode:
incidentCode:
dateCode:
highlighting:true
sessionUSID:
sessionUUID:test
listMode:
categoryTab:
newsId:
delnewsId:
delquotationtxt:
filterProviderCode:
filterCategoryCode:
filterIncidentCode:
filterDateCode:
filterAnalysisCode:
startNo:1
resultNumber:10
topmenuoff:
resultState:
keywordJson:
keywordFilterJson:
realKeyword:
totalCount:
interval:
quotationKeyword1:
quotationKeyword2:
quotationKeyword3:
searchFromUseYN:N
mainTodayPersonYn:
period:3month"""

split_data = raw_data.splitlines()
dict_data = {}

for data in split_data:
    key, value = data.split(':', 1)
    if value == 'null':
        value = None
    dict_data[key] = value


response = requests.post(request_url, data=dict_data)
print(response)

html = response.text

soup = BeautifulSoup(html, 'html.parser')
list = soup.select('#resultNews li a h3')
file = open('news.json', 'a', encoding='utf-8')

for data in list:
    doc_id = data.get('id').replace('news_', '')
    doc_url = 'https://www.bigkinds.or.kr/news/detailView.do?docId={}&returnCnt=1&sectionDiv=1000'.format(doc_id)
    data_json = json.loads(requests.get(doc_url).text)
    json.dump(data_json, file, ensure_ascii=False)