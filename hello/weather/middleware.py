#!encoding:utf-8
from django.http import HttpResponsePermanentRedirect
class TrustedHostMiddleware(object):

    def process_request(self, request):
        sae_host ='sms128.sinaapp.com'
        trust_me = 'hello-falconchen.dotcloud.com:22454'
        if request.META.has_key('TRUSTED_HOSTS') :
            request.META['TRUSTED_HOSTS'] = '%s %s' % (trust_me,request.META['TRUSTED_HOSTS'])
        else:
            request.META['TRUSTED_HOSTS'] = trust_me        
        if request.META['HTTP_HOST'] != sae_host and '127.0.0.1' not in request.META['HTTP_HOST'] and 'www' not in request.META['HTTP_HOST']:
            script_url = request.META['script_url'] if request.META.has_key('script_url') else ''
            return HttpResponsePermanentRedirect('http://%s%s' % (sae_host,script_url))