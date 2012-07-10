from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    #('^$',hello_world),
    ('^$',include('weather.urls')),
    ('^weather/',include('weather.urls')),
    (r'(?P<path>^favicon\.ico$)', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}), #icon url
    (r'^blog/',include('blog.urls')),
    
    # Example:
    # (r'^hello/', include('hello.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG == True:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
         (r'^(?P<path>favicon.ico$)', 'django.views.static.serve',         
         {'document_root': settings.STATIC_ROOT}),
                            
##        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
##         {'document_root': settings.STATIC_ROOT}),
                            
    )
