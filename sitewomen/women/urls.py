from django.urls import path, register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, "year4") # функция регистрации собственных конвертеров

urlpatterns = [
  path('', views.index, name='home'), # localhost:8000
  path('about/', views.about, name='about'), # localhost:8000/about/
  path('addpage/', views.addpage, name="add_page"), # localhost:8000/add_page/
  path('contact/', views.contact, name="contact"), # localhost:8000/contact/
  path('login/', views.login, name='login'), # localhost:8000/login/
  path('post/<int:post_id>/', views.show_post, name='post'),  # localhost:8000/post/1/
]