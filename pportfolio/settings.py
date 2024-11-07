# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-ea&txt6+a7-jxuopk^$8ij=ltbvyxs)7d*+lku##ix4dfgpeg6'
DEBUG = True
#DEBUG = False
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appportfolio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pportfolio.urls' #siempre por defecto, no se toca

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'pportfolio.wsgi.application'

if DEBUG == False:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Modo local windows
if DEBUG == True:
    print("************************DESARROLLO EN LOCAL")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'vportfolio', #nombre de la base de datos
            'USER': 'postgres',
            'PASSWORD': 'Adivinala1.',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SITE_ID = 1
SITE_NAME = "Portfolio"
LANGUAGE_CODE = 'es-ES'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Los comentarios de ## no son míos.
TEMPLATE_CONTEXT_PROCESSORS = ( #procesos de contexto, copiar pegar
'django.contrib.auth.context_processors.auth',
    'djblets.siteconfig.context_processors.siteconfig',
    'djblets.util.context_processors.settingsVars',
    'djblets.util.context_processors.siteRoot',
    'djblets.util.context_processors.ajaxSerial',
    'djblets.util.context_processors.mediaSerial',
    'django.template.context_processors.request',)


##la parte estática es obligatoria para Heroku y para nuestra máquina
STATIC_URL = '/static/'    ##js, css3, .. #(apunta a donde está el contenido estático)
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'  ##videos, imágenes #(apuntar a media)
STATIC_ROOT= os.path.join(BASE_DIR, 'static')


## declara la ruta donde se enlazará el contenido estático
STATICFILES_DIRS = ( #apunta a los directorios de static.
    ('css', os.path.join(STATIC_ROOT, 'css')),  ##os es de operating system
    ('js', os.path.join(STATIC_ROOT, 'js')), ##path para que coja el path (C:\....) de automáticamente
    ('images', os.path.join(STATIC_ROOT, 'images')),##join es para que una todo en un espectro de búsqueda.
    ('img', os.path.join(STATIC_ROOT, 'img')),
)

STATICFILES_FINDERS = ( #en las carpetas anteriores (staticfiles_dirs) busca los archivos, mientras que en el anterior le digo donde busca
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #finder es un buscador universal para todos los sistemas operativos
)
TEMPLATE_LOADERS = ( #cargadores de templates, los que cargan el html
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
)

# correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hajarziane24@gmail.com'  # emisor
EMAIL_HOST_PASSWORD = 'ngez yvrw wlxn tikg'
EMAIL_USE_TLS = True  # seguridad de gmail
