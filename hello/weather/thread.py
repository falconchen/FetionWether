#!/usr/bin/env python
#coding:utf-8

import sys,os,threading,time,urllib2,json
from datetime import datetime,timedelta
from os.path import pardir, abspath
sys.path.insert(0, abspath(pardir))
import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['TZ'] = settings.TIME_ZONE
from weather.models import MyFetion, Log, User,City,Weather 

PHONE = settings.FETION[0][0]
PSW = settings.FETION[0][1]


class TestThread(threading.Thread):
#    def run(self):
#        u = User.objects.get(phone_num='13714681456')
#        now = datetime.now()
#        ft = MyFetion(PHONE,PSW,False)
#        ft.sendBYid(u.fid,'now is %s,Send By %s' %(now,self.getName()),True)
#        #ft.send2self('hello falcon')
#        ft.logout()
        def run(self):
            limit = 5
            u = User.objects.get(phone_num='13714681456')
            for i in range(limit):
                try:
                    ft = MyFetion(PHONE,PSW,False)
                    if ft.sendBYid(u.fid,'My thread name is %s' % self.getName() ,True) == True:
                        break
                    else :
                        i+=1
                except:
                    i+=1
                    err_info = sys.exc_info()
                    log = '%s : %s' % (err_info[0],err_info[1])
            
                finally:
                    if 'ft' in locals():
                        ft.logout()
                
            else:
                print "5次尝试结束，记入日志 " + log

class InfoThread(threading.Thread):
    
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name
        
    def run(self):
        apply(self.func,self.args)

def into_db(weather):
    limit = 5
    base_url = 'http://m.weather.com.cn/data/%s.html'
    url = base_url % weather.cid.cid
    
    for i in range(limit):
        try:
            info = urllib2.urlopen(url).read()
            if bool(json.loads(info)): 
                break 
        except:
            info = '获取失败'
        finally:
            i+=1
            
    weather.info = info
    
    weather.save()
    print '%s : %s\n' % (weather.cid.city,url)
    
    sendGroupSms(weather)
    
    return True

#发飞信
def sendGroupSms(weather):
    users = weather.user_set.filter(active=True)
    #print len(users)
    if len(users)>0 :
        try:
            ft = MyFetion(PHONE,PSW)            
                                
            for u in users :
                message = parse_json(weather.info,u)
                if message == False:
                    Log(level=0,event='json数据解析出错:订阅天气信息%s:s%' %(weather.cid,weather.hour)).save()
                    return False    
                
                if message == None :
                    continue
                               
                ft.sendBYid(u.fid, message.encode('utf-8'))
                print 'send to %s : %s' % (u.phone_num,message)
                Log(level=2,event = 'Send to %s[%sh]:%s:(%s)' % (u.phone_num,weather.hour,weather.cid.city,message)).save()
        except:
            if 'ft' in locals():
                ft.logout()

def parse_json(jdata,user):
    try:
        info = json.loads(jdata)
    except:
        return False    
    winfo = info['weatherinfo']
    tail = u' (本消息由短信天气网www.sms-weather.com免费提供)'
    
    if user.sub_type == 'B':
        if 0 <= int(user.wid.hour) <=12:
            if u'雨' not in winfo['weather1']:
                return None
            else:                
                template = u'今天是%s(%s) ,%s天气 :%s,%s,%s; 出门请带好雨具。%s' % \
                (winfo['date_y'],winfo['week'],winfo['city'],winfo['weather1'],winfo['temp1'],winfo['wind1'],tail)
        else :
            if u'雨' not in winfo['weather2']:
                return None
            else:
                weekday_cn = (u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期天')
                tomorrow = datetime.now()+ timedelta(days=1)
                day = tomorrow.weekday()
                dt = u'%s年%s月%s日 %s' % (tomorrow.year,tomorrow.month,tomorrow.day,weekday_cn[day])
                                                
                template = u'%s明日(%s)天气 :%s,%s,%s; 出门请带好雨具。%s' % \
                (winfo['city'],dt,winfo['weather2'],winfo['temp2'],winfo['wind2'],tail)
    else:                
        template = u'今天是%s(%s) ,%s天气 :%s,%s,%s;%s;明天:%s,%s;后天:%s,%s。%s' % \
        (winfo['date_y'],winfo['week'],winfo['city'],winfo['weather1'],winfo['temp1'],winfo['wind1'],winfo['index_d'],
         winfo['weather2'],winfo['temp2'],winfo['weather3'],winfo['temp3'],tail)
    
    
    return template
    
    


def main():
    info_threads = []
    now = datetime.now()
    hour = now.hour
    #hour = 2
    #weathers = Weather.objects.filter(cid='101300901',hour=hour)
    weathers = Weather.objects.filter(hour=hour)
    for w in weathers:
        t = InfoThread(into_db,(w,))
        info_threads.append(t)
    
    for i in range(len(weathers)):
        info_threads[i].start()
    
    for i in range(len(weathers)):
        info_threads[i].join()
        
    print "finish into db"
        
if __name__ == '__main__':
    start = time.time()
    main()    
    stop = time.time()
    print "多线程耗时 :%s \n" % (stop-start)
# 
#    start = time.time()
#    u = User.objects.get(phone_num='13714681456')
#    print u.fid
#    ft = MyFetion(PHONE,PSW,cachefile=None)
#    for i in range(10):
#        ft.send('13714681456','haha',True)
#    ft.logout()
#    stop = time.time()
#    print "单线程耗时 :%s \n" % (stop-start)
#    
#    start = time.time()
#    for i in range(10):
#        t = TestThread() 
#        t.start() 
#    
#    stop = time.time()
#    print "多线程耗时 :%s \n" % (stop-start)