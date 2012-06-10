#!/usr/bin/env python
#coding:utf-8
import sys
from os.path import pardir, abspath

sys.path.insert(0, abspath(pardir))
import settings
from weather.PyWapFetion import Fetion
phone = settings.FETION[1][0]
psw = settings.FETION[1][1]
#psw = 'wrong password'
ft = Fetion(phone, psw,cachefile=None)
#friend_fid = ft.findid(settings.FETION[0][0])
#print friend_fid
print ft.addfriend(settings.FETION[0][0],'飞信天气','2')
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

