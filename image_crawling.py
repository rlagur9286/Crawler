import os
from PIL import Image as PILImage
import requests

"""
# ---------------------------------------------------------------------------------------------
# Case 1) 이미지를 다운받기
# requests의 response.content는 응답원본 : bytes 타입

image_url = ('https://ee5817f8e2e9a2e34042-3365e7f0719651e5b'
             '8d0979bce83c558.ssl.cf5.rackcdn.com/python.png')
image = requests.get(image_url).content # 서버응답을 받아, 파일내용 획득
filename = os.path.basename(image_url) # URL에서 파일명 획득
with open(filename, 'wb') as f:
    f.write(image)

"""

"""
# ---------------------------------------------------------------------------------------------
# Case 2) 이미지 품질 낮추기
# 다른 포맷으로 변경하기

WHITE = (255, 255, 255)  # RGB color
with PILImage.open('python.png') as im:
    # im.save('python3.jpg', quality=80)  # quality 옵션은 jpg에서만 유효

    with PILImage.new('RGBA', im.size, WHITE) as canvas:
        # alpha채널을 살리며, canvas 베이스에 im를 합성
        canvas_im = PILImage.alpha_composite(canvas, im)
        canvas_im.save('python3_bg_white.jpg', quality=80)

"""

"""
[#] ---------------------------------------------------------------------------------------------
# Case 3) 가로 세로 크기 줄이기

with PILImage.open("python.png") as im:
    im.thumbnail((300, 300))
    im.save("python_300_300.png")
"""

"""
# ---------------------------------------------------------------------------------------------
# Case 4) 이미지 이어 붙이기
# 투명을 살리고 싶으면, alpha_composite 활용 and RGBA 사용
WHITE = (255, 255, 255)
with PILImage.open('img1.jpg') as im1:
    with PILImage.open('img2.jpg') as im2:
        # 이미지 2개를 세로로 이어서 붙일려고 합니다.
        width = max(im1.width, im2.width)
        height = sum(im1.height, im2.height)
        size = (width, height)
        with PILImage.new('RGB', size, WHITE) as canvas:
            canvas.paste(im1, box=(0, 0))  # left/top 지정
            canvas.paste(im2, box=(0, im1.height))  # left/top 지정
            canvas.save('canvas.jpg')

"""

# ---------------------------------------------------------------------------------------------
# Case 5) 네이버 웹툰 합치기
headers = {
    'Referer': 'http://comic.naver.com/webtoon/detail.nhn?titleId=20853&no=1093&weekday=tue',
}
img1_data = requests.get('http://imgcomic.naver.net/webtoon/20853/1093/20170529163407_0ed8a697d896451fee4bc3642fb46db8_IMAG01_1.jpg', headers=headers).content
img2_data = requests.get('http://imgcomic.naver.net/webtoon/20853/1093/20170529163407_0ed8a697d896451fee4bc3642fb46db8_IMAG01_2.jpg', headers=headers).content

with open('img1.jpg', 'wb') as f:
    f.write(img1_data)

with open('img2.jpg', 'wb') as f:
    f.write(img2_data)

WHITE = (255, 255, 255)
with PILImage.open('img1.jpg') as img1:
    with PILImage.open('img2.jpg') as img2:
        width = max(img1.width, img2.width)
        height = img1.height + img2.height
        new_image_size = (width, height)

        with PILImage.new('RGB', new_image_size, WHITE) as canvas:
            canvas.paste(img1, (0, 0))  # box = (left top)
            canvas.paste(img2, (0, img1.height))
            canvas.save('image_merge.jpg')
