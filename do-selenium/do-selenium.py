from selenium import webdriver
from bs4 import BeautifulSoup
driver = webdriver.Chrome('./../chromedriver')
driver.implicitly_wait(3)

driver.get('https://nid.naver.com/nidlogin.login')

# id, pw 입력
driver.find_element_by_name('id').send_keys('rlagur9286')
driver.find_element_by_name('pw').send_keys('rlagur5252')

# 로그인 버튼 클릭
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

driver.get('https://order.pay.naver.com/home') # Naver 페이 들어가기
html = driver.page_source # 페이지의 elements모두 가져오기
soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup사용하기
notices = soup.select('div.p_inr > div.p_info > a > span')

for n in notices:
    print(n.text.strip())