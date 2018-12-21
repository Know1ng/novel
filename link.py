import requests
from lxml import etree

from proxy import random_user_agent  # ,random_proxy


class LinkSpider(object):

    def __init__(self, url):
        self.url = url

    def get_html(self):
        """
        得到页面的html
        :return: 返回响应体
        """
        response = requests.get(url=self.url, headers=random_user_agent())
        return response.text

    def parse(self, html):
        """
        解析页面，提取小说标题和小说链接
        :param html: 页面的html
        :return: 返回含有小说链接的字典
        """
        html = etree.HTML(html)
        # items是页面所有小说的信息
        items = html.xpath('//li[@data-rid]')
        # 从items遍历出小说标题和链接
        for item in items:
            # 小说标题
            title = item.xpath('.//div[@class="book-mid-info"]/h4/a/text()')[0]
            # 小说链接
            link = item.xpath('.//div[@class="book-img-box"]/a/@href')[0]
            # 构造一个包含小说标题和链接的字典
            info = {
                'title': title,
                'link': 'https:' + link + '#Catalog'  # 处理链接，得到有效的URL
            }
            # print(info)   用于测试代码，查看输入情况
            yield info['link']


if __name__ == '__main__':
    """
    测试模块
    """
    # 起始URL
    root_url = 'https://www.qidian.com/free/all'
    spider = LinkSpider(root_url)
    html = spider.get_html()
    spider.parse(html=html)
