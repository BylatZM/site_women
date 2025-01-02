from django import template
from django.db.models import Count
from women.models import Category, TagPost

register = template.Library() # инициализация экземпляра класса для регистрации собственных html тегов

# позволяет формировать собственный шаблон на основе данных и возвращать полноценную html разметку
# в шаблон women/list_categories.html будет передан словарь {'cats': cats} в качестве параметров
@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
  # отбираем все категории, в которых есть связанные с ними посты или объекты модели Women
  cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
  return {'categories': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
  # отбираем все теги, в которых есть связанные с ними посты или объекты модели Women
  tags = TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)
  return {'tags': tags}