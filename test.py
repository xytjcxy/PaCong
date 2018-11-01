import urllib.request
import requests
from urllib import parse
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import Gett

# 根据css提取相关数据，如摘要，作者，年份;
# ---------------------------------------------------------------------------------基本参数
base_url = 'http://search.cnki.com.cn/Search.aspx?q='
location = 'abstract:'
key = '人工冻结'
basic = '&rank=relevant&cluster=all&val=&p='
cookie = 'UM_distinctid=166c7e9044e20-0514edf993836d-8383268-144000-166c7e9044f6fb; ASP.NET_SessionId=vc2as0555bd5ek45o2k0a355; SID=201099; CNZZDATA1356416=cnzz_eid%3D2111347303-1540989057-%26ntime%3D1540989057; CNZZDATA3636877=cnzz_eid%3D1525767465-1540989057-%26ntime%3D1540989057'
origin = 'http://www.cnki.net'
# cur_paper是已下载的文献数量,max_paper是最大文献数量
cur_paper = 0
max_paper = 300
# ----------------------------------------------------------------------------------
result = []  # 最终的结果，以元组的形式展示
abstracts = []  # 所有的摘要
links = []  # 每篇文章的链接
titles = []  # 每篇文章的标题
while cur_paper < max_paper:
    attempts = 0  # 因为知网可能会不给你访问链接，所以得重试
    suc = False
    while attempts<50 and not suc:
        try:
            # 首先进入主页面
            url = base_url + location + key + basic + str(cur_paper)
            resp = Gett.getHtml(url, cookie, origin)
            soup = BeautifulSoup(resp, 'html.parser')
            # 获取主页面所有文章的title，link
            res1 = soup.find_all('a', href=re.compile(r'^http://(\w)*.cnki.com.cn/Article/.*.htm$'))
            for res in res1:
                links.append(res.get('href'))
                titles.append(res.get_text())
            # 获取摘要
            print('links.len=',links.__len__())
            abstracts.extend(Gett.getAbstract(links, cookie, url))
            cur_paper +=15
            suc=True
        except:
            attempts += 1
            print("第" + str(attempts) + "次重试！！")
            success = False
            if attempts == 50:
                break

for i in range(abstracts.__len__()):
    with open('result.txt', 'ab+') as f:
        f.write(bytes(abstracts[0] + '\r\n', encoding='utf-8'))
