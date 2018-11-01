import requests
from bs4 import BeautifulSoup
import socket


# 获取关键词为人工冻结的知网页面
def getHtml(url, cookie, origin):
    headers = {}
    headers.setdefault("Cookie", cookie)
    # headers.setdefault("Origin", origin)
    headers.setdefault("User-Agent",
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
    req = requests.get(url, timeout=40, headers=headers, stream=True)
    req.raise_for_status()
    req.encoding = req.apparent_encoding
    return req.text


def getAbstract(links, cookie, url):
    abstracts = []
    attempts = 0
    for link in links:
        # 每一个link都是需要去访问的网页
        success = False
        while attempts < 50 and not success:
            try:
                resp = getHtml(link, cookie, url)
                soup = BeautifulSoup(resp, 'html.parser')
                abstract = soup.find('div', style='text-align:left;word-break:break-all').get_text()[6:]
                abstract = abstract.replace('\r', '')
                abstract = abstract.replace('\n', '')
                abstract = abstract.replace(' ', '')
                abstracts.append(abstract)
                socket.setdefaulttimeout(10)
                success = True
            except:
                attempts += 1
                print("link第" + str(attempts) + "次重试！！")
                success = False
                if attempts == 50:
                    break
    return abstracts

def getCiyun():
    pass