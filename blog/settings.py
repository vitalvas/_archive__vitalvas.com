#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.conf import global_settings


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@b4t8dsqezyb+iq7)+$(ct@a@(15q2&+p7!o=12x9cp55l#3^w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getcwd().startswith('/Users/vitalvas') else False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sitemaps',
	'blog',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
#	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'htmlmin.middleware.HtmlMinifyMiddleware',
)

ROOT_URLCONF = 'blog.urls'

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'HOST': 'localhost',
		'NAME': 'vitalvascom',
		'USER': 'vitalvascom',
		'PASSWORD': '3E40fb1KOs4s2VbgUjNf',
	}
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-UA'

TIME_ZONE = 'EET'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/' if DEBUG else '/'

TEMPLATE_DIRS = (
	'templates',
)

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'www')

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
	'django.core.context_processors.request',
)

if DEBUG:
	LOGGING = {
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'standard': {
				'format': '[%(asctime)s] %(levelname)s \033[36m%(message)s\033[0m',
				'datefmt': '%d/%b/%Y %H:%M:%S',
			}
		},
		'filters': {
			'require_debug_true': {
				'()': 'django.utils.log.RequireDebugTrue',
			}
		},
		'handlers': {
			'console': {
				'level': 'DEBUG',
				'filters': ['require_debug_true'],
				'class': 'logging.StreamHandler',
				'formatter': 'standard',
			}
		},
		'loggers': {
			'django.db.backends': {
				'handlers': ['console'],
				'propagate': False,
				'level': 'DEBUG',
			}
		}
	}

sitemap_url = 'http://www.vitalvas.com/sitemap.xml'

ping_sitemap = [
	('http://google.com/webmasters/sitemaps/ping', {'sitemap':'%s'}),
	('http://webmaster.yandex.ru/wmconsole/sitemap_list.xml', {'host':'%s'}),
	('http://www.bing.com/webmaster/ping.aspx', {'siteMap':'%s'}),
]

