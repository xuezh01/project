# -*- coding: utf-8 -*-
# @Time    : 2019/5/27 9:23
# @Author  : project
# @File    : get_news.py
# @Software: PyCharm

import requests
from lxml import etree
from urllib.parse import quote
from retrying import retry
from 关键词搜索新闻.My_SQL import MySql


class SearchNews:
    def __init__(self, word):
        self.word = word
        self.headers = {'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/68.0.3440.106 Safari/537.36 '
                        }

    # 如果请求超时让被装饰的函数反复执行三次，三次全部报错才会报错
    @retry(stop_max_attempt_number=3)
    def _parse_url(self, url, data=None):

        # 随机获取一个请求头
        # headers = GetUserAgent().user_agent_list()
        try:
            if not data:
                response = requests.get(url, headers=self.headers, timeout=3)
            else:
                response = requests.post(url, data=data, headers=self.headers, timeout=3)  # 3秒无响应报错
        except:
            response = None

        return response

    def baidu_news(self):
        """百度新闻"""
        url = 'https://www.baidu.com/s?ie=utf-8&cl=2&rtt=1&bsst=1&rsv_dl=news_t_sk&tn=news&word={}'.format(quote(self.word))
        response = self._parse_url(url)
        content = response.content.decode()
        etree_html = etree.HTML(content)

        # 提取数据并处理
        data = []
        total = etree_html.xpath('//div[@id="header_top_bar"]/span/text()')  # 新闻总条数
        results = etree_html.xpath("//div[@class='result']")
        for result in results:
            fields = {}
            fields['keyword'] = self.word  # 关键词
            fields['url'] = result.xpath("./h3/a/@href")  # url
            tag = ''.join(result.xpath("./div/p/text()")).split()  # 来源 发布日期
            fields['tag'] = ''.join(tag)
            summary = ''.join(result.xpath("./div/text()")).split()  # 新闻摘要
            fields['summary'] = ''.join(summary)
            fields['source'] = '百度新闻'

            data.append(fields)

        return data

    def sina_news(self):
        """新浪新闻"""
        url = 'https://search.sina.com.cn/?q={}&c=news&from=index'.format(quote(self.word, encoding='GBK'))
        response = self._parse_url(url)
        content = response.content.decode(encoding='GBK')
        etree_html = etree.HTML(content)

        # 提取数据并处理
        data = []
        total = etree_html.xpath('//div[@class="l_v2"]/text()')  # 新闻总条数
        results = etree_html.xpath("//div[@class='box-result clearfix']")
        for result in results:
            fields = {}
            fields['keyword'] = self.word  # 关键词
            fields['url'] = result.xpath("./h2/a/@href")  # url
            tag = ''.join(result.xpath("./h2/span/text()")).split()  # 来源 发布日期
            fields['tag'] = ''.join(tag)
            summary = ''.join(result.xpath("./div[2]/p/text()")).split()  # 新闻摘要
            fields['summary'] = ''.join(summary)
            fields['source'] = '新浪新闻'

            data.append(fields)

        return data

    def xinhua_news(self):
        """新华网"""
        url = 'http://so.news.cn/getNews?keyword={}&curPage=1&sortField=0&searchFields=1&lang=cn'.format(quote(self.word))
        response = self._parse_url(url)
        content = response.json()

        # 提取数据并处理
        data = []
        total = content['content']['resultCount']  # 新闻总条数
        results = content['content']['results']
        for result in results:
            fields = {}
            fields['keyword'] = self.word  # 关键词
            fields['url'] = result['url']  # url
            pubtime = result['pubtime']  # 发布日期
            tag = result['sitename']  # 来源
            fields['tag'] = pubtime + tag
            fields['summary'] = result['des']  # 新闻摘要
            fields['source'] = '新华网'

            data.append(fields)
        print(data)
        return data

    def main(self):
        # baidu = self.baidu_news()
        # for i in baidu:
        #     fe = MySql()
        #     fe.create(i)
        # sina_new = self.sina_news()
        china_new = self.xinhua_news()
        for i in china_new:
            fe = MySql()
            fe.create(i)


if __name__ == '__main__':
    wd = input('输入关键词：')
    news = SearchNews(wd)
    news.main()


