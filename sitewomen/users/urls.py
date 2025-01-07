from django.urls import path
from . import views

# атрибут нужен чтобы указать namespace в sitewomen/urls.py в функции include
app_name = 'users'

urlpatterns = [
  path('login/', views.login_user, name='login'), # localhost:8000/users/login/
  path('logout/', views.logout_user, name='logout') # localhost:8000/users/logout/
]