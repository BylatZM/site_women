from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

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

class Register(CreateView):
  form_class = RegisterUserForm
  template_name = 'users/register.html'
  extra_context = {'title': 'Регистрация'}
  success_url = reverse_lazy('users:login')

# LoginRequiredMixin позволит ограничить доступ к странице, просматривать могут только авторизованные пользователи
# Если пользователь не авторизован то будет выполнен редирект на адрес указанный в LOGIN_URL
class ProfileUser(LoginRequiredMixin, UpdateView):
  model = get_user_model()
  template_name = 'users/profile.html'
  form_class = ProfileUserForm
  extra_context = {'title': 'Профиль'}

  # метод позволяет задать ссылку по которой будет перенаправлен пользователь в случае успешного обновления данных профиля
  def get_success_url(self):
    return reverse_lazy('users:profile')

  # Позволяет отобрать запись, которая будет отображаться и редактироваться
  def get_object(self, queryset=None):
    return self.request.user