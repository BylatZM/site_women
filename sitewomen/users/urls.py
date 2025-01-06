from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.login_user, name='login'), # localhost:8000/users/login/
  path('logout/', views.logout_user, name='logout') # localhost:8000/users/logout/
]