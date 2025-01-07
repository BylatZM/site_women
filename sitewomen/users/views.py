from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginUserForm
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

def login_user(request):
  if request.method == 'POST':
    form = LoginUserForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      # аутентифицируем пользователя
      # authenticate проверяет есть ли в бд модели User пользователь с таким username и паролем
      # возвращает либо объект модели User либо None
      user = authenticate(request, username=cd['username'], password=cd['password'])
      if user and user.is_active:
        # Авторизуем пользователя, навешиваем сессию
        # С помощью навешенной сессии можно заходить на панель администрации, если пользователь имеет на это права
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
  else:
    form = LoginUserForm()
  return render(request, 'users/login.html', {'form': form})

def logout_user(request):
  # метод убирает из куки сессию, а также пометки, что пользователь авторизован
  logout(request)
  # задает пространство имен с разделителем ":"
  return HttpResponseRedirect(reverse('users:login'))
