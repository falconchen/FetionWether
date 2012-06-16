FetionWether
============

Send Weather Message to user By Fetion

A Good Book Studying Git :Pro Git

Experience  at http://tq.sms128.net/ 


存在问题与解决方案：
--------------------------------------------------------------------------------------

1. crontab运行fetion发送时，当在某一时刻存在大量订阅用户时，有可能部分用户无法发送到：

    这里的解决方法是把原来正点（即每小时0分）执行一次 改成 0-20/1 ,即在每小时0-20分钟里每分钟执行一次，对发送时间在正点之前的用户（即没有发送到的用户发送），如果没有检测到这类用户，也不用启用飞信实例，同时优化了城市天气数据的获取，从原来每次都要远程获取改为仅当天气获取时间小于正点之前的城市才调用远程获取，这样原来把天气信息存入数据库也变得有意义了。

    crontab设置为::

        0-20/1 * * * * /home/dotcloud/env/bin/python /home/dotcloud/code/hello/weather/cron.py

    向weather_user表增加send_time字段的 SQL语句::

        ALTER TABLE `weather_user` ADD `send_time` DATETIME NOT NULL DEFAULT '1970-01-01 00:00:00'


