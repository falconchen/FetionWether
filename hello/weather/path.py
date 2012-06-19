#!/home/dotcloud/env/bin/python
#coding:utf-8

import sys,os,threading,time,urllib2,json
from datetime import datetime,timedelta

#only use in dotcloud 
package_dir = '/home/dotcloud/env/lib/python2.6/site-packages'
if os.path.exists(package_dir):
    sys.path.append(package_dir)

current_dir = os.path.dirname(__file__)
settings_dir = os.path.abspath(os.path.join(current_dir,os.path.pardir))
if settings_dir not in sys.path :
    sys.path.append(settings_dir)
import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['TZ'] = settings.TIME_ZONE
from weather.models import MyFetion, Log, User,City,Weather 

PHONE = settings.FETION[0][0]
PSW = settings.FETION[0][1]
ft = MyFetion(PHONE,PSW)  
message = u'''
风暴现状:今年第5号强热带风暴"泰利"，17时中心位于北纬20.2度，东经115.7度，近中心最大风速25米/秒，风力10级。未来风暴中心将以每小时15-20公里的速度向东北方向移动，可能于20日凌晨到下午在诏安到惠安之间沿海擦过或登陆，而后继续向东北方向移动。风的影响：今天夜里，崇武以南偏东风5-6级，阵风7级逐渐增强到6-7级阵风8-9级；崇武到闽江口之间沿海偏南风5-6级阵风7级转偏东风6-7级阵风8-9级；闽江口以北偏北风5-6级，阵风7-8级。20日，旋转风8-9级，阵风10-11级，热带风暴中心经过的海面阵风12级以上。雨的影响：今天夜里到20日，宁德、福州、莆田、泉州四市阴有大雨，部分暴雨到大暴雨，24小时雨量80-120mm，局部超过150mm；厦门、漳州两市阴有中到大雨，部分暴雨，局部大暴雨，24小时雨量50-100mm，局部超过100mm；其余各市阴有中雨，部分大雨。预警提示：目前在南海中北部海域和台湾海峡作业与过往的船只应注意安全，及时回港避风。
防御指南：
1.政府及相关部门按照职责做好防台风应急准备工作；
2.停止室内外大型集会和高空等户外危险作业；
3.相关水域水上作业和过往船舶采取积极的应对措施，加固港口设施，防止船舶走锚、搁浅和碰撞；
4.加固或者拆除易被风吹动的搭建物,人员切勿随意外出，确保老人小孩留在家中最安全的地方，危房人员及时转移。
'''
ft.sendBYid(MyFetion.test_id, message.encode('utf-8')) 
ft.logout()

