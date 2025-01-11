from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

class LoginUserForm(AuthenticationForm):
  username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
  password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

  class Meta:
    # get_user_model возвращает класс модели пользователя
    # использование метода является рекоммендуемой практикой, потому что модель пользователя можно легко переопределить и назвать по другому
    model = get_user_model()
    fields = ['username', 'password']

# UserCreationForm класс формы предназначенный для создания нового пользователя модели User
# UserCreationForm определяет собственный метод для проверки совпадения паролей
# В классе UserCreationForm определены валидаторы для проверка пароля 
class RegisterUserForm(UserCreationForm):
  username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
  password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
  password2 = forms.CharField(label="Повтор Пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

  class Meta:
    model = get_user_model()
    fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    labels = {
      'email': 'E-mail',
      'first_name': 'Имя',
      'last_name': 'Фамилия',
    }
    widgets = {
      'email': forms.TextInput(attrs={'class': 'form-input'}),
      'first_name': forms.TextInput(attrs={'class': 'form-input'}),
      'last_name': forms.TextInput(attrs={'class': 'form-input'}),
    }
  
  # в стандартной модели User нет проверки на уникальность поля email
  def clean_email(self):
    email = self.cleaned_data['email']
    if get_user_model().objects.filter(email=email).exists():
      raise forms.ValidationError("Такой E-mail уже существует!")
    return email
  
class ProfileUserForm(forms.ModelForm):
  username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
  email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))

  class Meta:
    model = get_user_model()
    fields = ['username', 'email', 'first_name', 'last_name']
    labels = {
      'first_name': 'Имя',
      'last_name': 'Фамилия',
    }
    widgets = {
      'first_name': forms.TextInput(attrs={'class': 'form-input'}),
      'last_name': forms.TextInput(attrs={'class': 'form-input'})
    }

# PasswordChangeForm - стандартный класс формы изменения пароля
class UserPasswordChangeForm(PasswordChangeForm):
  old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
  new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
  new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))