from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound, HttpResponse
from women.models import Women, Category, TagPost, UploadFiles
from .forms import AddPostForm, UploadFileForm
from django.views import View
from django.views.generic import TemplateView

menu = [
  {'title': 'О сайте', 'url_name': 'about'},
  {'title': 'Добавить статью', 'url_name': 'add_page'},
  {'title': 'Обратная связь', 'url_name': 'contact'},
  {'title': 'Войти', 'url_name': 'login'},
]

class WomenHome(TemplateView):
  template_name = 'women/index.html'
  # в словарь можно передать данные известные только на момент определения самого класса
  # передать kwargs нельзя
  extra_context = {
    'title': 'Главная страница', 
    'menu': menu, 
    'posts': Women.published.filter(is_published=1).select_related('cat'),
    'cat_selected': 0,
  }

  # в методе можно указать какие экстра параметры через url могут быть прокинуты
  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs) # возвращает словарь с данными
  #   context['title'] = 'Главная страница'
  #   context['menu'] = menu
  #   context['posts'] = Women.published.filter(is_published=1).select_related('cat')
  #   context['cat_selected'] = int(self.request.GET.get('cat_id', 0)) # получаем экстра параметр с url
  #   return context

def about(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      fp = UploadFiles(file=form.cleaned_data.get('file', None))
      fp.save()
  else:
    form = UploadFileForm()
  data = {
    'title': 'О сайте',
    'menu': menu,
    'form': form
  }
  return render(request, "women/about.html", data)

def show_post(request, post_slug):
  post = get_object_or_404(Women, slug=post_slug) # либо возвращает 1 элемент из базы данных либо генерирует страницу с исключением 404

  data = {
    'title': post.title,
    'menu': menu,
    'post': post,
    'cat_selected': 1,
  }

  return render(request, "women/post.html", context=data)

class AddPage(View):
  def get(self, request):
    data = {
      'menu': menu,
      'title': 'Добавить статью',
      'form': AddPostForm(),
    }
    return render(request, 'women/addpage.html', data)

  def post(self, request):
    form = AddPostForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('home')
    data = {
      'menu': menu,
      'title': 'Добавить статью',
      'form': form,
    }
    return render(request, 'women/addpage.html', data)

def login(request):
  return HttpResponse("Авторизация")

def contact(request):
  return HttpResponse("Обратная связь")

def page_not_found(request, exception):
  return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def show_category(request, cat_slug):
  category = get_object_or_404(Category, slug=cat_slug)
  posts = Women.published.filter(cat_id=category.pk).select_related('cat')
  data = {
    'title': f'Рублика {category.name}', 
    'menu': menu, 
    'posts': posts,
    'cat_selected': category.pk,
  }
  return render(request, "women/index.html", context=data)

def show_tag_postlist(request, tag_slug):
  tag = get_object_or_404(TagPost, slug=tag_slug)
  posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

  data = {
    'title': f"Тег: {tag.tag}",
    'menu': menu,
    'posts': posts,
    'cat_selected': None,
  }

  return render(request, 'women/index.html', context=data)

'''
полезные методы в django:
select_related(key) - "жадная" загрузка связанных данных по внешнему ключу key, который имеет тип ForeignKey
Women.published.filter(is_published=1).select_related('cat')
* одним запросом отберет все данные с двух моделей

prefetch_related(key) - "жадная" загрузка связанных данных по внешнему ключу key, который имеет тип ManyToManyField

* в качестве параметра методам передается атрибут связывающий 2 модели

* методы используются, чтобы можно было сразу одним запросом получить все записи как основной модели, так и побочных
связанных с основной

* в django по умолчанию используется ленивая загрузка данных
* в момент обращения к атрибуту побочной модели идет select запрос на получение данных
'''

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
------------------------------------------------------------
from django.db.models import F - класс, позволяющий обращаться к отдельным полям и производить над ними мат. вычисления

Women.objects.filter(pk__gt=F("cat_id"))
* отберет все записи, у которых id больше чем значение cat_id этого же поля
------------------------------------------------------------
h = Husband.objects.get(pk=1)
h.m_count = F("m_count") + 1
h.save() - изменит m_count на +1

h.m_count += 1 - НЕДОПУСТИМА могут возникать неопределенности при одновременном изменении одной записи
h.m_count = F("m_count") + 1 - правильный вариант
h.m_count = 3 - допустимый вариант
------------------------------------------------------------
Husband.objects.all().annotate(is_married=Value(True))
* возвращает список QuerySet, где дополнительно формируется поле is_married типа boolean

Husband.objects.all().annotate(is_married=F("m_count") * 3)
Husband.objects.all().annotate(work_age=F("age") - 20, salary=F("age") * 1.1)

annotate - метод позволяет генерировать список новых полей для выборки
from django.db.models import Value - позволяет явно указать новое значение для генерируемого поля в методе annotate

Husband.objects.all().annotate(is_married=True) - НЕДОПУСТИМО !!!
Husband.objects.all().annotate(is_married=Value(True)) - правильный вариант
------------------------------------------------------------
from django.db.models import Count, Sum, Avg, Max, Min - агрегирующие функции можно использовать только внутри метода aggregate

* Count - подсчет количества записей

* Sum - суммирование значений поля

* Avg - среднее значение
Husband.objects.aggregate(Avg("age")) - возвращает словарь, с ключем age__avg со средним значением для поля age
Пример вывода: {'age__avg': 31.5}

* Max - максимальное значение
Husband.objects.aggregate(Max("age")) - возвращает словарь, с ключем age__max с максимальным значением для поля age
Пример вывода: {'age__max': 25}

* Min - минимальное значение
Husband.objects.aggregate(Min("age")) - возвращает словарь, с ключем состоящим из age (поле для которого ищем минимум) и
min (название агрегирующей функции)
Пример вывода: {'age__min': 25}

Еще примеры:
Husband.objects.aggregate(Min("age"), Max("age"))
>> {'age__min': 25, 'age__max': 40}
Husband.objects.aggregate(young=Min("age"), old=Max("age"))
>> {'young': 25, 'old': 40}
Husband.objects.aggregate(res=Max("age") - Min("age")) - при вычислении значения, название поля нужно ЯВНО указать
>> {'res': 15}
------------------------------------------------------------
Women.objects.values("title", "cat_id")
* возвращает список QuerySet состаящий из словарей с полями "title" и "cat_id" модели Women

Еще примеры вызовов:
Women.objects.values("title", "cat_id").get(pk=1)
* вернет просто словарь, так как запись всего одна
Women.objects.values("title", "cat__name").get(pk=1)
* вернет словарь, но дополнительно сделает INNER JOIN, чтобы получить поле name модели Category связанной с объектом модели Women
------------------------------------------------------------
Women.objects.values("cat_id").annotate(Count("id"))
* сначала вернет все записи, где будут только поля cat_id
* потом сгруппирует записи по похожим значениям cat_id и присвоит результат количества записей переменной id__count
Пример вывода: <QuerySet [{'cat_id': 1, 'id__count': 3}, {'cat_id': 2, 'id__count': 2}]>

! последовательное использование методов values и annotate (в связке с агрегирующей функцией) позволяет
группировать записи по полю, указанному в values

Примеры выводов:
Women.objects.values("cat_id").annotate(total=Count("id"))
>> <QuerySet [{'cat_id': 1, 'total': 3}, {'cat_id': 2, 'total': 2}]>

Category.objects.annotate(total=Count("posts"))
* сначала вернет все записи
* далее для каждой записи вернет значение total равное количеству значений постов 
(через атрибут обратного связывания posts указанного в модели Women)
>> <QuerySet [<'Category': Актрисы>, <'Category': Певицы>, <'Category': Спортсменки>]>
расшифровка >> [{'id': 1, 'name': 'Актрисы', 'slug': 'aktrisy', 'total': 3}, 
{'id': 2, 'name': 'Певицы', 'slug': 'pevicy', 'total': 2}, {'id': 1, 'name': 'Спортсменки', 'slug': 'sportsmenki', 'total': 0}]

! запросы с методом annotate и агрегирующих функций медленные, нужно оценивать целесобразность их использования
------------------------------------------------------------
from django.db.models.function import Length - функция для вычисления на стороне СУБД

Husband.objects.annotate(len_name=Length('name'))
* вернет все записи модели Husband, но добавит в них поле len_name равное длинне их полей name

Примеры выводов:
Husband.objects.annotate(len_name=Length('name')).values('len_name')
>> <QuerySet [{'len_name': 9}, {'len_name': 10}, {'len_name': 12}, {'len_name': 10}]>
'''