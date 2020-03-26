from .base import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'HOST': 'cdb-kpkr35fu.cd.tencentcdb.com',
        'USER': 'root',
        'PASSWORD': 'gly1+1=2',
        'PORT': 10058,

    }
}

