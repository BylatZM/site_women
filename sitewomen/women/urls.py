from django.urls import path
from . import views

urlpatterns = [
  path('', views.index), # localhost:8000
  path('cats/', views.categories) # localhost:8000/cats/
]
