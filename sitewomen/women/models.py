from django.db import models
from django.urls import reverse

class PublishedManager(models.Manager): # создание кастомного менеджера по типу models.OBJECTS
  def get_queryset(self): # метод отвечает за конечный базовый QuerySet, который можно уже в дальнейшем фильтровать, сортировать и т.д
    return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)

class Women(models.Model):
  class Status(models.IntegerChoices):
    DRAFT = 0, 'Черновик'
    PUBLISHED = 1, 'Опубликовано'

  title = models.CharField(max_length=255, verbose_name="Заголовок")
  slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")
  content = models.TextField(blank=True, verbose_name="Текст статьи")
  time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
  time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
  # так как нет стандартного перечисления в формате Boolean, поэтому используем итератор map
  # проходимся по списку вида [(0, 'Черновик', ), (1, 'Опубликовано', )]
  # в результате возвращаем запись вида [(False, 'Черновик', ), (True, 'Опубликовано', )]
  is_published = models.BooleanField(choices=list(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.PUBLISHED, verbose_name="Статус")
  # Category прописали в виде строки, так как класс определен ниже и мы пытаемся вызвать не определенный класс
  # Модели Category будет соответствовать МНОЖЕСТВО записей из модели Women
  # Модели Women будет соответствовать ОДНА запись из модели Category
  # related_name изменяет название менеджера записи, который позволит с экземпляров класса Category получать все связанные записи из модели Women
  cat = models.ForeignKey(to="Category", on_delete=models.PROTECT, related_name="posts", verbose_name="Категории")
  # TagPost прописали в виде строки, так как класс определен ниже и мы пытаемся вызвать не определенный класс
  # Модели TagPost будет соответствовать МНОЖЕСТВО записей из модели Women
  # Модели Women будет соответствовать МНОЖЕСТВО записей из модели TagPost
  # related_name изменяет название менеджера записи, который позволит с экземпляров класса TagPost получать все связанные записи из модели Women
  tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Теги")
  # Husband прописали в виде строки, так как класс определен ниже и мы пытаемся вызвать не определенный класс
  # Модели Husband будет соответствовать ОДНА запись из модели Women
  # Модели Women будет соответствовать ОДНА запись из модели Husband
  # related_name изменяет название менеджера записи, который позволит с экземпляра класса Husband получать связанную запись из модели Women 
  husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='woman', verbose_name="Муж")

  # Чтобы иметь возможность использовать оба менеджера нужно явно его указать еще и objects менеджер
  objects = models.Manager()
  # При подключении своего собственного менеджера, менеджер objects становится недоступным
  published = PublishedManager()

  def __str__(self):
    return self.title
  
  class Meta:
    verbose_name = "Известные женщины" # изменяет название модели в панели администрирования (для ед.ч)
    verbose_name_plural = "Известные женщины" # изменяет название модели в панели администрирования (для мн.ч)
    ordering = ['-time_create'] # задает сортировку по умолчанию для QuerySet
    indexes = [
      models.Index(fields=['-time_create']) # задает индексирование поля time_create с учетом сортировки (т.к добавили символ "-")
    ]

  def get_absolute_url(self): # специальный метод, который может использовать admin панель для построения ссылок к конкретным записят модели
    return reverse('post', kwargs={'post_slug': self.slug})

class Category(models.Model):
  name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
  slug = models.SlugField(max_length=255, unique=True, db_index=True)

  class Meta:
    verbose_name = "Категория"
    verbose_name_plural = "Категории"

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
  tag = models.CharField(max_length=100, db_index=True)
  slug = models.SlugField(max_length=255, unique=True, db_index=True)

  def __str__(self):
    return self.tag
  
  def get_absolute_url(self):
    return reverse('tag', kwargs={'tag_slug': self.slug})
  
class Husband(models.Model):
  name = models.CharField(max_length=100)
  age = models.IntegerField(null=True)
  m_count = models.IntegerField(blank=True, default=0)

  def __str__(self):
    return self.name

'''
Типы связей между моделями в django:
-------------------------------------------------------
* ForeignKey - для связей Many to One (многие к одному)

Пример:
cat = models.ForeignKey(to="Category", on_delete=models.PROTECT)

w = Women.objects.get(pk=1)
w.cat - получаем объект модели Category связанный с экземпляром w модели Women
<Category: Актрисы>

w.cat.name - получаем поле name у объекта модели Category связанного с экземпляром w модели Women
'Актрисы'

c = Category.objects.get(pk=1)
! women_set - это менеджер записей, название можно изменить атрибутом related_name
c.women_set.all() - выводит все записи из таблицы Women связанные с экземпляром c из модели Category
<QuerySet [<Women: Анджелина Джоли>, <Women: Кира Найтли>, <Women: Ума Турман>, <Women: Джулия Робертс>]>

c.women_set.filter(...) - получение записей отфильтрованных по условию
<QuerySet [...]>

Women.objects.filter(cat__slug="...") - позволяет отобрать записи из таблицы Women, где связанные с нип объект из модели Category имеет
атрибут slug="..."
<QuerySet [...]>

Women.objects.filter(cat__slug__contains="ы") - позволяет отобрать записи из таблицы Women, 
где связанные с нип объект из модели Category имеет атрибут name содержащий в себе подстроку "ы"
<QuerySet [...]>

Обязательные параметры:
to - ссылка или строка класса модели, с которой происходит связывание (в нашем случае это класс Category - модели для категорий)
on_delete - тип ограничения при удалении внешней записи (в нашем примере - это удаление из таблицы Category)
-------------------------------------------------------
* ManyToManyField - для связей Many to Many (многие ко многим)

Пример:
tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

! для данной виды связи создается еще одна таблица базы данных с названием <имя приложение>_<имя первой модели>_<имя второй модели>, 
где определены поля id, <название первой модели>_id, <название второй модели>_id

w = Women.objects.get(pk=1)
tag_br, tag_o, tag_v = TagPost.objects.filter(id__in=[1, 3, 5])
w.tags.set([tag_br, tag_o, tag_v]) - связываем экземпляр модели Women с 3 записями из модели TagPost

w.tags.remove(tag_o) - если нужно удалить связь между экземпляром модели Women с экземпляром модели TagPost

w.tags.add(tag_br) - связываем экземпляр модели Women с одной записью из модели TagPost

w.tags.all() - получить все записи из модели TagPost связанные с экземпляром модели Women

tag_br.tags.all() - получить все записи из модели Women связанные с экземпляром модели TagPost

b = Women.objects.get(pk=2)
tag_br.tags.add(b) - связываем экземпляр модели TagPost с одной записью из модели Women

! нельзя создавать запись и сразу добавлять связи многие ко многим, так как у создаваемой записи еще не существует id
Women.objects.create(title='Ариана Гранде', slug='ariana', cat_id=2, tags=[tag_br, tag_v]) - НЕДОПУСТИМО!!!

w = Women.objects.create(title='Ариана Гранде', slug='ariana', cat_id=2)
w.tags.set([tag_br, tag_v]) - так правильно

Обязательный параметр:
to - ссылка или строка класса модели, с которой происходит связывание (в нашем случае это класс TagPost)
-------------------------------------------------------
* OneToOneField - для связей One to One (один к одному)

Пример:
husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='woman')

w = Women.objects.get(pk=1)
h = Husband.objects.get(pk=1)
w.husband = h - связываем объект w модели Women с объектом h модели Husband
w.save() - делаем sql запрос на обновление данных в базе

w.husband - получить объект модели Husband связанный с объектом w модели Women

h.woman - получить объект модели Women связанный с объектом h модели Husband

w = Women.objects.get(pk=2)
h = Husband.objects.get(pk=2)
h.woman = w - связываем объект h модели Husband с объектом w модели Women
w.save() - делаем сохранение уменного у объекта w модели Women т.к изменение выше - это изменение объекта w модели Women !!!

w = Women.objects.get(pk=3)
h = Husband.objects.get(pk=2) - данный объект уже связан с объектом Women.objects.get(pk=2)
w.husband = h - команда проходит
w.save() - вернет ОШИБКУ т.к объект h модели Husband связан с объектом Women.objects.get(pk=2)

Women.objects.filter(pk=3).husband - запусть НЕДОПУСТИМА, чтобы получить атрибут нам нужно работать с объектом, а не список QuerySet

w = Women.objects.get(pk=1)
w.husband.name - можем получить атрибуты объекта husband модели Husband

w = Women.objects.get(pk=1)
w.husband.age = 30 - изменяем экземпляр объекта husband
w.husband.save() - сохраняет изменения в объекте husband
'''

'''
Виды значений для параметра on_delete для класса ForeignKey:
* models.CASCADE - при удалении записи из первой модели, будут удалены все записи из второй модели, связанные с удаляемым полем из первой модели
* models.PROTECT - запрещает удаление записи из первичной модели, если она используется во вторичной (выдает исключение)
* models.SET_NULL - при удалении записи первичной модели устанавливает значение foreign key в NULL у соответствующих записей вторичной модели
* models.SET_DEFAULT - то же самое, что и SET_NULL, только вместо NULL устанавливает значение по умолчанию, которое должно быть определено через класс ForeignKey
* models.DO_NOTHING - удаление записи в первичной модели не вызывает никаких действий у вторичных моделей
'''

'''
! В методе filter при фильтрации можно к названию полей через двойное нижнее подчеркивание добавлять дополнительные условия

lookups в django:
--------------------------------------------------------
* <имя атрибута>__gte - сравнение больше или равно (>=)
Пример:
Women.objects.filter(pk__gte=2)
--------------------------------------------------------
* <имя атрибута>__gt - сравнение больше (>)
Пример:
Women.objects.filter(pk__gt=2)
--------------------------------------------------------
* <имя атрибута>__lte - сравнение меньше или равно (<=)
Пример:
Women.objects.filter(pk__gt=2)
--------------------------------------------------------
* <имя атрибута>__lt - сравнение меньше (<)
Пример:
Women.objects.filter(pk__lt=2)
--------------------------------------------------------
* <имя атрибута>__contains - атрибут должен включать в себя подстроку
Пример:
Women.objects.filter(pk__contains='ли')
--------------------------------------------------------
* <имя атрибута>__icontains - атрибут должен включать в себя подстроку без учета регистра (база данных sqlite не поддерживает)
Пример:
Women.objects.filter(pk__icontains='ли')
--------------------------------------------------------
* <имя атрибута>__in - атрибут должен быть равным одному из значений списка
Пример:
Women.objects.filter(pk__in=[1, 2, 3])
--------------------------------------------------------
'''