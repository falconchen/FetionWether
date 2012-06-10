#coding:utf-8
import os,urllib2,json
from datetime import datetime,timedelta

weekday_cn = (u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期天')
ch_date = lambda day: u'%s年%s月%s日' % (day.year,day.month,day.day)
ch_weekday = lambda day: weekday_cn[day.weekday()]

os.environ['TZ'] = 'Asia/Shanghai'
today = datetime.today()
yesterday = today +timedelta(days=-1)
tomorrow = today +timedelta(days=1)
print 'today:%s,yesterday:%s,tomorrow%s' %(today,yesterday,tomorrow)
url = 'http://m.weather.com.cn/data/101010100.html'
info = urllib2.urlopen(url).read()
info = json.loads(info)
winfo = info['weatherinfo']
print 'yesterday compare' ,ch_date(yesterday) == winfo['date_y']
print 'today compare', ch_date(today) == winfo['date_y']  
#print winfo['date_y']
print ch_weekday(today)


