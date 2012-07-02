#!/home/dotcloud/env/bin/python
#coding:utf-8

import sys,os,threading,time,urllib2,json,time
from BeautifulSoup import BeautifulSoup
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
from weather.models import MyFetion, Log, User,City,Weather, Alarm,AlarmLog
from cron import current_clock_dt

#环境设置
MODE = ('TEST','PRODUCT','DEVEL',)[2]

PHONE = settings.FETION[0][0]
PSW = settings.FETION[0][1]
LOGIN_LIMIT = 5
SEND_MAX = 50 #短信队列最大发送次数

def fetch_new_alarms():
    fetch_count = 0 
    alarms = Alarm.fetch_online(cancel=False)       
    if Alarm.objects.filter(url=alarms[0]['url']).count() > 0:
        return 0
    all_areas = City.get_all_areas()
    cities_below = {}
    for am in reversed(alarms):
        #print am['color_id'],am['title'],am['url'],am['pub_time']
        url = am['url']
        if Alarm.objects.filter(url=url).count()>0:                
            continue            
        alarm_obj =Alarm()
        for key,val in am.iteritems():        
            setattr(alarm_obj,key,val)        
        title = am['title']
        for code,area in all_areas:
            if area in title:
                alarm_obj.area_code = code
                break    
        else:        
            raise ValueError(u'%s failed to match any areas' % title)        
        #匹配城市
        if len(code) < 9:
            title = title[len(area):-1]
            if not cities_below.has_key(code):
                cities_below[code] = City.get_below_cities(code)                
            for cid,city in cities_below[code]:
                #print code,cid,city            
                if city in title:
                    alarm_obj.area_code = cid
                    break
            
        #print alarm_obj.area_code,alarm_obj.title
        alarm_obj.save()
        count+=1
        Log(level=1,event="new alarm:%s-%s(%s)" % (
        alarm_obj.title,alarm_obj.pub_time,alarm_obj.area_code)).save()
        
    return fetch_count
        
def send_alarm_sms():
    #组装飞信发送列表,测试数据为2012月7月2日12时
    clock = datetime(2012,7,2,16,0,0,0) if MODE == 'TEST' else current_clock_dt()    
    current_alarms = Alarm.objects.filter(pub_time=clock)    
    to_send_list = []
    for current_alarm in current_alarms :
        users = User.objects.filted_with_cid(current_alarm.area_code)
        if (len(users)>0 and current_alarm.content == ''):
            current_alarm.content = Alarm.fetch_content(current_alarm.url)
            current_alarm.save()
        for user in users:
            try:
                alarm_log = AlarmLog.objects.get(alarm=current_alarm,user=user)
                continue
            except:
                to_send_list.append((user,current_alarm))                
    #开始发送（单线程）
    send_count = 0
    if len(to_send_list) > 0 :
        for i in range(0,LOGIN_LIMIT):
            try:
                ft = MyFetion(PHONE,PSW)
                break
            except:i+=1         
        else:
            Log(level=1,event="failed to initial MyFetion in sending sms")
            sys.exit(1)
        #这里可以一次最大发送量
        for user,alarm in to_send_list[0:SEND_MAX]:
            fid = MyFetion.test_id if MODE == 'TEST' else user.fid
            tail = u'via飞信天气网(预警短信Beta)'
            content = u'[%s]\n%s %s' % (alarm.title,alarm.content,tail)
            send_result = ft.sendBYid(fid, content.encode('utf-8'))
            #测试和开发时给自己发送
            if MODE != 'PRODUCT':ft.send2self(content.encode('utf-8'))
            if send_result == True or send_result == None: 
                send_count +=1
                did = "OK" if send_result == True else "Failed"
                details = 'status:%s,area_code:%s,content:%s' % (
                did,alarm.area_code,content)
                try:
                    AlarmLog(alarm=alarm,user=user,details=details).save()
                except Except,e :
                    error_msg = 'Send Alarm error:%s:%s:%s' % (e,alarm,user)
                    Log(level=0,event = error_msg).save()
                    if MODE != 'PRODUCT': print error_msg                
            if MODE != 'PRODUCT': print user.phone_num,content        
        ft.logout()
    
    return send_count

if __name__ == '__main__':
    start = time.time()
    fetch_total = fetch_new_alarms()    
    send_total = send_alarm_sms()    
    stop = time.time()
    event = "Send alarms sms total:%s\nElapse :%6.3f" % (
    send_total,stop - start)    
    if send_total > 0:Log(level=1,event=event)
    if MODE != 'PRODUCT': 
        print 'Fetch new alarms total: %d' % fetch_total         
        print event    
    sys.exit(0)
    