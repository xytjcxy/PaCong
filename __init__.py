#!/usr/bin/python
# -*- coding: UTF-8 -*-
# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
# import time
from urllib.request import urlopen
from urllib.request import Request
from urllib import parse

# def work(browser, url):
#     browser.get(url)
#     ele_nums = []
#     time.sleep(5)
#     js = 'window.scrollTo(0, document.body.scrollHeight);'  # 模拟鼠标滚动
#     browser.execute_script(js)
#     time.sleep(5)
#     browser.execute_script(js)
#
#     try:
#         # 首先找到data-artnum，然后根据data-artnum找到对应的类的值；
#         # 若类的值=icon-pdf，那么就放入ele_num中
#         link_list = browser.find_elements_by_xpath("//*[@data-artnum]")
#         for link in link_list:
#             if isContainClass(link.get_attribute('className'), 'icon-pdf'):
#                 ele_num = link.get_attribute('data-artnum')
#                 path = '//*[@href="/document/{}/"]'.format(ele_num)
#                 name = browser.find_elements_by_xpath(path)[0].get_attribute('textContent')+".pdf"
#                 ele_nums.append((ele_num, name))
#
#         return ele_nums
#
#     except:
#         print('failure')

def getResp(url,postData,cookie,origin):
    req = Request(url)
    req.add_header("Cookie", cookie)
    req.add_header("Origin", origin)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
    resp = urlopen(req, data=postData.encode('utf-8'))
    return resp

def browser_init():
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0,
             'download.default_directory': r'E:\Python文件\PaCong\down'}
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=options)
    return browser


