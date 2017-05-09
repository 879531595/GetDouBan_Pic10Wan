#- * - coding:utf-8 - * -
import urllib
import time

picUrl = ''
picName =''

def get_pic(picUrl,picName):
    try:
        urllib.urlretrieve(picUrl,picName)
    except Exception,e:
        pass


with open('pic_Url.txt','r') as fp:
    urllist = fp.readlines()

for no,i in enumerate(urllist):
    nickname, picUrl = i.split('\t')
    picUrl = picUrl.strip()
    get_pic(picUrl,'picture\\%s.jpg'%nickname.decode('utf-8').encode('gbk'))
    print u'第{}张头像下载成功'.format(no+1)
    time.sleep(1)


