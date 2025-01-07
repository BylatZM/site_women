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
    'women.apps.WomenConfig', # указываем наше приложение women, чтобы можно было с ним работать
    'debug_toolbar', # название приложения для библиотеки django-debug-toolbar
    'users.apps.UsersConfig', # указываем наше приложение women, чтобы можно было с ним работать
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # чтобы работали сессии, с помощью которых работает доступ к admin панели
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # чтобы работала авторизация
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
                'django.template.context_processors.request', # позволяет обращаться к переменной request внутри шаблонов
                'django.contrib.auth.context_processors.auth', # позволяет обращаться к переменной user внутри шаблонов
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.get_women_context', # определили функцию, которая во все шаблоны будет передавать переменную mainmenu с нашим меню
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
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# по умолчанию в режиме разработки (DEBUG=True) django ищет нужные статичные файлы внутри папок static, которые находятся в папке с приложениями (к примеру, women),
# которые должны быть обязательно указаны INSTALLED_APPS
# python manage.py collectstatic - берет всю статику из приложений из папок static и переносит все в одну корневую папку static (нужно для продакшен версии)
# префикс для URL-адреса по которому будет идти обращение к статическому файлу
STATIC_URL = 'static/'
# путь к общей статической папке
# параметр не указывается, если задан STATICFILES_DIRS
# STATIC_ROOT = BASE_DIR / STATIC_URL
# список дополнительных (нестандартных) путей к статическим файлам, используемых для сбора и режима отладки
STATICFILES_DIRS = [BASE_DIR / 'static', ]

MEDIA_ROOT = BASE_DIR / 'media' # каталог, папка куда будут размещаться все загружаемые файлы
MEDIA_URL = '/media/' # добавляет префикс ко всем url адресам медиа файлов, по типу картинок

# задает URL-адрес, на который следует перенаправить пользователя после успешной авторизации
# можно указать имя паршрута, на который нужно перенаправить
LOGIN_REDIRECT_URL = 'home'

# LOGIN_URL - определяет URL-адрес, на который следует перенаправить неавторизованного пользователя при попытке посетить 
# закрытую страницу сайта

# задает URL-адрес, на который перенаправляется пользователь после выхода
LOGOUT_REDIRECT_URL = 'users:login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# python manage.py runserver --insecure - позволяет запустить веб сервер в режиме DEBUG=FALSE при этом статика будет подключаться

# python manage.py shell - команда запускает в терминале оболочку django, позволяет выполнять ORM команды для работы с базой данных

# python manage.py createsuperuser - создает пользователя, у которого будет доступ к панели администрирования