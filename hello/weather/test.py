#coding:utf-8

import sys,os
from os.path import pardir, abspath

sys.path.insert(0, abspath(pardir))
import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from forms import *
from django import forms
from weather.forms import SubscribeForm
#from util import flatatt, ErrorDict, ErrorList



class Test1(object):
    b = SubscribeForm
    
    
    
class testForm(forms.Form):
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class='', label_suffix=':',
                 empty_permitted=False):
    
        super(testForm,self).__init__(data,files,auto_id,prefix,initial,error_class,label_subffix,empty_permitted);
        self.b = SubscribeForm.base_fields['phone_num']

test = testForm()
print test.b
    