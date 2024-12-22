from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.defaultfilters import slugify # как работает смотри в файле women/templates/women/index.html

menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

data_db = [
  {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
  {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
  {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]

def index(request): # request экземпляр класса HttpRequest
  data = {
    'title': 'Главная страница', 
    'menu': menu, 
    'posts': data_db
  }
  return render(request, "women/index.html", context=data) # функция преобразует html в строку и возвращает результат, как HttpResponse

def about(request):
  return render(request, "women/about.html", {'title': 'О сайте'})

def categories(request, cat_id): # cat_id параметр, который передается через url для маршрута localhost:8000/cats/<число>/
  return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")

def categories_by_slug(request, cat_slug):
  # Получение экстра параметров с url
  if request.GET:
    '''
    Например
    url: localhost:8000/?name=Bylat
    результат: <QueryDict: {'name': ['Bylat']}>
    '''
    print(request.GET)
  return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")

def archive(request, year):
  if year > datetime.now().year:
    uri = reverse('cats', args=('music', )) # функция reverse формирует url адрес, позволяет удобно передавать аргументы через список, кортеж
    return redirect(uri)
  return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

# функция для обработки ошибки 404
def page_not_found(request, exception):
  return HttpResponseNotFound("<h1>Страница не найдена</h1>")