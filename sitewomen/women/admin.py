from django.contrib import admin
from women import models

# команда регистрирует модель, давая возможность ее просмотра в панели администрации
# добавляем класс настроек для модели
@admin.register(models.Women)
class WomenAdmin(admin.ModelAdmin):
  # указываем поля, которые будут видны при открытии вкладки с моделью Women (которые можно будет сортировать)
  list_display = ('id', 'title', 'time_create', 'is_published', 'cat', )
  # задает поля на которые можно будет кликнуть, чтобы провариться в запись
  list_display_links = ('id', 'title', )
  # выставляем сортировку записей в таблице модели по умолчанию по возрастанию для полей time_create и title
  # сортировка действует только в админ панели
  # как сортируется по двум полям?
  # сначала сортируем по time_create, далее если у полей одинаковые значения time_create
  # то идет сортировка по полю title
  ordering = ['time_create', 'title']
  # позволяет редактировать указанные в атрибуте поля, не проваливаясь к конкретной записи
  list_editable = ('is_published', )
  # указываем максимальное количество записей модели, которые будут отображаться на одной странице
  list_per_page = 5

  # !!! поле не может одновременно находится в переменных list_editable и list_display_links

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', )
  list_display_links = ('id', 'name', )