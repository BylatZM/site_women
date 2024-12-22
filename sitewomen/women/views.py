from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime
from django.shortcuts import redirect, reverse
from django.template.loader import render_to_string # функция преобразует html шаблоны в строку, чтобы их можно было передавать в соответствующие классы

def index(request): # request экземпляр класса HttpRequest
  t = render_to_string('women/index.html') # преобразует html в строку
  return HttpResponse(t) 

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