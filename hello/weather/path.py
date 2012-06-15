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

#f = open(os.path.join(current_dir,'path.txt'),'a')
#f.write('\n'.join(sys.path))
#f.write('\n--------\n')
#f.close()
PHONE = settings.FETION[0][0]
PSW = settings.FETION[0][1]

message = u'我想测试你'
ft = MyFetion(PHONE,PSW)  
if ft.sendBYid(MyFetion.test_id, message.encode('utf-8')):
    Log(level=2,event = 'Send test message %s to %s ' % (message,MyFetion.test_id)).save()
ft.logout()
