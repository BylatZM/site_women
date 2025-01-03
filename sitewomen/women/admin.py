from django.contrib import admin, messages
from women import models

class MarriedFilter(admin.SimpleListFilter):
  title = 'Статус женщин'
  parameter_name = 'status'

  # определяем queryset возможных значений, которые будут отображаться в фильтре
  def lookups(self, request, model_admin):
    # первый элемент кортежа будет использоваться в url адресе, к примеру, status=married
    return [('married', 'Замужем', ), ('single', 'Не замужем')]
  
  def queryset(self, request, queryset):
    if self.value() == 'married':
      # отбираем все записи из модели Women, у которых поле husband не равно Null
      return queryset.filter(husband__isnull=False)
    if self.value() == 'single':
      # отбираем все записи из модели Women, у которых поле husband равно Null
      return queryset.filter(husband__isnull=True)

# команда регистрирует модель, давая возможность ее просмотра в панели администрации
# добавляем класс настроек для модели
@admin.register(models.Women)
class WomenAdmin(admin.ModelAdmin):
  # указываем поля, которые будут видны при открытии вкладки с моделью Women (которые можно будет сортировать)
  list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info', )
  # задает поля на которые можно будет кликнуть, чтобы провариться в запись
  list_display_links = ('title', )
  # выставляем сортировку записей в таблице модели по умолчанию по возрастанию для полей time_create и title
  # сортировка действует только в админ панели
  # как сортируется по двум полям?
  # сначала сортируем по time_create, далее если у полей одинаковые значения time_create
  # то идет сортировка по полю title
  ordering = ['time_create', 'title']
  # позволяет редактировать указанные в атрибуте поля, не проваливаясь к конкретной записи
  # !!! поле не может одновременно находится в переменных list_editable и list_display_links
  list_editable = ('is_published', )
  # указываем максимальное количество записей модели, которые будут отображаться на одной странице
  list_per_page = 5
  # добоавляем методы, которые мы дополнительно может применять к выбранным зааписям
  actions = ['set_published', 'set_draft']
  # указываем поля возможные значения которых мы хотели бы искать в поле ввода для поиска (чувстивельно к регистру)
  # можно припысывать люкапы для полей, люкап startwith означает, будет искаться значение у поля title, начинающаяся с введенной подстроки 
  search_fields = ['title__startswith', 'cat__name']
  # поле добавляет блоки справа от таблицы с записями модели, которая позволит фильтровать записи по предопределенным значениям
  # можно указать ссылку на свой собственный класс фильтрации
  list_filter = [MarriedFilter, 'cat__name', 'is_published']

  # оборачиваем в декоратор, чтобы полю присвоить название, которое будет отображаться для него
  # также определяем возможную сортировку полю по полю модели 'content', то есть в лексико-графическом порядке
  # определенный метод используем в качестве нового отображаемого поля в таблице панели администрации
  @admin.display(description="Краткое описание", ordering='content')
  def brief_info(self, women: models.Women):
    return f"Описание {len(women.content)} символов."
  
  # метод используем чтобы добавить функционал рядом с кнопкой "удалить записи"
  # метод исменяет статус выбранных записей на "опубликовано"
  # оборачиваем в декоратор, чтобы изменить название действия
  @admin.action(description="Опубликовать выбранные записи")
  def set_published(self, request, queryset):
    # метод update возвращает количество записей, которые были изменены
    count = queryset.update(is_published=models.Women.Status.PUBLISHED)
    self.message_user(request, f"Изменено {count} записей")

  @admin.action(description="Снять с публикации выбранные записи")
  def set_draft(self, request, queryset):
    count = queryset.update(is_published=models.Women.Status.DRAFT)
    self.message_user(request, f"{count} записей, снято с публикации", messages.WARNING)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', )
  list_display_links = ('id', 'name', )