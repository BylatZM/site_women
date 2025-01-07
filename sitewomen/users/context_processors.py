from women.utils import menu

# создаем контекстный процессор, который автоматически будет передаваться во все шаблоны
def get_women_context(request): 
  return {'mainmenu': menu}