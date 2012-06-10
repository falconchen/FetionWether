#! /usr/bin/env python
# coding:utf-8

from django.db import models
#from django.contrib import admin
from PyWapFetion import Fetion,Errors


# Create your models here.
class City(models.Model):
    cid = models.CharField(max_length =9,primary_key = True)
    province = models.CharField(max_length = 10)
    city = models.CharField(max_length = 10)
    
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
    info = models.TextField()
    fetch_ts = models.DateTimeField(auto_now=True,verbose_name=u'获取时间')
    

    def __unicode__(self):
            return u"%s (每日%s时)" % (self.cid,self.hour)
        
    class Meta:
        ordering = ['-fetch_ts']
    

class User(models.Model):
    TYPE_CHOICES = (('E','每日发送三天预报'),('B','可能下雨时才发送')) 
    fid = models.CharField(verbose_name=u'飞信号',max_length = 9,blank = True,) #飞信id号，允许为空
    phone_num = models.CharField(max_length = 11)
    wid = models.ForeignKey(Weather,verbose_name=u'订阅城市/发送时间')
    sub_type = models.CharField(verbose_name=u'订阅类型',max_length=1,default='E',choices=TYPE_CHOICES) #订阅类型分别为每天一条短信和只有坏天气时发送短信
    reg_ts = models.DateTimeField(verbose_name=u'注册时间',auto_now=True)
    active = models.BooleanField(default=True,verbose_name="是否激活")
    
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
    
class MyFetion(Fetion):
    test_id = '299396032'
    limit =5
    
    def __init__(self,mobile,password,status='4',cachefile=None,keepalive=False):
        super(MyFetion,self).__init__(mobile,password,status,cachefile,keepalive)
    
    #定义最大尝试次数
    
    def sendBYid(self,id,message,sm=True):
         
        for i in range(self.limit):
                try:                    
                    if super(MyFetion,self).sendBYid(id,message,True) == True:
                        break
                    else :
                        i+=1
                except Errors.FetionNotYourFriend, e:
                    i+=1
                    Log(event=e.message).save()
                    return False
                except:
                    i+=1
                    #err_info = sys.exc_info()
                    #event = '%s : %s ' % (err_info[0],err_info[1])
                    #pritn event
                    #Log(event=event).save()
                    self._login()
                    
                finally:
                    pass
                
        else:
                Log(event = "5次尝试结束，记入日志 ,Fid: %s " % id).save() 
                return False
        return True