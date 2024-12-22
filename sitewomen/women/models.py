from django.db import models
from django.urls import reverse

class PublishedManager(models.Manager): # создание кастомного менеджера по типу models.OBJECTS
  def get_queryset(self): # метод отвечает за конечный базовый QuerySet, который можно уже в дальнейшем фильтровать, сортировать и т.д
    return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)

class Women(models.Model):
  class Status(models.IntegerChoices):
    DRAFT = 0, 'Черновик'
    PUBLISHED = 1, 'Опубликовано'

  '''
  Women.Status.choices - позволяет получить список кортежей, возможных значений
  Пример:
  [(0, 'Черновик'), (1, 'Опубликовано')]
  --------------------------------------
  Women.Status.labels - получение метод
  Пример:
  ['Черновик', 'Опубликовано']
  --------------------------------------
  Women.Status.values - получение значений
  Пример:
  [0, 1]
  '''

  title = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255, unique=True, db_index=True)
  content = models.TextField(blank=True)
  time_create = models.DateTimeField(auto_now_add=True)
  time_update = models.DateTimeField(auto_now=True)
  is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED)

  # При подключении своего собственного менеджера, менеджер objects становится недоступным
  published = PublishedManager()
  # Чтобы иметь возможность использовать оба менеджера нужно явно его указать еще и objects менеджер
  objects = models.Manager()

  def __str__(self):
    return self.title
  
  class Meta:
    ordering = ['-time_create'] # задает сортировку по умолчанию для QuerySet
    indexes = [
      models.Index(fields=['-time_create']) # задает индексирование поля time_create с учетом сортировки (т.к добавили символ "-")
    ]

  def get_absolute_url(self): # специальный метод, который может использовать admin панель для построения ссылок к конкретным записят модели
    return reverse('post', kwargs={'post_slug': self.slug})



'''
Типы связей между моделями в django:
* ForeignKey - для связей Many to One (многие к одному)
* ManyToManyField - для связей Many to Many (многие ко многим)
* OneToOneField - для связей One to One (один к одному)
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