#coding=utf-8
from cookielib import CookieJar
from urllib2 import Request,build_opener,HTTPHandler,HTTPCookieProcessor
from urllib import urlencode

from re import compile

from gzip import GzipFile
try:from cStringIO import StringIO
except:from StringIO import StringIO

#data="x=3&y=4"
opener = build_opener(HTTPCookieProcessor(CookieJar()), HTTPHandler)
html = opener.open(Request('http://test.com/s.php',data='',headers={'Accept-encoding':'gzip','Client-IP':'202.204.76.254'})).read()

print html