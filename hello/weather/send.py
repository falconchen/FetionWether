#!/usr/bin/env python
#coding:utf-8
import sys
from os.path import pardir, abspath

sys.path.insert(0, abspath(pardir))
import settings
from weather.PyWapFetion import Fetion
phone = settings.FETION[1][0]
psw = settings.FETION[1][1]
#psw = 'wrong password'
ft = Fetion(phone, psw,cachefile=None)
#friend_fid = ft.findid(settings.FETION[0][0])
#print friend_fid
#print ft.addfriend(settings.FETION[0][0],'飞信天气','2')
msg = '''
风暴现状:今年第5号强热带风暴"泰利"，17时中心位于北纬20.2度，东经115.7度，近中心最大风速25米/秒，风力10级。未来风暴中心将以每小时15-20公里的速度向东北方向移动，可能于20日凌晨到下午在诏安到惠安之间沿海擦过或登陆，而后继续向东北方向移动。风的影响：今天夜里，崇武以南偏东风5-6级，阵风7级逐渐增强到6-7级阵风8-9级；崇武到闽江口之间沿海偏南风5-6级阵风7级转偏东风6-7级阵风8-9级；闽江口以北偏北风5-6级，阵风7-8级。20日，旋转风8-9级，阵风10-11级，热带风暴中心经过的海面阵风12级以上。雨的影响：今天夜里到20日，宁德、福州、莆田、泉州四市阴有大雨，部分暴雨到大暴雨，24小时雨量80-120mm，局部超过150mm；厦门、漳州两市阴有中到大雨，部分暴雨，局部大暴雨，24小时雨量50-100mm，局部超过100mm；其余各市阴有中雨，部分大雨。预警提示：目前在南海中北部海域和台湾海峡作业与过往的船只应注意安全，及时回港避风。
防御指南：
1.政府及相关部门按照职责做好防台风应急准备工作；
2.停止室内外大型集会和高空等户外危险作业；
3.相关水域水上作业和过往船舶采取积极的应对措施，加固港口设施，防止船舶走锚、搁浅和碰撞；
4.加固或者拆除易被风吹动的搭建物,人员切勿随意外出，确保老人小孩留在家中最安全的地方，危房人员及时转移。
'''



#add = ft.send(settings.FETION[1][0],'hello man')
#print add


##
##
##limit = 5
##for i in range(limit):
##    try:
##        ft = Fetion(phone,psw)
##        if ft.send2self('hi man') == True:
##            break
##        else :
##            i+=1
##    except:
##        i+=1
##        err_info = sys.exc_info()
##        log = '%s : %s' % (err_info[0],err_info[1])
##
##    finally:
##        if 'ft' in locals():
##            ft.logout()
##    
##else:
##    print "5次尝试结束，记入日志吧 " + log    
##
##
##

