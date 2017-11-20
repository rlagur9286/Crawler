import json
import os
from bs4 import BeautifulSoup
import re
import requests
from webob.compat import urlparse

__author__ = 'moonkwonkim@gmail.com'
# 출처: https://moonkwonkim.github.io/python/2017/11/07/url_parsing.html


class NaverFinanceNewsCrawler:
    URL_NAVER_FINANCE = "http://finance.naver.com"
    URL_NAVER_FINANCE_NEWS_QUERY = "http://finance.naver.com/news/news_search.nhn?q=%s&x=0&y=0" # params: query
    URL_NAVER_FINANCE_NEWS_CODE = "http://finance.naver.com/item/news_news.nhn?code=%s&page=%s" # params: (code, page)
    URL_NAVER_NEWS_FLASH = "http://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258"
    URL_NAVER_STOCK_NOTICE = "http://finance.naver.com/item/news_notice.nhn?code=%s&page=%s" # params: (code, page)

    def __init__(self):
        pass

    def crawl(self, query=None, code=None, page=1):
        """

        :param query:
        :param code:
        :param page:
        :return:
        """
        if query:
            return self._crawl_by_query(query)
        elif code:
            return self._crawl_by_code(code, page=page)
        else:
            raise Exception("[Error] 'query' or 'code' should be entered.")

    def _crawl_by_query(self, query):
        """
        Crawl Naver Finance News
        :param query: string; search keywords
        :return: generator; [{title, summary, url, articleId, content, codes}, ...]
        """

        # Convert the query to euc-kr string
        q = ""
        for c in query.encode('euc-kr'):
            q += "%%%s" % format(c, 'x').capitalize()

        r_url = NaverFinanceNewsCrawler.URL_NAVER_FINANCE_NEWS_QUERY % (q)
        r = requests.get(r_url)

        soup = BeautifulSoup(r.text, "lxml")
        news = soup.find('div', class_='newsSchResult').find('dl', class_='newsList')
        news_title = news.find_all('dt', class_='articleSubject')
        news_summary = news.find_all('dd', class_='articleSummary')
        for title, summary in zip(news_title, news_summary):
            url = NaverFinanceNewsCrawler.URL_NAVER_FINANCE + title.a.get("href")
            res = {
                "title": title.a.text,
                "summary": summary.find(text=True).strip(' \t\n\r'),
                "url": url,
                "articleId": urlparse.parse_qs(urlparse.urlparse(url).query)["article_id"][0]
            }
            res.update(self._crawl_content(url))
            yield res

    def _crawl_by_code(self, code, page=1):
        """
        Crawl Naver Stock News
        :param code: string; a stock code
        :return: generator;
        """

        r_url = NaverFinanceNewsCrawler.URL_NAVER_FINANCE_NEWS_CODE % (code, page)
        r = requests.get(r_url)

        soup = BeautifulSoup(r.text, "lxml")
        news_rows = soup.find('table', class_='type2').find_all('td', class_='title')

        for row in news_rows:
            yield {"title": row.a.text.strip(' \t\n\r'), "url": row.a.get('href')}

    def _crawl_content(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        content = soup.find('div', id="content", class_='articleCont')
        codes = re.findall(r"\d{6}", content.text)
        return {"content": content.text.strip(' \t\n\r'), "codes": codes}

if __name__ == "__main__":
    crawler = NaverFinanceNewsCrawler()
    docs = crawler.crawl(query='삼성전자')
    for i, d in enumerate(docs):
        print("{i}번째 문서".format(i=i+1), end=" " + "-" * 50)
        print("-" * 50)
        print("내용: {content}".format(content=d["content"]))
        print("문서에 포함된 종목 코드: {codes}".format(codes=d["codes"]))