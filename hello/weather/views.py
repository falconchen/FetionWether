#coding:utf-8
from time import strftime
from django.template import loader, Context
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from weather.models import City, Weather, User,MyFetion, Log
from django.template import RequestContext
import urllib2, re
from weather.forms import SubscribeForm, VerifyForm, CodeForm, UpdateSubForm
#from weather.PyWapFetion import Fetion
import settings

PHONE = settings.FETION[0][0]
PSW = settings.FETION[0][1]
NICK = settings.FETION[0][2].encode('utf-8')

def index(request):
    msg = '请先填写手机号码和订阅信息, 天气短信将发送到你的手机。'
    if request.method == 'POST':
        form = SubscribeForm(request.POST)            
        if form.is_valid():
            fid = form.fid
            cd = form.cleaned_data
            
            
            #向天气订阅表增加记录或找出指定城市的订阅实例
            try:
                weather = Weather.objects.get(cid=cd['city'], hour=cd['hour'])
            except Weather.DoesNotExist:
                city = City.objects.get(cid=cd['city'])
                weather = Weather(cid=city, hour=cd['hour'])
                weather.save()
            
            #发送加为好友的短信
            ft = MyFetion(PHONE,PSW)
            add_res = ft.addfriend(cd['phone_num'], NICK, '2')
            if add_res:
                Log(level=2,event='success to send adding friend sms to %s' % cd['phone_num']).save()
            else:
                Log(level=1,event='failed to send adding friend sms to %s ,maybe he/she has been your friend.' % cd['phone_num']).save()

            #用户与天气订阅表关联，仅使用新增            
            user = User(fid=fid, phone_num=cd['phone_num'], wid=weather, sub_type=cd['sub_type'], active=True)
            user.save()            
            
            if add_res:
                msg = '你将收到一条"%s"的好友请求短信,请于24小时内确认,逾期无效' %  NICK
            else:
                msg = '订制成功'
            form = None
    
    else:    
        default_hour = int(strftime('%H')) + 1
        form = SubscribeForm(initial={'hour':default_hour, 'sub_type':'E'}) #定义字段的option默认值        
    return render_to_response('index.html', {'form':form, 'msg':msg, 'form_id':'subscribe'}, context_instance=RequestContext(request))
    

def verify(request, action):
    accept_actions = {'update':'更改订阅', 'deactive':'退订', 'active':'重新激活'}
    if action not in accept_actions:
        raise Http404
    
    title = accept_actions[action]    
    msg = None    
    if request.method == 'POST':
        form = VerifyForm(request.POST)        
        if not form.is_valid():
            raise Http404('非法请求')
        cd = form.cleaned_data
        try :
            s_phone_num = request.session['phone_num']
            s_code = request.session['code']
            phone_num = cd['phone_num']
            code = cd['code'].upper()
            if s_phone_num != phone_num or s_code != code:                
                raise Http404('验证码错误\n')
        except:            
            raise Http404('非法请求或验证码超时')
        
        if action == 'update':            
            request.session['update_phone_num'] = phone_num
            del request.session['phone_num']
            del request.session['code']
            return HttpResponseRedirect('/weather/update/')
        else:
            try :
                if change_status(s_phone_num, action) :
                    del request.session['phone_num']
                    del request.session['code']
                    request.session['announce'] = '%s成功' % title
                    Log(level=2,event='%s:%s' % (s_phone_num,action)).save()
                    if action == 'active':
                        request.session['user'] = User.objects.get(phone_num=phone_num)
                    return HttpResponseRedirect('/weather/announce/')
            except User.DoesNotExist:
                raise Http404('无效用户')      
    else :
        form = VerifyForm()
        msg = '请先验证手机,然后才能%s。' % title
    return render_to_response('verify.html', {'form':form, 'title':title, 'msg':msg, 'form_id':'verify', 'action':action}, context_instance=RequestContext(request))

def update(request):
    action = 'update'
    #title = '更新'
    try :                
        phone_num = request.session['update_phone_num']
        u = User.objects.get(phone_num=phone_num)
        msg = {'phone_num':u.phone_num, 'fid':u.fid}    
        msg['area'] = u.wid
        msg['sub_type'] = User.TYPE_CHOICES[0][1] if u.sub_type == User.TYPE_CHOICES[0][0] else User.TYPE_CHOICES[1][1]
        t = loader.get_template('user_info.html')
        msg = t.render(Context({'msg':msg}))
        if request.method == 'POST':
            #post_args = request.POST
            #post_args['phone_num'] = phone_num
            form = UpdateSubForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                #执行更新逻辑
                                
                try:
                    weather = Weather.objects.get(cid=cd['city'], hour=cd['hour'])
                except Weather.DoesNotExist:
                    city = City.objects.get(cid=cd['city'])
                    weather = Weather(cid=city, hour=cd['hour'])
                    weather.save()
                
                #更改订阅类型
                u.wid = weather
                u.sub_type = cd['sub_type']
                u.save()
                
                request.session['announce'] = u'更改成功'
                Log(level=2,event=u'%s:%s' % (u.phone_num,request.session['announce'])).save()
                request.session['user'] = u
                #if not settings.DEBUG:   
                del request.session['update_phone_num']        
                return HttpResponseRedirect('/weather/announce/')
                                                
            #表单字段无效时
            else:
                pass
        else:
            default_hour = int(strftime('%H')) + 1
            form = UpdateSubForm(initial={'hour':default_hour, 'sub_type':'E'}) #定义字段的option默认值
        return render_to_response('index.html', {'form':form, 'msg':msg, 'action':action,'form_id':'subscribe'}, context_instance=RequestContext(request))
    except Exception, e:
        #print Exception
        #raise e
        raise Http404('非法请求')
#    
#    

def announce(request):
    try :
        announce = request.session['announce']
        user = request.session.setdefault('user', None)
        #if not settings.DEBUG: 
        del request.session['announce']
        del request.session['user']
        return render_to_response('announce.html', {'msg':announce, 'user':user},context_instance=RequestContext(request))
    except Exception, e:
        #raise e 
        raise Http404('非法请求')


#退订与重新激活
def change_status (phone_num, action='deactive'):
    current_active = True if action == 'deactive' else False    
    user = User.objects.filter(phone_num=phone_num, active=current_active)
    if len(user) == 0:
        raise User.DoesNotExist ('用户不存在')
    return bool(user.update(active=not current_active))
        

def cid_js(request, cid):
    url = 'http://m.weather.com.cn/data/%s.html?' % cid
    try:
        urlopen = urllib2.urlopen(url)
    except urllib2.HTTPError:
        url = 'http://m.weather.com.cn/data/101010100.html?';
        urlopen = urllib2.urlopen(url)
    if 'weather_error_404' in urlopen.url:
        url = 'http://m.weather.com.cn/data/101010100.html?';
        urlopen = urllib2.urlopen(url)
    content = urlopen.read()
    jscontent = 'var state=%s;' % content
    jscontent = re.sub(r'(\-?[\d.]+)(℃|℉)~(\-?[\d.]+)\2', r'\3\2~\1\2', jscontent)
    return  HttpResponse(jscontent, mimetype='text/javascript')
        

def get_user_info(request):
    
    try :
        s_phone_num = request.session['phone_num']
        s_code = request.session['code']
        phone_num = request.GET['phone_num']
        code = request.GET['code'].upper()
        if s_phone_num != phone_num or s_code != code:
            #return HttpResponse('验证码错误或非法请求\n')
            raise Http404
    except:
        #return HttpResponse('验证码错误或请求超时\n')
        raise Http404
    
    #u = User.objects.get(phone_num=s_phone_num)
    u = get_object_or_404(User, phone_num=s_phone_num)
    msg = {'phone_num':u.phone_num, 'fid':u.fid}    
    msg['area'] = u.wid
    msg['sub_type'] = User.TYPE_CHOICES[0][1] if u.sub_type == User.TYPE_CHOICES[0][0] else User.TYPE_CHOICES[1][1]
    return render_to_response('user_info.html', {'msg':msg})
    #raise Http404('非法请求')
    
        
    
    
#发送验证码
def get_code(request):

    form = CodeForm(request.GET)
    if not form.is_valid():
        return HttpResponse(form.errors.pop('phone_num'))    
    else :
        phone_num = form.cleaned_data.get('phone_num')    
        fid = form.fid
    import random
    chars = 'abcdefghjklmnpqrstuvwxyz123456789'.upper() * 5
    code = ''.join(random.sample(chars, 6))
    t = loader.get_template('sms.html')
    sms = t.render(Context({'code': code}))
    
#    phone = settings.FETION[0][0]
#    psw = settings.FETION[0][1]
#    ft = Fetion(phone, psw, cachefile=None)
#    
    ft = MyFetion(PHONE,PSW)    
    #发送验证码，注意消息需要用utf-8编码
    if ft.sendBYid(fid, sms.encode('utf-8'), True) :
        #设置session
        request.session['phone_num'] = phone_num
        request.session['code'] = code
        request.session.set_expiry(300)                        
        msg = '验证码已发送到你的手机，请在5分钟内输入，不区分大小写。\n如果30秒内没有收到，请点击重新获取\n[飞信天气网:http://tq.sms128.net]' 
    else :
        msg = 'something wrong,retry please'
        
    ft.logout()
    return HttpResponse(msg)
        
    
