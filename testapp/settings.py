# Django settings for cms project.
import os
PROJECT_DIR = os.path.dirname(__file__)

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'cms.sqlite'

SITE_ID = 1

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = '*xq7m@)*f2awoj!spa0(jibsrz9%c0d=e(g)v*!17y(vx0ue_3'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    'django.core.context_processors.csrf',
)



ROOT_URLCONF = 'testapp.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'localcrawler',
    'testapp',
)

gettext = lambda s: s

LANGUAGE_CODE = "en"

APPEND_SLASH = True