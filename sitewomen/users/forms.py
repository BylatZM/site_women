from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class LoginUserForm(AuthenticationForm):
  username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
  password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

  class Meta:
    # get_user_model возвращает класс модели пользователя
    # использование метода является рекоммендуемой практикой, потому что модель пользователя можно легко переопределить и назвать по другому
    model = get_user_model()
    fields = ['username', 'password']