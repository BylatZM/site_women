from .forms import LoginUserForm
from django.contrib.auth.views import LoginView

# LoginView класс представления, который позволяет удобно аутентифицировать пользователя на сайте
# AuthenticationForm - форма для аутентификации пользователя, предоставляет форму с полями username и password
# класс AuthenticationForm использует набор методов и атрибутов, которые работают в связке с LoginView
# поэтому заменить этот класс формы на свой проблемотично, но возможно
# чтобы решить проблему нужно наш класс формы LoginUserForm унаследовать от AuthenticationForm
# при успешной авторизации, по умолчанию перенаправляет пользователя по адресу localhost:8000/accounts/profile/
class LoginUser(LoginView):
  form_class = LoginUserForm
  template_name = 'users/login.html'
  extra_context = {'title': 'Авторизация'}

  # изменяем url адрес на который нужно перенаправить пользователя, при успешной авторизации
  # можно в качестве альтернативы добавить пометку в файл settings.py
  # def get_success_url(self):
  #   return reverse_lazy('home')
