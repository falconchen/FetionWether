#!/usr/bin/env python
#coding:utf-8

import os,sys
import django

def backend_init():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'hello.settings'
    curdir = os.path.realpath(os.path.curdir)
    search_path = os.path.split(curdir)
    search_path = os.path.split(search_path[0])
    sys.path.insert(0,search_path[0])    


if __name__ =='__main__':
    backend_init()    
    try:
        import hello.settings
        from blog.models import *
        data = BlogPost.objects.all()
        for entry in data:
            print entry.title
    except ImportError,e:
        print e
    
    
