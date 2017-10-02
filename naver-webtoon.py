import os
import requests

image_urls = [
    'http://imgcomic.naver.net/webtoon/119874/1065/20170928164345_2ba16125d996035cd6ffaedba192a23b_IMAG01_1.jpg',
    'http://imgcomic.naver.net/webtoon/119874/1065/20170928164345_2ba16125d996035cd6ffaedba192a23b_IMAG01_2.jpg',
    'http://imgcomic.naver.net/webtoon/119874/1065/20170928164345_2ba16125d996035cd6ffaedba192a23b_IMAG01_3.jpg',
]

for image_url in image_urls:
    # 지나온 페이지 Referer!
    headers = {
        'Referer': 'http://comic.naver.com/webtoon/detail.nhn?titleId=119874&no=1015&weekday=tue',
    }
    response = requests.get(image_url, headers=headers)
    image_data = response.content
    filename = os.path.basename(image_url)
    with open(filename, 'wb') as f:
        print('writing to {} ({} bytes)'.format(filename, len(image_data)))
        f.write(image_data)