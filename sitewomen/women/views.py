from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from women.models import Women, Category, TagPost

menu = [
  {'title': 'О сайте', 'url_name': 'about'},
  {'title': 'Добавить статью', 'url_name': 'add_page'},
  {'title': 'Обратная связь', 'url_name': 'contact'},
  {'title': 'Войти', 'url_name': 'login'},
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

def show_category(request, cat_slug):
  category = get_object_or_404(Category, slug=cat_slug)
  posts = Women.published.filter(cat_id=category.pk)
  data = {
    'title': f'Рублика {category.name}', 
    'menu': menu, 
    'posts': posts,
    'cat_selected': category.pk,
  }
  return render(request, "women/index.html", context=data)

def show_tag_postlist(request, tag_slug):
  tag = get_object_or_404(TagPost, slug=tag_slug)
  posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)

  data = {
    'title': f"Тег: {tag.tag}",
    'menu': menu,
    'posts': posts,
    'cat_selected': None,
  }

  return render(request, 'women/index.html', context=data)

'''
Некоторые SELECT запросы:

Women.objects.filter(pk__in=[2, 5, 7, 10], is_published=True)
* делает select запрос, где "," - это логический символ "И"
------------------------------------------------------------
from django.db.models import Q - класс, которые позволяет писать более глубокие условия отбора данных

Women.objects.filter(Q(pk__lt=5) | Q(cat_id=2))
* символ "&" означает логическое И (средний приоритет)
* символ "|" означает логическое ИЛИ (низкий приоритет)
* символ "~" означает логический НЕ (высокий приоритет)
* делает select запрос, где выполняется условие (pk<5 ИЛИ cat_id=2)
* классы Q объединенные символами "|" или "&" формируют единый блок условий
* если в условии встречается символ "," то он разделяет условия на разные блоки подусловий
------------------------------------------------------------
Women.objects.filter(Q(pk__lt=5) & Q(cat_id=2))
* делает select запрос, где выполняется условие (pk<5 И cat_id=2)
------------------------------------------------------------
Women.objects.filter(~Q(pk__lt=5) & Q(cat_id=2))
* делает select запрос, где выполняется условие (pk НЕ меньше 5 И cat_id=2)
------------------------------------------------------------
Women.objects.filter(Q(pk__in=[1, 2, 5]) | Q(cat_id=2), title__icontains="ра")
* делает select запрос, где выполняется условие ((pk СОДЕРЖИТ ЛИБО 1, ЛИБО 2, ЛИБО 5 ИЛИ cat_id=2) И title="ра")
------------------------------------------------------------
Women.objects.filter(Q(title__icontains="ра") & Q(pk__in=[1, 2, 5]) | Q(cat_id=2))
* делает select запрос, где выполняется условие (title СОДЕРЖИТ "ра" И pk СОДЕРЖИТ ЛИБО 1, ЛИБО 2, ЛИБО 5 ИЛИ cat_id=2)

!! перед классами Q нельзя прописывать обычные параметры
Women.objects.filter(title__icontains="ра", Q(pk__in=[1, 2, 5]) | Q(cat_id=2)) - НЕДОПУСТИМО !!!
Women.objects.filter(Q(title__icontains="ра"), Q(pk__in=[1, 2, 5]) | Q(cat_id=2)) - исправленный вариант
------------------------------------------------------------
Women.objects.first()
* выбирает первую запись из списка QuerySet
------------------------------------------------------------
Women.objects.last()
* выбирает последнюю запись из списка QuerySet
------------------------------------------------------------
Women.objects.all().earliest("time_update")
* выбирает из модели запись, у которой значение time_update (datetimefield) меньше (самое далекое от настоящего)
------------------------------------------------------------
Women.objects.all().latest("time_update")
* выбирает из модели запись, у которой значение time_update (datetimefield) больше (самое ближайшее к настоящему)
------------------------------------------------------------
w = Women.objects.get(pk=2)
w.get_previous_by_time_update() - применяется только к полям типа время
* выбирает запись из модели Women, которая стоит раньше объекта w, причем раньше именно по полю time_update

расшифровка функции:
"get_previous_by" - константа означающая отобрать запись стоящую раньше
"_" - разделитель
"time_update" - по полю "time_update"

внутрь функции можно передать фильтры:
w.get_previous_by_time_update(pk__gt=1)

* если функция не найден запись, то будет возвращена ошибка "DoesNotExist"
------------------------------------------------------------
w = Women.objects.get(pk=2)
w.get_next_by_time_update() - применяется только к полям типа время
* выбирает запись из модели Women, которая стоит после объекта w, причем позже относительно поля time_update

расшифровка функции:
"get_next_by" - константа означающая отобрать запись стоящую после
"_" - разделитель
"time_update" - по полю "time_update"

внутрь функции можно передать фильтры:
w.get_next_by_time_update(pk__gt=1)

* если функция не найден запись, то будет возвращена ошибка "DoesNotExist"
------------------------------------------------------------
c3 = Category.objects.get(pk=3)
c3.posts.exists() - метод проверяет существуют ли запис-ь\и (результат типа boolean) из модели Women связанные с объектом c3 модели Category
------------------------------------------------------------
c2 = Category.objects.get(pk=2)
c2.posts.count() - метод возвращает количество записей из модели Women связанных с объектом c2 модели Category

Women.objects.filter(cat_id=1).count() - тоже отбирает количество записей, результат - число
'''