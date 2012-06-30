#encoding:utf-8
import urllib2, re, sys
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

def test1():
    page = urllib2.urlopen("http://www.nmc.gov.cn/alarm/index.htm")
    soup = BeautifulSoup(page)
    #released = soup.findAll(text=re.compile("Released"))
    #divs = soup.findAll('div')
    #print divs
    print soup.contents[2].contents[0]
    
    #print released

def test2():
    page = urllib2.urlopen('http://m.cnbeta.com').read()
    soup = BeautifulStoneSoup(page)
    #print soup.prettify()
    print soup.contents[0]

def get_alarms():
    alarm_url = 'http://www.nmc.gov.cn/alarm/index.htm'
    page = urllib2.urlopen(alarm_url).read()
    soup = BeautifulSoup(page.replace('\n',''))
    tds = soup.findAll('td', width="28")
    alarms = []
    #print td.contents[1]['id'] #取预警id号
    for td in tds :
        title_td = td.nextSibling.nextSibling
        
        info = {
            'id':td.contents[1]['id'],            
            'link':title_td.contents[1]['href'],
            'title':title_td.contents[1].text.strip(),
            'time':title_td.nextSibling.nextSibling.text.replace('&nbsp;','')
        }
        alarms.append(info)
    return alarms

    
def test3():
    all = get_alarms()
    for alarm in all :
        print alarm['id'],alarm['link'],alarm['title'],alarm['time']         
        
        
def fetch_oneline(url=''):
    
    if '' == url : url = '/sjyj/0002004/201206271832594311.htm'
    url = 'http://www.nmc.gov.cn%s' % url
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    alarmtexts = soup.findAll(id=re.compile('alarmtext'))
    return '\n'.join([alarmtext.text.strip() for alarmtext in alarmtexts])
    
    
    
        
if __name__ == '__main__':
    test4 = fetch_oneline
    test4('/sjyj/0002004/201206271631539230.htm')
    sys.exit(0)