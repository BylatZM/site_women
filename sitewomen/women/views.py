from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from datetime import datetime
from django.shortcuts import redirect, reverse

def index(request): # request экземпляр класса HttpRequest
  return HttpResponse("Страница приложения women.")

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
    return redirect(uri) # делает редирект на основную страницу с кодом 302
  return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

# функция для обработки ошибки 404
def page_not_found(request, exception):
  return HttpResponseNotFound("<h1>Страница не найдена</h1>")

'''
виды кодов редиректов:
* 301 - страница перемещена на другой постоянный URL-адрес
* 302 - страница перемещена временно на другой URL-адрес

Функция redirect в качестве первого параметра может принимать:
* redirect('/') - строка url адрес
* redirect(index) - функцию представления
* redirect('home') - имя маршрута (рекоммендуемый вариант)

Функция redirect может принимать дополнительные параметры, как аргументы для url адреса
* redirect('cats', 'music') - где 'music' является url аргументом конвертера slug

Перед функцией redirect обязательно нужно указать return

Чтобы сделать редирект с кодом 302, можно использовать:
------------------
from django.shortcuts import redirect
return redirect('/')
------------------

Чтобы сделать редирект с кодом 301, можно использовать:
------------------
from django.shortcuts import redirect
redirect('/', permanent=True)
------------------
'''