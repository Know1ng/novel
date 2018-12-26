import requests
from lxml import etree
import pymongo

import xiaoshuo_inter as xs_inter


class Spider(object):
    mongo_uri = 'localhost'
    mongo_db = 'xiaoshuo'

    def __init__(self, url, page, category):
        """
        初始化各个参数
        :param url: 小说url
        :param page: 页数
        :param category: 小说类型
        """
        self.url = url
        self.page = page
        self.collection = category
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        print('正在爬取第%s页..' % self.page)

    def get_html(self):
        """
        得到页面
        :return: 返回响应体
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36', }
        response = requests.get(url=self.url, headers=headers)
        return response.text

    def parse(self,html):
        """
        解析页面，得到小说相关信息
        :param html: 页面html
        :return: 返回包含小说信息的字典novel
        """
        html= etree.HTML(html)
        # 所有小说
        items = html.xpath('//li[@data-rid]')
        # 遍历每个小说
        for item in items:
            # 标题
            title = item.xpath('.//div[@class="book-mid-info"]/h4/a/text()')[0]
            # 作者
            author = item.xpath('.//p[@class="author"]/a[@class="name"][1]/text()')[0]
            # 封面
            cover = item.xpath('.//div[@class="book-img-box"]/a/img/@src')[0]
            # 简介
            intro = item.xpath('.//p[@class="intro"]//text()')[0].strip() + '...'
            # 链接
            link = item.xpath('.//div[@class="book-img-box"]/a/@href')[0]
            # 包含各个信息的字典
            novel = {
                'title': title,
                'author': author,
                'cover': cover,
                'intro': intro,
                'link': link
            }
            yield novel

    def write_to_mongoDB(self, novel):
        """
        把结果保存到mongoDB
        :param novel: 小说
        """
        if self.db[self.collection].insert(novel):
            print('保存成功！')


if __name__ == '__main__':
    # 定义最大页数，可修改
    max_page = 1000
    try:
        # 调用xiaoshuo_inter里面的接口函数
        xs_inter.interface()
        # 得到小说URL（小说类别）和category
        get_info = xs_inter.menu()
        url = get_info[0]
        category = get_info[1]
        input_page = int(input('请输入你好爬取的页数(最大页数为:%s):' % max_page))
        if 0 < input_page <= max_page:
            for page in range(1, input_page + 1):
                # 构造完整URL（每一个页面）
                new_url = url + '&page=%s' % page
                # 实例化一个spider，传入页面URL，要爬取得页数，小说种类
                spider = Spider(url=new_url, page=page, category=category)
                # 调用相应方法
                html = spider.get_html()
                novel = spider.parse(html)
                spider.write_to_mongoDB(novel)
        else:
            print('输入页面值超过最大页面')
    except Exception as error:
        print('出现错误，错误类型为：', error)
    finally:
        print('爬虫工作结束！')
