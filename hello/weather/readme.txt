Cron 后端作业
===============================================

多线程获取天气并存入数据库

向订阅用户发送天气短信

    1. 单线程发送

    2. 多线程发送天气（可行性未测试)
--------------------------------------------------------------------------------------
涉及模块:

 datetime
 json 
 urllib2
 django.models
===============================================
可替换方案：

SAE的异步队列：
    使用多线程存取天气
    使用顺序队列发送天气

Dotcloud平台和支持Cronjob的 *nix 系统
    cronjob+ python 线程库
===============================================



