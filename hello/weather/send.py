#!/usr/bin/env python
#coding:utf-8
import sys,os
from datetime import datetime
from time import strftime
from os.path import pardir, abspath

sys.path.insert(0, abspath(pardir))
import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from weather.PyWapFetion import Fetion
from weather.models import *
phone = settings.FETION[0][0]
psw = settings.FETION[0][1]
#psw = 'wrong password'
if len(sys.argv)>1 :
    msg = sys.argv[-1] 
else:
    msg = "Hello Guy : %s"  % strftime("%Y-%m-%d %H:%M:%S")


ft = MyFetion(phone, psw)
#friend_fid = ft.findid(settings.FETION[0][0])
#print friend_fid
#print ft.addfriend(settings.FETION[0][0],'飞信天气','2')


#msg = "hello world "

print ft.sendBYid('299396032',msg)
ft.logout()

#add = ft.send(settings.FETION[1][0],'hello man')
#print add


##
##
##limit = 5
##for i in range(limit):
##    try:
##        ft = Fetion(phone,psw)
##        if ft.send2self('hi man') == True:
##            break
##        else :
##            i+=1
##    except:
##        i+=1
##        err_info = sys.exc_info()
##        log = '%s : %s' % (err_info[0],err_info[1])
##
##    finally:
##        if 'ft' in locals():
##            ft.logout()
##    
##else:
##    print "5次尝试结束，记入日志吧 " + log    
##
##
##

