from wordcloud import WordCloud
from PIL import Image
import numpy as np
import jieba
# 使用 jieba 清理停用词
def jiebaclearText(stopwords_path,text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)
    f_stop = open(stopwords_path)
    try:
        f_stop_text = f_stop.read()
    finally:
        f_stop.close()
    f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not (myword.strip()) in f_stop_seg_list and len(myword.strip()) > 1:
            mywordlist.append(myword.strip())
    return ' '.join(mywordlist)


def getCiyun(filename, jpgname):
    stopwords_path = 'stopwords.txt'  # 停用词词表
    cloud_mask = np.array(Image.open(jpgname))
    with open(filename, encoding='utf-8')as f:
        mytext = f.read()
    mytext=jiebaclearText(stopwords_path,mytext)
    st = []
    count=1
    for mi in range(1, 10):
        for ma in range(30, 50):
            wordcolud = WordCloud(background_color="white", mask=cloud_mask, max_words=400, min_font_size=mi,
                                  max_font_size=ma, width=400, stopwords=st, font_path="simsun.ttf")
            wordcolud.generate(mytext)
            str = 'XXB{}.png'.format(count)
            count += 1
            wordcolud.to_file(str)


getCiyun('result.txt', '2.jpg')
