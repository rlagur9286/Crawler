import requests
import os
from PIL import Image as PILImage
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from itertools import count
from collections import OrderedDict
from urllib.parse import urljoin

BASE_URL = 'http://comic.naver.com'
ua = UserAgent()
headers = {
    'User-Agent': ua.ie
}


def get_list(week):
    URL = 'http://comic.naver.com/webtoon/weekdayList.nhn'
    params = {
        'week': week,
    }
    html = requests.get(URL, headers=headers, params=params).text
    soup = BeautifulSoup(html, 'html.parser')

    webtoon_list = soup.select('.img_list li dt')

    for webtoon in webtoon_list:
        # 해당 요일의 모든 웹툰의 제목과 URL GET
        title = webtoon.find('a').get('title')
        href = webtoon.find('a').get('href')
        toon_url = urljoin(BASE_URL, href)

        ep_dict = OrderedDict()

        # 웹툰별로 모든 페이지에 대해서 detail url을 얻어서 이름.txt 파일에 저장
        print(title, toon_url)
        done = False
        for page in count(1):
            if done:
                break
            params = {
                'page': page,
            }

            html = requests.get(toon_url, params=params).text
            webtoon_soup = BeautifulSoup(html, 'html.parser')
            writer = webtoon_soup.select('.wrt_nm')[0].text.strip()

            viewList = webtoon_soup.select('.viewList tr')
            with open(os.path.join('webtoons', title + '.txt'), 'a', encoding='utf-8') as f:
                for view in viewList:
                    try:
                        tag = view.select('a[href*=detail.nhn]')[0]
                    except IndexError:
                        continue
                    img_tag = tag.find('img')

                    is_new = bool(view.select('img[src*=toonup]'))
                    ep_url = urljoin(toon_url, tag.get('href'))

                    ep = {
                        'title': img_tag.get('title'),
                        'img_url': img_tag.get('src'),
                        'ep_url': ep_url,
                        'writer': writer,
                    }

                    if ep_url in ep_dict:
                        done = True
                        break
                    f.write('{}\t{}\t{}\t{}\n'.format(ep.get('title'), ep.get('img_url'), ep.get('ep_url'), ep.get('writer')))
                    ep_dict[ep_url] = ep


def ep_download(dir_name):
    webtoon_list = os.listdir(dir_name)
    for webtoon in webtoon_list:
        if os.path.isdir(os.path.join(dir_name, webtoon)):
            continue
        with open(os.path.join('webtoons', webtoon), 'r', encoding='utf-8') as f:
            print(webtoon, '시작')
            webtoon_info_list = f.readlines()
            for info in webtoon_info_list:
                title = info.split('\t')[0].replace('?', '').replace('!', '').replace('<', '').replace('>', '')\
                    .replace('*', '').replace(':', '').replace('.', '').replace('/', '-').strip()
                detail_url = info.split('\t')[2]
                writer = info.split('\t')[3].strip().replace('/', '-')

                if os.path.exists(os.path.join(dir_name, webtoon.split('.')[0] + '-' + writer, title)):
                    continue

                html = requests.get(detail_url, headers=headers).text
                ep_soup = BeautifulSoup(html, 'html.parser')
                img_list = ep_soup.select('.wt_viewer img')

                img_path_list = []
                for img in img_list:
                    img_src = img.get('src')
                    headers['Referer'] = detail_url

                    img_name = os.path.basename(img_src)
                    img_path = os.path.join('webtoons', webtoon.split('.')[0] + '-' + writer, title, img_name)
                    img_path_list.append(img_path)

                    dir_path = os.path.dirname(img_path)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)

                    if not os.path.exists(img_path):
                        img_data = requests.get(img_src, headers=headers).content

                        with open(img_path, 'wb') as img_file:
                            img_file.write(img_data)

                im_list = []
                for path in img_path_list:
                    im = PILImage.open(path)
                    im_list.append(im)

                canvas_size = (max(im.width for im in im_list), min(65500, sum(im.height for im in im_list)))

                canvas = PILImage.new('RGB', canvas_size, (255, 255, 255))
                left = 0
                top = 0
                for im in im_list:
                    canvas.paste(im, (left, top))
                    top += im.height
                canvas.save(os.path.join(dir_path, title + '.jpg'))

if __name__ == '__main__':
    # get_list(week='mon')
    ep_download(dir_name='webtoons')