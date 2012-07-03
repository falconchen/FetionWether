#!encoding:utf-8
class TrustedHostMiddleware(object):

    def process_request(self, request):
        trust_me = 'hello-falconchen.dotcloud.com:22454'
        if request.META.has_key('TRUSTED_HOSTS') :
            request.META['TRUSTED_HOSTS'] = '%s %s' % (trust_me,request.META['TRUSTED_HOSTS'])
        else:
            request.META['TRUSTED_HOSTS'] = trust_me
        return None