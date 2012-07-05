#! /usr/bin/env python
# coding:utf-8
import datetime, urllib2,re
from django.db import models, connection
#from django.contrib import admin
from PyWapFetion import Fetion,Errors
from BeautifulSoup import BeautifulSoup

# Create your models here.
class City(models.Model):
    cid = models.CharField(max_length =9,primary_key = True)
    province = models.CharField(max_length = 10)
    city = models.CharField(max_length = 10)
    
    @staticmethod
    def get_all_areas():
        '''
                取全部地区编码对,其中直辖市/特别行政区为9位,省份(含台湾)为5位，                
                '''                
        areas = [('101010100',u'北京'),('101020100',u'上海'),('101030100',u'天津'),('101040100',u'重庆'),('101320101',u'香港'),('101330101',u'澳门'),]
        cursor = connection.cursor()            
        sql = 'SELECT DISTINCT SUBSTR( cid, 1, 5 ) AS pid, province FROM weather_city WHERE cid>%s AND cid <>%s AND cid<>%s'            
        cursor.execute(sql,['101040100','101320101','101330101'])
        areas.extend(cursor.fetchall())                        
        return areas
    
    @staticmethod
    def get_below_cities(area_code):
        '''取指定省级下的全部城市'''
        cursor = connection.cursor()            
        sql = 'SELECT cid,city FROM weather_city WHERE cid LIKE %s'            
        cursor.execute(sql,['%s%s'% (area_code,'%')])
        return cursor.fetchall()
    
    def __unicode__(self):
        return u'%s:%s:%s' % (self.province,self.city,self.cid)
    
    class Meta:
        ordering = ['cid',]


class Weather(models.Model):
    HOURS_CHOICES = (
       ('0', '0点'),('1', '1点'),('2', '2点'),('3', '3点'),('4', '4点'),('5', '5点'),                     
       ('6', '6点'),('7', '7点'),('8', '8点'),('9', '9点'),('10', '10点'),('11', '11点'),
       ('12', '12点'),('13', '13点'),('14', '14点'),('15', '15点'),('16', '16点'),('17', '17点'),
       ('18', '18点'),('19', '19点'),('20', '20点'),('21', '21点'),('22', '22点'),('23', '23点'),
    )
    cid = models.ForeignKey(City)
    hour = models.CharField(max_length=2,choices=HOURS_CHOICES)
    info = models.TextField(blank=True)
    fetch_ts = models.DateTimeField(auto_now=True,verbose_name=u'获取时间')
    

    def __unicode__(self):
            return u"%s (每日%s时)" % (self.cid,self.hour)
        
    class Meta:
        ordering = ['-fetch_ts']
    

class UserManager(models.Manager):

    def filted_with_cid(self,cid):
        cursor = connection.cursor()
        sql = 'SELECT b.* FROM weather_city a, weather_user b, weather_weather c WHERE a.cid like %s AND a.cid=c.cid_id AND b.wid_id=c.id  AND b.active=1 ORDER BY b.id DESC'                
        cursor.execute(sql,['%s%s' % (cid,'%')])
        return [User.objects.get(id=row[0]) for row in cursor.fetchall()]
        
    
    
class User(models.Model):
    TYPE_CHOICES = (('E','每日发送三天预报'),('B','可能下雨时才发送')) 
    fid = models.CharField(verbose_name=u'飞信号',max_length = 10,blank = True,) #飞信id号，允许为空
    phone_num = models.CharField(max_length = 11)
    wid = models.ForeignKey(Weather,verbose_name=u'订阅城市/发送时间')
    sub_type = models.CharField(verbose_name=u'订阅类型',max_length=1,default='E',choices=TYPE_CHOICES) #订阅类型分别为每天一条短信和只有坏天气时发送短信
    reg_ts = models.DateTimeField(verbose_name=u'注册时间',default=datetime.datetime.now)
    active = models.BooleanField(default=True,verbose_name="是否激活")
    send_time = models.DateTimeField(default=datetime.datetime(1970,1,1,0,0,0),verbose_name=u'上次发送时间')
    objects = UserManager()
    
    def __unicode__(self):
        return self.phone_num
    
    @property
    def hour(self):
        return self.wid.hour
        
    class Meta:
        ordering = ['-reg_ts',]


#简单日志记录
class Log(models.Model):
    LEVELS = (('0','ALERT'),('1','DEBUG'),('2','INFO'))
    time = models.DateTimeField(auto_now=True,verbose_name=u'时间')
    level = models.CharField(verbose_name='等级',max_length=1,default='2',choices=LEVELS)
    event = models.TextField(verbose_name=u'事件')
    
    def __unicode__(self):
        return "%s(%s):%s" % (self.time,self.level_name(),self.event) 

    def level_name(self):
        for item in Log.LEVELS:
            if item[0] == self.level:
                return item[1]  


#天气预警
class Alarm(models.Model):
    color_id = models.CharField(verbose_name=u'预警颜色编号',max_length=8)
    title = models.TextField(verbose_name=u'预警标题')
    url = models.CharField(verbose_name=u'预警内容页网址',max_length=100)
    area_code = models.CharField(verbose_name=u'地区代号',max_length=9,default='0')    
    content = models.TextField(verbose_name=u'预警内容',blank=True)    
    pub_time = models.DateTimeField(verbose_name=u'发布时间')
    fetch_time = models.DateTimeField(verbose_name=u'获取时间',auto_now=True)

    class Meta:
        ordering = ['-id']    
    
    def __unicode__(self):
        return "%s(%s-%s)" % (self.title,self.area_code,self.pub_time)     
    
    '''在线取得预警信息,参数表示是否过滤含解除字样的预警信息，默认过滤'''
    @staticmethod
    def fetch_online(cancel=True):
        alarm_url = 'http://www.nmc.gov.cn/alarm/index.htm'
        page = urllib2.urlopen(alarm_url).read()
        soup = BeautifulSoup(page)
        tds = soup.findAll('td', width="28")
        alarms = []
        now = datetime.datetime.now()
        for td in tds :
            title_td = td.nextSibling.nextSibling
            title = title_td.contents[1].text.strip()
            pub_time = title_td.nextSibling.nextSibling.text.replace('&nbsp;','')
            pub_time = Alarm.chdate_convert(pub_time)
            if pub_time > now : continue #为了处理气象网站发布日期错误的情况
            if cancel and u'解除' in title: continue                
            info = {
                'color_id':td.contents[1]['id'],            
                'url':title_td.contents[1]['href'],
                'title':title,
                'pub_time': pub_time
            }
             
            alarms.append(info)
        return alarms
        
    @staticmethod
    def chdate_convert(chdate):        
        pattern = re.compile(ur'(?P<year>\d+)年(?P<month>\d+)月(?P<day>\d+)日(?P<hour>\d+)时',re.U)
        match = pattern.match(chdate)
        if match:
            # 使用Match获得分组信息
            datetime_tuple = (int(num) for num in list(match.groups()))    
            return datetime.datetime(*datetime_tuple)
        else :
            raise ValueError('chinese date formate convert error')
            
    @staticmethod
    def fetch_content(url=''):        
        if '' == url : url = '/sjyj/0002004/201206271832594311.htm'
        url = 'http://www.nmc.gov.cn%s' % url
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page)
        alarmtexts = soup.findAll(id=re.compile('alarmtext'))
        if u'解除' in alarmtexts[0].text:
            return alarmtexts[0].text.strip()
        return '\n'.join([alarmtext.text.strip() for alarmtext in alarmtexts])

        

#预警发送日志
class AlarmLog(models.Model):
    alarm = models.ForeignKey(Alarm)
    user = models.ForeignKey(User)
    details = models.TextField(verbose_name=u'详细信息',blank=True)
    send_time = models.DateTimeField(verbose_name=u'发送时间',auto_now=True)
    
    def __unicode__(self):
        return u'%s/%s' % (self.user,self.alarm)
        
    class Meta:
        ordering = ['-send_time']            
        
class MyFetion(Fetion):
    test_id = '299396032'
    limit =5
    
    def __init__(self,mobile,password,status='4',cachefile=None,keepalive=False):
        super(MyFetion,self).__init__(mobile,password,status,cachefile,keepalive)
    
    #定义最大尝试次数
    #默认不是非得发到对方手机
    def sendBYid(self,id,message,sm=False):
         
        for i in range(self.limit):
                try:                    
                    if super(MyFetion,self).sendBYid(id,message,sm=sm) == True:
                        break
                    else :
                        i+=1
                except Errors.FetionNotYourFriend, e:
                    i+=1
                    #如果在一天内不确认好友关系，则删除用户的注册关系
                    #这样会导致过期后用户确认加好友，也会无效。需要重新注册
                    try:
                        not_friend = User.objects.get(fid=id)
                    except User.DoesNotExist:
                        pass
                    else:  
                        delta = datetime.datetime.now() - not_friend.reg_ts                                              
                        if  delta.days > 0:                            
                            not_friend.active = False
                            not_friend.save()
                            res = "Success" if not_friend.delete() == None else "Failed" 
                            Log(level=1,event='%s to delete not friend :%s ' % (res ,not_friend.phone_num)).save()
                                                
                    Log(level=1,event='fid:%s is not your Friend' % id).save()
                    return None
                except Exception, e:
                    i+=1
                    #err_info = sys.exc_info()
                    #event = '%s : %s ' % (err_info[0],err_info[1])
                    #pritn event
                    #Log(event=event).save()
                    self._login()
                    
                    
                finally:
                    pass
                
        else:
                Log(event = u"send sms trying too many times,,Fid: %s " % id).save() 
                return False
        return True
