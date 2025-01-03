from pathlib import Path
import environ
from os import path

env = environ.Env(
  SECRET_KEY=(str, ''),
  DEBUG=(bool, True),
  EMAIL_HOST=(str, ''),
  EMAIL_HOST_PASSWORD=(str, ''),
  EMAIL_PORT=(int, 0),
  EMAIL_HOST_USER=(str, ''),
  EMAIL_USE_SSL=(bool, True)
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # нужно чтобы django мог подключать статические файлы к проекту
    'women.apps.WomenConfig', # указываем наше приложение, чтобы можно было с ним работать
    'debug_toolbar', # название приложения для библиотеки django-debug-toolbar
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', # дополнительный пакет для работы библиотеки django-debug-toolbar
]

ROOT_URLCONF = 'sitewomen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
          BASE_DIR / 'templates',
        ], # позволяет указать нестандартные пути к шаблонам, к примеру, BASE_DIR / 'templates'
        'APP_DIRS': True, # с выставленным параметром в True ищет шаблоны во всех приложения, которые прописаны в коллекции INSTALLED_APPS
        # в папке templates
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

WSGI_APPLICATION = 'sitewomen.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'ru-RU' # устанавливаем язык на русский (чтобы локализаци админ панели была на русском)
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# по умолчанию в режиме разработки (DEBUG=True) django ищет нужные статичные файлы внутри папок static, которые находятся в папке с приложениями (к примеру, women),
# которые должны быть обязательно указаны INSTALLED_APPS
# python manage.py collectstatic - берет всю статику из приложений из папок static и переносит все в одну корневую папку static (нужно для продакшен версии)
STATIC_URL = 'static/' # префикс для URL-адреса по которому будет идти обращение к статическому файлу
STATIC_ROOT = BASE_DIR / STATIC_URL # путь к общей статической папке
#STATICFILES_DIRS # список дополнительных (нестандартных) путей к статическим файлам, используемых для сбора и режима отладки

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# python manage.py runserver --insecure - позволяет запустить веб сервер в режиме DEBUG=FALSE при этом статика будет подключаться

# python manage.py shell - команда запускает в терминале оболочку django, позволяет выполнять ORM команды для работы с базой данных

# python manage.py createsuperuser - создает пользователя, у которого будет доступ к панели администрирования