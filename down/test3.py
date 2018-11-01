#爬取知网论文作者，关键字，和摘要等信息，并保存在Excel里
import requests  # 导入requests 模块
import re
from urllib import request
import random
import time
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy


class BeautifulPicture():
    def get_pic(self):
        data = xlrd.open_workbook(r'C:\\flim\library_my\new.xls')  # 打开xls文件，自己新建这个文件在运行路径，不然不行的哦
        table = data.sheets()[0]  # 打开第一张表
        table2 = data.sheets()[1]  # 打开第一张表
        i = table.nrows #上一次爬到的表1的行数
        i1 = 0
        i2 = table2.nrows #上一次爬到的表2的行数
        told = 0

        rb = open_workbook(r'C:\\flim\library_my\new.xls','utf-8')
        wb = copy(rb) # 将上一次爬到的复制到新表里，并在新表里继续添加纪录
        # 通过get_sheet()获取的sheet有write()方法
        ws = wb.get_sheet(0)
        ws1 = wb.get_sheet(1)
        p = 1  # 这里是页数
        for num in range(p, p + 100):
            # 这里的num是页码

            web_url ='http://kns.cnki.net/kns/brief/brief.aspx?curpage=%s&Reco' \
                     'rdsPerPage=50&QueryID=8&ID=&turnpage=1&tpagemode=L&dbPref' \
                     'ix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_' \
                     'default_result_aspx#J_ORDER&' % num #这里的URL实现了二次加载
            print('搜素页的URL=',web_url)





            # 这里开始是时间控制
            t = int(time.clock())
            print(t / 60, '分钟')
            useTime = t - told
            # 如果一个周期的时间使用太短，则等待一段时间
            # 主要用于防止被禁
            if (useTime < 120 and useTime > 10):
                print("useTime=%s" % useTime)
                whiteTime = 120 - useTime
                print("等待%s秒" % whiteTime)
                time.sleep(whiteTime)
            told = int(time.clock())
            print(t)

            print('开始网页get请求')
            r = self.request(web_url)  #



            # 这里是报错的解释，能知道到底是因为什么不能继续爬了
            # 一开始会看爬到的源代码，但是之后正式开始爬的时候，打印页面源代码会拉低爬虫效率
            yan = re.search(r'参数错误', r.text)
            if yan != None:
                print("参数")
                break
            yan = re.search(r'验证码', r.text)
            if yan != None:
                print("验证")
                break

            #这里开始抓列表里每一个文献的url
            soup = re.findall(r'<TR([.$\s\S]*?)</TR>', r.text)
            print("soup=",soup)#测试打印
            for a in soup:
                print("-", i1)
                #print(a)#测试代码
                i1 += 1
                name = re.search(r'_blank.*<', a)
                #print('初次取的=',name)#测试代码
                name = name.group()[8:-1]
                #print('第二次=',name)#测试代码
                name = re.sub(r'<font class=Mark>', '', name)
                #print('第三次=', name)  # 测试代码
                name = re.sub(r'</font>', '', name)
                #print('第四次=', name)  # 测试代码

                url = re.search(r'href=.*? ', a)#将’‘看做一个子表达式，惰性匹配一次就可以了
                url = url.group()
                #print('爬取的详情页的URL=',url)#测试代码

                # 将爬来的相对地址，补充为绝对地址
                url = "http://kns.cnki.net/KCMS/" + url[11:-2]#数字是自己数的。。。
                #print("url:%s" % url) # 这里是写代码时测试留下的print记录

                #下面是参考文献详情的URL
                FN = re.search(r'FileName.*?&', url)#.group()#出现错误 没有匹配！！！
                if FN !=None:#测试代码
                    FN = re.search(r'FileName.*?&', url).group()

                #print(FN)#测试代码
                DN = re.search(r'DbName.*?&', url)#.group()
                if DN !=None:#测试代码
                    DN=re.search(r'DbName.*?&', url).group()

                #print(DN) #测试代码
                DC = re.search(r'DbCode.*?&', url).group()
                DUrl = "http://kns.cnki.net/KCMS/detail/frame/list.aspx?%s%s%sRefType=1" % (FN, DN, DC)
                #print('DUrl=',DUrl)#测试代码
                # 这里打开文献详情页
                R = self.request(DUrl)

                #如果没有参考文献，则认为是劣质文献，不爬，转爬下一篇
                isR = re.search(r'参考文献', R.text)
                if i1 == 1:
                    print("没有参考文献的文章:%s" % name)
                if isR == None:
                    continue

                # 详情页
                print(i)
                print("文章名字:%s" % name)
                d = self.request(url).text
                #print('d=',d)#测试代码

                # 这里是文献摘要，自己写的！！！我拷
                summary = re.search(r'(?<=name="ChDivSummary">).+?(?=</span>)', d)
                summary=summary.group()
                #print('摘要=',summary)


                type = re.search(r'"\).html\(".*?"', d)
                type = type.group()[9:-1]
                ins = re.search(r'TurnPageToKnet\(\'in\',\'.*?\'', d)
                if ins == None:
                    continue
                ins = ins.group()[21:-1]
                wt = re.findall(r'TurnPageToKnet\(\'au\',\'.*?\'', d)
                writer = ""
                for w in wt:
                    writer = writer + "," + w[21:-1]
                writer = writer[1:]
                ws.write(i, 0, name)    #文献名
                ws.write(i, 1, writer)  #作者名
                ws.write(i, 2, type)    #文献类别
                ws.write(i, 15, num)    #列表的页码
                ws.write(i, 3, summary)  # 摘要
                ws.write(i, 16, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) #记录的时间

                # 这里是文献的关键词，最多可以记录8个关键词
                kw = re.findall(r'TurnPageToKnet\(\'kw\',\'.*?\'', d)
                tnum = 0
                for tkw in kw:
                    tnum += 1
                    tkw = tkw[21:-1]
                    if tnum > 8:
                        break
                    ws.write(i, 3 + tnum, tkw)




                 # 这里是文献的来源基金
                fund = re.search(r'TurnPageToKnet\(\'fu\',\'.*?\'', d)
                if fund != None:
                    fund = fund.group()[21:-1]
                    ws.write(i, 11, fund)

                # 分类号
                cn = re.search(r'ZTCLS.*?</p', d)
                if cn != None:
                    cn = cn.group()[19:-3]
                    ws.write(i, 12, cn)

                # 这是机构
                jg = re.search(r'TurnPageToKnet\(\'in\',\'.*?\'', d)
                if jg != None:
                    jg = jg.group()[21:-1]
                    #print(jg)
                    ws.write(i, 17, jg)
                # 是否为核心期刊
                sourinfo = re.search(r'sourinfo([.$\s\S]*?)</div', d)
                if sourinfo != None:
                    sourinfo = sourinfo.group()
                    # print(sourinfo)
                    from_ = re.search(r'title.*</a', sourinfo).group()
                    from_ = re.sub(r'title">.*?>', '', from_)
                    from_ = re.sub(r'</a', '', from_)
                    ws.write(i, 13, from_)
                    core = re.search(r'中文核心期刊', sourinfo)
                    if core != None:
                        print(core.group())
                        ws.write(i, 14, "中文核心期刊")

                 # ws.write(i, 0, a)
                i += 1 # 增加页码的计数

        wb.save('new.xls') # 保存表格*******有改变 有问题

    def request(self, url):  # 返回网页的response

        # print(url)
        # 这里是伪造浏览器信息，和伪造来源
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Ch' \
                     'rome/58.0.3029.81 Safari/537.36'
        referer = "http://kns.cnki.net/kns/brief/result.aspx"

        # 这里是伪造cookie，你要从浏览器里复制出来，粘贴在这里
        # 可以把里面的时间不断更新，这样能爬久一点
        cookie = 'cnkiUserKey=e0b40271-cdc0-fd83-36fa-9d4c5f8f2a86; RsPerPage=5' \
                 '0; KNS_DisplayModel=custommode@CJFQ; UM_distinctid=161275ba757a' \
                 '16-0ed232d4ab2da2-6010107f-15f900-161275ba75895e; Ecp_Cli' \
                 'entId=3170915092701569567; ASP.NET_SessionId=3dnqvlsxovsla4' \
                 'ywvr2ykp4c; SID_kns=123106; SID_crrs=125131; SID_klogin=12514' \
                 '3; SID_krsnew=125132; SID_kcms=124113; SID_knsdelivery=125124;' \
                 ' CNZZDATA3258975=cnzz_eid%3D995934993-1516843818-http%253A%252' \
                 'F%252Fkns.cnki.net%252F%26ntime%3D1517383256; Ecp_session=1; ' \
                 'c_m_LinID=LinID=WEEvREcwSlJHSldRa1FhdkJkVWI2VUJNODFzUHlUaC9LN' \
                 'XZrUDkrcXhYbz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4ggI8Fm4gTkoU' \
                 'KaID8j8gFw!!&ot=02/01/2018 18:13:09; LID=WEEvREcwSlJHSldRa1F' \
                 'hdkJkVWI2VUJNODFzUHlUaC9LNXZrUDkrcXhYbz0=$9A4hF_YAuvQ5obgVAqN' \
                 'KPCYcEjKensW4ggI8Fm4gTkoUKaID8j8gFw!!; c_m_expire=2018-02-01 ' \
                 '18:13:09; Ecp_LoginStuts=%7B%22IsAutoLogin%22%3Afalse%2C%22U' \
                 'serName%22%3A%22KT1008%22%2C%22ShowName%22%3A%22%25E8%25A5%2' \
                 '5BF%25E5%258D%2597%25E7%259F%25B3%25E6%25B2%25B9%25E5%25A4%' \
                 '25A7%25E5%25AD%25A6%22%2C%22UserType%22%3A%22bk%22%2C%22r%2' \
                 '2%3A%22RrMW7A%22%7D'

        headers = {'User-Agent': user_agent,
                   "Referer": referer,
                   "cookie": cookie}
        r = requests.get(url, headers=headers, timeout=30)
        return r


print(time.clock())
beauty = BeautifulPicture()  # 创建类的实例
beauty.get_pic()  # 执行类中的方法
