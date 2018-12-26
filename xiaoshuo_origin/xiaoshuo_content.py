import re

from lxml import etree
import requests
import os
import random


class ContentSpider(object):
    # UA列表
    UserAgent_list = [
        'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    ]

    def __init__(self, url):
        self.url = url
        self.user_agent = random.choice(self.UserAgent_list)
        

    def get_content(self):
        headers = {
            'User-Agent': self.user_agent, }
        response = requests.get(url=self.url, headers=headers)
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
                grand_path = 'D:/自选小说/' + info['name']
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
                # 小说文本内容的response
                child_response = requests.get(url=info['link'], headers=headers)
                child_html = etree.HTML(child_response.text)
                # 小说文本
                content = '\n'.join(child_html.xpath('//div[@class="read-content j_readContent"]//p/text()'))
                with open(child_path + '.txt', 'w') as file:
                    file.write(content)
                    print(content)



if __name__ == '__main__':
    try:
        input = str(input('请输入小说的URL:'))
        url = 'https:' + input + '#Catalog'
        spider = ContentSpider(url)
        spider.get_content()
    except UnicodeEncodeError:
        print('写入出现错误')
