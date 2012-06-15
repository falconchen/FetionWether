#coding:utf-8
#Send message to all subscribers

from wsgi import *
from hello.weather.models import User,City,Weather
from hello.weather.PyWapFetion import Fetion
from hello.weather.PyWapFetion.Errors import FetionNotYourFriend, FetionNotLogin
from hello import settings

PHONE_NUM, PSW, NAME = settings.FETION[0]


def msg2all (msg) :
    msg = msg.encode('utf-8')
    users = User.objects.all()
    ft = Fetion(PHONE_NUM,PSW,'1',None)
    send_flag = add_flag = fail_flag = 0
    for u in users :
        for time in range(5):
            try:            
                if ft.sendBYid(u.fid,msg,True) == True:
                    send_flag +=1
                    print u'send msg success to %s' % u.phone_num
                    break
            except FetionNotYourFriend :
                add_flag +=1
                if ft.addfriend(u.phone_num,NAME,'2') == False :
                    print u'add friend error: %s' % u.phone_num
                else :
                    print u'send add Friend msg to %s ' % u.phone_num
                break
            except FetionNotLogin :
                ft._login()
        else :
            fail_flag +=1
            print u'unknown error: %s' % u.phone_num

    else :
        ft.logout()
        print 'finish all announces send :success:%s ,add:%s,failed:%s' % (send_flag,add_flag,fail_flag)


if __name__ == '__main__':
    msg = u'亲，你使用的免费短信天气预报服务已经迁移到飞信天气网，我们将提供更加准确稳定的天气预报和灵活、免费的订制方式,你的原订制信息已经导入成功，如需更改和退订，欢迎访问:http://tq.sms128.net。'
    msg2all(msg)
    
