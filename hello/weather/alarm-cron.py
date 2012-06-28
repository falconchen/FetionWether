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
#print settings_dir
if settings_dir not in sys.path :
    sys.path.append(settings_dir)
import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['TZ'] = settings.TIME_ZONE
from weather.models import MyFetion, Log, User,City,Weather, Alarm,AlarmLog

PHONE = settings.FETION[0][0]
PSW = settings.FETION[0][1]
#ft = MyFetion(PHONE,PSW)  
# url = 'http://www.nmc.gov.cn/alarm/index.htm'
# html = urllib2.urlopen(url).read().decode('gbk').encode('utf-8')
# #print html
# soup = BeautifulSoup(html)
# #soup.contents[0].name
# print soup.contents[0].name

alarms = Alarm.fetch_online(cancel=False)
all_areas = City.get_all_areas()
cities_below = {}

for am in reversed(alarms):
    #print am['color_id'],am['title'],am['url'],am['pub_time']
    url = am['url']
    if Alarm.objects.filter(url=url).count()>0:        
        #pass
        continue
        
    alarm_obj =Alarm()
    for key,val in am.iteritems():        
        setattr(alarm_obj,key,val)
    #alarm_obj.content = Alarm.fetch_content(url)
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
        
    #print alarm_obj.area,alarm_obj.title    
    alarm_obj.save()
    
  
    
