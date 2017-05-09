#- * - coding:utf-8 - * -
import requests
import urllib
import sys
import random
import re
from Queue import Queue
import time
from  bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
url_queue = Queue()
'''
0、获取user_agents.txt文件中的user-Agent便于之后的使用，起到防反爬作用
1、登入豆瓣保存cookie方便之后进入页面爬取
2、进入初始url对所需信息进行爬取
'''
#headers信息
hd = {
    'Host': 'www.douban.com',
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer':'www.douban.com',
    # 'Cookie': 'bid=dgNynDYwumk; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1493945409%2C%22https%3A%2F%2Faccounts.douban.com%2Flogin%3Falias%3D17854273112%26redir%3Dhttps%253A%252F%252Fwww.douban.com%252Fpeople%252F110000000%252F%26source%3DNone%26error%3D1011%22%5D; _pk_id.100001.8cb4=a30473553f8a00cc.1489981207.7.1493946798.1493902112.; __utma=30149280.1808252653.1489981210.1493899491.1493945421.13; __utmz=30149280.1493899491.12.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ll="128136"; _vwo_uuid_v2=4808F43005483E03F479304FFA0A99BA|c2092277fd3fc602bddc4f3550d34910; ap=1; ct=y; ps=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16103; _pk_ses.100001.8cb4=*; __utmb=30149280.10.10.1493945421; __utmc=30149280; __utmt=1; regpop=1; dbcl2="161033308:4r46pafP/Ao"; ck=g2WT',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
#登陆信息
postdata = {

    'source':'None',
    'redir':'https%3A%2F%2Fwww.douban.com',
    'form_email':'***********',
    'form_password':'***********',
    'login':'%E7%99%BB%E5%BD%95',
    'captcha-solution':'',
    'captcha-id':'',
}
#入口url
initialUrl = 'https://www.douban.com/people/26384755/contacts'
url_queue.put(initialUrl)
#登陆url
loginUrl = 'https://www.douban.com/accounts/login?'



usalist = []
s = requests.session()
#数据量的获取
def getlen():
    with open('pic_Url.txt','r') as fp:
        urllist  = fp.readlines()
    return len(urllist)

#获取文件中的User_Agent返回给列表
def getUser_Agent(fname):
    uas = []
    with open(fname, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)#random.shuffle表示随机打乱列表
    # shuffle v洗牌
    # member n成员
    return uas
#1获取user_agents.txt中的信息返回给usalist
usalist = getUser_Agent('user_agents.txt')

#2登陆豆瓣网
'''
1、不需要验证码时，直接使用postdata登陆

2、需要验证码时get captcha.jpg 手动输入
'''

def logindouban():
    hd['User-Agent'] = random.choice(usalist)
    html = s.get(loginUrl,headers = hd).text
    if 'Please try later.'in html:
        print u'ip已被限制'
        sys.exit()
    reqlink = r'<img id="captcha_image" src="(.*?)" alt="captcha" class="captcha_image"/>'
    reqid = r'<input type="hidden" name="captcha-id" value="(.*?)"/>'
    try:
        postdata['captcha-id'] = re.findall(reqid,html)[0]
        link =  re.findall(reqlink,html)[0]
    except Exception,e:
        s.post(loginUrl,headers = hd,data=postdata)
    else:
        urllib.urlretrieve(link,'captcha.jpg')
        postdata['captcha-solution'] = raw_input('please input captcha:')
        s.post(loginUrl,headers = hd,data=postdata)
    print 'login success'

    '''登陆成功'''

#3、爬取数据

def getdata():
    rep = r'<dt><a href="(.*?)/" class="nbg"><img src="(.*?)" class="m_sub_img" alt="(.*?)"/>'
    hd['User-Agent'] = random.choice(usalist)
    initialUrl = url_queue.get()
    html = s.get(initialUrl,headers = hd).content
    try:
        content = re.findall(rep,html)
    except Exception,e:
        return
    for i in content:
        print i[2]
        '''
        1、url存储在url_queue中
        2、昵称和下载地址存储在pic_Url.txt
        '''
        url_queue.put(i[0]+'/contacts')
        with open('pic_Url0.txt','a') as fp:
            fp.write(i[2]+'\t'+i[1]+'\n')

def run():
    logindouban()
    while True:
        getdata()
        len = getlen()
        '''if the data that get from  '''
        if len >=100000:
            break
        time.sleep(6)
if __name__ == "__main__":
    run()





