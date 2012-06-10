#coding:utf-8

from backend import backend_init
import django,json


def import_city():
    '''
    导入城市代码列表
    '''
    try:
        import hello.settings
        from hello.weather.models import *
        f = open('jdata.js')
        jdata = f.read()[11:-1]

        cities = json.loads(jdata)
        for prov,city_info in cities.iteritems():
            for cid,city in city_info.iteritems():
                print prov,cid,city
                c = City(cid=cid,province=prov,city=city)
                c.save()

        
        
    except ImportError,e:
        print e


##    for city in City.objects.all():
##        print city,city.cid
##        
    
    

if __name__ =='__main__':
    backend_init()
    import_city()
