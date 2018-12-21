import requests
from lxml import etree

import link
import content
from proxy import random_user_agent  # ,random_proxy 这里的代理ip不稳定，所以没有使用

# 小说网站起始URL
root_url = 'https://www.qidian.com/free/all'


def get_max_page():
    """
    在首页中得到页面的最大页数并返回最大页面的值
    :return: 返回最大页面数max_page
    """
    response = requests.get(url=root_url, headers=random_user_agent())
    html = etree.HTML(response.text)
    # 得到最大页数
    max_page = int(
        html.xpath('//ul[@class="lbf-pagination-item-list"]/li[@class="lbf-pagination-item"][last()-1]/a/text()')[0])
    print('最大页数是:', max_page)
    return max_page


if __name__ == '__main__':
    # 最大页数
    Max_page = get_max_page()
    # Max_page = 10000    # 自定义对大页数
    # 单页小说数
    item_mun = 20
    for page in range(1, Max_page + 1):
        # 构造每一页的URL
        url = root_url + '?' + 'page=' + str(page)
        # 打印url，便于定位出错点
        print(url)
        # 实例化一个linkSpider对象
        link_spider = link.LinkSpider(url)
        # 调用get_html方法得到每一个页面的html
        page_html = link_spider.get_html()
        # 调用parse方法，得到小说链接
        get_info = link_spider.parse(html=page_html)
        # 从得到的小说链接的生成器中，next出每一个链接
        for num in range(item_mun):
            get_link = next(get_info)
            # 实例化一个ContentSpider对象
            content_spider = content.ContentSpider(get_link)
            # 调用主方法，实现创建文件夹的到小说内容以及保存小说，输出小说信息
            content_spider.get_it_done()

"""
可以用来做错误报告
# import datetime
    # 当时时间
    now_time = datetime.datetime.now()
    # 日期（年月日）
    date_time = str(now_time)[:10]
    # 时间（时分秒）
    time = str(now_time)[11:19]
    # 将错误信息保存到本地文件
    path = 'D:/xiaoshuo/error/'
    with open(path + 'error_report' + date_time + '.txt', 'w') as file:
        file.write(str(error) + time)
"""
