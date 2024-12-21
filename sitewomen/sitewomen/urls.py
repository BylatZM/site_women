from django.contrib import admin
from django.urls import path, include
from women import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
]

'''
Прописывая url адресов в основном приложении не правильно, так как нарушается приницип автономности приложений
(если поменяются url адреса в одном приложении, то в этом надо будет руками изменения править, а это плохо)

Так не правильно !!!
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index), # localhost:8000
    path('cats/', views.categories), # localhost:8000/cats/
]
Так правильно
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
]
'''
