#coding:utf-8
from django import forms
from settings import FETION
from weather.models import Weather, User, City, MyFetion, Log
from weather.PyWapFetion import Fetion
from  django.core.exceptions import ValidationError
import re


CHOICES = (('0', '--请选择--'),)

class ProvinceChoiceField(forms.ChoiceField):
    def validate(self, value):
        if value == '0':
            raise ValidationError(u'请选择正确的省份')
        
class CityChoiceField(forms.ChoiceField):    

    def validate(self, value):
        if not re.match(r'^\d{9}$', value):
            raise ValidationError(u'请选择正确的城市')

        if not City.objects.filter(cid=value):
            raise ValidationError('无效城市代号')
       

class SubscribeForm(forms.Form):
    
    province = ProvinceChoiceField(choices=CHOICES, label="省份",
                                 widget=forms.Select(attrs={'id':'province', 'class':'province', 'onchange':'on_pro_select_change(this.id)'}),
                                 )
    
    city = CityChoiceField(choices=CHOICES, label="城市",
                             widget=forms.Select(attrs={'id':'city', 'class':'city', 'onchange':'on_city_change(this.id)'}),
                             
                             )
     
    hour = forms.ChoiceField(choices=Weather.HOURS_CHOICES, label='发送时间',
                                 widget=forms.Select(attrs={'id':'hour', 'class':'hour'})
                                 )
    sub_type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'subtype', 'id':'subtype'}), initial={'sub_type':'E'}, choices=User.TYPE_CHOICES, label='订阅类型')
    
    phone_num = forms.CharField(label='手机号码', min_length=11, max_length=11, widget=forms.TextInput(attrs={'id':'phone_num'}))
    
    def clean_phone_num(self):
        
        phone_num = self.cleaned_data['phone_num']
        Log(level=2,event='%s tried to subscribe' % phone_num).save()        
        #self.phone_num = phone_num
        china_mobile_num = ('134','135','136','137','138','139','150','151','152','158','159','157','187','188','147')
        if phone_num[0:3] not in china_mobile_num:
            raise ValidationError('非中国移动号码不能注册')
        try:            
            user = User.objects.get(phone_num=phone_num)
        except User.DoesNotExist:
            pass
        else :
            if user.active == True :
                raise ValidationError('你已经注册过了')
            else :
                raise ValidationError('帐户已冻结,请激活后继续使用')
        
        #这里的管理员手机可能使用模型存取
        phone = FETION[0][0]
        psw = FETION[0][1]
        ft = MyFetion(phone, psw)
        fid = ft.findid(phone_num)
        ft.logout()
        if fid == None:
            raise ValidationError('无效手机号或没有开通飞信服务')
        else :
            
            self.fid = fid
            return phone_num
        


# 验证表
class VerifyForm(forms.Form):
       
    phone_num = forms.CharField(label='手机号码', min_length=11, max_length=11, widget=forms.TextInput(attrs={'id':'phone_num'}))
    code = forms.CharField(label='验证码', min_length=6, max_length=6, widget=forms.TextInput(attrs={'id':'code'}))     
    #phone_num =  SubscribeForm.phone_num
    #def clean_phone_num(self):
        



class CodeForm(forms.Form):
       
    phone_num = forms.CharField(label='手机号码', min_length=11, max_length=11, widget=forms.TextInput(attrs={'id':'phone_num'}))

    def clean_phone_num(self):
            
        phone_num = self.cleaned_data['phone_num']
        Log(level=2,event='%s asked for verify code' % phone_num).save()        
        #self.phone_num = phone_num
        try:            
            user = User.objects.get(phone_num=phone_num)
            self.fid = user.fid
        except User.DoesNotExist:
            raise ValidationError('找不到该帐户，请先注册。')
                                    
        return phone_num    

class UpdateSubForm(forms.Form):
    province = ProvinceChoiceField(choices=CHOICES, label="省份",
                                 widget=forms.Select(attrs={'id':'province', 'class':'province', 'onchange':'on_pro_select_change(this.id)'}),
                                 )
    
    city = CityChoiceField(choices=CHOICES, label="城市",
                             widget=forms.Select(attrs={'id':'city', 'class':'city', 'onchange':'on_city_change(this.id)'}),
                             
                             )
     
    hour = forms.ChoiceField(choices=Weather.HOURS_CHOICES, label='发送时间',
                                 widget=forms.Select(attrs={'id':'hour', 'class':'hour'})
                                 )
    sub_type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'subtype', 'id':'subtype'}), initial={'sub_type':'E'}, choices=User.TYPE_CHOICES, label='订阅类型')
    
    
    
    
    