from django import template
import women.views as views

register = template.Library() # инициализация экземпляра класса для регистрации собственных html тегов

@register.simple_tag(name='get_cats') # создаем простой тег, даем название тегу через параметр name
def get_categories():
  return views.cats_db

# позволяет формировать собственный шаблон на основе данных и возвращать полноценную html разметку
# в шаблон women/list_categories.html будет передан словарь {'cats': cats} в качестве параметров
@register.inclusion_tag('women/list_categories.html')
def show_categories():
  cats = views.cats_db
  return {'cats': cats}