FetionWeather
============

Send Weather Message to user By Fetion

A Good Book Studying Git :Pro Git

Experience  at http://tq.sms128.net/ 


存在问题与解决方案：
--------------------------------------------------------------------------------------

1. `crontab运行fetion发送时，当在某一时刻存在大量订阅用户时，有可能部分用户无法发送到`

    这里的解决方法是把原来正点（即每小时0分）执行一次 改成 0-20/1 ,即在每小时0-20分钟里每分钟执行一次，对发送时间在正点之前的用户（即没有发送到的用户），如果没有检测到这类用户，也不用启用飞信实例，同时优化了城市天气数据的获取，从原来每次都要远程获取改为仅当天气获取时间小于正点的城市才调用远程获取，这样原来把天气信息存入数据库也变得有意义了。还有一个效果是如果用户订制时如果选择在当前小时，填写完订阅表单即可收到天气短信。这也只需要crontab 设置为0-59每分钟执行一次而非0-20。

    crontab设置为::

        0-20/1 * * * * /home/dotcloud/env/bin/python /home/dotcloud/code/hello/weather/cron.py

    向weather_user表增加send_time字段的 SQL语句::

        ALTER TABLE `weather_user` ADD `send_time` DATETIME NOT NULL DEFAULT '1970-01-01 00:00:00'


2. `订阅时提示: `"手机号错误或没有开通飞信业务"` ,而实际用户开通飞信业务。`

    实际wap飞信会根据该手机号是否为飞信好友会返回两种不同页面，`PyWapFetion` 的 `_getid` 方法只是好友列表内，陌生人列表和黑名单内查找，如果用户手机不在这些范围内，会返回None, 于是增加了非飞信好友(这个表达不太准确，应该说是不在所有用户列表内）的查找和判定。实际就是加入了对非飞信好友查询页的处理。感谢用户：138******78的反馈。

3. `预警短信地区匹配不准确的问题`

    预警里出现的城市在天气预报里的城市列表并不一定出现（省份是可以匹配到的），于是就出现这样的情况：向该城市订阅用户发送预警时会发送到该省全部市的订阅用户，
    比如湖北襄阳，在天气预报城市列表不存在，但是有这么一条预警“湖北省襄阳市发布雷电黄色预警”，则会造成向湖北省全部下属市的用户都发送预警短信。
    已知的存在问题的此类城市：吉林延边、湖北襄阳

    解决方法:省份匹配完毕后，如果没有匹配到城市，会对预警标题再作一次是否含有市或自治州字样的的判断，有则为市级预警，不会发送到全省，当然这个实际上是不会发送出去的，因为该城市在数据库不存在 。
    如果没有那些字样，则确实为省级预警。目前这个算法的判断准确率尚可，不会给用户发送错误城市的预警信息。