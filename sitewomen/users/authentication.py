from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailAuthBackend(BaseBackend):
  # метод позволяет аутентифицировать пользователя на сайте
  def authenticate(self, request, username=None, password=None, **kwargs):
    user_model = get_user_model()
    try:
      user = user_model.objects.get(email=username)
      # check_password стандартный метод модели User для проверки совпадения паролей
      if user.check_password(password):
        return user
      else: return
    # DoesNotExist стандартная ошибка класса User, означает что запись пользователя не найдена
    # MultipleObjectsReturned стандартная ошибка класса User, означает что найдено несколько записей
    except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
      return
  
  # метод, который возвращает объект user, который используется в шаблонах
  # без него пользователь все еще будет не авторизован
  # отрабатывает, если был успешно пройден метод authenticate
  def get_user(self, user_id):
    user_model = get_user_model()
    try:
      return user_model.objects.get(pk=user_id)
    except user_model.DoesNotExist:
      return