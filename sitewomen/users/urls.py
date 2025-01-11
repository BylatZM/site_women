from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

# атрибут нужен чтобы указать namespace в sitewomen/urls.py в функции include
app_name = 'users'

urlpatterns = [
  path('login/', views.LoginUser.as_view(), name='login'), # localhost:8000/users/login/
  # по умолчанию класс LogoutView перенаправляет по url localhost:8000/users/logout/
  # чтобы изменить поведение можно задать переменную LOGOUT_REDIRECT_URL в settings.py
  path('logout/', LogoutView.as_view(), name='logout'), # localhost:8000/users/logout/
  path('password-change/', views.UserPasswordChange.as_view(), name="password_change"), # localhost:8000/users/password-change/
  # PasswordChangeDoneView - стандартный класс отображающий станицу о том, что пароль был успешно изменен
  path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"), # localhost:8000/users/password-change/done/
  path('register/', views.Register.as_view(), name='register'), # localhost:8000/register/
  path('profile/', views.ProfileUser.as_view(), name="profile"), # localhost:8000/profile/1/
]