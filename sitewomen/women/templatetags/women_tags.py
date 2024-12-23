from django import template
import women.views as views

from women.models import Category

register = template.Library() # инициализация экземпляра класса для регистрации собственных html тегов



# позволяет формировать собственный шаблон на основе данных и возвращать полноценную html разметку
# в шаблон women/list_categories.html будет передан словарь {'cats': cats} в качестве параметров
@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
  cats = Category.objects.all()
  return {'categories': cats, 'cat_selected': cat_selected}