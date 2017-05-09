需求：
	功能：
		爬取豆瓣网10万用户的昵称和头像
	豆瓣网的url：
		https://www.douban.com/

分析：
	对项目需求进行分析，我们需要实现的功能是对用户的昵称和头像进行获取。
	首先，我们要确定抓取数据的形式，对url进行分析找出其中的规律。经过分析我发现每个用户的个人主页url为：
	https://www.douban.com/people/（.*？）类型。所以每个用户的url是存在着规律的。	

思路：
	首先访问了一个初始url：https://www.douban.com/people/26384755/。
![](http://i.imgur.com/oXzmQ0v.png)	
	发现个人页面中存在个人关注他人的信息，于是楼主灵机一动进入到关注成员的页面
![](http://i.imgur.com/X4GaqMf.png)
	进入页面后楼主清晰的看到了需要的爬取的昵称和头像。对于一个专业的爬虫手，这个时候就应该去观察html的源代码
![](http://i.imgur.com/kop8cia.png)
	查看源代码，楼主发现其中的规律下面就开始实现需求的功能



下为实现功能后的主要文件：
![](http://i.imgur.com/r0EKIyu.png)
douban2.py：
	获取页面中用户的昵称和头像的下载url存储到pic_Url.txt文件中，存在当前页面中的用户个人主要的url，修改为：url/contacts后访问，循环获取信息

getpic.py:
	读取pic_Url.txt的昵称和url，下载头像 

user_agent.txt:
	内存放着大量用于模拟浏览器的user-Agent键值对信息



	
	
