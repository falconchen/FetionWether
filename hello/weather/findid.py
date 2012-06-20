#!/home/dotcloud/env/bin/python
#coding:utf-8

import sys,os,threading,time,urllib2,json
from datetime import datetime,timedelta

#only use in dotcloud 
package_dir = '/home/dotcloud/env/lib/python2.6/site-packages'
if os.path.exists(package_dir):
    sys.path.append(package_dir)

current_dir = os.path.dirname(__file__)
settings_dir = os.path.abspath(os.path.join(current_dir,os.path.pardir))
if settings_dir not in sys.path :
    sys.path.append(settings_dir)
import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['TZ'] = settings.TIME_ZONE
from weather.models import MyFetion, Log, User,City,Weather 

PHONE = settings.FETION[0][0]
PSW = settings.FETION[0][1]

ft = MyFetion(PHONE,PSW)
fid = ft.findid('13686892480')
print fid
fid = ft.findid('13480999585')
print fid

