"""
Django settings for academicstoday_project project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+hjm%=(6hyfz+jh+n9w3_)=#4obtl=xtn37@0fm_m3k9f7)rp7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'account',
    'landpage',
    'registrar',
    'student',
    'teacher',
    'publisher'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'academicstoday_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'academicstoday_project.wsgi.application'


# Captcha App

if 'test' in sys.argv:
    CAPTCHA_TEST_MODE = True


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "academicstoday_db",
        "USER": "django",
        "PASSWORD": "123password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


# User uploaded content.
#

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# JavaScript Libraries
#
SB_ADMIN_2_CSS_LIBRARY_URLS = [
    "bower_components/bootstrap/dist/css/bootstrap.min.css",
    "bower_components/metisMenu/dist/metisMenu.min.css",
    "css/timeline.css",
    "css/sb-admin-2.css",
    "bower_components/morrisjs/morris.css",
    "bower_components/font-awesome/css/font-awesome.min.css",
]

SB_ADMIN_2_JS_LIBRARY_URLS = [
    "bower_components/jquery/dist/jquery.min.js",
    "bower_components/bootstrap/dist/js/bootstrap.min.js",
    "bower_components/metisMenu/dist/metisMenu.min.js",
    "bower_components/raphael/raphael-min.js",
#    "bower_components/morrisjs/morris.min.js",
#    "js/morris-data.js",
    "js/sb-admin-2.js",
]

AGENCY_CSS_LIBRARY_URLS = [
    "js/jquery/1.11.1/jquery-ui.css",
    "js/bootstrap/3.3.2/css/bootstrap.min.css",
    "js/font-awesome/4.2.0/css/font-awesome.css",
    "js/font-awesome/4.2.0/css/font-awesome.min.css",
    "css/landpage.css",
    "css/agency.css"
]

AGENCY_JS_LIBRARY_URLS = [
    "js/jquery/1.11.1/jquery.min.js",
    "js/jquery/1.11.1/jquery.tablesorter.js",
    "js/jquery/1.11.1/jquery-ui.js",
    "js/jquery-easing/1.3/jquery.easing.min.js",
    "js/bootstrap/3.3.2/js/bootstrap.min.js",
    "js/bootstrap/3.3.2/js/bootstrap.js",
    "js/classie/1.0.0/classie.js",
    "js/cbpanimatedheader/1.0.0/cbpAnimatedHeader.js",
    "js/cbpanimatedheader/1.0.0/cbpAnimatedHeader.min.js",
    "js/jqbootstrapvalidation/1.3.6/jqBootstrapValidation.js",
    "js/misc/agency.js"
]


# Custom Constants
#

# Question Types
ESSAY_QUESTION_TYPE = 1
MULTIPLECHOICE_QUESTION_TYPE = 2
TRUEFALSE_QUESTION_TYPE = 3
RESPONSE_QUESTION_TYPE = 4
QUESTION_TYPES = [
    ESSAY_QUESTION_TYPE,
    MULTIPLECHOICE_QUESTION_TYPE,
    TRUEFALSE_QUESTION_TYPE,
    RESPONSE_QUESTION_TYPE,
]

# Course Status
COURSE_UNAVAILABLE_STATUS = 0
COURSE_AVAILABLE_STATUS = 1
COURSE_SUBMITTED_FOR_REVIEW_STATUS = 2
COURSE_IN_REVIEW_STATUS = 3
COURSE_REJECTED_STATUS = 4

# Video player choices
NO_VIDEO_PLAYER = '0'
YOUTUBE_VIDEO_PLAYER = '1'
VIMEO_VIDEO_PLAYER = '2'
BLIPTV_VIDEO_PLAYER = '3'

# File Upload Types
UNKNOWN_FILE_UPLOAD_TYPE = 0
PDF_FILE_UPLOAD_TYPE = 1