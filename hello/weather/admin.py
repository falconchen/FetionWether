#! /usr/bin/env python
# coding:utf-8

from django.contrib import admin
from weather.models import City,User,Weather,Log,Alarm,AlarmLog


class CityAdmin(admin.ModelAdmin):
    list_display = ('cid','province','city')
    search_fields = ('province','city','cid')

class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_num','fid','reg_ts','sub_type','active','wid','send_time')
    list_filter = ('reg_ts','active')
    search_fields = ('phone_num','fid',)
    date_hierarchy = 'reg_ts'

    
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('cid','hour','info','fetch_ts')
    list_filter = ('hour','cid','fetch_ts')

class LogAdmin(admin.ModelAdmin):
    list_display = ('time','level','event')
    list_filter = ('level',)
    date_hirerachy = 'time'
    search_fields = ('event',)

class AlarmAdmin(admin.ModelAdmin):
    list_display = ('color_id','title','url','content','area_code','pub_time','fetch_time')
    list_filter = ('area_code','color_id')
    search_fields = ('title','content','area_code','color_id',)
    date_hierarchy = 'pub_time'

class AlarmLogAdmin(admin.ModelAdmin):
    list_display = ('alarm','user','details','send_time')
    date_hierarchy = 'send_time'
    
admin.site.register(City,CityAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Weather,WeatherAdmin)
admin.site.register(Log,LogAdmin)
admin.site.register(Alarm,AlarmAdmin)
admin.site.register(AlarmLog,AlarmLogAdmin)