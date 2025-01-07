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

class RegisterUserForm(forms.ModelForm):
  username = forms.CharField(label="Логин")
  password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
  password2 = forms.CharField(label="Повтор Пароля", widget=forms.PasswordInput())

  class Meta:
    model = get_user_model()
    fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
    labels = {
      'email': 'E-mail',
      'firstname': 'Имя',
      'lastname': 'Фамилия',
    }

  def clean_password2(self):
    cd = self.cleaned_data
    if cd['password'] != cd['password2']:
      raise forms.ValidationError("Пароли не совпадают!")
    return cd['password2']
  
  # в стандартной модели User нет проверки на уникальность поля email
  def clean_email(self):
    email = self.cleaned_data['email']
    if get_user_model().objects.filter(email=email).exists():
      raise forms.ValidationError("Такой E-mail уже существует!")
    return email