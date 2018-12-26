# 起始URL
root_url = 'https://www.qidian.com/free/all'

# 小说种类URL参数列表
novel_list = {
    '奇幻': '?chanld=1',
    '武侠': '?chanld=2',
    '仙侠': '?chanld=22',
    '都市': '?chanId=4',
    '历史': '?chanId=5',
    '游戏': '?chanId=7',
    '科幻': '?chanId=9',
    '灵异': '?chanId=10',
    '短篇': '?chanId=20076',
    '玄幻': '?chanld=21'
}


def interface():
    print('-' * 50)
    print('小说种类清单：')
    print(''' 
    奇幻
    武侠
    仙侠
    都市 
    历史
    游戏
    科幻
    灵异
    短篇
    玄幻
        ''')
    print('-' * 50)


def menu():
    """
    接口函数，得到小说种类category
    :return: 返回对应的url以及category
    """
    category = str(input('请输入你要看的小说类别：'))
    chanId = novel_list[category]
    # 构造出完整的URL
    url = root_url + chanId
    return url, category


if __name__ == '__main__':
    """
    测试模块
    """
    interface()
    menu()
