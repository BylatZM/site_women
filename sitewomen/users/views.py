from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render

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

def register(request):
  if request.method == 'POST':
    form = RegisterUserForm(request.POST)
    if form.is_valid():
      # метод save возвращает экземпляр модели, а также делает SQL запрос на создание записи таблице бд, НО 
      # атрибут со значением commit=False отменяет SQL запрос на создание
      user = form.save(commit=False)
      user.set_password(form.cleaned_data.get('password'))
      user.save()
      return render(request, 'users/register_done.html')
  else:
    form = RegisterUserForm()
  return render(request, 'users/register.html', {'form': form})