import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'hello.settings'
#os.environ['TZ'] = 'Asia/Shanghai'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()