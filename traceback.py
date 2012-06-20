#coding:utf-8
# import sys
# import traceback

# try:
    # s2 = '%s欢迎您' % u'北京'
# except Exception, e:
    # print e.reason
    # print sys.exc_info()
    # exstr   =   traceback.format_exc() 
    # print exstr
    
import traceback


try:
    1/0
except Exception, e:
    traceback.print_exception()