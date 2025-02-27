from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from django.urls import reverse_lazy
from women.models import Women
from .forms import AddPostForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from .utils import DataMixin
from django.core.paginator import Paginator

#ListView предназначен для отображения шаблонов со списком чего-нибудь, в данном случае статей
# по умолчанию класс ListView шаблон берет по шаблону: <имя приложения>/<имя модели>_list.html
# по умолчанию список записей указанной модели класс ListView дает доступ через переменную object_list
# в ListView есть функционал пагинации, чтобы указать количество записей модели нужно задать атрибут paginate_by
# в template ListView передает экземпляр класса пагинации под названием page_obj
class WomenHome(DataMixin, ListView):
  model = Women
  template_name = 'women/index.html'
  context_object_name = 'posts' # переопределяем словарь с записями нашей модели
  title_page = 'Главная страница'
  cat_selected = 0

  def get_queryset(self): # позволяет указать то, что будет указано в качестве списка значений из модели Women
    return self.model.published.all().select_related('cat')
  # чтобы динамически определять параметры передаваемые в шаблон, можно переопределить метод get_context_data

def about(request):
  contact_list = Women.published.all()
  paginator = Paginator(contact_list, 3)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, "women/about.html", {'title': 'О сайте', 'page_obj': page_obj, })

# DetailView класс предназначен для вывода в template детальной информации по конкретному экземпляру модели
# Ищет запись по pk или по slug
# Если запись не будет найдена, то автоматически будет возвращена ошибка 404
# DetailView выводит информацию по одной записи, ListView информацию по списку записей
# по умолчанию выбранную запись модели класс DetailView передает в шаблон через переменную object
class ShowPost(DataMixin, DetailView):
  model = Women
  template_name = 'women/post.html'
  slug_url_kwarg = 'post_slug' # указываем название переменной, передаваемой через url, по которой нужно искать запись в модели по полю slug
  context_object_name = 'post' # указываем название переменной, которая будет содержать единственную запись модели
  # pk_url_kwarg = 'post_pk' - указываем название переменной, передаваемой через url, по которой нужно искать запись в модели по полю pk

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return self.get_mixin_context(context, title=context['post'].title)
  
  def get_object(self, queryset=None): # метод получения самого объекта, проверим, если запись опубликовано пропускаем, иначе ошибка 404
    return get_object_or_404(self.model.published, slug=self.kwargs[self.slug_url_kwarg])

# класс CreateView похож на класс FormView за одним исключением, что у него реализован по умолчанию метод сохранения данных в бд
# так как форма связана с моделью, то класс обратится к модели и вызовет метод save, чтобы сделать запрос на создание в 
# базе данных и передать в запрос провалидированные данные
# PermissionRequiredMixin - класс, который позволит ограничить доступ к шаблону, давая доступ только авторизованному пользователю
class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
  form_class = AddPostForm # ссылка на класс формы
  template_name = 'women/addpage.html'
  # success_url определеяет url адрес после успешной отправки и обработки формы
  # reverse_lazy возвращает полный маршрут, в данном случае по имени маршрута
  # используем reverse_lazy вместо reverse потому что на момент создания самого класса AddPage маршрута 'home' еще не существует
  # reverse_lazy строит маршрут не сразу, а тогда, когда он необходим
  success_url = reverse_lazy('home')
  title_page = "Добавить статьи"
  # permission_required позволяет прописать какие действия может совершать пользователь с определенными правами
  # в данном случае, если через панель администрации дать пользователю разрешение вида: Can add известные женщины, то пользователю разблокируется страница
  # если пользователь не будет иметь данное право, то он получит ошибку 403 Forbidden
  # по умолчанию пользователь в модели User которого указаны is_superuser: True имеет все права
  # women.add_women - women нанвание приложения, add - право добавлять записи, women - название модели, в которую разрешено добавлять
  permission_required = 'women.add_women'

# класс UpdateView позволяет редактировать записи из модели
# класс UpdateView ищет запись по id или по slug-у, через url нужно передать переменную pk типа int или slug типа slug
# есть параметры pk_url_kwarg и slug_url_kwarg также как и у DetailView
class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
  model = Women # указываем модель, записи которой будет редактировать
  fields = ['title', 'content', 'photo', 'is_published', 'cat'] # Указываем поля генерируемой формы, которые будем редактировать
  template_name = 'women/addpage.html'
  # success_url определеяет url адрес после успешной отправки и обработки формы
  # reverse_lazy возвращает полный маршрут, в данном случае по имени маршрута
  # используем reverse_lazy вместо reverse потому что на момент создания самого класса AddPage маршрута 'home' еще не существует
  # reverse_lazy строит маршрут не сразу, а тогда, когда он необходим
  success_url = reverse_lazy('home')
  title_page = "Редактирование статьи"
  # даем права на изменение модели Women
  permission_required = "women.change_women"

class DeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
  model = Women
  template_name = 'women/addpage.html'
  success_url = reverse_lazy('home')
  title_page = "Удаление статьи"
  permission_required = 'women.delete_women'
  permission_denied_message = 'Недостаточно прав доступа'

# декоратор для ограничения доступа к view функции только авторизованным пользователям
# perm указывает какой тип разрешения нужен, а raise_exception нужно ли выводить ошибку 403, если False, то перенаправит на страницу авторизации
@permission_required(perm='women.view_women', raise_exception=True)
def contact(request):
  return HttpResponse("Обратная связь")

def page_not_found(request, exception):
  return HttpResponseNotFound("<h1>Страница не найдена</h1>")

class WomenCategory(DataMixin, ListView):
  model = Women
  template_name = 'women/index.html'
  context_object_name = 'posts'
  allow_empty = False # при пустом списке posts генерирует ошибку 404

  def get_queryset(self):
    #self.kwargs - возвращает словарь всех экстра параметров переданных по url
    return self.model.published.filter(cat__slug=self.kwargs.get('cat_slug')).select_related('cat')
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    cat = context['posts'][0].cat # передается по умолчанию, так как используем ListView, с определенными переменными model и context_object_name
    return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)

class TagPostList(DataMixin, ListView):
  model = Women
  context_object_name = 'posts'
  template_name = 'women/index.html'
  allow_empty = False # при пустом списке posts генерирует ошибку 404

  def get_queryset(self):
    return self.model.published.filter(tags__slug=self.kwargs.get('tag_slug')).select_related('cat')
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    tag = context['posts'].first().tags.first()
    return self.get_mixin_context(context, title='Тег: ' + tag.tag)

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