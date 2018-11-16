import os, subprocess

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Calculate the directory outside of BASE_DIR
PREV_DIR = "/".join(BASE_DIR.split("/")[:-1])


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p7o+hrs^95t8yw)^_yy8f7*$^!1!fp0s-@&6v@u3vf5+2k+ge#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = [
    'apps.video_app',
    'apps.user_app',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# spa middleware from https://github.com/metakermit/django-spa
# pip install django-spa

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'spa.middleware.SPAMiddleware'
]

ROOT_URLCONF = 'config.urls'


WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PREV_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


STATIC_URL = '/static/'

STATIC_ROOT = PREV_DIR + "/client/dist/client/"

# added for use with django spa middleware

STATICFILES_STORAGE = 'spa.storage.SPAStaticFilesStorage'

# add file uploads too

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PREV_DIR, 'thumbs')

ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif')


# programatically determine host when django starts up

b = subprocess.Popen("hostname -I", stdout=subprocess.PIPE, shell=True)
out, err = b.communicate()
HOST = out.decode().strip().split(" ")[0]
ALLOWED_HOSTS.append(HOST)
print("to connect, go to http://" + HOST + ":8000")
