#!/home/dotcloud/env/bin/python
#coding:utf-8

import sys,os,threading,time,urllib2,json
from BeautifulSoup import BeautifulSoup
from datetime import datetime,timedelta

#only use in dotcloud 
package_dir = '/home/dotcloud/env/lib/python2.6/site-packages'
if os.path.exists(package_dir):
    sys.path.append(package_dir)

current_dir = os.path.dirname(__file__)
settings_dir = os.path.abspath(os.path.join(current_dir,os.path.pardir))
print settings_dir
if settings_dir not in sys.path :
    sys.path.append(settings_dir)
import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['TZ'] = settings.TIME_ZONE
from weather.models import MyFetion, Log, User,City,Weather 

PHONE = settings.FETION[0][0]
PSW = settings.FETION[0][1]
#ft = MyFetion(PHONE,PSW)  
url = 'http://www.nmc.gov.cn/alarm/index.htm'
html = urllib2.urlopen(url).read().decode('gbk').encode('utf-8')
#print html
soup = BeautifulSoup(html)
#soup.contents[0].name
print soup.contents[0].name

