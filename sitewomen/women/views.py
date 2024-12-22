from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from women.models import Women

menu = [
  {'title': 'О сайте', 'url_name': 'about'},
  {'title': 'Добавить статью', 'url_name': 'add_page'},
  {'title': 'Обратная связь', 'url_name': 'contact'},
  {'title': 'Войти', 'url_name': 'login'},
]

cats_db = [
  {'id': 1, 'name': 'Актрисы'},
  {'id': 2, 'name': 'Певицы'},
  {'id': 3, 'name': 'Спортсменки'},
]

def index(request): # request экземпляр класса HttpRequest
  posts = Women.published.filter(is_published=1)
  data = {
    'title': 'Главная страница', 
    'menu': menu, 
    'posts': posts,
    'cat_selected': 0,
  }
  return render(request, "women/index.html", context=data) # функция преобразует html в строку и возвращает результат, как HttpResponse

def about(request):
  return render(request, "women/about.html", {'title': 'О сайте', 'menu': menu})

def show_post(request, post_slug):
  post = get_object_or_404(Women, slug=post_slug) # либо возвращает 1 элемент из базы данных либо генерирует страницу с исключением 404

  data = {
    'title': post.title,
    'menu': menu,
    'post': post,
    'cat_selected': 1,
  }

  return render(request, "women/post.html", context=data)

def addpage(request):
  return HttpResponse("Добавление статьи")

def login(request):
  return HttpResponse("Авторизация")

def contact(request):
  return HttpResponse("Обратная связь")

def page_not_found(request, exception):
  return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def show_category(request, cat_id):
  posts = Women.published.filter(is_published=1)
  data = {
    'title': 'Отображение по рубрикам', 
    'menu': menu, 
    'posts': posts,
    'cat_selected': cat_id,
  }
  return render(request, "women/index.html", context=data)
