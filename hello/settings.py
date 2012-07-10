#coding:utf-8
# Django settings for hello project.
import os.path, sys
#from trusthost import TrustedHostMiddleware

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.append(HERE)

STATIC_PATH=os.path.join(HERE, 'medias').replace('\\','/')
import json
#json_file =r'F:\cygwin\home\dotcloud\environment.json' if os.sep =='\\' else '/home/dotcloud/environment.json'
json_file = os.path.abspath(os.path.join(HERE,os.path.pardir,os.path.pardir,'environment.json'))
#print json_file

with open(json_file) as f:
    env = json.load(f,encoding='utf-8')

#DEBUG = True if '127.0.0.1' in env['DOTCLOUD_DB_MYSQL_HOST'] else False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

FETION = env['FETION']

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #'ENGINE': 'pymysql_django',
        'NAME': 'hello',                      # Or path to database file if using sqlite3.
        'USER': env['DOTCLOUD_DB_MYSQL_LOGIN'],                      # Not used with sqlite3.
        'PASSWORD': env['DOTCLOUD_DB_MYSQL_PASSWORD'],                  # Not used with sqlite3.
        'HOST': env['DOTCLOUD_DB_MYSQL_HOST'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': env['DOTCLOUD_DB_MYSQL_PORT'],                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/dotcloud/data/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

#Maybe 1.2.x not show the differences between static and media
STATIC_ROOT = '/home/dotcloud/data/static/'
STATIC_URL = '/static/'

#ADMIN_MEDIA_PREFIX = '/static/admin/'
#STATICFILES_DIRS = ('/home/dotcloud/data/static/',)


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wju@h&-#z553f=@bl85!kd-k-_^#v28q2huf42!_-9l2rr(dx5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'weather.middleware.TrustedHostMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    #'staticfiles',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'blog',
    'weather',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    #'staticfiles.context_processors.static', #
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)