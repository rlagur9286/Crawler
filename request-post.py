import requests
import json

request_headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
                                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'),
                   'Referer': 'http://httpbin.org', }

get_params = {'k1': 'v1', 'k2': 'v2'}

response = requests.post('http://httpbin.org/post',
                         headers=request_headers,
                         params=get_params)

print(response.text)

# ---------------------------------------------------------------------------------------------
# form 형태로 데이터 보내기

data = {'k1': 'v1', 'k2': 'v2'}
response = requests.post('http://httpbin.org/post', data=data)
print(response.json())

# ---------------------------------------------------------------------------------------------
# json Type으로 data 보내기
json_data = {'k1': 'v1', 'k2': [1, 2, 3], 'name': 'hyuk'}
json_string = json.dumps(json_data)
response = requests.post('http://httpbin.org/post', data=json_string)
print(response.json())

# ---------------------------------------------------------------------------------------------
# file data 보내기
# tuple 형태로 같은 이름에 이미지 여러개 업로드도 가능 나머지 데이터는 form으로 감
files = {'photo1': open('f1.jpg', 'rb'),  # 데이터만 전송
         'photo2': open('f2.jpg', 'rb'),
         'photo3': ('f3.jpg', open('f3.jpg', 'rb'), 'image/jpeg', {'Expires': '0'}),
         }
post_params = {'k1': 'v1'}
response = requests.post('http://httpbin.org/post', files=files, data=post_params)
