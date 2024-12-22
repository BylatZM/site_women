from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse

menu = [
  {'title': 'О сайте', 'url_name': 'about'},
  {'title': 'Добавить статью', 'url_name': 'add_page'},
  {'title': 'Обратная связь', 'url_name': 'contact'},
  {'title': 'Войти', 'url_name': 'login'},
]

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

def show_post(request, post_id):
  return HttpResponse(f"Отображение статьи с id = {post_id}")

def addpage(request):
  return HttpResponse("Добавление статьи")

def login(request):
  return HttpResponse("Авторизация")

def contact(request):
  return HttpResponse("Обратная связь")

def page_not_found(request, exception):
  return HttpResponseNotFound("<h1>Страница не найдена</h1>")


#<p><a href="{% url 'post' p.id %}">Читать пост</a></p>