import requests
import xlwt
from bs4 import BeautifulSoup


def getResp(url, cookie):
    headers = {}
    headers.setdefault("Cookie", cookie)
    # headers.setdefault("Origin", origin)
    headers.setdefault("User-Agent",
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
    req = requests.get(url, timeout=40, headers=headers)
    req.raise_for_status()
    req.encoding = req.apparent_encoding
    return req.text


cookie = 'UM_distinctid=166c7e9044e20-0514edf993836d-8383268-144000-166c7e9044f6fb; ASP.NET_SessionId=vc2as0555bd5ek45o2k0a355; SID=201099; CNZZDATA1356416=cnzz_eid%3D2111347303-1540989057-%26ntime%3D1540989057; CNZZDATA3636877=cnzz_eid%3D1525767465-1540989057-%26ntime%3D1540989057'

url = 'http://cdmd.cnki.com.cn/Article/CDMD-10298-2004092345.htm'
response = getResp(url, cookie)
soup = BeautifulSoup(response, 'html.parser')
abstract = soup.find_all('div', style='text-align:left;word-break:break-all')
# print(abstract)
abstracts=[]
for thing in abstract:
    a=thing.get_text()[6:]
    a=a.replace('\r','')
    a=a.replace('\n','')
    a=a.replace(' ','')
    abstracts.append(a)

print(abstracts)
with open('111.txt','ab+') as f:
    print(abstracts[0])
    f.write(bytes(abstracts[0]+'\r\n',encoding='utf-8'))
    # f.write('\n')
    f.write(bytes('1111',encoding='utf-8'))
# filename=xlwt.Workbook()
# sheet=filename.add_sheet('test')
# sheet.write(1,1,abstracts[0])
# filename.save("111.xls")
# print(soup.find_all("font", attrs={'strong': "【摘要】："}))
