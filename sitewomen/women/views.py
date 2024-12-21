from django.http import HttpResponse

def index(request): # request экземпляр класса HttpRequest
  return HttpResponse("Страница приложения women.")

def categories(request):
  return HttpResponse("<h1>Статьи по категориями</h1>")