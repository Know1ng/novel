import os
import re
from lxml import etree
import requests

from proxy import random_proxy, random_user_agent


class ContentSpider(object):

    def __init__(self, url):
        self.url = url

    def get_it_done(self):
        """
        该类的主方法
        获得小说名称name（用于创建文件夹主目录）
        获得所有章节名称chapter（用于章节创建文件夹）
        获得所有小章节名称title（用来命名文件）和链接link（用于获得小说内容），
        调用其他方法实现创建文件夹、得到小说内容和保存小说，输出小说信息
        """
        response = requests.get(url=self.url, headers=random_user_agent())
        html = etree.HTML(response.text)
        # name是小说名称
        novel_name = html.xpath('//div[@class="book-info "]/h1/em/text()')[0]
        # 处理非法字符
        name = re.sub(r'[\\/:*?"<>|\r\n]+', '_', novel_name)
        # items是所有小说所有章节目录
        items = html.xpath('//div[@class="volume"]')
        for item in items:
            # 章节名
            chapter_name = "".join(item.xpath('.//h3/text()')).strip()
            # 处理非法字符
            chapter = re.sub(r'[\\/:*?"<>|\r\n]+', '_', chapter_name)
            # 章节下所有小章节
            sections = item.xpath('.//li[@data-rid]')
            # 遍历出每个小章节的名称和链接
            for section in sections:
                # 小章节名称
                title_name = section.xpath('./a/text()')[0]
                # 处理非法字符
                title = re.sub(r'[\\/:*?"<>|\r\n]+', '_', title_name)
                # 小章节链接
                link = section.xpath('./a/@href')[0]
                # 含有小说名称name，章节名称chapter，小章节名称title，以及链接link的字典info
                info = {
                    'name': name,
                    'chapter': chapter,
                    'title': title,
                    'link': 'https:' + link
                }
                # 创建文件目录，返回child_path
                child_path = self.mkdir(info=info)
                # 获得小说内容
                content = self.get_content(link=info['link'])
                # 保存小说
                self.write(child_path=child_path, content=content)
                # 打印小说信息
                print(info)

    def mkdir(self, info):
        """
        创建路径为grand_path的小说同名文件夹主目录
        主目录下再创建路径为father_path各个章节同名的文件夹
        最后定义child_path，返回child_path
        :param info: 小说相关信息，即小说名称，章节名称等
        :return: 返回最终创建小说文件的子路径child_path
        """
        # 章节路径
        grand_path = 'D:/xiaoshuo/qidian/' + info['name']
        # 小章节路径
        father_path = grand_path + '/' + info['chapter']
        # 小说文件路径
        child_path = father_path + '/' + info['title']
        isExist1 = os.path.exists(grand_path)
        isExist2 = os.path.exists(father_path)
        # 文件不存在就创建文件
        if not isExist1:
            os.mkdir(path=grand_path)
        if not isExist2:
            os.mkdir(path=father_path)
        return child_path

    def get_content(self, link):
        """
        获取小说内容
        :param link: 小说内容的链接
        :return: 返回小说内容
        """
        response = requests.get(url=link, headers=random_user_agent())
        html = etree.HTML(response.text)
        # 小说内容
        content = '\n'.join(html.xpath('//div[@class="read-content j_readContent"]//p/text()'))
        return content

    def write(self, child_path, content):
        """
        保存小说到本地
        :param child_path: 小说文件路径
        :param content: 小说内容
        :return: None
        """
        try:
            with open(child_path + '.txt', 'w') as file:
                file.write(content)
        except UnicodeEncodeError:
            e_report = '写入时编码错误,错误章节为' + child_path
            print(e_report)


if __name__ == '__main__':
    """
    测试模块
    """
    # 起始URL
    root_url = 'https://book.qidian.com/info/3684254#Catalog'
    # 测试用的url列表
    url_list = ['https://book.qidian.com/info/3684254#Catalog', 'https://book.qidian.com/info/1013406185#Catalog', ]
    for url in url_list:
        print(url)
        spider = ContentSpider(url)
        spider.get_it_done()
