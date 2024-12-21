from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, "year4") # функция регистрации собственных конвертеров

urlpatterns = [
  path('', views.index), # localhost:8000
  path('cats/<int:cat_id>/', views.categories), # пример возможного url: localhost:8000/cats/2/
  path('cats/<slug:cat_slug>/', views.categories_by_slug), # пример возможного url: localhost:8000/cats/cdcsdcsd/
  # объявление url с собственным конвертером
  path('archive/<year4:year>/', views.archive), # пример возможного url: localhost:8000/archive/2002
]

'''
При запросе django проходиться по всем path и смотрит, где совпадает url адрес, после нахождения совпадения отрабатывает определенная
функция view

path('cats/<int:cat_id>/', ...) - такому path в url должно передаваться только число, которое будет присвоено переменной cat_id
cat_id можно будет получить в функции views.categories

виды конвертаров в url:
* str - принимает строку, КРОМЕ символа "/"
* int - принимает числовые значения
* slug - набор английских букв, цифр, подчеркиваний, дефисов, КРОМЕ символа "/"
* uuid - принимает цифры, малые английские буквы и дефис
* path - любая не пустая строка, включая символ "/"

Конвертер slug включается в себя конвертер int, поэтому, если url будут совпадать, и при этом url где принимается конвертер
slug будет стоять выше, то path с url включающий конвертер int никогда не сработает

Второй path не сработает, так как будет всегда отрабатывать первый !!
path('cats/<slug:cat_slug>/', views.categories_by_slug)
path('cats/<int:cat_id>/', views.categories)
'''