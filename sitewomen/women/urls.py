from django.urls import path, register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, "year4") # функция регистрации собственных конвертеров

urlpatterns = [
  # внутри as_view можно указать параметр extra_context и передать туда content, данные для html шаблона
  path('', views.WomenHome.as_view(), name='home'), # localhost:8000
  path('about/', views.about, name='about'), # localhost:8000/about/
  path('addpage/', views.AddPage.as_view(), name="add_page"), # localhost:8000/add_page/
  path('contact/', views.contact, name="contact"), # localhost:8000/contact/
  path('login/', views.login, name='login'), # localhost:8000/login/
  path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),  # localhost:8000/post/slag-1/
  path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'), # localhost:8000/category/1
  path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'), # localhost:8000/tag/blonde/
  path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'), # localhost:8000/edit/1/
]