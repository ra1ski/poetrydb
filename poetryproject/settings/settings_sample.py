try:
    from poetryproject.settings import *
except ImportError:
    pass

DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'debug_toolbar',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_poetry',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, "../static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

LANGUAGE_CODE = 'en-En'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/email-messages/'
EMAIL_HOST_USER = 'test@localhost.dev'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "../static"),
]
