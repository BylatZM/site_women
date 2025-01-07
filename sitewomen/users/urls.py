from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

# атрибут нужен чтобы указать namespace в sitewomen/urls.py в функции include
app_name = 'users'

urlpatterns = [
  path('login/', views.LoginUser.as_view(), name='login'), # localhost:8000/users/login/
  # по умолчанию класс LogoutView перенаправляет по url localhost:8000/users/logout/
  # чтобы изменить поведение можно задать переменную LOGOUT_REDIRECT_URL в settings.py
  path('logout/', LogoutView.as_view(), name='logout'), # localhost:8000/users/logout/
  path('register/', views.register, name='register'), # localhost:8000/register/
]