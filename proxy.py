import random
import requests


def random_user_agent():
    """
    随机生成user_agent
    :return: 返回由随机生成user_agent构成的headers
    """
    # user_agent列表
    User_Agent = [
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
    user_agent = random.choice(User_Agent)
    headers = {'User-Agent': user_agent}
    # print (headers)
    return headers


def random_proxy():
    """
    随机生成代理ip
    :return: 返回proxies
    """
    https_ip_pool = [
        '60.191.201.38:45461',
        '223.244.252.58:45744',
        '123.139.56.238:9999',
        '59.78.2.140:1080',
        '223.244.252.58:45744',
        '120.25.203.182:7777',
    ]

    http_ip_pool = [
        '61.178.238.122:63000',
        '118.187.58.34:53281',
    ]

    http_ip = random.choice(http_ip_pool)
    https_ip = random.choice(https_ip_pool)

    proxies = {
        'http': 'http://' + http_ip,
        'https': 'https://' + https_ip
    }
    # print(proxies)
    return proxies


if __name__ == '__main__':
    """
    测试模块
    """
    # 测试URL
    url = 'http://httpbin.org/get'
    headers = random_user_agent()
    proxies = random_proxy()
    response = requests.get(url=url, headers=headers, proxies=proxies, timeout=5)
    print(response.text)


