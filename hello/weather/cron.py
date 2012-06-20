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
send_count = 0 #是否发送过消息

class InfoThread(threading.Thread):
    
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name
        
    def run(self):
        apply(self.func,self.args)

def into_db(weather):
    if weather.fetch_ts < _current_clock_dt() or weather.info=='':
        #仅当当前数据过期才获取
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
        else:
             Log(level=1,event="failed to fetch weather info %s" % url).save()
                
        weather.info = info        
        weather.save()
        
    
    sendGroupSms(weather)
    
    return True

#发飞信
def sendGroupSms(weather):
    clock_dt = _current_clock_dt()
    users = weather.user_set.filter(active=True,send_time__lt=clock_dt)
    
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
                send_result = ft.sendBYid(u.fid, message.encode('utf-8'))
                if send_result == True :  #发送计数
                    global send_count
                    send_count += 1
                #返回none表示非好友,对非好友不重复发送                 
                if send_result == True or send_result == None:

                    did = "Did" if send_result == True else "Didn't"
                    u.send_time = datetime.now()
                    u.save()                    
                    Log(level=2,event = '%s Send to %s[%sh]:%s:(%s)' % (did,u.phone_num,weather.hour,weather.cid.city,message)).save()
        except Exception,e :            
#            print "except Happen: ",e
            raise e
            if 'ft' in locals():
                ft.logout()

def parse_json(jdata,user):
    try:
        info = json.loads(jdata)
    except:
        return False    
    winfo = info['weatherinfo']
    tail = u' via飞信天气网: http://tq.sms128.net'
    weekday_cn = (u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期日')
    ch_weekday = lambda day: weekday_cn[day.weekday()]
    ch_date = lambda day: u'%s年%s月%s日' % (day.year,day.month,day.day)
    today = datetime.today()
    tomorrow = today +timedelta(days=1)
    is_today = (ch_date(today) == winfo['date_y'])
    today_weather = winfo['weather1'] if is_today else winfo['weather2']
    today_temp = winfo['temp1'] if is_today else winfo['temp2']
    today_wind = winfo['wind1'] if is_today else winfo['wind2']
    today_fl = winfo['fl1'] if is_today else winfo['fl2']
    if len(today_wind)>3:
        today_fl = ''
    #print "wind:%s(%d),fl:%s(%d)" %(today_wind,len(today_wind),today_fl,len(today_fl))
    
    
    if user.sub_type == 'B':
        if 0 <= int(user.wid.hour) <=12:            
            if u'雨' not in today_weather:
                return None
            else:                
                template = u'今天是%s(%s) ,%s天气 :%s,%s,%s%s; 出门请带好雨具。%s' % \
                (ch_date(today),ch_weekday(today),winfo['city'],today_weather,today_temp,today_wind,today_fl,tail)
        else :
            #13点到23点不必判断是否为昨天数据，取得的数据必为今日
            if u'雨' not in winfo['weather2']:
                return None
            else:
                                                                
                dt = u'%s年%s月%s日 %s' % (tomorrow.year,tomorrow.month,tomorrow.day,ch_weekday(tomorrow))                                                
                template = u'%s明日(%s)天气 :%s,%s,%s%s; 出门请带好雨具。%s' % \
                (winfo['city'],dt,winfo['weather2'],winfo['temp2'],winfo['wind2'],'' if len(winfo['wind2'])>3 else winfo['fl2'],tail)
    else:
        tomorrow_weather = winfo['weather2'] if is_today else winfo['weather3']
        tomorrow_temp = winfo['temp2'] if is_today else winfo['temp3']
        tomorrow_wind = winfo['wind2'] if is_today else winfo['wind3']
        tomorrow_fl = winfo['fl2'] if is_today else winfo['fl3']
        if len(tomorrow_wind)>3:
            tomorrow_fl = ''
        after_tomorrow_weather = winfo['weather3'] if is_today else winfo['weather4']
        after_tomorrow_temp = winfo['temp3'] if is_today else winfo['temp4']
        after_tomorrow_wind = winfo['wind3'] if is_today else winfo['wind4']                                
        after_tomorrow_fl = winfo['fl3'] if is_today else winfo['fl4']                                
        if len(after_tomorrow_wind)>3:
            after_tomorrow_fl = ''
        template = u'今天是%s(%s) ,%s天气 :%s,%s,%s%s;明天:%s,%s,%s%s;后天:%s,%s,%s%s。%s' % \
        (ch_date(today),ch_weekday(today),winfo['city'],today_weather,today_temp,today_wind,today_fl,
         tomorrow_weather,tomorrow_temp,tomorrow_wind,tomorrow_fl,after_tomorrow_weather,after_tomorrow_temp,after_tomorrow_wind,after_tomorrow_fl,tail)
        
    return template
        

    
def _current_clock_dt():
    now = datetime.now()
    clock_tuple = (now.year, now.month, now.day, now.hour, 0, 0)
    clock_dt = datetime(*clock_tuple)
    return clock_dt
    



def main():
    info_threads = []
    now = datetime.now()
    hour = now.hour
    #hour = 17
    #weathers = Weather.objects.filter(cid='101300901',hour=hour)
    weathers = Weather.objects.filter(hour=hour)
    for w in weathers:
        t = InfoThread(into_db,(w,))
        info_threads.append(t)
    
    for i in range(len(weathers)):
        info_threads[i].start()
    
    for i in range(len(weathers)):
        info_threads[i].join()
        
    print "Finish fetching data into db,hour:%s" % hour
        
if __name__ == '__main__':
    start = time.time()
    main()    
    stop = time.time()    
    if send_count > 0 :
        msg = "Send sms count: %s , Threads time Elapsed :%s \n" % (send_count, stop-start) 
        Log(level=1,event = msg ).save()
