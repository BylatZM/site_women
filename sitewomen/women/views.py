from django.http import HttpResponse

def index(request): # request экземпляр класса HttpRequest
  return HttpResponse("Страница приложения women.")

def categories(request, cat_id): # cat_id параметр, который передается через url для маршрута localhost:8000/cats/<число>/
  return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")

def categories_by_slug(request, cat_slug):
  return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")

def archive(request, year):
  return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")