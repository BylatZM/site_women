from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

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
  
  # ссылка на шаблон, где пользователь вводит свой email
  path('password-reset/', PasswordResetView.as_view(
    template_name="users/password_reset_form.html", # шаблон для отображения формы
    email_template_name="users/password_reset_email.html", # шаблон для формирования текста сообщения для электронной почты 
    success_url=reverse_lazy("users:password_reset_done") # после успешного отправки сообщения перенаправить пользователя по url
    ), name="password_reset"), # localhost:8000/users/password-reset/
  # ссылка на шаблон с текстом, что ссылка на изменение пароля на ящике
  path('password-reset/done/', PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"), # localhost:8000/users/password-reset/done/
  # одноразовая ссылка на шаблон, где пользователь сможет изменить пароль
  path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
    template_name="users/password_reset_confirm.html", # шаблон для отображения формы
    success_url=reverse_lazy("users:password_reset_complete") # после успешного отправки сообщения перенаправить пользователя по url
    ), name="password_reset_confirm"), # localhost:8000/users/password-reset/.../.../
  # ссылка на шаблон с текстом об успешном изменении пароля
  path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"), # localhost:8000/users/password-reset/complete/

  path('register/', views.Register.as_view(), name='register'), # localhost:8000/register/
  path('profile/', views.ProfileUser.as_view(), name="profile"), # localhost:8000/profile/1/
]

'''
Идея изменения пароля:
1) Пользователь переход по url: localhost:8000/users/password-change/
2) Вводит старый пароль
3) Вводит новый пароль
4) Вводит новый пароль повторно
5) Если все ок, его направляет на url: localhost:8000/users/password-change/done/

Идея восстановления пароля:
1) На форме авторизации пользователь нажимает на кнопку "Забыл пароль?"
2) Переход по url: localhost:8000/users/password-reset/
3) Указывает E-mail, на который привязан аккаунт
4) Если все ок, переход по url: localhost:8000/users/password-reset/done/
5) Получает текст, что ссылка для посстановления пароля сброшена ему на почту
6) На почте переходит по одноразовому url: localhost:8000/users/password-reset/<uuid64>/<token>/
7) Вводит новый пароль и еще раз вводит новый пароль
8) Если все ок, переход по url: localhost:8000/users/password-reset/complete/
9) Получает текст, что пароль успешно изменен
'''